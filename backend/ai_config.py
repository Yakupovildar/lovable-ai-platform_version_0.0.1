import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class AIConfig:
    def __init__(self):
        # Hugging Face Inference API (бесплатный)
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN', '')
        self.huggingface_enabled = bool(self.huggingface_token)
        
        # Groq API (быстрый и бесплатный)
        self.groq_api_key = os.getenv('GROQ_API_KEY', '')
        self.groq_enabled = bool(self.groq_api_key)
        
        # Настройки по умолчанию
        self.default_ai = os.getenv('DEFAULT_AI', 'huggingface')
        
        # Промпты для различных задач
        self.prompts = {
            'project_generation': """
            Создай веб-приложение на основе следующего описания: {description}
            
            Требования:
            - Используй современные технологии (HTML5, CSS3, JavaScript)
            - Сделай код чистым и хорошо документированным
            - Добавь интерактивность и анимации
            - Обеспечь адаптивный дизайн
            - Включи комментарии в коде
            
            Создай следующие файлы:
            1. index.html - основная структура
            2. styles.css - стили и анимации
            3. script.js - интерактивность
            4. README.md - описание проекта
            """,
            
            'project_improvement': """
            Улучши следующий код веб-приложения:
            
            {code}
            
            Улучшения должны включать:
            - Оптимизацию производительности
            - Улучшение UX/UI
            - Добавление новых функций
            - Исправление ошибок
            - Современные практики разработки
            """,
            
            'chat': """
            Ты - полезный AI ассистент для разработки веб-приложений.
            Помогай пользователям с:
            - Созданием проектов
            - Отладкой кода
            - Объяснением технологий
            - Советами по дизайну
            - Оптимизацией кода
            """,
            
            'code_review': """
            Проведи код-ревью следующего кода:
            
            {code}
            
            Проверь:
            - Качество кода
            - Безопасность
            - Производительность
            - Читаемость
            - Соответствие стандартам
            """
        }
    
    def get_available_ais(self):
        """Возвращает список доступных AI сервисов"""
        available = []
        if self.huggingface_enabled:
            available.append('huggingface')
        if self.groq_enabled:
            available.append('groq')
        return available
    
    def is_ai_available(self, ai_name):
        """Проверяет доступность AI сервиса"""
        if ai_name == 'huggingface':
            return self.huggingface_enabled
        elif ai_name == 'groq':
            return self.groq_enabled
        return False
