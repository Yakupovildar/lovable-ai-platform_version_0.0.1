#!/usr/bin/env python3
"""
Тест системы генерации сложного приложения - ИИ Наставник Миллиардеров
"""

import sys
import os
sys.path.append('backend')

from advanced_ai_processor import AdvancedAIProcessor, RequestType, ProjectType

def test_ai_mentor_generation():
    """Тестируем создание ИИ наставника с 3D и голосом"""
    
    processor = AdvancedAIProcessor()
    
    # Сложный запрос пользователя
    user_message = """
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
    
    Интерфейс должен быть максимально простым - даже бабушка сможет пользоваться. 
    Все на русском языке.
    """
    
    print("🧪 Тестируем генерацию сложного ИИ наставника...")
    print("📱 Запрос:", user_message[:100] + "...")
    
    # Анализируем запрос
    analysis = processor.analyze_user_request(user_message)
    
    print(f"\n📊 Результат анализа:")
    print(f"   🎯 Тип запроса: {analysis.request_type}")
    print(f"   📱 Тип проекта: {analysis.project_type}")
    print(f"   ⚙️ Функции: {', '.join(analysis.features[:5])}...")
    print(f"   🛠️ Технологии: {', '.join(analysis.tech_stack)}")
    print(f"   🎨 Дизайн: {', '.join(analysis.design_requirements)}")
    print(f"   📈 Сложность: {analysis.complexity}")
    print(f"   🎯 Уверенность: {analysis.confidence}%")
    
    if analysis.request_type == RequestType.CREATE_NEW_PROJECT:
        print(f"\n🚀 Генерируем проект...")
        
        # Генерируем проект
        generated_project = processor.generate_project(analysis)
        
        print(f"✅ Проект создан:")
        print(f"   📛 Название: {generated_project.name}")
        print(f"   📝 Описание: {generated_project.description}")
        print(f"   📁 Файлы: {', '.join(generated_project.files.keys())}")
        print(f"   🛠️ Технологии: {', '.join(generated_project.technologies)}")
        print(f"   ⚙️ Функции: {', '.join(generated_project.features)}")
        
        # Показываем превью HTML
        html_content = generated_project.files.get('index.html', '')
        if html_content:
            print(f"\n📄 HTML превью (первые 500 символов):")
            print(html_content[:500] + "..." if len(html_content) > 500 else html_content)
        
        # Проверяем наличие 3D технологий
        js_content = generated_project.files.get('script.js', '')
        if 'three.js' in js_content.lower() or 'webgl' in js_content.lower():
            print("✅ 3D технологии: Обнаружены")
        else:
            print("❌ 3D технологии: НЕ обнаружены")
            
        # Проверяем аудио
        if 'audio' in html_content.lower() or 'speech' in js_content.lower():
            print("✅ Аудио технологии: Обнаружены")
        else:
            print("❌ Аудио технологии: НЕ обнаружены")
            
        # Проверяем базу данных
        if any(db in js_content.lower() for db in ['supabase', 'firebase', 'indexeddb', 'localstorage']):
            print("✅ База данных: Обнаружена")
        else:
            print("❌ База данных: НЕ обнаружена")
        
        print(f"\n📋 Инструкции:")
        print(generated_project.instructions)
        
        # Генерируем рекомендации
        recommendations = processor.generate_project_recommendations(
            generated_project.files, 
            analysis.project_type
        )
        
        print(f"\n💡 Рекомендации по улучшению:")
        print(f"   📊 Всего предложений: {recommendations['summary']['total_suggestions']}")
        print(f"   🔥 Высокий приоритет: {recommendations['summary']['high_priority']}")
        print(f"   📋 Области улучшения: {', '.join(recommendations['summary']['improvement_areas'])}")
        
        return generated_project, recommendations
    
    else:
        print(f"❌ Проект не был сгенерирован. Тип запроса: {analysis.request_type}")
        return None, None

if __name__ == "__main__":
    project, recs = test_ai_mentor_generation()
    
    if project:
        print(f"\n🎉 Тест УСПЕШНО завершен!")
        print(f"📱 Создано приложение: {project.name}")
        print(f"🗂️ Файлов сгенерировано: {len(project.files)}")
    else:
        print(f"\n❌ Тест ПРОВАЛЕН!")