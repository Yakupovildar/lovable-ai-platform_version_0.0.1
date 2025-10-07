#!/usr/bin/env python3
"""
Прямой тест AdvancedAIProcessor для проверки качества генерации приложений
Тест обходит авторизацию и напрямую тестирует уровень 1000/100
"""
import os
import sys
import json
import time
from datetime import datetime

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импорт системы
from advanced_ai_processor import AdvancedAIProcessor

def test_3d_calculator_generation():
    """🔥 ТЕСТ: Создание 3D калькулятора с революционными возможностями"""
    print("\n🚀 ЗАПУСК ТЕСТА: Генерация 3D калькулятора уровня 1000/100")
    print("="*70)
    
    # Инициализация процессора
    processor = AdvancedAIProcessor()
    
    # Тестовый запрос с 3D требованиями
    test_request = {
        "message": "создай приложение калькулятор с 3D элементами, голосовыми ответами, видео качество, профессиональный дизайн уровня Pixar",
        "user_id": "test_user_direct",
        "features": ["3D элементы", "голосовые ответы", "высокое качество видео", "профессиональный дизайн"]
    }
    
    print(f"📝 Запрос: {test_request['message']}")
    print(f"🎯 Функции: {', '.join(test_request['features'])}")
    print("-"*70)
    
    start_time = time.time()
    
    try:
        # Создаем запрос для анализа
        from advanced_ai_processor import AnalyzedRequest, ProjectType, RequestType
        
        analyzed_request = AnalyzedRequest(
            request_type=RequestType.CREATE_NEW_PROJECT,
            project_type=ProjectType.CALCULATOR,
            features=test_request.get("features", []),
            tech_stack=["HTML5", "CSS3", "JavaScript", "Three.js", "WebGL", "Web Audio API"],
            design_requirements=["3D", "professional", "interactive", "modern"],
            complexity="complex",
            confidence=0.95,
            extracted_data={
                "name": "3D Calculator Pro",
                "description": "Профессиональный 3D калькулятор с голосовыми функциями и видео качеством уровня Pixar"
            }
        )
        
        # Обработка запроса напрямую с callback функцией
        def progress_callback(msg, progress):
            print(f"🔄 {progress}%: {msg}")
            
        result = processor.generate_project(analyzed_request, progress_callback=progress_callback)
        
        processing_time = time.time() - start_time
        
        print(f"⏱️  Время обработки: {processing_time:.2f} секунд")
        print("-"*70)
        
        if result and result.files:
            print("✅ УСПЕХ! Приложение создано успешно")
            print(f"🆔 ID проекта: {result.project_id}")
            print(f"📁 Файлов создано: {len(result.files)}")
            
            # Анализируем качество созданных файлов
            files = result.files
            
            print("\n📋 АНАЛИЗ КАЧЕСТВА:")
            print("="*50)
            
            # HTML анализ
            if 'index.html' in files:
                html_content = files['index.html']
                html_score = analyze_html_quality(html_content)
                print(f"🌐 HTML качество: {html_score}/100")
            
            # CSS анализ  
            if 'styles.css' in files:
                css_content = files['styles.css']
                css_score = analyze_css_quality(css_content)
                print(f"🎨 CSS качество: {css_score}/100")
            
            # JavaScript анализ
            if 'script.js' in files:
                js_content = files['script.js']
                js_score = analyze_js_quality(js_content)
                print(f"⚡ JavaScript качество: {js_score}/100")
            
            # Общая оценка
            total_score = (html_score + css_score + js_score) / 3
            print(f"\n🏆 ОБЩАЯ ОЦЕНКА: {total_score:.1f}/100")
            
            if total_score >= 85:
                print("🎉 ОТЛИЧНОЕ КАЧЕСТВО! Цель достигнута!")
            elif total_score >= 70:
                print("✅ ХОРОШЕЕ КАЧЕСТВО!")
            else:
                print("⚠️  Качество требует улучшения")
                
            # Сохраняем результаты теста
            save_test_results(result, total_score, processing_time)
            
        else:
            print("❌ ОШИБКА при создании приложения")
            print(f"🔍 Причина: {result.error if hasattr(result, 'error') else 'Неизвестная ошибка'}")
            
    except Exception as e:
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {str(e)}")
        import traceback
        traceback.print_exc()

