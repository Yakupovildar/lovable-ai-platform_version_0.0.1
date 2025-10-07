import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from enum import Enum
import logging
from dataclasses import dataclass
import hashlib
import time

from .service_registry import service_registry, ServiceInstance

logger = logging.getLogger(__name__)

class LoadBalanceStrategy(Enum):
    ROUND_ROBIN = "round_robin"
    RANDOM = "random"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"

@dataclass
class RouteRule:
    path_prefix: str
    service_name: str
    strip_prefix: bool = True
    require_auth: bool = False
    timeout: int = 30
    retry_count: int = 3
    load_balance: LoadBalanceStrategy = LoadBalanceStrategy.ROUND_ROBIN

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = {}
        
    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
            
        # Очищаем старые запросы
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if now - req_time < self.window_seconds
        ]
        
        # Проверяем лимит
        if len(self.requests[client_id]) >= self.max_requests:
            return False
            
        self.requests[client_id].append(now)
        return True

class APIGateway:
    def __init__(self):
        self.routes: List[RouteRule] = []
        self.rate_limiter = RateLimiter()
        self.session: Optional[aiohttp.ClientSession] = None
        self.connection_counts: Dict[str, int] = {}
        self.round_robin_counters: Dict[str, int] = {}
        
    async def start(self):
        """Запускает API Gateway"""
        self.session = aiohttp.ClientSession()
        await service_registry.start()
        logger.info("API Gateway started")
        
    async def stop(self):
        """Останавливает API Gateway"""
        if self.session:
            await self.session.close()
        await service_registry.stop()
        logger.info("API Gateway stopped")
        
    def add_route(self, rule: RouteRule):
        """Добавляет правило маршрутизации"""
        self.routes.append(rule)
        logger.info(f"Added route: {rule.path_prefix} -> {rule.service_name}")
        
    def remove_route(self, path_prefix: str):
        """Удаляет правило маршрутизации"""
        self.routes = [r for r in self.routes if r.path_prefix != path_prefix]
        logger.info(f"Removed route: {path_prefix}")
        
    async def handle_request(self, method: str, path: str, headers: Dict[str, str], 
                           body: bytes, client_ip: str) -> Dict[str, Any]:
        """Обрабатывает HTTP запрос"""
        try:
            # Rate limiting
            if not self.rate_limiter.is_allowed(client_ip):
                return {
                    "status": 429,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Rate limit exceeded"}).encode()
                }
            
            # Находим подходящий маршрут
            route = self._find_route(path)
            if not route:
                return {
                    "status": 404,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Route not found"}).encode()
                }
            
            # Проверяем авторизацию
            if route.require_auth and not self._check_auth(headers):
                return {
                    "status": 401,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Unauthorized"}).encode()
                }
            
            # Выбираем сервис
            service = await self._select_service(route)
            if not service:
                return {
                    "status": 503,
                    "headers": {"Content-Type": "application/json"},
                    "body": json.dumps({"error": "Service unavailable"}).encode()
                }
            
            # Формируем целевой URL
            target_path = path
            if route.strip_prefix:
                target_path = path[len(route.path_prefix):]
                if not target_path.startswith('/'):
                    target_path = '/' + target_path
                    
            target_url = f"{service.base_url}{target_path}"
            
            # Выполняем запрос с retry
            for attempt in range(route.retry_count):
                try:
                    response = await self._make_request(
                        method, target_url, headers, body, route.timeout
                    )
                    return response
                    
                except Exception as e:
                    if attempt == route.retry_count - 1:
                        raise
                    logger.warning(f"Request attempt {attempt + 1} failed: {str(e)}")
                    await asyncio.sleep(0.5 * (attempt + 1))  # Exponential backoff
                    
        except Exception as e:
            logger.error(f"Gateway error: {str(e)}")
            return {
                "status": 500,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"error": "Internal server error"}).encode()
            }
    
    def _find_route(self, path: str) -> Optional[RouteRule]:
        """Находит подходящий маршрут"""
        for route in self.routes:
            if path.startswith(route.path_prefix):
                return route
        return None
        
    def _check_auth(self, headers: Dict[str, str]) -> bool:
        """Проверяет авторизацию"""
        auth_header = headers.get('Authorization')
        if not auth_header:
            return False
        
        # Простая проверка Bearer token
        if not auth_header.startswith('Bearer '):
            return False
            
        token = auth_header[7:]
        # TODO: Реализовать проверку JWT токена
        return len(token) > 0
        
    async def _select_service(self, route: RouteRule) -> Optional[ServiceInstance]:
        """Выбирает сервис согласно стратегии балансировки"""
        services = await service_registry.get_all_services(route.service_name)
        healthy_services = [s for s in services if s.status.value == "healthy"]
        
        if not healthy_services:
            return None
            
        if route.load_balance == LoadBalanceStrategy.ROUND_ROBIN:
            return self._round_robin_select(route.service_name, healthy_services)
        elif route.load_balance == LoadBalanceStrategy.RANDOM:
            import random
            return random.choice(healthy_services)
        elif route.load_balance == LoadBalanceStrategy.LEAST_CONNECTIONS:
            return self._least_connections_select(healthy_services)
        else:
            return healthy_services[0]
            
    def _round_robin_select(self, service_name: str, services: List[ServiceInstance]) -> ServiceInstance:
        """Round-robin балансировка"""
        if service_name not in self.round_robin_counters:
            self.round_robin_counters[service_name] = 0
            
        index = self.round_robin_counters[service_name] % len(services)
        self.round_robin_counters[service_name] += 1
        
        return services[index]
        
    def _least_connections_select(self, services: List[ServiceInstance]) -> ServiceInstance:
        """Выбор сервиса с наименьшим количеством соединений"""
        min_connections = float('inf')
        selected_service = services[0]
        
        for service in services:
            connections = self.connection_counts.get(service.service_id, 0)
            if connections < min_connections:
                min_connections = connections
                selected_service = service
                
        return selected_service
        
    async def _make_request(self, method: str, url: str, headers: Dict[str, str], 
                          body: bytes, timeout: int) -> Dict[str, Any]:
        """Выполняет HTTP запрос к сервису"""
        if not self.session:
            raise Exception("Session not initialized")
            
        # Увеличиваем счетчик соединений
        service_id = self._extract_service_id(url)
        if service_id:
            self.connection_counts[service_id] = self.connection_counts.get(service_id, 0) + 1
            
        try:
            # Подготавливаем заголовки
            request_headers = dict(headers)
            request_headers.pop('Host', None)  # Удаляем Host заголовок
            
            # Добавляем заголовки Gateway
            request_headers['X-Forwarded-By'] = 'API-Gateway'
            request_headers['X-Request-ID'] = self._generate_request_id()
            
            async with self.session.request(
                method, url, 
                headers=request_headers,
                data=body,
                timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:
                response_body = await response.read()
                response_headers = dict(response.headers)
                
                return {
                    "status": response.status,
                    "headers": response_headers,
                    "body": response_body
                }
                
        finally:
            # Уменьшаем счетчик соединений
            if service_id and service_id in self.connection_counts:
                self.connection_counts[service_id] -= 1
                if self.connection_counts[service_id] <= 0:
                    del self.connection_counts[service_id]
    
    def _extract_service_id(self, url: str) -> Optional[str]:
        """Извлекает ID сервиса из URL"""
        # Простая логика - можно улучшить
        for service in service_registry.services.values():
            if service.base_url in url:
                return service.service_id
        return None
        
    def _generate_request_id(self) -> str:
        """Генерирует уникальный ID запроса"""
        return hashlib.md5(f"{time.time()}".encode()).hexdigest()[:8]
        
    async def get_gateway_stats(self) -> Dict[str, Any]:
        """Возвращает статистику Gateway"""
        registry_status = await service_registry.get_registry_status()
        
        return {
            "gateway_uptime": time.time(),  # TODO: реальное время работы
            "active_connections": sum(self.connection_counts.values()),
            "connections_by_service": dict(self.connection_counts),
            "routes_count": len(self.routes),
            "routes": [
                {
                    "path_prefix": route.path_prefix,
                    "service_name": route.service_name,
                    "load_balance": route.load_balance.value
                }
                for route in self.routes
            ],
            "service_registry": registry_status
        }

# Глобальный экземпляр Gateway
api_gateway = APIGateway()

# Предустановленные маршруты
default_routes = [
    RouteRule("/api/ai/", "ai-service", strip_prefix=True, require_auth=True),
    RouteRule("/api/mobile/", "mobile-service", strip_prefix=True, require_auth=True),
    RouteRule("/api/audio/", "audio-service", strip_prefix=True, require_auth=True),
    RouteRule("/api/video/", "video-service", strip_prefix=True, require_auth=True),
    RouteRule("/api/build/", "build-service", strip_prefix=True, require_auth=True),
    RouteRule("/api/templates/", "template-service", strip_prefix=True, require_auth=False),
    RouteRule("/health", "health-service", strip_prefix=False, require_auth=False),
]

async def setup_default_routes():
    """Настраивает маршруты по умолчанию"""
    for route in default_routes:
        api_gateway.add_route(route)