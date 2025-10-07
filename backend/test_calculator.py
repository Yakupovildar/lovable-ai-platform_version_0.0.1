#!/usr/bin/env python3
"""Тест генерации калькулятора"""

import sys
sys.path.append('.')

from advanced_ai_processor import AdvancedAIProcessor

def test_calculator_generation():
    """Тестируем генерацию калькулятора"""
    
    processor = AdvancedAIProcessor()
    
    # Анализируем запрос на калькулятор
    analysis = processor.analyze_user_request("Создай калькулятор")
    
    print(f"Тип запроса: {analysis.request_type}")
    print(f"Тип проекта: {analysis.project_type}")
    print(f"Особенности: {analysis.features}")
    
    # Генерируем проект
    project = processor.generate_project(analysis)
    
    print(f"\nПроект: {project.name}")
    print(f"Файлы: {list(project.files.keys())}")
    
    # Проверяем HTML на наличие элементов калькулятора
    html_content = project.files['index.html']
    calculator_keywords = ['calculator', 'калькулятор', 'button', 'кнопка', 'display', 'дисплей', 'result', 'результат']
    
    print(f"\nПроверка HTML на элементы калькулятора:")
    for keyword in calculator_keywords:
        if keyword.lower() in html_content.lower():
            print(f"✅ Найдено: {keyword}")
        else:
            print(f"❌ НЕ найдено: {keyword}")
    
    # Показываем первые строки HTML
    print(f"\nПервые строки HTML:")
    print('\n'.join(html_content.split('\n')[:15]))
    
    return project

if __name__ == "__main__":
    project = test_calculator_generation()
    print("\n" + "="*50)
    print("Тест завершен!")