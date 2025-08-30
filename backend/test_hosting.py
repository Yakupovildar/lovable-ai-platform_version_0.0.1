#!/usr/bin/env python3
"""Тест хостинг системы"""

import sys
sys.path.append('.')

from project_hosting_system import ProjectHostingSystem

def test_hosting():
    """Тестируем хостинг проекта"""
    
    hosting = ProjectHostingSystem()
    
    # Тестовые данные
    project_data = {
        'name': 'Test Calculator',
        'files': {
            'index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Test Calculator</title>
    <style>body { font-family: Arial; padding: 20px; }</style>
</head>
<body>
    <h1>Тестовый калькулятор</h1>
    <input type="text" id="display" readonly>
    <br><br>
    <button onclick="document.getElementById('display').value += '1'">1</button>
    <button onclick="document.getElementById('display').value += '2'">2</button>
    <button onclick="calculate()">=</button>
    <script>
        function calculate() {
            const display = document.getElementById('display');
            try {
                display.value = eval(display.value);
            } catch(e) {
                display.value = 'Error';
            }
        }
    </script>
</body>
</html>''',
            'styles.css': 'body { background: #f5f5f5; }',
            'script.js': 'console.log("Calculator loaded!");'
        },
        'description': 'Тестовый калькулятор',
        'technologies': ['HTML', 'CSS', 'JavaScript'],
        'features': ['Базовые вычисления']
    }
    
    # Создаем проект
    result = hosting.host_project(project_data, user_id='test_user')
    
    print(f"Проект создан: {result['project_id']}")
    print(f"URL: {result['live_url']}")
    
    return result

if __name__ == "__main__":
    result = test_hosting()
    print("\nТест завершен успешно!")