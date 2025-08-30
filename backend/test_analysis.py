#!/usr/bin/env python3
"""Тест анализа запросов AI процессора"""

import sys
sys.path.append('.')

from advanced_ai_processor import AdvancedAIProcessor, RequestType

def test_request_analysis():
    """Тестируем анализ различных запросов"""
    
    processor = AdvancedAIProcessor()
    
    test_requests = [
        "Создай калькулятор",
        "Сделай игру тетрис", 
        "Построй лендинг для кафе",
        "Привет, как дела?",
        "Что умеет твоя платформа?",
        "Измени цвет кнопки на красный",
        "Generate a calculator app",
        "Make a simple game"
    ]
    
    print("=== Тестирование анализа запросов ===\n")
    
    for i, request in enumerate(test_requests, 1):
        print(f"{i}. Тестируем запрос: '{request}'")
        print("-" * 50)
        
        try:
            analysis = processor.analyze_user_request(request)
            
            print(f"Тип запроса: {analysis.request_type}")
            print(f"Тип проекта: {analysis.project_type}")
            print(f"Описание: {analysis.extracted_data.get('description', 'N/A')}")
            print(f"Функции: {analysis.features}")
            print(f"Технологии: {analysis.tech_stack}")
            
        except Exception as e:
            print(f"ОШИБКА: {e}")
            
        print("\n" + "=" * 60 + "\n")

if __name__ == "__main__":
    test_request_analysis()