def analyze_html_quality(html_content):
    """Анализ качества HTML кода"""
    score = 0
    
    # Проверки профессиональных функций
    quality_checks = [
        ("DOCTYPE", "<!DOCTYPE html>" in html_content, 10),
        ("Мета теги", '<meta name="viewport"' in html_content, 10),
        ("Семантика", any(tag in html_content for tag in ['<header>', '<main>', '<section>']), 15),
        ("3D поддержка", "three.js" in html_content or "WebGL" in html_content, 20),
        ("PWA манифест", 'manifest' in html_content, 10),
        ("Структура", len(html_content.split('\n')) > 50, 10),
        ("Комментарии", "<!--" in html_content, 5),
        ("Аксессибилити", 'aria-' in html_content or 'role=' in html_content, 10),
        ("Оптимизация", 'loading="lazy"' in html_content, 5),
        ("Микроданные", 'itemscope' in html_content or 'schema.org' in html_content, 5)
    ]
    
    for check_name, condition, points in quality_checks:
        if condition:
            score += points
        print(f"    {'✓' if condition else '✗'} {check_name}: {points if condition else 0} баллов")
    
    return min(score, 100)

def analyze_css_quality(css_content):
    """Анализ качества CSS кода"""
    score = 0
    
    quality_checks = [
        ("CSS Grid/Flexbox", "display: grid" in css_content or "display: flex" in css_content, 15),
        ("Анимации", "@keyframes" in css_content or "animation:" in css_content, 15),
        ("Переменные", "--" in css_content and "var(" in css_content, 10),
        ("Медиа запросы", "@media" in css_content, 10),
        ("3D трансформы", "transform3d" in css_content or "perspective" in css_content, 20),
        ("Градиенты", "gradient" in css_content, 10),
        ("Тени", "box-shadow" in css_content or "text-shadow" in css_content, 5),
        ("Современный дизайн", "backdrop-filter" in css_content or "clip-path" in css_content, 10),
        ("Структура", len(css_content.split('\n')) > 100, 5)
    ]
    
    for check_name, condition, points in quality_checks:
        if condition:
            score += points
        print(f"    {'✓' if condition else '✗'} {check_name}: {points if condition else 0} баллов")
    
    return min(score, 100)

def analyze_js_quality(js_content):
    """Анализ качества JavaScript кода"""
    score = 0
    
    quality_checks = [
        ("ES6+ синтаксис", "const " in js_content and "=>" in js_content, 15),
        ("Модульность", "class " in js_content or "function " in js_content, 10),
        ("3D библиотеки", "THREE." in js_content or "WebGL" in js_content, 25),
        ("Аудио/Видео", "Audio" in js_content or "speechSynthesis" in js_content, 15),
        ("Обработка событий", "addEventListener" in js_content, 10),
        ("Асинхронность", "async " in js_content or "Promise" in js_content, 10),
        ("Валидация", "try" in js_content and "catch" in js_content, 5),
        ("DOM манипуляции", "querySelector" in js_content or "getElementById" in js_content, 5),
        ("Комментарии", "//" in js_content or "/*" in js_content, 5)
    ]
    
    for check_name, condition, points in quality_checks:
        if condition:
            score += points
        print(f"    {'✓' if condition else '✗'} {check_name}: {points if condition else 0} баллов")
    
    return min(score, 100)

def save_test_results(result, score, processing_time):
    """Сохранение результатов теста"""
    test_result = {
        "timestamp": datetime.now().isoformat(),
        "project_id": result.project_id if hasattr(result, 'project_id') else None,
        "quality_score": score,
        "processing_time": processing_time,
        "target_quality": "1000/100 (AAA level)",
        "files_generated": list(result.files.keys()) if hasattr(result, 'files') else [],
        "success": True
    }
    
    # Сохраняем в файл
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Результаты сохранены в test_results.json")

if __name__ == "__main__":
    print("🤖 ТЕСТ СИСТЕМЫ VIBECODE AI (1000/100 QUALITY)")
    print("Прямое тестирование AdvancedAIProcessor без авторизации")
    test_3d_calculator_generation()