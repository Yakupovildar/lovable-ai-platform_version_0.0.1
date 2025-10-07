import asyncio
import aiohttp
import json
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy" 
    STARTING = "starting"
    STOPPED = "stopped"

@dataclass
class ServiceInstance:
    service_id: str
    service_name: str
    host: str
    port: int
    health_endpoint: str
    status: ServiceStatus
    last_health_check: datetime
    metadata: Dict[str, Any]
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"
    
    @property
    def health_url(self) -> str:
        return f"{self.base_url}{self.health_endpoint}"

class ServiceRegistry:
    def __init__(self):
        self.services: Dict[str, ServiceInstance] = {}
        self.service_groups: Dict[str, List[str]] = {}
        self.health_check_interval = 30
        self.health_timeout = 5
        self.session: Optional[aiohttp.ClientSession] = None
        self._running = False
        
    async def start(self):
        """Запускает реестр сервисов"""
        if self._running:
            return
            
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.health_timeout)
        )
        self._running = True
        
        # Запускаем фоновую задачу проверки здоровья
        asyncio.create_task(self._health_check_loop())
        logger.info("Service Registry started")
        
    async def stop(self):
        """Останавливает реестр сервисов"""
        self._running = False
        if self.session:
            await self.session.close()
        logger.info("Service Registry stopped")
        
    async def register_service(self, service: ServiceInstance):
        """Регистрирует новый сервис"""
        self.services[service.service_id] = service
        
        # Добавляем в группу по имени
        if service.service_name not in self.service_groups:
            self.service_groups[service.service_name] = []
        
        if service.service_id not in self.service_groups[service.service_name]:
            self.service_groups[service.service_name].append(service.service_id)
            
        logger.info(f"Registered service: {service.service_name} [{service.service_id}]")
        
    async def unregister_service(self, service_id: str):
        """Отключает сервис"""
        if service_id in self.services:
            service = self.services[service_id]
            
            # Удаляем из группы
            if service.service_name in self.service_groups:
                if service_id in self.service_groups[service.service_name]:
                    self.service_groups[service.service_name].remove(service_id)
                    
                if not self.service_groups[service.service_name]:
                    del self.service_groups[service.service_name]
            
            del self.services[service_id]
            logger.info(f"Unregistered service: {service_id}")
            
    async def get_service(self, service_name: str) -> Optional[ServiceInstance]:
        """Возвращает здоровый экземпляр сервиса"""
        if service_name not in self.service_groups:
            return None
            
        healthy_services = []
        for service_id in self.service_groups[service_name]:
            if service_id in self.services:
                service = self.services[service_id]
                if service.status == ServiceStatus.HEALTHY:
                    healthy_services.append(service)
                    
        if not healthy_services:
            return None
            
        # Простой round-robin
        import random
        return random.choice(healthy_services)
        
    async def get_all_services(self, service_name: str) -> List[ServiceInstance]:
        """Возвращает все экземпляры сервиса"""
        if service_name not in self.service_groups:
            return []
            
        services = []
        for service_id in self.service_groups[service_name]:
            if service_id in self.services:
                services.append(self.services[service_id])
                
        return services
        
    async def get_service_status(self, service_id: str) -> Optional[ServiceStatus]:
        """Возвращает статус сервиса"""
        if service_id in self.services:
            return self.services[service_id].status
        return None
        
    async def _health_check_loop(self):
        """Фоновая задача проверки здоровья сервисов"""
        while self._running:
            await self._check_all_services_health()
            await asyncio.sleep(self.health_check_interval)
            
    async def _check_all_services_health(self):
        """Проверяет здоровье всех сервисов"""
        tasks = []
        for service_id, service in self.services.items():
            task = asyncio.create_task(self._check_service_health(service))
            tasks.append(task)
            
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            
    async def _check_service_health(self, service: ServiceInstance):
        """Проверяет здоровье одного сервиса"""
        try:
            if not self.session:
                return
                
            async with self.session.get(service.health_url) as response:
                if response.status == 200:
                    service.status = ServiceStatus.HEALTHY
                    service.last_health_check = datetime.now()
                else:
                    service.status = ServiceStatus.UNHEALTHY
                    
        except Exception as e:
            service.status = ServiceStatus.UNHEALTHY
            logger.warning(f"Health check failed for {service.service_id}: {str(e)}")
            
    async def get_registry_status(self) -> Dict[str, Any]:
        """Возвращает статус всего реестра"""
        status = {
            "total_services": len(self.services),
            "healthy_services": 0,
            "unhealthy_services": 0,
            "services_by_group": {},
            "services": []
        }
        
        for service in self.services.values():
            service_info = {
                "service_id": service.service_id,
                "service_name": service.service_name,
                "host": service.host,
                "port": service.port,
                "status": service.status.value,
                "last_health_check": service.last_health_check.isoformat()
            }
            status["services"].append(service_info)
            
            if service.status == ServiceStatus.HEALTHY:
                status["healthy_services"] += 1
            else:
                status["unhealthy_services"] += 1
                
            # Группировка по именам
            if service.service_name not in status["services_by_group"]:
                status["services_by_group"][service.service_name] = {
                    "total": 0,
                    "healthy": 0
                }
                
            status["services_by_group"][service.service_name]["total"] += 1
            if service.status == ServiceStatus.HEALTHY:
                status["services_by_group"][service.service_name]["healthy"] += 1
                
        return status

# Глобальный экземпляр реестра
service_registry = ServiceRegistry()