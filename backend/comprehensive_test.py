#!/usr/bin/env python3
"""
Комплексное тестирование Vibecode AI Platform
Тестирует реальные пользовательские сценарии
"""

import requests
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Конфигурация
BASE_URL = "http://localhost:5002"
TEST_SCENARIOS = [
    {
        "name": "Предприниматель создает лендинг для услуг",
        "description": "Лендинг для студии веб-дизайна с портфолио и формой заказа",
        "expected_type": "landing"
    },
    {
        "name": "Фитнес-тренер создает приложение",
        "description": "Приложение для фитнес-тренировок с календарем и трекером прогресса",
        "expected_type": "fitness"
    },
    {
        "name": "Стартап создает e-commerce",
        "description": "Интернет-магазин для продажи эко-продуктов с корзиной и оплатой",
        "expected_type": "ecommerce"
    },
    {
        "name": "Разработчик создает портфолио",
        "description": "Портфолио для JavaScript разработчика с проектами и резюме",
        "expected_type": "portfolio"
    },
    {
        "name": "Геймер создает браузерную игру",
        "description": "Простая игра-кликер с очками и достижениями",
        "expected_type": "game"
    }
]

class VibecodeTestSuite:
    def __init__(self):
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
            "performance": {},
            "user_scenarios": []
        }
        self.session = requests.Session()
        
    def log(self, message, level="INFO"):
        """Логирование с временной меткой"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = "✅" if level == "SUCCESS" else "❌" if level == "ERROR" else "ℹ️"
        print(f"{icon} [{timestamp}] {message}")
        
    def test_server_availability(self):
        """Тест доступности сервера"""
        self.log("Проверка доступности сервера...")
        try:
            response = self.session.get(f"{BASE_URL}/api/health", timeout=5)
            if response.status_code == 404:
                # Если /api/health не существует, проверим основной endpoint
                response = self.session.get(BASE_URL, timeout=5)
                if response.status_code == 200:
                    self.log("Сервер доступен", "SUCCESS")
                    return True
            elif response.status_code == 200:
                self.log("Сервер доступен", "SUCCESS")
                return True
                
            self.log(f"Сервер недоступен: {response.status_code}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Ошибка подключения к серверу: {e}", "ERROR")
            return False
            
    def test_user_registration(self):
        """Тест регистрации пользователя"""
        self.log("Тестирование регистрации пользователя...")
        test_user = {
            "email": f"test_{int(time.time())}@example.com",
            "name": "Тестовый Пользователь",
            "password": "securepassword123"
        }
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{BASE_URL}/api/register",
                json=test_user,
                timeout=10
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log(f"Регистрация успешна за {duration:.2f}с", "SUCCESS")
                    self.results["performance"]["registration"] = duration
                    return test_user
                else:
                    self.log(f"Ошибка регистрации: {data.get('message')}", "ERROR")
                    
            self.log(f"Регистрация не удалась: {response.status_code}", "ERROR")
            return None
            
        except Exception as e:
            self.log(f"Исключение при регистрации: {e}", "ERROR")
            return None
            
    def test_user_login(self, user_data):
        """Тест входа пользователя"""
        if not user_data:
            return False
            
        self.log("Тестирование входа пользователя...")
        try:
            response = self.session.post(
                f"{BASE_URL}/api/login",
                json={
                    "email": user_data["email"],
                    "password": user_data["password"]
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    self.log("Вход выполнен успешно", "SUCCESS")
                    return True
                    
            self.log(f"Вход не удался: {response.status_code}", "ERROR")
            return False
            
        except Exception as e:
            self.log(f"Исключение при входе: {e}", "ERROR")
            return False
            
    def test_project_generation(self, scenario):
        """Тест генерации проекта по сценарию"""
        self.log(f"Тестирование сценария: {scenario['name']}")
        
        try:
            start_time = time.time()
            response = self.session.post(
                f"{BASE_URL}/api/smart-generate-project",
                json={
                    "description": scenario["description"],
                    "project_name": f"Тест - {scenario['name']}"
                },
                timeout=30  # Увеличенный таймаут для генерации
            )
            generation_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    project_id = data.get('project_id')
                    project_type = data.get('project_type')
                    files_count = data.get('files_count')
                    
                    # Проверка качества результата
                    quality_score = self.evaluate_project_quality(data)
                    
                    scenario_result = {
                        "name": scenario["name"],
                        "success": True,
                        "generation_time": generation_time,
                        "project_id": project_id,
                        "project_type": project_type,
                        "files_count": files_count,
                        "quality_score": quality_score,
                        "expected_type": scenario["expected_type"],
                        "type_match": project_type == scenario["expected_type"]
                    }
                    
                    self.log(f"✅ Проект создан за {generation_time:.2f}с, тип: {project_type}, файлов: {files_count}, качество: {quality_score}/5", "SUCCESS")
                    
                    # Тестируем предпросмотр
                    preview_success = self.test_project_preview(project_id)
                    scenario_result["preview_works"] = preview_success
                    
                    return scenario_result
                else:
                    self.log(f"Ошибка генерации: {data.get('message')}", "ERROR")
                    
            self.log(f"Генерация не удалась: {response.status_code}", "ERROR")
            return None
            
        except Exception as e:
            self.log(f"Исключение при генерации: {e}", "ERROR")
            return None
            
    def evaluate_project_quality(self, project_data):
        """Оценка качества созданного проекта"""
        score = 0
        
        # Проверка наличия основных полей
        if project_data.get('project_id'): score += 1
        if project_data.get('project_type'): score += 1
        if project_data.get('files_count', 0) > 0: score += 1
        
        # Проверка наличия summary с рекомендациями
        summary = project_data.get('summary', {})
        if summary.get('features'): score += 1
        if summary.get('recommendations'): score += 1
        
        return score
        
    def test_project_preview(self, project_id):
        """Тест предпросмотра проекта"""
        try:
            response = self.session.get(
                f"{BASE_URL}/preview/{project_id}",
                timeout=10
            )
            
            if response.status_code == 200 and 'html' in response.headers.get('content-type', '').lower():
                content = response.text
                # Проверяем что контент не пустой и содержит HTML
                if len(content) > 100 and '<html' in content:
                    return True
                    
            return False
            
        except Exception as e:
            self.log(f"Ошибка предпросмотра: {e}", "ERROR")
            return False
            
    def run_performance_test(self):
        """Тест производительности - несколько одновременных запросов"""
        self.log("Запуск теста производительности...")
        
        def generate_project():
            response = self.session.post(
                f"{BASE_URL}/api/smart-generate-project",
                json={
                    "description": "Простой калькулятор с основными операциями",
                    "project_name": f"Тест производительности {time.time()}"
                },
                timeout=30
            )
            return response.status_code == 200
            
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(generate_project) for _ in range(3)]
            results = [f.result() for f in futures]
            
        duration = time.time() - start_time
        success_count = sum(results)
        
        self.log(f"Тест производительности: {success_count}/3 успешно за {duration:.2f}с", "SUCCESS" if success_count >= 2 else "ERROR")
        self.results["performance"]["concurrent_requests"] = {
            "duration": duration,
            "success_rate": success_count / 3
        }
        
        return success_count >= 2
        
    def generate_report(self):
        """Генерация итогового отчета"""
        print("\n" + "="*60)
        print("🎯 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
        print("="*60)
        
        # Общая статистика
        print(f"📊 Общие результаты:")
        print(f"   Всего тестов: {self.results['total_tests']}")
        print(f"   Успешно: {self.results['passed']}")
        print(f"   Неудачно: {self.results['failed']}")
        print(f"   Процент успеха: {(self.results['passed']/self.results['total_tests']*100):.1f}%")
        
        # Производительность
        if self.results["performance"]:
            print(f"\n⚡ Производительность:")
            if "registration" in self.results["performance"]:
                print(f"   Регистрация: {self.results['performance']['registration']:.2f}с")
            if "concurrent_requests" in self.results["performance"]:
                perf = self.results["performance"]["concurrent_requests"]
                print(f"   Параллельные запросы: {perf['duration']:.2f}с, успех: {perf['success_rate']*100:.1f}%")
        
        # Сценарии пользователей
        if self.results["user_scenarios"]:
            print(f"\n👥 Пользовательские сценарии:")
            for scenario in self.results["user_scenarios"]:
                status = "✅" if scenario["success"] else "❌"
                print(f"   {status} {scenario['name']}:")
                if scenario["success"]:
                    print(f"      Время создания: {scenario['generation_time']:.2f}с")
                    print(f"      Тип проекта: {scenario['project_type']} {'✓' if scenario['type_match'] else '✗'}")
                    print(f"      Качество: {scenario['quality_score']}/5")
                    print(f"      Предпросмотр: {'✓' if scenario['preview_works'] else '✗'}")
        
        # Рекомендации
        print(f"\n💡 Рекомендации:")
        if self.results["failed"] == 0:
            print("   🎉 Все тесты прошли успешно! Система работает отлично.")
        else:
            print(f"   ⚠️ {self.results['failed']} тестов не прошли. Требуется доработка:")
            for error in self.results["errors"]:
                print(f"      • {error}")
                
        print("="*60)
        
    def run_full_test_suite(self):
        """Запуск полного набора тестов"""
        print("🚀 ЗАПУСК КОМПЛЕКСНОГО ТЕСТИРОВАНИЯ VIBECODE AI PLATFORM")
        print("="*60)
        
        # 1. Проверка доступности сервера
        if not self.test_server_availability():
            self.results["errors"].append("Сервер недоступен")
            self.results["failed"] += 1
            self.results["total_tests"] += 1
            self.generate_report()
            return False
            
        self.results["passed"] += 1
        self.results["total_tests"] += 1
        
        # 2. Регистрация пользователя
        user_data = self.test_user_registration()
        self.results["total_tests"] += 1
        if user_data:
            self.results["passed"] += 1
            
            # 3. Вход пользователя
            if self.test_user_login(user_data):
                self.results["passed"] += 1
            else:
                self.results["failed"] += 1
                self.results["errors"].append("Ошибка входа пользователя")
            self.results["total_tests"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append("Ошибка регистрации пользователя")
            
        # 4. Тестирование пользовательских сценариев
        for scenario in TEST_SCENARIOS:
            self.results["total_tests"] += 1
            result = self.test_project_generation(scenario)
            if result and result["success"]:
                self.results["passed"] += 1
                self.results["user_scenarios"].append(result)
            else:
                self.results["failed"] += 1
                self.results["errors"].append(f"Сценарий '{scenario['name']}' не прошел")
        
        # 5. Тест производительности
        self.results["total_tests"] += 1
        if self.run_performance_test():
            self.results["passed"] += 1
        else:
            self.results["failed"] += 1
            self.results["errors"].append("Тест производительности не прошел")
            
        # Генерируем отчет
        self.generate_report()
        
        return self.results["failed"] == 0

if __name__ == "__main__":
    print("🎯 VIBECODE AI PLATFORM - КОМПЛЕКСНОЕ ТЕСТИРОВАНИЕ")
    print("=" * 60)
    
    test_suite = VibecodeTestSuite()
    success = test_suite.run_full_test_suite()
    
    sys.exit(0 if success else 1)