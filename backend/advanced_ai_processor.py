#!/usr/bin/env python3
"""
Продвинутый AI процессор для глубокой обработки запросов
Конкурирует с Lovable.dev, V0.dev, Bolt.new
"""

import os
import re
import json
import requests
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum

class RequestType(Enum):
    """Типы запросов пользователя"""
    CREATE_NEW_PROJECT = "create_new"
    MODIFY_EXISTING = "modify_existing"  
    ADD_FEATURE = "add_feature"
    FIX_BUG = "fix_bug"
    IMPROVE_DESIGN = "improve_design"
    GENERAL_QUESTION = "general_question"
    CODE_REVIEW = "code_review"

class ProjectType(Enum):
    """Типы проектов"""
    LANDING_PAGE = "landing"
    E_COMMERCE = "ecommerce"
    PORTFOLIO = "portfolio"
    BLOG = "blog"
    DASHBOARD = "dashboard"
    GAME = "game"
    CALCULATOR = "calculator"
    TODO_APP = "todo"
    CHAT_APP = "chat"
    WEATHER_APP = "weather"
    SOCIAL_APP = "social"
    FITNESS_APP = "fitness"

@dataclass
class AnalyzedRequest:
    """Результат анализа запроса"""
    request_type: RequestType
    project_type: Optional[ProjectType]
    features: List[str]
    tech_stack: List[str]
    design_requirements: List[str]
    complexity: str  # "simple", "medium", "complex"
    confidence: float
    extracted_data: Dict[str, Any]

@dataclass 
class GeneratedProject:
    """Результат генерации проекта"""
    project_id: str
    name: str
    description: str
    files: Dict[str, str]  # filename -> content
    preview_url: Optional[str]
    technologies: List[str]
    features: List[str]
    instructions: str

