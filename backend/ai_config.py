import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class AIConfig:
    def __init__(self):
        # GigaChat (Sber) конфигурация
        self.gigachat_api_key = os.getenv('GIGACHAT_API_KEY', '')
        self.gigachat_enabled = bool(self.gigachat_api_key)
        
        # Yandex GPT конфигурация
        self.yandex_api_key = os.getenv('YANDEX_API_KEY', '')
        self.yandex_enabled = bool(self.yandex_api_key)
        
        # LocalAI конфигурация
        self.localai_url = os.getenv('LOCALAI_URL', 'http://localhost:8080')
        self.localai_enabled = os.getenv('LOCALAI_ENABLED', 'false').lower() == 'true'
        
        # Hugging Face Inference API (бесплатный)
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN', '')
        self.huggingface_enabled = bool(self.huggingface_token)
        
        # DeepSeek API (очень дешевый/бесплатный)  
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY', '')
        self.deepseek_enabled = bool(self.deepseek_api_key)
        
        # Groq API (быстрый и бесплатный)
        self.groq_api_key = os.getenv('GROQ_API_KEY', '')
        self.groq_enabled = bool(self.groq_api_key)
        
        # Настройки по умолчанию
        self.default_ai = os.getenv('DEFAULT_AI', 'gigachat')
        
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
        if self.gigachat_enabled:
            available.append('gigachat')
        if self.yandex_enabled:
            available.append('yandex')
        if self.localai_enabled:
            available.append('localai')
        if self.huggingface_enabled:
            available.append('huggingface')
        if self.deepseek_enabled:
            available.append('deepseek')
        if self.groq_enabled:
            available.append('groq')
        return available
    
    def is_ai_available(self, ai_name):
        """Проверяет доступность AI сервиса"""
        if ai_name == 'gigachat':
            return self.gigachat_enabled
        elif ai_name == 'yandex':
            return self.yandex_enabled
        elif ai_name == 'localai':
            return self.localai_enabled
        elif ai_name == 'huggingface':
            return self.huggingface_enabled
        elif ai_name == 'deepseek':
            return self.deepseek_enabled
        elif ai_name == 'groq':
            return self.groq_enabled
        return False
