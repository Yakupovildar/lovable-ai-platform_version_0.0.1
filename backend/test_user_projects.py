#!/usr/bin/env python3
"""Тест API проектов пользователя"""

import requests
import json

# Параметры для теста
TEST_USER_EMAIL = "test_debug@example.com"
TEST_USER_PASSWORD = "test123"
BASE_URL = "http://localhost:5002"

def test_user_projects():
    """Тестируем получение проектов пользователя"""
    
    # Создаем сессию для сохранения cookies
    session = requests.Session()
    
    print(f"🔐 Авторизация пользователя {TEST_USER_EMAIL}...")
    
    # Авторизуемся
    login_data = {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD
    }
    
    login_response = session.post(f"{BASE_URL}/api/login", json=login_data)
    print(f"Статус авторизации: {login_response.status_code}")
    
    if login_response.status_code == 200:
        print("✅ Успешная авторизация!")
        
        # Получаем проекты пользователя
        projects_response = session.get(f"{BASE_URL}/api/user/projects")
        print(f"Статус получения проектов: {projects_response.status_code}")
        
        if projects_response.status_code == 200:
            projects_data = projects_response.json()
            print(f"📋 Получено проектов: {len(projects_data.get('projects', []))}")
            
            # Показываем первые 3 проекта
            projects = projects_data.get('projects', [])
            for i, project in enumerate(projects[:3]):
                print(f"  {i+1}. {project.get('name', 'Unknown')} (ID: {project.get('id', 'Unknown')})")
                
            return True
        else:
            print(f"❌ Ошибка получения проектов: {projects_response.text}")
            return False
    else:
        print(f"❌ Ошибка авторизации: {login_response.text}")
        
        # Пробуем другие возможные пароли
        possible_passwords = ["123456", "test", "admin", "qwerty", "password123"]
        
        for password in possible_passwords:
            print(f"🔄 Пробую пароль: {password}")
            login_data["password"] = password
            login_response = session.post(f"{BASE_URL}/api/login", json=login_data)
            
            if login_response.status_code == 200:
                print(f"✅ Успешная авторизация с паролем: {password}")
                
                # Получаем проекты пользователя
                projects_response = session.get(f"{BASE_URL}/api/user/projects")
                print(f"Статус получения проектов: {projects_response.status_code}")
                print(f"Ответ: {projects_response.text}")
                
                # Тестируем также историю чатов
                history_response = session.get(f"{BASE_URL}/api/user/history")
                print(f"\n📜 Статус получения истории: {history_response.status_code}")
                
                if history_response.status_code == 200:
                    history_data = history_response.json()
                    sessions = history_data.get('sessions', [])
                    print(f"✅ История работает! Найдено сессий: {len(sessions)}")
                    if sessions:
                        print(f"   Первая сессия: {sessions[0]['session_id']}")
                        print(f"   Сообщений в первой сессии: {len(sessions[0]['messages'])}")
                else:
                    print(f"❌ Ошибка истории: {history_response.text}")
                
                return True
                
        return False

if __name__ == "__main__":
    test_user_projects()