class AdvancedAIProcessor:
    """Продвинутый AI процессор для обработки пользовательских запросов"""
    
    def __init__(self):
        self.huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        self.default_ai = os.getenv('DEFAULT_AI', 'groq')
        
        # Модели для разных задач
        self.models = {
            'groq': {
                'fast': 'llama3-8b-8192',      # Быстрая модель для анализа
                'smart': 'llama3-70b-8192',    # Умная модель для генерации
                'code': 'mixtral-8x7b-32768'   # Специально для кода
            },
            'huggingface': {
                'code': 'codellama/CodeLlama-34b-Instruct-hf',
                'text': 'meta-llama/Llama-2-70b-chat-hf'
            }
        }
        
        # Шаблоны проектов
        self.project_templates = self._load_project_templates()
        
    def analyze_user_request(self, message: str, context: List[Dict] = None) -> AnalyzedRequest:
        """Анализирует запрос пользователя и определяет что нужно делать"""
        
        # Очистка и предобработка
        cleaned_message = self._preprocess_message(message)
        
        # Определение типа запроса
        request_type = self._detect_request_type(cleaned_message)
        
        # Определение типа проекта
        project_type = self._detect_project_type(cleaned_message)
        
        # Извлечение функций и требований
        features = self._extract_features(cleaned_message)
        tech_stack = self._extract_tech_stack(cleaned_message) 
        design_requirements = self._extract_design_requirements(cleaned_message)
        
        # Оценка сложности
        complexity = self._assess_complexity(features, tech_stack)
        
        # AI анализ для улучшения понимания
        ai_analysis = self._ai_deep_analysis(cleaned_message, request_type, project_type)
        
        return AnalyzedRequest(
            request_type=request_type,
            project_type=project_type,
            features=features,
            tech_stack=tech_stack,
            design_requirements=design_requirements,
            complexity=complexity,
            confidence=ai_analysis.get('confidence', 0.8),
            extracted_data=ai_analysis
        )
    
    def generate_project(self, request: AnalyzedRequest, user_preferences: Dict = None) -> GeneratedProject:
        """Генерирует готовый проект на основе анализа запроса"""
        
        # Выбираем подходящий шаблон
        base_template = self._select_template(request.project_type)
        
        # Генерируем код с AI
        generated_files = self._generate_project_files(request, base_template)
        
        # Создаем проект
        project_id = f"proj_{int(time.time())}_{hash(request.extracted_data.get('name', 'app')) % 10000}"
        
        return GeneratedProject(
            project_id=project_id,
            name=request.extracted_data.get('name', 'AI Generated App'),
            description=request.extracted_data.get('description', 'Приложение созданное AI'),
            files=generated_files,
            preview_url=f"/preview/{project_id}",
            technologies=request.tech_stack or ['HTML5', 'CSS3', 'JavaScript'],
            features=request.features,
            instructions=self._generate_instructions(request, generated_files)
        )
    
    def modify_project(self, project_id: str, modification_request: str, current_files: Dict[str, str]) -> Dict[str, str]:
        """Модифицирует существующий проект"""
        
        # Анализируем запрос на изменения
        analysis = self.analyze_user_request(modification_request)
        
        # Генерируем изменения
        modified_files = self._generate_modifications(current_files, analysis)
        
        return modified_files
    
    def _preprocess_message(self, message: str) -> str:
        """Предобработка сообщения пользователя"""
        # Убираем лишние пробелы и переводы строк
        cleaned = re.sub(r'\s+', ' ', message).strip()
        
        # Исправляем типичные опечатки
        cleaned = re.sub(r'\b(сайт|sight)\b', 'сайт', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\b(игру|game)\b', 'игра', cleaned, flags=re.IGNORECASE)
        
        return cleaned
    
    def _detect_request_type(self, message: str) -> RequestType:
        """Определяет тип запроса"""
        
        create_keywords = ['создай', 'сделай', 'построй', 'разработай', 'generate', 'create', 'make', 'build']
        modify_keywords = ['измени', 'обнови', 'исправь', 'добавь', 'убери', 'modify', 'change', 'update', 'add', 'remove']
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in create_keywords):
            return RequestType.CREATE_NEW_PROJECT
        elif any(keyword in message_lower for keyword in modify_keywords):
            return RequestType.MODIFY_EXISTING
        else:
            return RequestType.GENERAL_QUESTION
    
    def _detect_project_type(self, message: str) -> Optional[ProjectType]:
        """Определяет тип проекта"""
        
        patterns = {
            ProjectType.LANDING_PAGE: ['лендинг', 'landing', 'сайт-визитка', 'одностраничник'],
            ProjectType.E_COMMERCE: ['магазин', 'интернет-магазин', 'ecommerce', 'shop', 'store'],
            ProjectType.PORTFOLIO: ['портфолио', 'portfolio', 'резюме', 'cv'],
            ProjectType.BLOG: ['блог', 'blog', 'новости', 'статьи'],
            ProjectType.DASHBOARD: ['дашборд', 'dashboard', 'панель управления', 'админка'],
            ProjectType.GAME: ['игра', 'game', 'игру', 'тетрис', 'змейка', 'арканоид'],
            ProjectType.CALCULATOR: ['калькулятор', 'calculator', 'счетчик'],
            ProjectType.TODO_APP: ['todo', 'список дел', 'задачи', 'планировщик'],
            ProjectType.CHAT_APP: ['чат', 'chat', 'мессенджер'],
            ProjectType.WEATHER_APP: ['погода', 'weather', 'прогноз погоды'],
        }
        
        message_lower = message.lower()
        
        for project_type, keywords in patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return project_type
        
        return None
    
    def _extract_features(self, message: str) -> List[str]:
        """Извлекает функции из описания"""
        
        feature_patterns = {
            'авторизация': ['авторизация', 'регистрация', 'вход', 'login', 'auth'],
            'корзина': ['корзина', 'cart', 'basket'],
            'поиск': ['поиск', 'search', 'найти'],
            'фильтры': ['фильтр', 'filter', 'сортировка'],
            'комментарии': ['комментарии', 'comments', 'отзывы'],
            'уведомления': ['уведомления', 'notifications', 'alerts'],
            'темная тема': ['темная тема', 'dark theme', 'dark mode'],
            'адаптивность': ['адаптивный', 'responsive', 'мобильный'],
            'анимации': ['анимация', 'animation', 'эффекты']
        }
        
        found_features = []
        message_lower = message.lower()
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                found_features.append(feature)
        
        return found_features
    
    def _extract_tech_stack(self, message: str) -> List[str]:
        """Извлекает технологический стек"""
        
        tech_patterns = {
            'React': ['react', 'реакт'],
            'Vue': ['vue', 'вью'],
            'Angular': ['angular', 'ангуляр'],
            'Bootstrap': ['bootstrap', 'бутстрап'],
            'Tailwind': ['tailwind'],
            'TypeScript': ['typescript', 'ts'],
            'Node.js': ['node', 'nodejs'],
            'Python': ['python', 'питон'],
            'PHP': ['php', 'пхп']
        }
        
        found_tech = ['HTML5', 'CSS3', 'JavaScript']  # База по умолчанию
        message_lower = message.lower()
        
        for tech, keywords in tech_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                found_tech.append(tech)
        
        return found_tech
    
    def _extract_design_requirements(self, message: str) -> List[str]:
        """Извлекает требования к дизайну"""
        
        design_patterns = {
            'минимализм': ['минимализм', 'minimalist', 'простой', 'чистый'],
            'яркий': ['яркий', 'colorful', 'цветной'],
            'современный': ['современный', 'modern', 'модерн'],
            'корпоративный': ['корпоративный', 'corporate', 'деловой'],
            'игровой': ['игровой', 'gaming', 'геймерский']
        }
        
        found_design = []
        message_lower = message.lower()
        
        for design, keywords in design_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                found_design.append(design)
        
        return found_design
    
    def _assess_complexity(self, features: List[str], tech_stack: List[str]) -> str:
        """Оценивает сложность проекта"""
        
        complexity_score = len(features) + (len(tech_stack) - 3) * 0.5
        
        if complexity_score <= 2:
            return "simple"
        elif complexity_score <= 5:
            return "medium" 
        else:
            return "complex"
    
    def _ai_deep_analysis(self, message: str, request_type: RequestType, project_type: Optional[ProjectType]) -> Dict[str, Any]:
        """Глубокий AI анализ запроса"""
        
        prompt = f"""
        Проанализируй запрос пользователя для создания веб-приложения:
        
        Запрос: "{message}"
        Определенный тип: {request_type.value}
        Определенный проект: {project_type.value if project_type else 'неизвестно'}
        
        Извлеки и верни в JSON:
        {{
            "name": "название проекта",
            "description": "подробное описание", 
            "main_purpose": "основная цель",
            "target_audience": "целевая аудитория",
            "key_pages": ["список страниц"],
            "color_scheme": "цветовая схема",
            "confidence": 0.95
        }}
        """
        
        try:
            if self.default_ai == 'groq' and self.groq_api_key:
                return self._call_groq_api(prompt, model='llama3-8b-8192')
            elif self.huggingface_token:
                return self._call_huggingface_api(prompt)
        except:
            pass
        
        # Fallback анализ
        return {
            "name": "AI Generated App",
            "description": "Приложение созданное на основе пользовательского запроса",
            "confidence": 0.7
        }
    
    def _call_groq_api(self, prompt: str, model: str = 'llama3-8b-8192') -> Dict[str, Any]:
        """Вызов Groq API"""
        
        headers = {
            'Authorization': f'Bearer {self.groq_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messages': [
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'model': model,
            'temperature': 0.1,
            'max_tokens': 1024
        }
        
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Попытка извлечь JSON
            try:
                # Ищем JSON в ответе
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
        
        return {"confidence": 0.5}
    
    def _call_huggingface_api(self, prompt: str) -> Dict[str, Any]:
        """Вызов Hugging Face API"""
        
        headers = {
            'Authorization': f'Bearer {self.huggingface_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': 512,
                'temperature': 0.1
            }
        }
        
        try:
            response = requests.post(
                'https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf',
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    content = result[0].get('generated_text', '')
                    # Простой анализ ответа
                    return {"confidence": 0.8}
        except:
            pass
            
        return {"confidence": 0.6}
    
    def _load_project_templates(self) -> Dict[ProjectType, Dict]:
        """Загружает шаблоны проектов"""
        
        return {
            ProjectType.LANDING_PAGE: {
                'structure': ['index.html', 'styles.css', 'script.js'],
                'features': ['hero_section', 'about', 'services', 'contact'],
                'complexity': 'simple'
            },
            ProjectType.GAME: {
                'structure': ['index.html', 'styles.css', 'game.js'],
                'features': ['game_canvas', 'controls', 'score', 'animations'],
                'complexity': 'medium'
            },
            ProjectType.E_COMMERCE: {
                'structure': ['index.html', 'styles.css', 'shop.js', 'cart.js'],
                'features': ['product_catalog', 'cart', 'checkout', 'search'],
                'complexity': 'complex'
            }
        }
    
    def _select_template(self, project_type: Optional[ProjectType]) -> Dict:
        """Выбирает подходящий шаблон"""
        
        if project_type and project_type in self.project_templates:
            return self.project_templates[project_type]
        
        # Шаблон по умолчанию
        return self.project_templates[ProjectType.LANDING_PAGE]
    
    def _generate_project_files(self, request: AnalyzedRequest, template: Dict) -> Dict[str, str]:
        """Генерирует файлы проекта с помощью AI"""
        
        files = {}
        
        # Генерируем HTML
        html_prompt = self._create_html_prompt(request)
        html_content = self._generate_with_ai(html_prompt, 'code')
        files['index.html'] = html_content
        
        # Генерируем CSS  
        css_prompt = self._create_css_prompt(request)
        css_content = self._generate_with_ai(css_prompt, 'code')
        files['styles.css'] = css_content
        
        # Генерируем JavaScript
        js_prompt = self._create_js_prompt(request)
        js_content = self._generate_with_ai(js_prompt, 'code')
        files['script.js'] = js_content
        
        return files
    
    def _create_html_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации HTML"""
        
        return f"""
        Создай современный HTML файл для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        Требования:
        - Функции: {', '.join(request.features)}
        - Технологии: {', '.join(request.tech_stack)}
        - Дизайн: {', '.join(request.design_requirements)}
        - Адаптивный дизайн
        - Семантичная разметка HTML5
        - Подключение styles.css и script.js
        
        Верни только чистый HTML код без объяснений.
        """
    
    def _create_css_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации CSS"""
        
        return f"""
        Создай современные CSS стили для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        Требования:
        - Дизайн: {', '.join(request.design_requirements)}
        - Адаптивность для мобильных
        - Современные CSS3 свойства
        - Анимации и переходы
        - Flexbox/Grid макет
        - Красивые цвета и типографика
        
        Верни только чистый CSS код без объяснений.
        """
    
    def _create_js_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации JavaScript"""
        
        return f"""
        Создай интерактивный JavaScript для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        Функции для реализации:
        {', '.join(request.features)}
        
        Требования:
        - Современный ES6+ JavaScript
        - Обработка событий
        - Валидация форм (если есть)
        - Анимации
        - Адаптивное поведение
        
        Верни только чистый JavaScript код без объяснений.
        """
    
    def _generate_with_ai(self, prompt: str, task_type: str = 'code') -> str:
        """Генерирует код с помощью AI"""
        
        try:
            if self.default_ai == 'groq' and self.groq_api_key:
                result = self._call_groq_api(prompt, model=self.models['groq']['code'])
                if 'content' in result:
                    return result['content']
        except:
            pass
        
        # Fallback - простой шаблон
        return self._generate_fallback_code(task_type)
    
    def _generate_fallback_code(self, file_type: str) -> str:
        """Генерирует базовый код если AI недоступен"""
        
        if file_type == 'html':
            return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <header>
        <h1>Добро пожаловать!</h1>
    </header>
    <main>
        <p>Ваше приложение создано с помощью AI</p>
    </main>
    <script src="script.js"></script>
</body>
</html>'''
        elif file_type == 'css':
            return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    text-align: center;
    padding: 2rem;
}

main {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}'''
        else:  # JavaScript
            return '''// AI Generated JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded successfully!');
    
    // Add your interactive features here
});'''
    
    def _generate_modifications(self, current_files: Dict[str, str], analysis: AnalyzedRequest) -> Dict[str, str]:
        """Генерирует модификации существующего проекта"""
        
        modified_files = current_files.copy()
        
        # Анализируем что нужно изменить и генерируем с AI
        for filename, content in current_files.items():
            modification_prompt = f"""
            Модифицируй следующий код согласно требованиям:
            
            Требования: {', '.join(analysis.features)}
            
            Текущий код:
            {content}
            
            Верни только обновленный код без объяснений.
            """
            
            modified_content = self._generate_with_ai(modification_prompt, 'code')
            if modified_content and modified_content != content:
                modified_files[filename] = modified_content
        
        return modified_files
    
    def _generate_instructions(self, request: AnalyzedRequest, files: Dict[str, str]) -> str:
        """Генерирует инструкции по использованию"""
        
        return f"""
        🎉 Ваш проект готов!
        
        📁 Созданные файлы:
        {', '.join(files.keys())}
        
        ✨ Реализованные функции:
        {', '.join(request.features) if request.features else 'Базовый функционал'}
        
        🛠 Технологии:
        {', '.join(request.tech_stack)}
        
        📝 Дальнейшие шаги:
        1. Откройте index.html в браузере
        2. Протестируйте все функции
        3. При необходимости запросите доработки через чат
        
        💡 Для модификации просто напишите что хотите изменить!
        """