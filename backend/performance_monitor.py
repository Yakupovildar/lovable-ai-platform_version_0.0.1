
import time
import threading
import psutil
import logging
from datetime import datetime
from typing import Dict, List, Any
from collections import deque

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.request_times = deque(maxlen=1000)  # Последние 1000 запросов
        self.error_count = 0
        self.total_requests = 0
        self.start_time = time.time()
        self.lock = threading.Lock()
        
    def record_request(self, duration: float, success: bool = True):
        """Записывает время выполнения запроса"""
        with self.lock:
            self.request_times.append(duration)
            self.total_requests += 1
            if not success:
                self.error_count += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Получает статистику производительности"""
        with self.lock:
            if not self.request_times:
                return {"status": "no_data"}
            
            avg_time = sum(self.request_times) / len(self.request_times)
            min_time = min(self.request_times)
            max_time = max(self.request_times)
            
            # Системная информация
            cpu_percent = psutil.cpu_percent()
            memory_info = psutil.virtual_memory()
            
            uptime = time.time() - self.start_time
            error_rate = (self.error_count / max(self.total_requests, 1)) * 100
            
            return {
                "uptime_seconds": uptime,
                "total_requests": self.total_requests,
                "error_rate_percent": round(error_rate, 2),
                "response_time": {
                    "average_ms": round(avg_time * 1000, 2),
                    "min_ms": round(min_time * 1000, 2),
                    "max_ms": round(max_time * 1000, 2)
                },
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory_info.percent,
                    "memory_available_mb": round(memory_info.available / 1024 / 1024, 2)
                },
                "performance_grade": self._calculate_grade(avg_time, error_rate, cpu_percent)
            }
    
    def _calculate_grade(self, avg_time: float, error_rate: float, cpu_percent: float) -> str:
        """Вычисляет оценку производительности"""
        if avg_time < 0.1 and error_rate < 1 and cpu_percent < 70:
            return "A+ (Отличная)"
        elif avg_time < 0.2 and error_rate < 2 and cpu_percent < 80:
            return "A (Очень хорошая)"
        elif avg_time < 0.5 and error_rate < 5 and cpu_percent < 90:
            return "B (Хорошая)"
        else:
            return "C (Требует оптимизации)"

# Глобальный монитор производительности
performance_monitor = PerformanceMonitor()

def monitor_performance(func):
    """Декоратор для мониторинга производительности функций"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise e
        finally:
            duration = time.time() - start_time
            performance_monitor.record_request(duration, success)
    return wrapper
import time
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any
from collections import deque

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    def __init__(self):
        self.stats = {
            "requests_count": 0,
            "average_response_time": 0,
            "active_sessions": 0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        self.request_times = deque(maxlen=100)
        self._lock = threading.Lock()
    
    def record_request(self, response_time, success=True):
        """Записать время запроса"""
        with self._lock:
            self.stats["requests_count"] += 1
            self.request_times.append(response_time)
            if self.request_times:
                self.stats["average_response_time"] = sum(self.request_times) / len(self.request_times)
    
    def get_stats(self):
        """Получить статистику"""
        return self.stats.copy()
    
    def increment_active_sessions(self):
        """Увеличить счетчик активных сессий"""
        with self._lock:
            self.stats["active_sessions"] += 1
    
    def decrement_active_sessions(self):
        """Уменьшить счетчик активных сессий"""
        with self._lock:
            self.stats["active_sessions"] = max(0, self.stats["active_sessions"] - 1)

    def record_cache_hit(self):
        """Записать попадание в кэш"""
        with self._lock:
            self.stats["cache_hits"] += 1

    def record_cache_miss(self):
        """Записать промах кэша"""
        with self._lock:
            self.stats["cache_misses"] += 1

    def get_performance_grade(self):
        """Получить оценку производительности"""
        avg_time = self.stats.get("average_response_time", 0)
        if avg_time < 0.5:
            return "A (Отлично)"
        elif avg_time < 1.0:
            return "B (Хорошо)"
        else:
            return "C (Требует оптимизации)"# Глобальный экземпляр
performance_monitor = PerformanceMonitor()

def monitor_performance(func):
    """Декоратор для мониторинга производительности функций"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        success = True
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            success = False
            raise e
        finally:
            duration = time.time() - start_time
            performance_monitor.record_request(duration, success)
    return wrapperности"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            response_time = end_time - start_time
            performance_monitor.record_request(response_time)
            logger.info(f"⚡ {func.__name__} выполнен за {response_time:.3f}с")
    return wrapper
