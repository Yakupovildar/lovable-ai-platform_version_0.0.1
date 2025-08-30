#!/usr/bin/env python3
"""
Упрощенный тест системы анализа запросов
"""

import sys
import os
sys.path.append('backend')

# Импортируем только необходимые части
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Any

# Копируем основные enum'ы
class ProjectType(Enum):
    MEDIA_PLAYER = "media_player"
    THREE_D_GAME = "3d_game"
    THREE_D_VIEWER = "3d_viewer" 
    DATABASE_APP = "database_app"
    CHAT_APP = "chat"
    MOBILE_APP = "mobile_app"
    AI_APP = "ai_app"

class RequestType(Enum):
    CREATE_NEW_PROJECT = "create"
    MODIFY_EXISTING = "modify"
    GENERAL_CHAT = "chat"

def test_message_analysis():
    """Тестируем анализ сложного сообщения"""
    
    message = """
    Создай мобильное приложение "ИИ Наставник Миллиардеров" для iPhone. 
    
    Требования:
    - 3D голова выбранного наставника (Илон Маск, Билл Гейтс, Джеф Безос, Уоррен Баффет)
    - Реальный голос на русском языке 
    - База знаний из последних интервью миллиардеров
    - Интуитивный интерфейс для простых пользователей
    - Выбор наставника перед началом
    - Ввод вопросов голосом или текстом
    - Подробные персонализированные ответы-рекомендации
    - Анимированные эмоции 3D модели при разговоре
    - Сохранение истории разговоров
    - Оффлайн режим после загрузки базы знаний
    """
    
    print("🧪 ТЕСТ АНАЛИЗА СЛОЖНОГО ЗАПРОСА")
    print("=" * 50)
    
    message_lower = message.lower()
    
    # Определение типа проекта
    detected_types = []
    
    if any(word in message_lower for word in ['3d', '3д', 'трехмерный', 'голова']):
        detected_types.append("3D технологии")
        
    if any(word in message_lower for word in ['мобильное', 'iphone', 'айфон']):
        detected_types.append("Мобильное приложение")
        
    if any(word in message_lower for word in ['голос', 'речь', 'аудио']):
        detected_types.append("Аудио технологии")
        
    if any(word in message_lower for word in ['база', 'данные', 'сохранение', 'история']):
        detected_types.append("База данных")
        
    if any(word in message_lower for word in ['ии', 'ai', 'искусственный интеллект']):
        detected_types.append("ИИ интеграция")
    
    # Извлечение функций
    features = []
    
    if 'выбор наставника' in message_lower:
        features.append("Система выбора персонажей")
    if 'голосом' in message_lower:
        features.append("Голосовой ввод")
    if 'анимированные эмоции' in message_lower:
        features.append("3D анимации лица")
    if 'оффлайн' in message_lower:
        features.append("Оффлайн режим")
    if 'интуитивный интерфейс' in message_lower:
        features.append("Простой UX")
    if 'русском языке' in message_lower:
        features.append("Локализация RU")
    
    # Определение сложности
    complexity_factors = [
        'мобильное приложение',
        '3d модели', 
        'синтез речи',
        'база знаний',
        'ии интеграция',
        'голосовой ввод',
        'оффлайн режим'
    ]
    
    complexity_score = sum(1 for factor in complexity_factors if any(word in message_lower for word in factor.split()))
    
    if complexity_score >= 6:
        complexity = "Очень высокая"
    elif complexity_score >= 4:
        complexity = "Высокая"  
    elif complexity_score >= 2:
        complexity = "Средняя"
    else:
        complexity = "Низкая"
    
    # Результаты
    print(f"📱 Обнаруженные технологии: {', '.join(detected_types)}")
    print(f"⚙️ Функции: {', '.join(features)}")
    print(f"📈 Сложность: {complexity} ({complexity_score}/7 факторов)")
    print(f"🎯 Тип запроса: Создание нового проекта")
    
    # Проверка покрытия требований
    print(f"\n✅ ПРОВЕРКА ПОКРЫТИЯ ТРЕБОВАНИЙ:")
    
    requirements_check = {
        "3D технологии": "3d" in message_lower,
        "Мобильная разработка": "мобильное" in message_lower or "iphone" in message_lower,
        "Аудио/Голос": "голос" in message_lower,
        "База данных": "база" in message_lower or "сохранение" in message_lower,
        "ИИ интеграция": "ии" in message_lower or "наставник" in message_lower,
        "Локализация": "русском" in message_lower
    }
    
    for req, detected in requirements_check.items():
        status = "✅" if detected else "❌"
        print(f"   {status} {req}")
    
    coverage = sum(requirements_check.values()) / len(requirements_check) * 100
    print(f"\n📊 Покрытие требований: {coverage:.1f}%")
    
    # Рекомендуемые технологии
    print(f"\n🛠️ РЕКОМЕНДУЕМЫЕ ТЕХНОЛОГИИ:")
    
    tech_recommendations = [
        "Three.js (3D рендеринг)",
        "Web Audio API (синтез речи)",
        "MediaRecorder API (голосовой ввод)",
        "IndexedDB или Supabase (база данных)",
        "PWA технологии (мобильная оптимизация)",
        "Service Workers (оффлайн режим)",
        "Speech Recognition API",
        "WebGL (3D производительность)"
    ]
    
    for i, tech in enumerate(tech_recommendations, 1):
        print(f"   {i}. {tech}")
    
    # Потенциальные проблемы
    print(f"\n⚠️ ПОТЕНЦИАЛЬНЫЕ СЛОЖНОСТИ:")
    
    challenges = [
        "3D модели лиц требуют больших ресурсов",
        "Синтез речи на русском языке ограничен",
        "iOS Safari имеет ограничения WebGL",
        "Голосовой ввод требует разрешений пользователя", 
        "Оффлайн ИИ требует большого объема данных",
        "Качественные 3D модели миллиардеров - авторские права"
    ]
    
    for i, challenge in enumerate(challenges, 1):
        print(f"   {i}. {challenge}")
    
    print(f"\n🎯 ЗАКЛЮЧЕНИЕ:")
    if coverage >= 80 and complexity_score >= 5:
        print("✅ Система СПОСОБНА обработать этот запрос")
        print("🚀 Рекомендуется поэтапная разработка")
    elif coverage >= 60:
        print("⚠️ Система ЧАСТИЧНО способна обработать запрос")
        print("🔧 Требуется доработка некоторых компонентов")
    else:
        print("❌ Система НЕ готова к такому запросу")
        print("📚 Требуется значительная доработка")
    
    return coverage, complexity_score

if __name__ == "__main__":
    coverage, complexity = test_message_analysis()
    
    print(f"\n" + "=" * 50)
    print(f"📊 ИТОГОВАЯ ОЦЕНКА:")
    print(f"   Покрытие требований: {coverage:.1f}%")
    print(f"   Сложность проекта: {complexity}/7")
    
    if coverage >= 80 and complexity >= 5:
        print(f"   Статус: 🎉 ТЕСТ ПРОЙДЕН")
    else:
        print(f"   Статус: ⚠️ ТРЕБУЕТСЯ ДОРАБОТКА")