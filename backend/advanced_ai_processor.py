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
<<<<<<< HEAD
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
=======
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62

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
    PORTFOLIO_WEBSITE = "portfolio_website"
    AI_APP = "ai_app"
<<<<<<< HEAD
    AI_MENTOR = "ai_mentor"
    AI_COACH = "ai_coach"
    AI_ASSISTANT = "ai_assistant"
=======
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    MOBILE_APP = "mobile_app"
    BLOG = "blog"
    DASHBOARD = "dashboard"
    GAME = "game"
    IDLE_GAME = "idle_game"
    CALCULATOR = "calculator"
    TODO_APP = "todo"
    CHAT_APP = "chat"
    WEATHER_APP = "weather"
    SOCIAL_APP = "social"
    FITNESS_APP = "fitness"
    MEDIA_PLAYER = "media_player"
    VIDEO_EDITOR = "video_editor"
    MUSIC_APP = "music_app"
    THREE_D_GAME = "3d_game"
    THREE_D_VIEWER = "3d_viewer"
<<<<<<< HEAD
    THREE_D_AVATAR = "3d_avatar"
    VOICE_APP = "voice_app"
=======
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    DATABASE_APP = "database_app"
    RECORDING_APP = "recording_app"
    BUSINESS_LANDING = "business_landing"

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
        
<<<<<<< HEAD
        print(f"🔑 AI Keys loaded: Groq={'✅' if self.groq_api_key else '❌'}, Default AI: {self.default_ai}")
        
        # Модели для разных задач
        self.models = {
            'groq': {
                'fast': 'llama-3.1-8b-instant',      # Быстрая модель для анализа
                'smart': 'llama-3.1-70b-versatile',  # Умная модель для генерации
                'code': 'llama-3.1-8b-instant'       # Код генерация
=======
        # Модели для разных задач
        self.models = {
            'groq': {
                'fast': 'llama3-8b-8192',      # Быстрая модель для анализа
                'smart': 'llama3-70b-8192',    # Умная модель для генерации
                'code': 'mixtral-8x7b-32768'   # Специально для кода
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
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
    
<<<<<<< HEAD
    def generate_project(self, request: AnalyzedRequest, user_preferences: Dict = None, progress_callback=None) -> GeneratedProject:
        """🚀 РЕВОЛЮЦИОННАЯ СИСТЕМА! Генерирует проект через Groq AI с поэтапным прогрессом"""

        if progress_callback:
            progress_callback("🚀 Запуск революционной AI системы...", 1)

        # Инициализируем SmartAIGenerator
        from smart_ai_generator import SmartAIGenerator
        ai_generator = SmartAIGenerator()

        # Формируем описание проекта из запроса
        description = self._build_project_description(request)

        if progress_callback:
            progress_callback("📝 Подготовка описания проекта...", 3)

        # Генерируем проект через SmartAI с живым прогрессом
        project_result = ai_generator.generate_project(
            description=description,
            preferred_ai='groq',
            progress_callback=progress_callback
        )

        # Создаем проект ID
        project_id = f"proj_{int(time.time())}_{hash(request.extracted_data.get('name', 'app')) % 10000}"

        # Конвертируем результат в GeneratedProject
        generated_files = {}
        for file in project_result.files:
            generated_files[file.name] = file.content

        project = GeneratedProject(
            project_id=project_id,
            name=request.extracted_data.get('name', project_result.message.split('!')[-1] if project_result.success else 'AI Generated App'),
            description=request.extracted_data.get('description', 'Революционное приложение созданное через Groq AI'),
            files=generated_files,
            preview_url=f"/preview/{project_id}",
            technologies=request.tech_stack or self._extract_technologies_from_files(generated_files),
            features=request.features,
            instructions=project_result.instructions
        )

        return project

    def _build_project_description(self, request: AnalyzedRequest) -> str:
        """Строит детальное описание проекта для AI генератора"""
        description_parts = []

        # Основное описание
        if request.extracted_data.get('description'):
            description_parts.append(request.extracted_data['description'])

        # Название проекта
        if request.extracted_data.get('name'):
            description_parts.append(f"Название: {request.extracted_data['name']}")

        # Функции
        if request.features:
            description_parts.append(f"Функции: {', '.join(request.features)}")

        # Технологии
        if request.tech_stack:
            description_parts.append(f"Технологии: {', '.join(request.tech_stack)}")

        # Тип проекта
        if request.project_type:
            description_parts.append(f"Тип: {request.project_type.value}")

        return '. '.join(description_parts)

    def _extract_technologies_from_files(self, files: Dict[str, str]) -> List[str]:
        """Извлекает список технологий из сгенерированных файлов"""
        technologies = set()

        for filename in files.keys():
            if filename.endswith('.html'):
                technologies.add('HTML5')
            elif filename.endswith('.css'):
                technologies.add('CSS3')
            elif filename.endswith('.js'):
                technologies.add('JavaScript')
            elif filename.endswith('.json'):
                technologies.add('JSON')
            elif filename.endswith('.py'):
                technologies.add('Python')
            elif filename.endswith('.md'):
                technologies.add('Markdown')

        return list(technologies)
=======
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
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    
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
        print(f"Анализ запроса: '{message_lower}'")
        
        for keyword in create_keywords:
            if keyword in message_lower:
                print(f"Найдено ключевое слово создания: {keyword}")
                return RequestType.CREATE_NEW_PROJECT
                
        for keyword in modify_keywords:
            if keyword in message_lower:
                print(f"Найдено ключевое слово модификации: {keyword}")
                return RequestType.MODIFY_EXISTING
        
        print("Ключевые слова не найдены, возвращаю GENERAL_QUESTION")
        return RequestType.GENERAL_QUESTION
    
    def _detect_project_type(self, message: str) -> Optional[ProjectType]:
<<<<<<< HEAD
        """Определяет тип проекта с улучшенным алгоритмом для сложных запросов"""
        
        print(f"Определение типа проекта для: '{message}'")
        
        message_lower = message.lower()
        
        # ПРИОРИТЕТ 1: Проверка комплексных проектов (ИИ наставники, 3D приложения с наставниками)
        complex_patterns = {
            ProjectType.AI_MENTOR: [
                'ии наставник', 'ai наставник', 'наставник',
                'искусственный интеллект наставник',
                'приложение с наставником',
                'ментор', 'mentor', 'коуч', 'тренер'
            ],
            ProjectType.THREE_D_AVATAR: [
                '3d аватар', '3d avatar', '3d персонаж', 
                '3d character', 'аватар в 3d',
                'трёхмерный аватар', 'трехмерный аватар'
            ],
            ProjectType.THREE_D_GAME: [
                '3d игра', '3d game', 'трехмерная игра', 
                'трёхмерная игра', 'webgl игра'
            ],
            ProjectType.VOICE_APP: [
                'голосовой', 'voice', 'голос', 'речь',
                'говорить', 'слушать', 'распознавание речи',
                'text to speech', 'tts'
            ]
        }
        
        # Проверяем комплексные паттерны ПЕРВЫМИ
        for project_type, keywords in complex_patterns.items():
            for keyword in keywords:
                if keyword in message_lower:
                    print(f"🎯 Найден ПРИОРИТЕТНЫЙ тип проекта: {project_type.value} по ключевому слову: '{keyword}'")
                    return project_type
        
        # ПРИОРИТЕТ 2: Мобильные приложения
        if any(word in message_lower for word in [
            'мобильное приложение', 'mobile app', 'full stack',
            'фулл стак', 'полноценное приложение'
        ]):
            # Если есть упоминание 3D - делаем 3D приложение
            if any(word in message_lower for word in ['3d', '3д', 'трехмерный', 'трёхмерный']):
                print(f"🎯 Определен мобильный 3D проект")
                return ProjectType.THREE_D_GAME
            # Если есть наставник - делаем AI наставника
            elif any(word in message_lower for word in ['наставник', 'ии', 'ai', 'искусственный интеллект']):
                print(f"🎯 Определен мобильный AI наставник")
                return ProjectType.AI_MENTOR
            else:
                print(f"🎯 Определено общее мобильное приложение как игра")
                return ProjectType.GAME
        
        # ПРИОРИТЕТ 3: Стандартные паттерны
=======
        """Определяет тип проекта"""
        
        print(f"Определение типа проекта для: '{message}'")
        
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        patterns = {
            ProjectType.LANDING_PAGE: ['лендинг', 'landing', 'сайт-визитка', 'одностраничник'],
            ProjectType.E_COMMERCE: ['магазин', 'интернет-магазин', 'ecommerce', 'shop', 'store'],
            ProjectType.PORTFOLIO: ['портфолио', 'portfolio', 'резюме', 'cv'],
            ProjectType.BLOG: ['блог', 'blog', 'новости', 'статьи'],
            ProjectType.DASHBOARD: ['дашборд', 'dashboard', 'панель управления', 'админка'],
            ProjectType.GAME: ['игра', 'game', 'игру', 'тетрис', 'змейка', 'арканоид', 'clicker', 'кликер'],
            ProjectType.IDLE_GAME: ['idle', 'айдл', 'инкремент', 'clicker heroes', 'cookie clicker'],
            ProjectType.CALCULATOR: ['калькулятор', 'calculator', 'счетчик'],
            ProjectType.TODO_APP: ['todo', 'список дел', 'задачи', 'планировщик'],
            ProjectType.CHAT_APP: ['чат', 'chat', 'мессенджер'],
            ProjectType.WEATHER_APP: ['погода', 'weather', 'прогноз погоды'],
            ProjectType.MEDIA_PLAYER: ['плеер', 'player', 'музыка', 'music', 'видео', 'video', 'медиаплеер'],
            ProjectType.VIDEO_EDITOR: ['видеоредактор', 'video editor', 'монтаж', 'editing'],
            ProjectType.MUSIC_APP: ['музыкальное приложение', 'music app', 'аудио', 'audio'],
<<<<<<< HEAD
            ProjectType.THREE_D_VIEWER: ['3d просмотрщик', '3d viewer', '3d модели', 'three.js'],
            ProjectType.AI_COACH: ['ai тренер', 'ии тренер', 'персональный тренер', 'coach'],
            ProjectType.AI_ASSISTANT: ['ai помощник', 'ии помощник', 'ассистент', 'assistant'],
=======
            ProjectType.THREE_D_GAME: ['3d игра', '3d game', '3д', 'трехмерный', 'трёхмерный', 'webgl'],
            ProjectType.THREE_D_VIEWER: ['3d просмотрщик', '3d viewer', '3d модели', 'three.js'],
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
            ProjectType.DATABASE_APP: ['база данных', 'database', 'бд', 'crud', 'данные'],
            ProjectType.RECORDING_APP: ['запись', 'recording', 'диктофон', 'recorder', 'микрофон', 'камера'],
        }
        
<<<<<<< HEAD
        for project_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in message_lower:
                    print(f"Найден стандартный тип проекта: {project_type.value} по ключевому слову: '{keyword}'")
                    return project_type
        
        print("❌ Тип проекта не определен, возвращаю None")
        return None
    
    def _extract_features(self, message: str) -> List[str]:
        """Извлекает функции из описания с улучшенным распознаванием"""
        
        message_lower = message.lower()
        
        # КРИТИЧЕСКИЕ ФУНКЦИИ для full-stack приложений
        critical_features = {
            '3D графика': ['3d', '3д', 'three.js', 'webgl', 'трехмерный', '3d модель', 'трёхмерный'],
            'голосовой ввод': ['голос', 'voice', 'речь', 'говорить', 'микрофон', 'распознавание речи'],
            'озвучивание': ['озвучка', 'text to speech', 'tts', 'голосовой вывод', 'говорящий', 'отвечает голосом'],
            'ИИ наставник': ['ии наставник', 'ai наставник', 'наставник', 'mentor', 'искусственный интеллект'],
            'ИИ диалоги': ['диалог с ии', 'общение с ии', 'чат с ии', 'разговор с ии'],
            'полное меню': ['меню', 'навигация', 'главное меню', 'полное меню', 'navigation'],
            'настройки приложения': ['настройки', 'settings', 'конфигурация', 'параметры'],
            'мобильная адаптация': ['мобильное', 'mobile', 'смартфон', 'телефон', 'full stack']
        }
        
        # Стандартные функции
        standard_features = {
=======
        message_lower = message.lower()
        
        for project_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in message_lower:
                    print(f"Найден тип проекта: {project_type.value} по ключевому слову: '{keyword}'")
                    return project_type
        
        print("Тип проекта не определен, возвращаю None")
        return None
    
    def _extract_features(self, message: str) -> List[str]:
        """Извлекает функции из описания"""
        
        feature_patterns = {
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
            'авторизация': ['авторизация', 'регистрация', 'вход', 'login', 'auth'],
            'корзина': ['корзина', 'cart', 'basket'],
            'поиск': ['поиск', 'search', 'найти'],
            'фильтры': ['фильтр', 'filter', 'сортировка'],
            'комментарии': ['комментарии', 'comments', 'отзывы'],
            'уведомления': ['уведомления', 'notifications', 'alerts'],
            'темная тема': ['темная тема', 'dark theme', 'dark mode'],
<<<<<<< HEAD
            'адаптивность': ['адаптивный', 'responsive', 'адаптация'],
            'анимации': ['анимация', 'animation', 'эффекты'],
            'психологический анализ': ['психология', 'анализ', 'эмоции', 'настроение', 'личность'],
            'персонализация': ['персональный', 'индивидуальный', 'под пользователя'],
            'реалтайм': ['реальное время', 'real-time', 'онлайн', 'live', 'мгновенно'],
            'офлайн режим': ['офлайн', 'offline', 'без интернета', 'локально'],
            'история разговоров': ['история', 'сохранение', 'память', 'запоминание'],
            'мультиязычность': ['многоязычный', 'перевод', 'языки', 'локализация']
        }
        
        found_features = []
        
        # ПРИОРИТЕТ 1: Критические функции для full-stack приложений
        for feature, keywords in critical_features.items():
            if any(keyword in message_lower for keyword in keywords):
                found_features.append(feature)
                print(f"🔥 КРИТИЧЕСКАЯ ФУНКЦИЯ обнаружена: {feature}")
        
        # ПРИОРИТЕТ 2: Стандартные функции
        for feature, keywords in standard_features.items():
            if any(keyword in message_lower for keyword in keywords):
                found_features.append(feature)
                print(f"✅ Функция обнаружена: {feature}")
        
        # ПРИНУДИТЕЛЬНЫЕ ФУНКЦИИ для мобильных приложений
        if any(word in message_lower for word in ['мобильное приложение', 'mobile app', 'full stack', 'полноценное приложение']):
            mandatory_mobile_features = ['полное меню', 'настройки приложения', 'мобильная адаптация']
            for feature in mandatory_mobile_features:
                if feature not in found_features:
                    found_features.append(feature)
                    print(f"🔥 ОБЯЗАТЕЛЬНАЯ МОБИЛЬНАЯ ФУНКЦИЯ добавлена: {feature}")
        
        # ПРИНУДИТЕЛЬНЫЕ ФУНКЦИИ для ИИ наставников
        if any(word in message_lower for word in ['наставник', 'ии наставник', 'ai наставник']):
            mandatory_ai_features = ['ИИ наставник', 'ИИ диалоги']
            if 'голосовой' in message_lower or 'голос' in message_lower or 'отвечает голосом' in message_lower:
                mandatory_ai_features.extend(['озвучивание', 'голосовой ввод'])
            
            for feature in mandatory_ai_features:
                if feature not in found_features:
                    found_features.append(feature)
                    print(f"🤖 ОБЯЗАТЕЛЬНАЯ ИИ ФУНКЦИЯ добавлена: {feature}")
        
        print(f"🎯 Итоговые функции: {found_features}")
=======
            'адаптивность': ['адаптивный', 'responsive', 'мобильный'],
            'анимации': ['анимация', 'animation', 'эффекты']
        }
        
        found_features = []
        message_lower = message.lower()
        
        for feature, keywords in feature_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                found_features.append(feature)
        
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
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
<<<<<<< HEAD
                result = self._call_groq_api(prompt, model='llama-3.1-8b-instant')
                # Небольшая задержка между запросами для предотвращения rate limiting
                time.sleep(2)
                return result
=======
                return self._call_groq_api(prompt, model='llama3-8b-8192')
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
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
    
<<<<<<< HEAD
    def _call_groq_api(self, prompt: str, model: str = 'llama-3.1-8b-instant', max_retries: int = 3) -> Dict[str, Any]:
        """Вызов Groq API с обработкой rate limiting"""
=======
    def _call_groq_api(self, prompt: str, model: str = 'llama3-8b-8192') -> Dict[str, Any]:
        """Вызов Groq API"""
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        
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
        
<<<<<<< HEAD
        for attempt in range(max_retries):
            try:
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
                    
                    return {"confidence": 0.8}
                
                elif response.status_code == 429 or response.status_code == 413:
                    # Rate limit или request too large - ждем и повторяем
                    wait_time = (2 ** attempt) * 15  # Экспоненциальная задержка: 15s, 30s, 60s
                    error_type = "rate limit" if response.status_code == 429 else "request too large"
                    print(f"⏱️  Groq {error_type} - ждем {wait_time}с перед повтором (попытка {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                
                else:
                    print(f"❌ Groq API ошибка: {response.status_code} - {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(5)  # Короткая пауза перед повтором для других ошибок
                        continue
                    
            except Exception as e:
                print(f"❌ Groq API исключение: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
        
        return {"confidence": 0.5}
    
    def _call_groq_api_for_code(self, prompt: str, model: str = 'llama-3.1-8b-instant', max_retries: int = 3) -> str:
        """Вызов Groq API для генерации кода с обработкой rate limiting"""
=======
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
    
    def _call_groq_api_for_code(self, prompt: str, model: str = 'llama3-8b-8192') -> str:
        """Вызов Groq API для генерации кода"""
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        
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
            'max_tokens': 2048
        }
        
<<<<<<< HEAD
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    'https://api.groq.com/openai/v1/chat/completions',
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    print(f"🎯 Groq ответил: {len(content)} символов")
                    
                    # Извлекаем код из markdown блоков если есть
                    code_match = re.search(r'```(?:html|css|javascript|js)?\n(.*?)\n```', content, re.DOTALL)
                    if code_match:
                        return code_match.group(1).strip()
                    
                    # Возвращаем весь контент если нет markdown
                    return content.strip()
                
                elif response.status_code == 429 or response.status_code == 413:
                    # Rate limit или request too large - ждем и повторяем
                    wait_time = (2 ** attempt) * 20  # Экспоненциальная задержка: 20s, 40s, 80s для кода
                    error_type = "rate limit" if response.status_code == 429 else "request too large"
                    print(f"⏱️  Groq {error_type} для кода - ждем {wait_time}с перед повтором (попытка {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue
                    
                else:
                    print(f"❌ Groq API ошибка: {response.status_code} - {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(5)  # Короткая пауза перед повтором для других ошибок
                        continue
                        
            except Exception as e:
                print(f"❌ Groq API исключение: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                    continue
=======
        response = requests.post(
            'https://api.groq.com/openai/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            
            # Извлекаем код из markdown блоков если есть
            code_match = re.search(r'```(?:html|css|javascript|js)?\n(.*?)\n```', content, re.DOTALL)
            if code_match:
                return code_match.group(1).strip()
            
            # Возвращаем весь контент если нет markdown
            return content.strip()
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        
        return ""
    
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
<<<<<<< HEAD
            print(f"🤗 Вызываем Hugging Face API...")
            # Попробуем разные модели
            models_to_try = [
                'microsoft/DialoGPT-small',
                'facebook/blenderbot-400M-distill',
                'gpt2'
            ]
            
            for model in models_to_try:
                print(f"🔄 Пробуем модель: {model}")
                response = requests.post(
                    f'https://api-inference.huggingface.co/models/{model}',
                    headers=headers,
                    json=data,
                    timeout=30
                )
                
                print(f"📡 HF Status ({model}): {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"📝 HF Response: {result}")
                    
                    if isinstance(result, list) and len(result) > 0:
                        content = result[0].get('generated_text', '')
                        print(f"✅ HF сгенерировал: {len(content)} символов")
                        return {"content": content, "confidence": 0.8}
                    elif 'error' in result:
                        print(f"❌ HF ошибка модели {model}: {result['error']}")
                        continue  # Пробуем следующую модель
                    else:
                        print(f"✅ HF успешный ответ от {model}")
                        return {"content": str(result), "confidence": 0.8}
                else:
                    print(f"❌ HF HTTP ошибка ({model}): {response.text}")
                    continue  # Пробуем следующую модель
                
        except Exception as e:
            print(f"❌ HF Exception: {e}")
            
        return {"confidence": 0.0, "error": "API недоступен"}
=======
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
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    
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
    
<<<<<<< HEAD
    def _generate_project_files(self, request: AnalyzedRequest, template: Dict, progress_callback=None) -> Dict[str, str]:
        """Генерирует файлы проекта с помощью AI с прогрессом"""
        
        files = {}
        
        if progress_callback:
            progress_callback("📋 Начинаю создание проекта...", 0)
        
        # Генерируем HTML
        if progress_callback:
            progress_callback("📝 Создаю HTML структуру приложения...", 10)
        html_prompt = self._create_html_prompt(request)
        html_content = self._generate_with_ai(html_prompt, 'code', 
            lambda msg, prog: progress_callback(f"HTML: {msg}", 10 + prog * 0.3),
            target_file='index.html')
        files['index.html'] = html_content
        
        # Генерируем CSS
        if progress_callback:
            progress_callback("🎨 Разрабатываю дизайн и стили...", 40)
        css_prompt = self._create_css_prompt(request)
        css_content = self._generate_with_ai(css_prompt, 'code',
            lambda msg, prog: progress_callback(f"CSS: {msg}", 40 + prog * 0.3),
            target_file='styles.css')
        files['styles.css'] = css_content
        
        # Генерируем JavaScript
        if progress_callback:
            progress_callback("⚡ Программирую логику приложения...", 70)
        js_prompt = self._create_js_prompt(request)
        js_content = self._generate_with_ai(js_prompt, 'code',
            lambda msg, prog: progress_callback(f"JS: {msg}", 70 + prog * 0.3),
            target_file='script.js')
        files['script.js'] = js_content
        
        if progress_callback:
            progress_callback("✅ Проект готов!", 100)
        
        return files
    
    def _get_project_specific_requirements(self, request: AnalyzedRequest) -> Dict[str, str]:
        """🎯 РЕВОЛЮЦИОННАЯ СИСТЕМА: Возвращает требования УРОВНЯ 1000/100 для каждого типа проекта"""
=======
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
    
    def _get_project_specific_requirements(self, request: AnalyzedRequest) -> Dict[str, str]:
        """Возвращает детальные требования для конкретного типа проекта"""
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        
        project_type = request.project_type
        requirements = {
            'html_specifics': '',
            'css_specifics': '',
            'js_specifics': '',
            'additional_features': []
        }
        
        if project_type == ProjectType.IDLE_GAME or project_type == ProjectType.GAME:
            requirements.update({
                'html_specifics': '''
                ОБЯЗАТЕЛЬНЫЕ ЭЛЕМЕНТЫ ДЛЯ ИГР:
                - Игровая статистика: HP, уровень, опыт, ресурсы
                - Область игрового процесса с визуальными элементами
                - Система улучшений/апгрейдов с кнопками покупки
                - Инвентарь или слоты предметов
                - Индикаторы прогресса (полоски здоровья, опыта)
                - Кнопки действий (атака, использование предметов)
                - Лог событий или уведомлений
                ''',
                'css_specifics': '''
                СТИЛИ ДЛЯ ИГР:
                - Темная/цветная игровая тема (не белый фон в игровой области)
                - Анимации для игровых действий (атака, получение урона)
                - Прогресс-бары с градиентами и свечением
                - Визуальная обратная связь при клике (пульсация, изменение цвета)
                - Стили для игровых кнопок (крупные, контрастные)
                - Анимированные числа и эффекты
                - Стили для игрового интерфейса (статистика, инвентарь)
                ''',
                'js_specifics': '''
                ИГРОВАЯ ЛОГИКА:
                - Игровой цикл с состоянием игры (GameState объект)
                - Система уровней и опыта с расчетом прогресса
                - Система боя с расчетом урона и здоровья
                - Экономика игры (валюты, стоимость улучшений)
                - Система сохранения в localStorage
                - Таймеры и автоматические действия (для idle игр)
                - Система достижений или прогресса
                - Обновление UI в реальном времени
                ''',
                'additional_features': [
                    'Автосохранение игры', 'Система достижений', 'Различные типы противников',
                    'Магазин улучшений', 'Звуковые эффекты (опционально)', 'Анимации атак'
                ]
            })
            
        elif project_type == ProjectType.PORTFOLIO_WEBSITE:
            requirements.update({
                'html_specifics': '''
                ОБЯЗАТЕЛЬНЫЕ СЕКЦИИ ДЛЯ ПОРТФОЛИО:
                - Hero секция с фото и кратким описанием
                - Секция "Обо мне" с подробной информацией
                - Портфолио работ с галереей и описаниями
                - Навыки и технологии с прогресс-барами
                - Опыт работы или образование (временная шкала)
                - Контактная форма и социальные сети
                - Отзывы или рекомендации (если есть)
                ''',
                'css_specifics': '''
                ПРОФЕССИОНАЛЬНЫЙ ДИЗАЙН:
                - Современная типографика (красивые шрифты)
                - Цветовая схема в стиле минимализм
                - Плавная прокрутка и анимации появления элементов
                - Адаптивная галерея работ (сетка)
                - Стили для форм и интерактивных элементов
                - Градиенты и тени для современного вида
                ''',
                'js_specifics': '''
                ИНТЕРАКТИВНОСТЬ ПОРТФОЛИО:
                - Плавная прокрутка по якорям
                - Фильтрация работ по категориям
                - Лайтбокс для просмотра изображений
                - Валидация и отправка контактной формы
                - Анимации появления элементов при скролле
                - Адаптивное меню для мобильных устройств
                ''',
                'additional_features': [
                    'Темная/светлая тема', 'Многоязычность', 'Интеграция с соцсетями',
                    'Блог или статьи', 'Календарь встреч', 'Скачивание резюме'
                ]
            })
            
        elif project_type == ProjectType.MEDIA_PLAYER or 'видео' in str(request.features).lower() or 'музыка' in str(request.features).lower():
            requirements.update({
                'html_specifics': '''
                МЕДИА ПЛЕЕР ЭЛЕМЕНТЫ:
                - HTML5 video/audio элементы с контролами
                - Плейлист с треками/видео
                - Регулировка громкости и скорости
                - Полноэкранный режим для видео
                - Субтитры и языковые дорожки
                - Запись аудио/видео (MediaRecorder API)
                - Загрузка файлов drag-and-drop
                
                ДОПОЛНИТЕЛЬНЫЕ БИБЛИОТЕКИ (по необходимости):
                <script src="https://cdnjs.cloudflare.com/ajax/libs/wavesurfer.js/6.6.3/wavesurfer.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/video.js/8.0.4/video.min.js"></script>
                ''',
                'css_specifics': '''
                МЕДИА ИНТЕРФЕЙС:
                - Кастомные контролы плеера
                - Прогресс-бар с возможностью перемотки
                - Визуализация звука (waveform)
                - Адаптивный дизайн для мобильных
                - Темная тема для комфортного просмотра
                - Анимации воспроизведения/паузы
                ''',
                'js_specifics': '''
                МЕДИА ФУНКЦИОНАЛ:
                - Web Audio API для обработки звука
                - MediaRecorder для записи аудио/видео
                - getUserMedia для доступа к камере/микрофону
                - Управление плейлистами
                - Сохранение настроек в localStorage
                - Обработка различных форматов файлов
                - Синхронизация субтитров
                ''',
                'additional_features': [
                    'Эквалайзер', 'Запись с микрофона', 'Видеоредактор',
                    'Потоковое воспроизведение', 'Плейлисты', 'Закладки времени'
                ]
            })

        elif project_type == ProjectType.BUSINESS_LANDING:
            requirements.update({
                'html_specifics': '''
                СТРУКТУРА ЛЕНДИНГА:
                - Hero секция с призывом к действию (CTA)
                - Преимущества продукта/услуги
                - Отзывы клиентов с фото и именами
                - Тарифы и цены с кнопками покупки
                - FAQ секция с ответами на вопросы
                - Контакты и форма обратной связи
                - Гарантии и сертификаты
                ''',
                'css_specifics': '''
                КОНВЕРСИОННЫЙ ДИЗАЙН:
                - Яркие CTA кнопки (контрастные цвета)
                - Профессиональная цветовая схема
                - Читаемая типографика с акцентами
                - Стили для отзывов и карточек тарифов
                - Анимации для привлечения внимания
                - Иконки и визуальные элементы
                ''',
                'js_specifics': '''
                ЛЕНДИНГ ФУНКЦИОНАЛ:
                - Обработка форм с валидацией
                - Модальные окна для дополнительной информации
                - Калькулятор стоимости (если применимо)
                - Таймер акций и специальных предложений
                - Отслеживание кликов по CTA
                - Плавные переходы между секциями
                ''',
                'additional_features': [
                    'Интеграция с CRM', 'Онлайн-чат', 'Социальные доказательства',
                    'A/B тестирование элементов', 'Пиксель Facebook/Google', 'Счетчик посетителей'
                ]
            })
            
        elif project_type == ProjectType.THREE_D_GAME or project_type == ProjectType.THREE_D_VIEWER:
            requirements.update({
                'html_specifics': '''
                3D ПРИЛОЖЕНИЕ ЭЛЕМЕНТЫ:
                - Canvas элемент для WebGL рендеринга
                - Элементы управления (мышь, клавиатура, touch)
                - Интерфейс для настройки 3D параметров
                - Загрузчик 3D моделей (drag-and-drop)
                - FPS счетчик и статистика
                - VR/AR поддержка (при наличии)
                
                ОБЯЗАТЕЛЬНО ПОДКЛЮЧИ Three.js:
                <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
                <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
                ''',
                'css_specifics': '''
                3D ИНТЕРФЕЙС:
                - Полноэкранный canvas
                - Overlay UI элементы поверх 3D сцены
                - Адаптивный дизайн для разных экранов
                - Кастомные курсоры для 3D навигации
                - Загрузочные индикаторы для моделей
                - Стили для 3D контролов
                ''',
                'js_specifics': '''
                3D ФУНКЦИОНАЛ:
                - Three.js для 3D рендеринга
                - WebGL шейдеры и материалы
                - 3D модели загрузка (GLTF, OBJ, FBX)
                - Камера контролы (orbit, first-person)
                - Освещение и тени
                - Анимации и физика
                - Оптимизация производительности
                ''',
                'additional_features': [
                    'Three.js интеграция', 'Шейдеры', 'Физический движок',
                    '3D модели', 'Анимации', 'VR/AR поддержка'
                ]
            })
            
        elif project_type == ProjectType.DATABASE_APP or 'база данных' in str(request.features).lower():
            requirements.update({
                'html_specifics': '''
                DATABASE ПРИЛОЖЕНИЕ:
                - Формы для CRUD операций
                - Таблицы для отображения данных
                - Поиск и фильтрация записей
                - Пагинация больших наборов данных
                - Импорт/экспорт данных (CSV, JSON)
                - Схема базы данных (диаграммы)
                
                БИБЛИОТЕКИ БАЗ ДАННЫХ (выбери подходящую):
                <!-- SQLite в браузере -->
                <script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.js"></script>
                
                <!-- Supabase (PostgreSQL в облаке) -->
                <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
                
                <!-- Firebase (Google NoSQL) -->
                <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-app.js"></script>
                <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-firestore.js"></script>
                <script src="https://www.gstatic.com/firebasejs/9.0.0/firebase-auth.js"></script>
                
                <!-- Dexie.js для IndexedDB -->
                <script src="https://unpkg.com/dexie@3.2.4/dist/dexie.js"></script>
                
                <!-- Axios для REST API (MongoDB Atlas, etc) -->
                <script src="https://cdn.jsdelivr.net/npm/axios@1.1.2/dist/axios.min.js"></script>
                ''',
                'css_specifics': '''
                DATABASE ИНТЕРФЕЙС:
                - Табличный дизайн с сортировкой
                - Формы с валидацией
                - Модальные окна для редактирования
                - Индикаторы загрузки данных
                - Респонсивные таблицы
                - Цветовая кодировка статусов
                ''',
                'js_specifics': '''
                DATABASE ЛОГИКА:
                - Выбор БД: localStorage, IndexedDB, SQLite, Supabase, Firebase, MongoDB Atlas
                - CRUD операции (Create, Read, Update, Delete)
                - Валидация данных на клиенте
                - Кэширование запросов для производительности
                - Оффлайн синхронизация и conflict resolution
                - Миграции схемы базы данных
                - SQL Builder или ORM паттерны
                - Реальное время обновления (WebSocket/Server-Sent Events)
                - Индексирование для быстрого поиска
                - Backup и restore функциональность
                
                ПРИМЕРЫ ПОДКЛЮЧЕНИЯ:
                
                // Supabase (PostgreSQL)
                const supabase = createClient('URL', 'ANON_KEY')
                
                // Firebase (NoSQL)
                import { initializeApp } from 'firebase/app'
                import { getFirestore } from 'firebase/firestore'
                
                // SQLite в браузере
                const SQL = await initSqlJs()
                const db = new SQL.Database()
                
                // IndexedDB с Dexie
                const db = new Dexie('MyDatabase')
                db.version(1).stores({ items: '++id, name, category' })
                
                // MongoDB Atlas через REST API
                const response = await axios.post('https://data.mongodb-api.com/app/data-xxxxx/endpoint/data/v1/action/insertOne', data)
                ''',
                'additional_features': [
                    'Supabase интеграция', 'Firebase Firestore', 'SQLite поддержка', 'IndexedDB',
                    'MongoDB Atlas API', 'Реальное время', 'Backup/Restore', 'Аналитика данных',
                    'GraphQL поддержка', 'Автоматическая синхронизация', 'Конфликт-резолюшн'
                ]
            })
            
        elif project_type == ProjectType.RECORDING_APP or 'запись' in str(request.features).lower():
            requirements.update({
                'html_specifics': '''
                ПРИЛОЖЕНИЕ ЗАПИСИ:
                - Кнопки записи/остановки
                - Предварительный просмотр камеры
                - Список записанных файлов
                - Настройки качества записи
                - Выбор источников (камера/микрофон)
                - Обрезка и базовое редактирование
                ''',
                'css_specifics': '''
                ИНТЕРФЕЙС ЗАПИСИ:
                - Полноэкранное видео превью
                - Кнопки в стиле профессиональных приложений
                - Индикаторы записи (красная точка, таймер)
                - Прогресс-бары обработки
                - Респонсивный дизайн
                - Темная тема для записи
                ''',
                'js_specifics': '''
                ФУНКЦИОНАЛ ЗАПИСИ:
                - MediaRecorder API
                - getUserMedia для доступа к камере/микрофону
                - Обработка различных форматов (WebM, MP4)
                - Сжатие и оптимизация файлов
                - Потоковая запись
                - Постобработка (фильтры, эффекты)
                ''',
                'additional_features': [
                    'Screen Recording', 'Веб-камера', 'Микрофон',
                    'Видео эффекты', 'Стриминг', 'Облачное хранение'
                ]
            })
<<<<<<< HEAD
        
        elif project_type == ProjectType.CALCULATOR:
            requirements.update({
                'html_specifics': '''
                ОБЯЗАТЕЛЬНЫЕ ЭЛЕМЕНТЫ ДЛЯ КАЛЬКУЛЯТОРА:
                - Дисплей для отображения чисел и результатов (input readonly или div)
                - Кнопки цифр 0-9 в стандартной раскладке
                - Кнопки операций (+, -, ×, ÷)
                - Кнопка равно (=) для вычислений  
                - Кнопка очистки (C) или (AC)
                - Кнопка удаления последнего символа (⌫)
                - Кнопка десятичной точки (.)
                - Дополнительно: кнопки %, ±, память (M+, M-, MR, MC)
                
                СТРУКТУРА:
                - НЕ используй экраны main/settings/app - сделай прямой интерфейс калькулятора
                - Калькулятор должен быть виден сразу при загрузке страницы
                - Используй сетку (grid) для правильного расположения кнопок
                ''',
                'css_specifics': '''
                СТИЛИ ДЛЯ КАЛЬКУЛЯТОРА:
                - Современный дизайн в стиле iOS/Android калькуляторов
                - Центрированный калькулятор с максимальной шириной 400px
                - Дисплей: большой шрифт (2-3em), темный фон, светлый текст
                - Кнопки: одинаковый размер, скругленные углы, hover эффекты
                - Цветовая схема: цифры (светлые), операции (акцентные), равно (яркое)
                - Адаптивность: хорошо выглядит на мобильных
                - Тени и градиенты для объемного вида
                - Анимации нажатий (активные состояния)
                ''',
                'js_specifics': '''
                ФУНКЦИОНАЛ КАЛЬКУЛЯТОРА:
                - Переменные: currentInput, previousInput, operation, shouldResetDisplay
                - Функции: appendNumber(), setOperation(), calculate(), clear(), deleteLast()
                - Обработка всех арифметических операций (+, -, *, /)
                - Корректная работа с десятичными числами
                - Защита от деления на ноль
                - Очистка дисплея при начале нового вычисления
                - Поддержка клавиатурного ввода (опционально)
                - Сохранение истории вычислений (опционально)
                - Функции памяти M+, M-, MR, MC (опционально)
                ''',
                'additional_features': [
                    'История вычислений', 'Научный режим (sin, cos, log)', 'Клавиатурная поддержка', 
                    'Копирование результата', 'Размер шрифта по длине числа', 'Звуковая обратная связь'
                ]
            })
        
        # 🚀 РЕВОЛЮЦИОННЫЕ ОБЩИЕ ТРЕБОВАНИЯ КАЧЕСТВА УРОВНЯ 1000/100
=======
            
        # Добавляем общие требования качества
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        for key in requirements:
            if key.endswith('_specifics'):
                requirements[key] += '''
                
<<<<<<< HEAD
                🚀 РЕВОЛЮЦИОННЫЕ ТРЕБОВАНИЯ КАЧЕСТВА УРОВНЯ 1000/100:
                
                🏆 HTML ПРОФЕССИОНАЛЬНЫЕ СТАНДАРТЫ:
                - Семантическая HTML5 разметка уровня W3C эксперта
                - ARIA accessibility полная поддержка
                - Microdata/JSON-LD разметка для SEO
                - Progressive Web App (PWA) готовность
                - AMP (Accelerated Mobile Pages) совместимость
                - Structured data для поисковых систем
                - Open Graph и Twitter Cards meta теги
                - WebP изображения с fallback
                - Critical CSS inline для мгновенной загрузки
                - Resource hints (preload, prefetch, dns-prefetch)
                
                🎨 CSS ПРОФЕССИОНАЛЬНЫЕ СТАНДАРТЫ:
                - CSS Custom Properties для темизации
                - CSS Grid и Flexbox мастер-уровень
                - Клиппинг и маскирование для сложных форм
                - CSS Containment для производительности
                - CSS Subgrid для сложных макетов
                - CSS Scroll Snap для плавной навигации
                - CSS Painting API для custom effects
                - Variable fonts поддержка
                - Container queries для адаптивности
                - CSS animations 60FPS с will-change
                
                🧠 JAVASCRIPT ПРОФЕССИОНАЛЬНЫЕ СТАНДАРТЫ:
                - ES2023+ современный синтаксис
                - TypeScript JSDoc annotations
                - Web Components с Custom Elements
                - Service Workers для offline работы
                - WebAssembly интеграция готовность
                - Intersection Observer для lazy loading
                - Resize Observer для адаптивности
                - Performance Observer для мониторинга
                - Web Workers для фоновых вычислений
                - Streaming APIs для real-time данных
                
                ⚡ ПРОИЗВОДИТЕЛЬНОСТЬ ААА УРОВНЯ:
                - Core Web Vitals оптимизация (CLS, FID, LCP)
                - 99+ PageSpeed Insights score
                - Sub-second первая отрисовка
                - Tree shaking для минимизации bundle
                - Code splitting по маршрутам
                - Lazy loading всех не-критичных ресурсов
                - Image optimization с responsive images
                - Font loading strategies (font-display)
                - Critical resource prioritization
                - Memory leak prevention
                
                📱 МОБИЛЬНАЯ ОПТИМИЗАЦИЯ APPLE/GOOGLE УРОВНЯ:
                - Touch-first design подход
                - 44px minimum touch targets
                - iOS Safe Area поддержка
                - Android Edge-to-edge поддержка
                - Haptic feedback интеграция
                - Device orientation адаптация
                - Battery API awareness
                - Network Information API
                - Pointer events для universal input
                - Mobile-specific gestures (swipe, pinch)
                
                🛡️ БЕЗОПАСНОСТЬ ENTERPRISE УРОВНЯ:
                - Content Security Policy (CSP) strict
                - Subresource Integrity (SRI) для всех CDN
                - Cross-Origin Resource Sharing (CORS) правильная настройка
                - XSS protection на всех уровнях
                - CSRF tokens где необходимо
                - Input sanitization и validation
                - Secure cookies (HttpOnly, Secure, SameSite)
                - HTTPS everywhere с HSTS
                - Feature Policy для API permissions
                - Trusted Types для DOM manipulation
                
                ♿ ACCESSIBILITY AAA УРОВНЯ:
                - WCAG 2.2 AAA compliance полная
                - Screen reader полная поддержка
                - Keyboard navigation 100% покрытие
                - High contrast mode поддержка
                - Focus management профессиональный
                - ARIA live regions для dynamic content
                - Alternative text для всего visual content
                - Color contrast 7:1 для AAA
                - Voice control compatibility
                - Cognitive accessibility considerations
                
                🌐 КРОССБРАУЗЕРНАЯ СОВМЕСТИМОСТЬ:
                - Chrome/Edge/Firefox/Safari последние 2 версии
                - Mobile browsers (iOS Safari, Chrome Mobile)
                - Progressive enhancement подход
                - Graceful degradation для старых браузеров
                - Feature detection вместо browser detection
                - Polyfills для critical functionality
                - Vendor prefixes где необходимо
                - Testing на реальных устройствах
                
                🔮 БУДУЩЕЕ-ГОТОВНОСТЬ:
                - HTTP/3 и QUIC готовность
                - WebXR (AR/VR) compatibility hooks
                - Web Bluetooth/USB APIs поддержка
                - AI/ML APIs интеграционные точки
                - Blockchain/Web3 готовность
                - 5G network optimization
                - Foldable devices поддержка
                - Next-generation image formats (AVIF, HEIC)
=======
                ОБЩИЕ ТРЕБОВАНИЯ КАЧЕСТВА:
                - Профессиональный код с комментариями
                - Семантическая HTML разметка
                - Современные веб-стандарты
                - Кроссбраузерная совместимость
                - Доступность (accessibility)
                - Производительность и оптимизация
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
                '''
        
        return requirements
    
<<<<<<< HEAD
    def _generate_mandatory_features_html(self, features: List[str]) -> str:
        """🎯 РЕВОЛЮЦИОННАЯ СИСТЕМА: Генерирует HTML ПРОФЕССИОНАЛЬНОГО УРОВНЯ 1000/100"""
        
        mandatory_html = "\n🚀 КРИТИЧЕСКИ ВАЖНО - СОЗДАЙ HTML УРОВНЯ ААА-СТУДИЙ (1000/100):"
        
        for feature in features:
            if '3D графика' in feature:
                mandatory_html += """
                
                🎮 ПРОФЕССИОНАЛЬНАЯ 3D СИСТЕМА (УРОВЕНЬ UNREAL ENGINE):
                
                🔥 БАЗОВАЯ 3D ИНФРАСТРУКТУРА:
                - <canvas id="mainCanvas3D" class="professional-3d-canvas">
                - <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js">
                - <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/examples/js/loaders/GLTFLoader.js">
                - <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/examples/js/controls/OrbitControls.js">
                - <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/examples/js/postprocessing/EffectComposer.js">
                
                🌟 CINEMATIC 3D ОКРУЖЕНИЕ:
                - <div class="cinema-viewport"> (минимум 800x600, 4K ready)
                - <div class="advanced-lighting-panel"> панель профессионального освещения
                - <div class="material-inspector"> инспектор материалов реального времени
                - <div class="animation-timeline"> временная шкала анимаций
                - <div class="particle-systems"> системы частиц для эффектов
                
                🎬 CAMERA SYSTEM (КАК В HOLLYWOOD):
                - <div class="camera-controls-professional"> полный набор камеры
                - <button class="cinematic-shot">Cinematic Shot</button>
                - <button class="dolly-zoom">Dolly Zoom</button>
                - <button class="orbit-smooth">Smooth Orbit</button>
                - <input type="range" class="focal-length" min="14" max="200">
                - <input type="range" class="aperture" min="1.4" max="22" step="0.1">
                
                🔥 REAL-TIME RENDERING CONTROLS:
                - <div class="pbr-material-editor"> PBR Material Editor
                - <div class="hdri-environment"> HDRI Environment Maps
                - <div class="shadow-quality-controls"> Shadow Quality (Ultra/High/Medium)
                - <div class="anti-aliasing-controls"> AA: FXAA/TAA/MSAA
                - <div class="post-processing-stack"> Post-Processing Stack
                
                ⚡ PERFORMANCE ПРОФИЛИРОВЩИК:
                - <div class="fps-counter-professional">FPS: <span id="fpsDisplay">60</span></div>
                - <div class="gpu-memory">GPU: <span id="gpuMemory">0</span> MB</div>
                - <div class="triangles-count">Triangles: <span id="triangleCount">0</span></div>
                - <div class="draw-calls">Draw Calls: <span id="drawCalls">0</span></div>
                """
                
            if 'ИИ наставник' in feature:
                mandatory_html += """
                
                🤖 РЕВОЛЮЦИОННЫЙ ИИ НАСТАВНИК (УРОВЕНЬ JARVIS):
                
                🧠 ADVANCED AI NEURAL INTERFACE:
                - <div class="ai-consciousness-container"> главный контейнер ИИ сознания
                - <canvas class="ai-neural-visualization"> визуализация нейронной активности
                - <div class="ai-emotion-indicators"> индикаторы эмоций ИИ (радость, сосредоточенность, заинтересованность)
                - <div class="ai-knowledge-graph"> граф знаний в реальном времени
                
                🎭 PHOTOREALISTIC AI AVATAR SYSTEM:
                - <canvas class="ai-avatar-3d-realistic"> фотореалистичный 3D аватар
                - <div class="facial-expression-engine"> движок лицевой анимации
                - <div class="lip-sync-advanced"> продвинутая синхронизация губ
                - <div class="eye-tracking-system"> система отслеживания взгляда
                - <div class="micro-expressions"> микровыражения лица
                
                💬 CINEMATIC DIALOGUE SYSTEM:
                - <div class="dialogue-container-professional"> (min-height: 600px, 4K ready)
                - <div class="conversation-memory-bank"> банк памяти разговоров
                - <div class="context-awareness-panel"> панель понимания контекста
                - <div class="sentiment-analysis-realtime"> анализ настроения в реальном времени
                - <div class="typing-indicator-advanced"> продвинутый индикатор печати с анимацией мозговых волн
                
                🎤 PROFESSIONAL VOICE INTERFACE:
                - <button class="voice-input-studio-quality">🎙️ Studio Voice Input</button>
                - <div class="voice-waveform-visualizer"> профессиональная визуализация голоса
                - <div class="noise-cancellation-controls"> шумоподавление реального времени
                - <div class="voice-emotion-detection"> детекция эмоций в голосе
                - <canvas class="audio-spectrum-analyzer"> спектр-анализатор аудио
                
                🧮 INTELLIGENT RESPONSE SYSTEM:
                - <div class="response-quality-meter"> метр качества ответов
                - <div class="knowledge-confidence-bar"> уровень уверенности в знаниях
                - <div class="response-time-optimizer"> оптимизатор времени ответа
                - <div class="multi-language-processor"> мультиязычный процессор
                
                🎯 PERSONALIZATION ENGINE:
                - <div class="user-profile-analyzer"> анализатор профиля пользователя  
                - <div class="learning-progress-tracker"> трекер прогресса обучения
                - <div class="adaptive-difficulty-system"> адаптивная система сложности
                - <div class="personality-matching-ai"> подбор личности ИИ
                """
                
            if 'озвучивание' in feature or 'голосовой ввод' in feature:
                mandatory_html += """
                
                🎙️ PROFESSIONAL STUDIO AUDIO SYSTEM (УРОВЕНЬ ABBEY ROAD):
                
                🎚️ STUDIO-GRADE RECORDING INTERFACE:
                - <div class="recording-studio-interface"> интерфейс студии звукозаписи
                - <canvas class="professional-waveform-display"> профессиональный дисплей волны
                - <div class="multi-channel-mixer"> многоканальный микшер
                - <div class="audio-compressor-controls"> управление компрессором
                - <div class="equalizer-professional"> профессиональный эквалайзер (31-полосный)
                
                🎤 BROADCAST-QUALITY MICROPHONE SYSTEM:
                - <button class="studio-mic-input">🎙️ Broadcast Quality Input</button>
                - <div class="microphone-gain-control"> управление усилением микрофона
                - <div class="phantom-power-indicator"> индикатор фантомного питания
                - <div class="noise-gate-controls"> шумовые ворота
                - <canvas class="real-time-spectrum"> спектр в реальном времени
                
                🎵 ADVANCED VOICE PROCESSING:
                - <div class="voice-enhancement-suite"> набор улучшения голоса
                - <div class="de-esser-controls"> де-эссер для убирания шипящих
                - <div class="pitch-correction-auto"> автокоррекция высоты тона
                - <div class="formant-shifting"> сдвиг формант
                - <div class="vocal-doubling-effect"> эффект удвоения вокала
                
                🔊 CINEMATIC AUDIO PLAYBACK:
                - <div class="surround-sound-processor"> процессор объемного звука
                - <div class="audio-mastering-chain"> цепочка мастеринга
                - <div class="dynamic-range-control"> контроль динамического диапазона
                - <canvas class="stereo-field-visualizer"> визуализатор стерео поля
                - <div class="loudness-metering"> измерение громкости (LUFS)
                
                🎭 EMOTIONAL VOICE SYNTHESIS:
                - <div class="emotion-voice-controls"> управление эмоциональным синтезом
                - <select class="voice-personality-selector"> селектор личности голоса
                - <div class="breathing-simulation"> симуляция дыхания
                - <div class="vocal-age-adjustment"> настройка возраста голоса
                - <div class="accent-selector-global"> глобальный селектор акцента
                
                📊 AUDIO ANALYTICS DASHBOARD:
                - <div class="voice-quality-analyzer"> анализатор качества голоса
                - <div class="speech-clarity-meter"> метр четкости речи
                - <div class="emotional-tone-detector"> детектор эмоционального тона
                - <canvas class="pitch-contour-display"> отображение контура высоты тона
                - <div class="pronunciation-accuracy"> точность произношения
                """
                
            if 'полное меню' in feature:
                mandatory_html += """
                
                📋 ПОЛНОЦЕННОЕ МЕНЮ (ОБЯЗАТЕЛЬНО):
                - Главная страница
                - Профиль пользователя
                - История активности
                - Настройки
                - Справка/О программе
                - Выход (если есть авторизация)
                """
                
            if 'настройки приложения' in feature:
                mandatory_html += """
                
                ⚙️ ЭКРАН НАСТРОЕК (ОБЯЗАТЕЛЬНО):
                - Настройки интерфейса (тема, язык)
                - Настройки уведомлений
                - Настройки звука
                - Настройки приватности
                - Сброс настроек к умолчанию
                - Кнопка "Сохранить изменения"
                """
        
        # ПРОФЕССИОНАЛЬНАЯ ВИДЕО СИСТЕМА
        if any(word in str(features).lower() for word in ['видео', 'video', 'камера', 'съемка']):
            mandatory_html += """
            
            🎬 PROFESSIONAL VIDEO PRODUCTION SUITE (УРОВЕНЬ HOLLYWOOD):
            
            📹 CINEMA-GRADE VIDEO CAPTURE:
            - <video class="professional-video-display" controls></video>
            - <canvas class="video-processing-canvas"> обработка видео в реальном времени
            - <div class="camera-controls-professional"> профессиональные управления камерой
            - <div class="video-resolution-selector"> 8K/4K/HD selector
            - <div class="frame-rate-controls"> 24/30/60/120 FPS controls
            
            🎨 REAL-TIME VIDEO EFFECTS:
            - <div class="color-grading-suite"> набор цветокоррекции
            - <div class="lut-selector"> селектор LUT таблиц
            - <div class="chroma-key-controls"> хромакей управления
            - <canvas class="green-screen-processor"> процессор зеленого фона
            - <div class="beauty-filter-controls"> фильтры красоты
            
            🎞️ PROFESSIONAL VIDEO EDITING:
            - <div class="timeline-editor-professional"> профессиональная временная шкала
            - <div class="multi-track-video-editor"> многодорожечный видеоредактор
            - <div class="transition-effects-library"> библиотека переходов
            - <div class="motion-graphics-engine"> движок моушн графики
            - <canvas class="video-compositing"> видеокомпозитинг
            """
        
        # Добавляем принудительные требования для мобильных приложений  
        if any('мобильная' in feature.lower() for feature in features):
            mandatory_html += """
            
            📱 NEXT-GEN MOBILE EXPERIENCE (УРОВЕНЬ APPLE/GOOGLE):
            
            📲 NATIVE-LIKE MOBILE INTERFACE:
            - <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
            - <meta name="theme-color" content="#000000">
            - <link rel="manifest" href="/manifest.json"> (PWA support)
            - <meta name="apple-mobile-web-app-capable" content="yes">
            - <meta name="mobile-web-app-capable" content="yes">
            
            🔄 ADVANCED GESTURE SYSTEM:
            - <div class="gesture-recognition-layer"> слой распознавания жестов
            - <div class="swipe-navigation-advanced"> продвинутая навигация свайпами
            - <div class="pinch-zoom-controls"> управление пинч-зумом
            - <div class="haptic-feedback-engine"> движок тактильной обратной связи
            - <div class="force-touch-detection"> детекция силы нажатия
            
            🔋 PERFORMANCE OPTIMIZATION:
            - <div class="battery-usage-optimizer"> оптимизатор использования батареи
            - <div class="network-adaptive-loading"> адаптивная загрузка по сети
            - <div class="cache-management-system"> система управления кешем
            - <div class="lazy-loading-engine"> движок ленивой загрузки
            - <div class="memory-usage-monitor"> монитор использования памяти
            """
            
        mandatory_html += """
        
        🚀 РЕВОЛЮЦИОННЫЕ ДОПОЛНЕНИЯ:
        
        🎯 AI-POWERED RECOMMENDATIONS:
        - <div class="ai-recommendation-engine"> движок ИИ рекомендаций
        - <div class="user-behavior-analyzer"> анализатор поведения пользователя
        - <div class="predictive-interface"> предиктивный интерфейс
        
        🔮 FUTURE-TECH INTEGRATION:
        - <div class="blockchain-integration"> интеграция с блокчейном
        - <div class="nft-gallery-viewer"> просмотрщик NFT галереи  
        - <div class="metaverse-portal"> портал в метавселенную
        - <div class="quantum-computing-interface"> интерфейс квантовых вычислений
        """
            
        mandatory_html += "\n\n🎯 КРИТИЧЕСКИ ВАЖНО: ВСЕ ВЫШЕПЕРЕЧИСЛЕННЫЕ ЭЛЕМЕНТЫ ДОЛЖНЫ БЫТЬ РЕАЛИЗОВАНЫ В HTML СО 100% СООТВЕТСТВИЕМ! НИ ОДИН ЭЛЕМЕНТ НЕ ДОЛЖЕН БЫТЬ ПРОПУЩЕН!"
        return mandatory_html
    
    def _generate_mandatory_css_features(self, features: List[str]) -> str:
        """🎯 РЕВОЛЮЦИОННАЯ СИСТЕМА: Генерирует CSS ПРОФЕССИОНАЛЬНОГО УРОВНЯ 1000/100"""
        
        mandatory_css = "\n🚀 КРИТИЧЕСКИ ВАЖНО - СОЗДАЙ CSS УРОВНЯ PIXAR/DISNEY (1000/100):"
        
        for feature in features:
            if '3D графика' in feature:
                mandatory_css += """
                
                🎮 CINEMATIC 3D CSS SYSTEM (УРОВЕНЬ UNREAL ENGINE):
                
                🌟 PROFESSIONAL 3D VIEWPORT:
                .professional-3d-canvas {
                    position: relative;
                    min-height: 800px;
                    width: 100%;
                    background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
                    border-radius: 20px;
                    box-shadow: 
                        0 0 50px rgba(0, 255, 255, 0.3),
                        inset 0 0 100px rgba(255, 255, 255, 0.05);
                    overflow: hidden;
                    backdrop-filter: blur(10px);
                    transform-style: preserve-3d;
                    perspective: 2000px;
                }
                
                🎬 HOLLYWOOD-STYLE CAMERA CONTROLS:
                .camera-controls-professional {
                    position: absolute;
                    top: 20px;
                    right: 20px;
                    background: rgba(0, 0, 0, 0.8);
                    backdrop-filter: blur(20px);
                    border-radius: 15px;
                    padding: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                    animation: floatGlow 3s ease-in-out infinite alternate;
                }
                
                ⚡ PERFORMANCE COUNTER STYLES:
                .fps-counter-professional {
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    background: linear-gradient(45deg, #00ff00, #ffff00);
                    -webkit-background-clip: text;
                    background-clip: text;
                    color: transparent;
                    font-family: 'JetBrains Mono', monospace;
                    font-weight: bold;
                    font-size: 18px;
                    text-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
                    animation: pulseGlow 1s infinite;
                }
                
                🌈 POST-PROCESSING EFFECTS:
                .post-processing-stack {
                    filter: 
                        contrast(1.2) 
                        saturate(1.3) 
                        brightness(1.1)
                        drop-shadow(0 0 30px rgba(255, 255, 255, 0.2));
                    transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                }
                
                @keyframes floatGlow {
                    0% { transform: translateY(0px) scale(1); box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5); }
                    100% { transform: translateY(-10px) scale(1.02); box-shadow: 0 30px 60px rgba(0, 255, 255, 0.3); }
                }
                
                @keyframes pulseGlow {
                    0%, 100% { text-shadow: 0 0 20px rgba(0, 255, 0, 0.5); }
                    50% { text-shadow: 0 0 40px rgba(0, 255, 0, 1), 0 0 60px rgba(255, 255, 0, 0.8); }
                }
                """
                
            if 'ИИ наставник' in feature:
                mandatory_css += """
                
                🤖 REVOLUTIONARY AI MENTOR CSS (УРОВЕНЬ JARVIS/FRIDAY):
                
                🧠 AI CONSCIOUSNESS CONTAINER:
                .ai-consciousness-container {
                    position: relative;
                    min-height: 700px;
                    background: 
                        radial-gradient(circle at 30% 20%, rgba(120, 119, 198, 0.3), transparent 50%),
                        radial-gradient(circle at 80% 80%, rgba(255, 119, 198, 0.3), transparent 50%),
                        radial-gradient(circle at 40% 40%, rgba(120, 200, 255, 0.3), transparent 50%),
                        linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
                    border-radius: 25px;
                    overflow: hidden;
                    backdrop-filter: blur(15px);
                    border: 2px solid rgba(255, 255, 255, 0.1);
                    box-shadow: 
                        0 0 100px rgba(120, 119, 198, 0.4),
                        inset 0 0 50px rgba(255, 255, 255, 0.05);
                    animation: consciousnessGlow 4s ease-in-out infinite alternate;
                }
                
                🎭 PHOTOREALISTIC AI AVATAR:
                .ai-avatar-3d-realistic {
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    background: 
                        linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border: 5px solid rgba(255, 255, 255, 0.2);
                    box-shadow: 
                        0 0 50px rgba(102, 126, 234, 0.8),
                        inset 0 0 50px rgba(255, 255, 255, 0.1);
                    animation: avatarBreathing 3s ease-in-out infinite, avatarGlow 2s infinite alternate;
                    transform-style: preserve-3d;
                    position: relative;
                    overflow: hidden;
                }
                
                .ai-avatar-3d-realistic::before {
                    content: '';
                    position: absolute;
                    top: -50%;
                    left: -50%;
                    width: 200%;
                    height: 200%;
                    background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
                    animation: avatarScan 3s linear infinite;
                }
                
                💬 CINEMATIC DIALOGUE SYSTEM:
                .dialogue-container-professional {
                    min-height: 600px;
                    background: rgba(0, 0, 0, 0.3);
                    backdrop-filter: blur(20px);
                    border-radius: 20px;
                    border: 1px solid rgba(255, 255, 255, 0.1);
                    padding: 30px;
                    overflow-y: auto;
                    scrollbar-width: thin;
                    scrollbar-color: rgba(120, 119, 198, 0.5) transparent;
                }
                
                .ai-message {
                    background: linear-gradient(135deg, rgba(120, 119, 198, 0.2), rgba(255, 119, 198, 0.1));
                    border: 1px solid rgba(120, 119, 198, 0.3);
                    border-radius: 20px 20px 20px 5px;
                    padding: 20px;
                    margin: 15px 0;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 10px 30px rgba(120, 119, 198, 0.2);
                    animation: messageSlideIn 0.5s ease-out;
                    position: relative;
                    overflow: hidden;
                }
                
                .ai-message::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100%;
                    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                    animation: messageShimmer 2s infinite;
                }
                
                .user-message {
                    background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 20px 20px 5px 20px;
                    padding: 20px;
                    margin: 15px 0;
                    margin-left: auto;
                    max-width: 80%;
                    backdrop-filter: blur(10px);
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
                    animation: messageSlideIn 0.5s ease-out;
                }
                
                🎤 PROFESSIONAL VOICE VISUALIZER:
                .voice-waveform-visualizer {
                    height: 100px;
                    background: rgba(0, 0, 0, 0.5);
                    border-radius: 15px;
                    padding: 10px;
                    margin: 20px 0;
                    position: relative;
                    overflow: hidden;
                }
                
                .audio-spectrum-analyzer {
                    width: 100%;
                    height: 80px;
                    filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.8));
                    animation: spectrumGlow 1s infinite alternate;
                }
                
                📊 NEURAL ACTIVITY VISUALIZATION:
                .ai-neural-visualization {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    opacity: 0.3;
                    pointer-events: none;
                    filter: blur(1px);
                    animation: neuralPulse 2s ease-in-out infinite;
                }
                
                @keyframes consciousnessGlow {
                    0% { box-shadow: 0 0 100px rgba(120, 119, 198, 0.4), inset 0 0 50px rgba(255, 255, 255, 0.05); }
                    100% { box-shadow: 0 0 150px rgba(255, 119, 198, 0.6), inset 0 0 100px rgba(255, 255, 255, 0.1); }
                }
                
                @keyframes avatarBreathing {
                    0%, 100% { transform: scale(1) rotateY(0deg); }
                    50% { transform: scale(1.05) rotateY(5deg); }
                }
                
                @keyframes avatarGlow {
                    0% { box-shadow: 0 0 50px rgba(102, 126, 234, 0.8), inset 0 0 50px rgba(255, 255, 255, 0.1); }
                    100% { box-shadow: 0 0 80px rgba(118, 75, 162, 1), inset 0 0 80px rgba(255, 255, 255, 0.2); }
                }
                
                @keyframes avatarScan {
                    0% { transform: translateX(-200%); }
                    100% { transform: translateX(200%); }
                }
                
                @keyframes messageSlideIn {
                    0% { opacity: 0; transform: translateY(20px) scale(0.95); }
                    100% { opacity: 1; transform: translateY(0) scale(1); }
                }
                
                @keyframes messageShimmer {
                    0% { left: -100%; }
                    100% { left: 100%; }
                }
                
                @keyframes neuralPulse {
                    0%, 100% { opacity: 0.3; transform: scale(1); }
                    50% { opacity: 0.6; transform: scale(1.02); }
                }
                
                @keyframes spectrumGlow {
                    0% { filter: drop-shadow(0 0 10px rgba(0, 255, 255, 0.8)); }
                    100% { filter: drop-shadow(0 0 20px rgba(255, 0, 255, 1)); }
                }
                """
                
            if 'озвучивание' in feature or 'голосовой ввод' in feature:
                mandatory_css += """
                
                🔊 ГОЛОСОВЫЕ CSS (ОБЯЗАТЕЛЬНО):
                - .voice-btn: стили для кнопки записи с микрофона
                - .voice-recording: анимация активной записи (пульсация)
                - .voice-volume: визуальный индикатор громкости
                - .voice-controls: панель управления голосовыми функциями
                - .audio-waveform: анимация звуковой волны
                - .voice-settings: стили для настроек голоса
                """
                
            if 'полное меню' in feature:
                mandatory_css += """
                
                📋 ПОЛНОЦЕННОЕ МЕНЮ CSS (ОБЯЗАТЕЛЬНО):
                - .main-menu: основное навигационное меню
                - .menu-item: стили для элементов меню с hover эффектами
                - .menu-icon: иконки пунктов меню
                - .menu-mobile: адаптивное меню для мобильных
                - .hamburger-menu: анимированная иконка гамбургера
                - .menu-overlay: фоновая подложка для мобильного меню
                """
                
            if 'настройки приложения' in feature:
                mandatory_css += """
                
                ⚙️ НАСТРОЙКИ CSS (ОБЯЗАТЕЛЬНО):
                - .settings-panel: панель настроек с прокруткой
                - .settings-group: группы настроек с заголовками
                - .setting-item: отдельные настройки с лейблами
                - .toggle-switch: стилизованные переключатели
                - .settings-button: кнопки в настройках
                - .settings-tabs: вкладки настроек если много групп
                """
        
        # REVOLUTIONARY AUDIO/VIDEO CSS SYSTEMS
        if 'озвучивание' in feature or 'голосовой ввод' in feature:
            mandatory_css += """
            
            🎙️ PROFESSIONAL STUDIO AUDIO CSS (УРОВЕНЬ ABBEY ROAD):
            
            🎚️ STUDIO INTERFACE:
            .recording-studio-interface {
                background: 
                    linear-gradient(135deg, #1a1a1a 0%, #2d2d30 50%, #3a3a3c 100%);
                border-radius: 20px;
                padding: 30px;
                box-shadow: 
                    0 0 50px rgba(255, 255, 255, 0.1),
                    inset 0 0 100px rgba(0, 0, 0, 0.5);
                border: 2px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(20px);
                animation: studioGlow 3s ease-in-out infinite alternate;
            }
            
            .professional-waveform-display {
                width: 100%;
                height: 150px;
                background: radial-gradient(circle, rgba(0, 255, 0, 0.1), transparent);
                border-radius: 10px;
                border: 1px solid rgba(0, 255, 0, 0.3);
                animation: waveformPulse 1s infinite;
            }
            
            .studio-mic-input {
                background: linear-gradient(135deg, #ff6b6b, #ee5a24);
                border: none;
                border-radius: 50%;
                width: 80px;
                height: 80px;
                font-size: 24px;
                color: white;
                box-shadow: 
                    0 0 30px rgba(255, 107, 107, 0.6),
                    0 10px 30px rgba(0, 0, 0, 0.3);
                animation: micPulse 2s ease-in-out infinite;
                transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            }
            
            .studio-mic-input:active {
                transform: scale(0.95);
                box-shadow: 
                    0 0 50px rgba(255, 107, 107, 1),
                    0 5px 15px rgba(0, 0, 0, 0.5);
            }
            
            @keyframes studioGlow {
                0% { box-shadow: 0 0 50px rgba(255, 255, 255, 0.1), inset 0 0 100px rgba(0, 0, 0, 0.5); }
                100% { box-shadow: 0 0 80px rgba(255, 215, 0, 0.3), inset 0 0 150px rgba(255, 215, 0, 0.1); }
            }
            
            @keyframes waveformPulse {
                0%, 100% { background: radial-gradient(circle, rgba(0, 255, 0, 0.1), transparent); }
                50% { background: radial-gradient(circle, rgba(0, 255, 255, 0.3), transparent); }
            }
            
            @keyframes micPulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            """
            
        # REVOLUTIONARY VIDEO CSS SYSTEM
        if any(word in str(features).lower() for word in ['видео', 'video', 'камера']):
            mandatory_css += """
            
            🎬 HOLLYWOOD VIDEO PRODUCTION CSS:
            
            📹 CINEMA VIEWPORT:
            .professional-video-display {
                width: 100%;
                min-height: 500px;
                border-radius: 20px;
                background: linear-gradient(135deg, #0c0c0c, #1a1a2e);
                border: 3px solid rgba(255, 215, 0, 0.5);
                box-shadow: 
                    0 0 100px rgba(255, 215, 0, 0.3),
                    inset 0 0 50px rgba(255, 255, 255, 0.05);
                animation: cinemaGlow 4s ease-in-out infinite alternate;
                position: relative;
                overflow: hidden;
            }
            
            .professional-video-display::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255, 215, 0, 0.1), transparent);
                animation: filmScan 4s linear infinite;
            }
            
            🎨 COLOR GRADING SUITE:
            .color-grading-suite {
                background: rgba(0, 0, 0, 0.8);
                backdrop-filter: blur(20px);
                border-radius: 15px;
                padding: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                gap: 15px;
                animation: colorGradeGlow 2s infinite alternate;
            }
            
            @keyframes cinemaGlow {
                0% { box-shadow: 0 0 100px rgba(255, 215, 0, 0.3), inset 0 0 50px rgba(255, 255, 255, 0.05); }
                100% { box-shadow: 0 0 150px rgba(255, 69, 0, 0.5), inset 0 0 100px rgba(255, 255, 255, 0.1); }
            }
            
            @keyframes filmScan {
                0% { transform: translateX(-200%) rotate(45deg); }
                100% { transform: translateX(200%) rotate(45deg); }
            }
            
            @keyframes colorGradeGlow {
                0% { border-color: rgba(255, 255, 255, 0.1); }
                100% { border-color: rgba(255, 215, 0, 0.5); }
            }
            """
            
        # NEXT-GEN MOBILE CSS
        if any('мобильная' in feature.lower() for feature in features):
            mandatory_css += """
            
            📱 NEXT-GEN MOBILE CSS (УРОВЕНЬ APPLE/GOOGLE):
            
            🔄 ADVANCED GESTURES:
            .gesture-recognition-layer {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1000;
                background: radial-gradient(circle at var(--touch-x, 50%) var(--touch-y, 50%), 
                           rgba(255, 255, 255, 0.1) 0%, transparent 50%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .swipe-navigation-advanced {
                position: relative;
                overflow: hidden;
                border-radius: 20px;
                background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                animation: swipeGlow 2s infinite alternate;
            }
            
            📱 MOBILE OPTIMIZATION:
            @media (max-width: 768px) {
                .professional-3d-canvas { min-height: 400px; }
                .ai-consciousness-container { min-height: 500px; }
                .dialogue-container-professional { min-height: 400px; }
                .ai-avatar-3d-realistic { width: 120px; height: 120px; }
            }
            
            @media (max-width: 480px) {
                .professional-3d-canvas { min-height: 300px; }
                .ai-consciousness-container { min-height: 400px; }
                .camera-controls-professional { 
                    position: relative; 
                    top: auto; 
                    right: auto; 
                    margin: 20px 0; 
                }
            }
            
            @keyframes swipeGlow {
                0% { border-color: rgba(255, 255, 255, 0.2); }
                100% { border-color: rgba(0, 255, 255, 0.5); }
            }
            """
            
        mandatory_css += """
        
        🚀 UNIVERSAL REVOLUTIONARY STYLES:
        
        /* GLASSMORPHISM GLOBAL */
        .glass-morphism {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        
        /* NEON GLOW EFFECTS */
        .neon-glow {
            text-shadow: 
                0 0 5px currentColor,
                0 0 10px currentColor,
                0 0 15px currentColor,
                0 0 20px currentColor;
            animation: neonFlicker 2s infinite alternate;
        }
        
        @keyframes neonFlicker {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        /* HOLOGRAPHIC EFFECTS */
        .holographic {
            background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5, #ffbe0b);
            background-size: 300% 300%;
            animation: holographicShift 3s ease infinite;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        
        @keyframes holographicShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        """
            
        mandatory_css += "\n\n🎯 КРИТИЧЕСКИ ВАЖНО: ВСЕ ВЫШЕПЕРЕЧИСЛЕННЫЕ CSS СТИЛИ ДОЛЖНЫ БЫТЬ РЕАЛИЗОВАНЫ НА 100%! КАЧЕСТВО ДОЛЖНО БЫТЬ УРОВНЯ 1000/100!"
        return mandatory_css
    
=======
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    def _create_html_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации HTML"""
        
        # Получаем детальные требования для конкретного типа проекта
        project_requirements = self._get_project_specific_requirements(request)
        
<<<<<<< HEAD
        # Генерируем обязательные функции на основе пользовательского запроса
        required_features_html = self._generate_mandatory_features_html(request.features)
        
        # Обязательная структура UI для всех приложений
        mandatory_ui_structure = f"""
        🔥 КРИТИЧЕСКИ ВАЖНО - ОБЯЗАТЕЛЬНАЯ СТРУКТУРА UI (РЕАЛИЗУЙ ВСЕ БЕЗ ИСКЛЮЧЕНИЙ):
        
        1. 📱 ГЛАВНАЯ СТРАНИЦА с заголовком и описанием приложения
        2. 🧭 ПОЛНОЦЕННОЕ НАВИГАЦИОННОЕ МЕНЮ (всегда добавляй даже для простых приложений)
        3. ⚙️  ЭКРАН НАСТРОЕК с реальными настройками (не заглушка!)
        4. 🚀 СТАРТОВЫЙ ЭКРАН с кнопкой "Начать"
        5. 💼 ОСНОВНОЙ ФУНКЦИОНАЛ приложения (скрытый по умолчанию)
        6. 🔄 ПЕРЕКЛЮЧЕНИЕ между экранами через data-screen атрибуты
        
        📋 ОБЯЗАТЕЛЬНАЯ СТРУКТУРА ЭКРАНОВ:
        - #main-screen: главная страница с описанием и кнопкой "Начать"
        - #settings-screen: экран настроек (скрытый по умолчанию, НО РЕАЛЬНЫЙ!)
        - #app-screen: основной функционал приложения (скрытый по умолчанию)
        
        🔗 ОБЯЗАТЕЛЬНАЯ НАВИГАЦИЯ:
        - Кнопка "Начать/Открыть" переводит из main-screen в app-screen
        - Кнопка "Настройки" показывает settings-screen
        - Кнопка "Назад" возвращает на main-screen из любого экрана
        - Хлебные крошки для навигации между экранами
        
        {required_features_html}
        """
        
        # Для калькулятора не используем стандартную структуру экранов
        ui_structure = mandatory_ui_structure
        if request.project_type == ProjectType.CALCULATOR:
            ui_structure = """
            СТРУКТУРА ДЛЯ КАЛЬКУЛЯТОРА:
            Создай простой HTML с калькулятором БЕЗ экранов и навигации.
            Калькулятор должен быть виден сразу при загрузке страницы.
            """
        
        prompt = f"""
        ⚠️  ВНИМАНИЕ: ЭТО КРИТИЧЕСКИ ВАЖНОЕ ЗАДАНИЕ - СОЗДАЙ HTML С 100% СООТВЕТСТВИЕМ ПОЛЬЗОВАТЕЛЬСКОМУ ЗАПРОСУ!
        
        🎯 СОЗДАЙ ПОЛНОФУНКЦИОНАЛЬНЫЙ HTML ДЛЯ: {request.project_type.value if request.project_type else 'веб-приложения'}
        
        {ui_structure}
        
        {project_requirements['html_specifics']}
        
        🔥 ПОЛЬЗОВАТЕЛЬСКИЕ ТРЕБОВАНИЯ (РЕАЛИЗУЙ ВСЕ БЕЗ ИСКЛЮЧЕНИЙ):
        - 📋 ФУНКЦИИ: {', '.join(request.features)}
        - 💻 ТЕХНОЛОГИИ: {', '.join(request.tech_stack)}
        - 🎨 ДИЗАЙН: {', '.join(request.design_requirements)}
        - ⭐ ДОПОЛНИТЕЛЬНО: {', '.join(project_requirements['additional_features'])}
        
        🏆 ТРЕБОВАНИЯ К КАЧЕСТВУ (ОБЯЗАТЕЛЬНО):
        - 📱 Адаптивный дизайн для ВСЕХ устройств (mobile-first подход)
        - 🏗️  Семантичная HTML5 разметка с полной accessibility поддержкой
        - 📎 Подключение styles.css и script.js
        - 🔍 SEO-оптимизация (мета-теги, структурированные данные, Open Graph)
        - ✅ Валидный HTML код (W3C стандарты)
        - 🚀 Производительность (оптимизированные изображения, минифицированный код)
        
        🔥 КРИТИЧЕСКИ ВАЖНО:
        - НЕ УПУСТИ НИ ОДНОЙ ФУНКЦИИ из пользовательского запроса
        - Каждая указанная технология ДОЛЖНА быть использована
        - ВСЕ дизайнерские требования ДОЛЖНЫ быть отражены в HTML
        - Если пользователь просил 3D - ОБЯЗАТЕЛЬНО добавь Three.js
        - Если пользователь просил голос - ОБЯЗАТЕЛЬНО добавь голосовые элементы
        - Если пользователь просил ИИ наставника - ОБЯЗАТЕЛЬНО создай полный интерфейс
        """
        
        # Добавляем специальное предупреждение для калькулятора
        if request.project_type == ProjectType.CALCULATOR:
            prompt += """
            
            ВНИМАНИЕ ДЛЯ КАЛЬКУЛЯТОРА: 
            Показывай калькулятор СРАЗУ - без экранов, меню и кнопки "Начать"!
            Калькулятор должен быть готов к использованию при загрузке страницы.
            """
        else:
            prompt += """
            
            ВАЖНО: НЕ показывай игровой процесс или основной функционал сразу! 
            Всегда начинай с главной страницы и кнопки "Начать".
            """
        
        prompt += """
        
        Создай детальную и функциональную HTML структуру. Верни только чистый HTML код без объяснений.
        """
        
        print(f"🔍 HTML PROMPT для {request.project_type}: {prompt[:200]}...")
        return prompt
=======
        # Обязательная структура UI для всех приложений
        mandatory_ui_structure = """
        ОБЯЗАТЕЛЬНАЯ СТРУКТУРА UI (ВСЕГДА включай эти элементы):
        1. Главная страница с заголовком и описанием приложения
        2. Навигационное меню (если больше одного экрана)
        3. Кнопка "Настройки" или ссылка на настройки
        4. Стартовый экран с кнопкой "Начать" (для игр) или "Открыть" (для других приложений)
        5. Основной функционал приложения должен быть скрыт по умолчанию
        6. Используй атрибуты data-screen для переключения между экранами
        
        Структура:
        - #main-screen: главная страница с описанием и кнопкой "Начать"
        - #settings-screen: экран настроек (скрытый по умолчанию)  
        - #app-screen: основной функционал приложения (скрытый по умолчанию)
        
        Навигация:
        - Кнопка "Начать/Открыть" переводит из main-screen в app-screen
        - Кнопка "Настройки" показывает settings-screen
        - Кнопка "Назад" возвращает на main-screen из любого экрана
        """
        
        return f"""
        Создай профессиональный HTML файл для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        {mandatory_ui_structure}
        
        {project_requirements['html_specifics']}
        
        Пользовательские требования:
        - Функции: {', '.join(request.features)}
        - Технологии: {', '.join(request.tech_stack)}
        - Дизайн: {', '.join(request.design_requirements)}
        - Дополнительные возможности: {', '.join(project_requirements['additional_features'])}
        
        Технические требования:
        - Адаптивный дизайн для всех устройств
        - Семантичная HTML5 разметка с accessibility
        - Подключение styles.css и script.js
        - SEO-оптимизация (мета-теги, структурированные данные)
        - Валидный HTML код
        
        ВАЖНО: НЕ показывай игровой процесс или основной функционал сразу! 
        Всегда начинай с главной страницы и кнопки "Начать".
        
        Создай детальную и функциональную HTML структуру. Верни только чистый HTML код без объяснений.
        """
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
    
    def _create_css_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации CSS"""
        
        # Получаем детальные требования для конкретного типа проекта
        project_requirements = self._get_project_specific_requirements(request)
        
        mandatory_css_structure = """
        ОБЯЗАТЕЛЬНЫЕ CSS КЛАССЫ для многоэкранной структуры:
        - .screen: базовый класс для всех экранов
        - .screen.active: активный (видимый) экран
        - .screen:not(.active): скрытые экраны (display: none)
        - .btn-primary: основные кнопки (Начать, Открыть)
        - .btn-secondary: вторичные кнопки (Настройки, Назад)
        - .nav-header: навигационная шапка с кнопками
        - .main-content: основное содержимое экрана
        - .settings-panel: панель настроек
        - .game-area / .app-area: область основного функционала
        
        Анимации переходов между экранами:
        - Плавные переходы opacity/transform при смене экранов
        - Анимация появления кнопок и элементов
        """
        
<<<<<<< HEAD
        # Генерируем обязательные CSS требования на основе функций
        required_css_features = self._generate_mandatory_css_features(request.features)
        
        return f"""
        🔥 КРИТИЧЕСКИ ВАЖНО - СОЗДАЙ CSS С ПОЛНЫМ СООТВЕТСТВИЕМ ПОЛЬЗОВАТЕЛЬСКОМУ ЗАПРОСУ!
        
        🎨 СОЗДАЙ ПРОФЕССИОНАЛЬНЫЕ CSS СТИЛИ ДЛЯ: {request.project_type.value if request.project_type else 'веб-приложения'}
=======
        return f"""
        Создай профессиональные CSS стили для {request.project_type.value if request.project_type else 'веб-приложения'}.
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
        
        {mandatory_css_structure}
        
        {project_requirements['css_specifics']}
        
<<<<<<< HEAD
        {required_css_features}
        
        🔥 ПОЛЬЗОВАТЕЛЬСКИЕ ТРЕБОВАНИЯ ДИЗАЙНА (РЕАЛИЗУЙ ВСЕ БЕЗ ИСКЛЮЧЕНИЙ):
        - 🎨 СТИЛЬ: {', '.join(request.design_requirements)}
        - ⭐ ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ: {', '.join(project_requirements['additional_features'])}
        
        🏆 ТЕХНИЧЕСКИЕ ТРЕБОВАНИЯ CSS (ОБЯЗАТЕЛЬНО):
        - 📱 Полная адаптивность (mobile-first подход, все экраны 320px-4K)
        - 🔥 Современные CSS3 свойства (flexbox, grid, custom properties, CSS variables)
        - ✨ Плавные анимации и micro-interactions (transitions, keyframes, transforms)
        - 🌐 Кроссбраузерная совместимость (последние 2 версии всех браузеров)
        - ⚡ Высокая производительность (оптимизированные селекторы, минимум reflow)
        - ♿ Полная accessibility (контрастность 4.5:1+, фокус, screen readers)
        - 🚀 Progressive enhancement (graceful degradation)
        
        🎨 ЦВЕТОВАЯ СХЕМА И ТИПОГРАФИКА (ОБЯЗАТЕЛЬНО):
        - Современная цветовая палитра с контрастными акцентами
        - Читаемые шрифты с четкой иерархией (h1-h6, body, small)
        - Консистентность в spacing (8px grid system) и sizing
        - Темная тема поддержка через CSS custom properties
        
        ⚠️ КРИТИЧЕСКИ ВАЖНО ДЛЯ ЭКРАНОВ:
        - По умолчанию показывай только главный экран (#main-screen.active)
        - Остальные экраны должны быть скрыты (.screen:not(.active))
        - Плавные переходы между экранами (fade/slide animations)
        
        🔥 ОБЯЗАТЕЛЬНО РЕАЛИЗУЙ ВСЕ УКАЗАННЫЕ ПОЛЬЗОВАТЕЛЕМ ФУНКЦИИ В CSS!
        
        Создай детальную и высококачественную CSS структуру. Верни только чистый CSS код без объяснений.
        """

    def _generate_mandatory_js_features(self, features: List[str]) -> str:
        """🎯 РЕВОЛЮЦИОННАЯ СИСТЕМА: Генерирует JavaScript ПРОФЕССИОНАЛЬНОГО УРОВНЯ AAA СТУДИЙ (1000/100)"""
        
        mandatory_js = "\n🚀 КРИТИЧЕСКИ ВАЖНО - СОЗДАЙ JAVASCRIPT УРОВНЯ AAA ИГРОВЫХ СТУДИЙ (1000/100):"
        
        for feature in features:
            if '3D графика' in feature or '3D' in feature or '3д' in feature.lower():
                mandatory_js += """
                
                🎮 ПРОФЕССИОНАЛЬНАЯ 3D СИСТЕМА (УРОВЕНЬ UNREAL ENGINE):
                
                🔥 CORE 3D ENGINE:
                class Professional3DEngine {
                    constructor(canvasId) {
                        this.canvas = document.getElementById(canvasId);
                        this.scene = new THREE.Scene();
                        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 10000);
                        this.renderer = new THREE.WebGLRenderer({
                            canvas: this.canvas,
                            antialias: true,
                            powerPreference: "high-performance",
                            stencil: true,
                            depth: true,
                            logarithmicDepthBuffer: true
                        });
                        
                        this.postProcessing = new PostProcessingPipeline(this.renderer, this.scene, this.camera);
                        this.materialSystem = new AdvancedMaterialSystem();
                        this.lightingSystem = new CinematicLightingSystem(this.scene);
                        this.animationSystem = new AdvancedAnimationSystem();
                        this.particleSystem = new ParticleSystemManager();
                        
                        this.setupRenderer();
                        this.setupPhysics();
                        this.setupAudio();
                    }
                    
                    setupRenderer() {
                        this.renderer.setSize(window.innerWidth, window.innerHeight);
                        this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                        this.renderer.outputColorSpace = THREE.SRGBColorSpace;
                        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
                        this.renderer.toneMappingExposure = 1.2;
                        this.renderer.shadowMap.enabled = true;
                        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                        this.renderer.shadowMap.autoUpdate = true;
                    }
                    
                    render() {
                        this.postProcessing.render(this.scene, this.camera);
                    }
                }
                
                🌟 POST-PROCESSING PIPELINE:
                class PostProcessingPipeline {
                    constructor(renderer, scene, camera) {
                        this.composer = new THREE.EffectComposer(renderer);
                        this.renderPass = new THREE.RenderPass(scene, camera);
                        this.bloomPass = new THREE.UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.5, 0.4, 0.85);
                        this.ssaoPass = new THREE.SSAOPass(scene, camera, window.innerWidth, window.innerHeight);
                        this.fxaaPass = new THREE.ShaderPass(THREE.FXAAShader);
                        
                        this.setupPipeline();
                    }
                    
                    setupPipeline() {
                        this.composer.addPass(this.renderPass);
                        this.composer.addPass(this.ssaoPass);
                        this.composer.addPass(this.bloomPass);
                        this.composer.addPass(this.fxaaPass);
                    }
                    
                    render() {
                        this.composer.render();
                    }
                }
                
                ⚡ PERFORMANCE MONITORING:
                class PerformanceMonitor {
                    constructor() {
                        this.stats = new Stats();
                        this.memoryStats = new Stats();
                        this.setupMonitoring();
                    }
                    
                    setupMonitoring() {
                        this.stats.showPanel(0); // FPS
                        document.body.appendChild(this.stats.dom);
                        
                        // GPU Memory tracking
                        setInterval(() => {
                            if (performance.memory) {
                                document.getElementById('gpuMemory').textContent = 
                                    Math.round(performance.memory.usedJSHeapSize / 1024 / 1024);
                            }
                        }, 1000);
                    }
                    
                    update() {
                        this.stats.update();
                    }
                }
                """
                
            if 'ИИ наставник' in feature or 'AI' in feature or 'чат' in feature.lower():
                mandatory_js += """
                
                🤖 РЕВОЛЮЦИОННЫЙ ИИ НАСТАВНИК (УРОВЕНЬ JARVIS):
                
                🧠 AI CONSCIOUSNESS SYSTEM:
                class AIConsciousness {
                    constructor() {
                        this.personality = new AIPersonality();
                        this.emotionalState = new EmotionalEngine();
                        this.knowledgeBase = new KnowledgeGraph();
                        this.conversationMemory = new ConversationMemory();
                        this.neuralVisualization = new NeuralVisualization();
                        
                        this.setupConsciousness();
                    }
                    
                    async processMessage(userInput) {
                        this.emotionalState.analyzeInput(userInput);
                        const context = await this.conversationMemory.getContext();
                        const response = await this.generateIntelligentResponse(userInput, context);
                        
                        this.neuralVisualization.showThinking();
                        this.updatePersonality(userInput, response);
                        
                        return response;
                    }
                    
                    async generateIntelligentResponse(input, context) {
                        // AI response generation with context awareness
                        const sentiment = this.emotionalState.analyzeSentiment(input);
                        const knowledge = await this.knowledgeBase.search(input);
                        
                        return {
                            text: await this.constructResponse(input, knowledge, sentiment),
                            emotion: sentiment,
                            confidence: this.calculateConfidence(knowledge),
                            suggestions: this.generateSuggestions(input, context)
                        };
                    }
                }
                
                🎭 PHOTOREALISTIC AVATAR SYSTEM:
                class RealisticAvatar {
                    constructor() {
                        this.faceEngine = new FacialExpressionEngine();
                        this.lipSyncEngine = new AdvancedLipSync();
                        this.eyeTracking = new EyeTrackingSystem();
                        this.microExpressions = new MicroExpressionSystem();
                        
                        this.setupAvatar();
                    }
                    
                    setupAvatar() {
                        this.avatar3D = new THREE.Object3D();
                        this.loadRealisticModel();
                        this.setupFacialRig();
                        this.setupEyeMovement();
                    }
                    
                    expressEmotion(emotion, intensity = 1.0) {
                        this.faceEngine.animate({
                            emotion: emotion,
                            intensity: intensity,
                            duration: 800,
                            easing: 'easeInOutCubic'
                        });
                        
                        this.microExpressions.trigger(emotion);
                    }
                    
                    speak(text, emotion = 'neutral') {
                        this.lipSyncEngine.syncWithText(text);
                        this.expressEmotion(emotion);
                        this.eyeTracking.focusOnUser();
                    }
                }
                
                🎤 PROFESSIONAL VOICE SYSTEM:
                class ProfessionalVoiceSystem {
                    constructor() {
                        this.speechEngine = new AdvancedSpeechEngine();
                        this.voiceAnalyzer = new VoiceAnalyzer();
                        this.emotionDetector = new VoiceEmotionDetector();
                        this.noiseReduction = new NoiseReductionEngine();
                        
                        this.setupAudio();
                    }
                    
                    async startRecording() {
                        const stream = await navigator.mediaDevices.getUserMedia({
                            audio: {
                                echoCancellation: true,
                                noiseSuppression: true,
                                autoGainControl: true,
                                sampleRate: 48000,
                                channelCount: 1
                            }
                        });
                        
                        this.mediaRecorder = new MediaRecorder(stream);
                        this.setupRecordingCallbacks();
                        this.mediaRecorder.start();
                    }
                    
                    async processVoice(audioData) {
                        const cleanedAudio = await this.noiseReduction.process(audioData);
                        const emotion = await this.emotionDetector.analyze(cleanedAudio);
                        const transcript = await this.speechEngine.transcribe(cleanedAudio);
                        
                        return {
                            text: transcript,
                            emotion: emotion,
                            quality: this.voiceAnalyzer.assessQuality(cleanedAudio)
                        };
                    }
                }
                """
                
            if 'озвучивание' in feature or 'голосовой ввод' in feature or 'аудио' in feature.lower():
                mandatory_js += """
                
                🎙️ PROFESSIONAL STUDIO AUDIO (УРОВЕНЬ ABBEY ROAD):
                
                🎚️ STUDIO-GRADE AUDIO ENGINE:
                class StudioAudioEngine {
                    constructor() {
                        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                        this.masterGain = this.audioContext.createGain();
                        this.compressor = this.audioContext.createDynamicsCompressor();
                        this.equalizer = new ParametricEqualizer(this.audioContext);
                        this.reverb = new ConvolutionReverb(this.audioContext);
                        this.noiseGate = new NoiseGate(this.audioContext);
                        
                        this.setupAudioChain();
                        this.setupRealTimeAnalysis();
                    }
                    
                    setupAudioChain() {
                        // Professional audio signal chain
                        this.masterGain.connect(this.compressor);
                        this.compressor.connect(this.equalizer.input);
                        this.equalizer.output.connect(this.reverb.input);
                        this.reverb.output.connect(this.audioContext.destination);
                        
                        // Set professional compressor settings
                        this.compressor.threshold.setValueAtTime(-18, this.audioContext.currentTime);
                        this.compressor.ratio.setValueAtTime(8, this.audioContext.currentTime);
                        this.compressor.attack.setValueAtTime(0.003, this.audioContext.currentTime);
                        this.compressor.release.setValueAtTime(0.1, this.audioContext.currentTime);
                    }
                    
                    createVoiceProcessor() {
                        return new VoiceProcessor({
                            deEsser: true,
                            pitchCorrection: true,
                            formantShifting: false,
                            vocalDoubling: true,
                            breathingReduction: true
                        });
                    }
                }
                
                🎵 ADVANCED VOICE PROCESSING:
                class VoiceProcessor {
                    constructor(options) {
                        this.options = options;
                        this.pitchDetector = new PitchDetector();
                        this.formantAnalyzer = new FormantAnalyzer();
                        this.deEsser = new DeEsser();
                        this.breathRemover = new BreathRemover();
                    }
                    
                    async processVoice(audioBuffer) {
                        let processedBuffer = audioBuffer;
                        
                        if (this.options.breathingReduction) {
                            processedBuffer = await this.breathRemover.process(processedBuffer);
                        }
                        
                        if (this.options.deEsser) {
                            processedBuffer = await this.deEsser.process(processedBuffer);
                        }
                        
                        if (this.options.pitchCorrection) {
                            const pitch = this.pitchDetector.detect(processedBuffer);
                            processedBuffer = this.correctPitch(processedBuffer, pitch);
                        }
                        
                        return processedBuffer;
                    }
                }
                
                🔊 CINEMATIC AUDIO PLAYBACK:
                class CinematicAudioSystem {
                    constructor() {
                        this.spatialAudio = new SpatialAudioEngine();
                        this.masteringChain = new MasteringChain();
                        this.loudnessMonitor = new LoudnessMonitor();
                        
                        this.setupSurroundSound();
                    }
                    
                    setupSurroundSound() {
                        this.panner = this.audioContext.createPanner();
                        this.panner.panningModel = 'HRTF';
                        this.panner.distanceModel = 'inverse';
                        this.panner.refDistance = 1;
                        this.panner.maxDistance = 10000;
                        this.panner.rolloffFactor = 1;
                        this.panner.coneInnerAngle = 360;
                        this.panner.coneOuterAngle = 0;
                        this.panner.coneOuterGain = 0;
                    }
                }
                """
                
            if 'видео' in feature.lower() or 'камера' in feature.lower():
                mandatory_js += """
                
                🎬 HOLLYWOOD VIDEO PRODUCTION (УРОВЕНЬ CINEMA):
                
                📹 PROFESSIONAL CAMERA SYSTEM:
                class CinematicCameraSystem {
                    constructor() {
                        this.videoElement = document.createElement('video');
                        this.canvas = document.createElement('canvas');
                        this.ctx = this.canvas.getContext('2d');
                        
                        this.colorGrading = new ColorGradingEngine();
                        this.stabilization = new VideoStabilization();
                        this.focusPulling = new AutoFocusSystem();
                        this.exposureControl = new ExposureControl();
                        
                        this.setupCamera();
                    }
                    
                    async startRecording(constraints = {}) {
                        const defaultConstraints = {
                            video: {
                                width: { ideal: 3840 },  // 4K
                                height: { ideal: 2160 },
                                frameRate: { ideal: 60 },
                                facingMode: 'user',
                                aspectRatio: { ideal: 16/9 }
                            },
                            audio: {
                                sampleRate: 48000,
                                channelCount: 2,
                                echoCancellation: true,
                                noiseSuppression: true
                            }
                        };
                        
                        const stream = await navigator.mediaDevices.getUserMedia({
                            ...defaultConstraints,
                            ...constraints
                        });
                        
                        this.setupRecording(stream);
                        return stream;
                    }
                    
                    applyColorGrading(preset = 'cinematic') {
                        this.colorGrading.applyLUT(preset);
                        this.colorGrading.adjustExposure(0.2);
                        this.colorGrading.adjustContrast(1.1);
                        this.colorGrading.adjustSaturation(1.05);
                    }
                }
                
                🎨 COLOR GRADING ENGINE:
                class ColorGradingEngine {
                    constructor() {
                        this.luts = new Map();
                        this.loadCinematicLUTs();
                    }
                    
                    loadCinematicLUTs() {
                        this.luts.set('cinematic', new CinematicLUT());
                        this.luts.set('vintage', new VintageLUT());
                        this.luts.set('dramatic', new DramaticLUT());
                        this.luts.set('natural', new NaturalLUT());
                    }
                    
                    applyLUT(lutName) {
                        const lut = this.luts.get(lutName);
                        if (lut) {
                            this.currentLUT = lut;
                            this.processFrame();
                        }
                    }
                }
                
                🎞️ VIDEO EFFECTS SYSTEM:
                class VideoEffectsSystem {
                    constructor() {
                        this.webglRenderer = new WebGLRenderer();
                        this.shaderLibrary = new ShaderLibrary();
                        this.particleSystem = new VideoParticleSystem();
                        
                        this.loadShaders();
                    }
                    
                    loadShaders() {
                        this.shaders = {
                            filmGrain: this.shaderLibrary.load('filmGrain'),
                            vignette: this.shaderLibrary.load('vignette'),
                            chromaKey: this.shaderLibrary.load('chromaKey'),
                            motionBlur: this.shaderLibrary.load('motionBlur'),
                            bokeh: this.shaderLibrary.load('bokeh')
                        };
                    }
                    
                    applyEffect(effectName, parameters = {}) {
                        const shader = this.shaders[effectName];
                        if (shader) {
                            this.webglRenderer.applyShader(shader, parameters);
                        }
                    }
                }
                """
        
        # Universal revolutionary JavaScript features
        mandatory_js += """
        
        🚀 UNIVERSAL REVOLUTIONARY FEATURES:
        
        💎 PERFORMANCE OPTIMIZATION ENGINE:
        class PerformanceOptimizer {
            constructor() {
                this.frameRateTarget = 60;
                this.memoryThreshold = 100 * 1024 * 1024; // 100MB
                this.performanceMetrics = new PerformanceMetrics();
                
                this.setupOptimization();
            }
            
            setupOptimization() {
                // Object pooling for frequent allocations
                this.objectPool = new ObjectPool();
                
                // Throttle/debounce utilities
                this.throttle = this.createThrottle();
                this.debounce = this.createDebounce();
                
                // Virtual scrolling for large lists
                this.virtualScroller = new VirtualScroller();
                
                // Lazy loading system
                this.lazyLoader = new IntersectionObserver(this.handleLazyLoad.bind(this));
                
                // Memory leak detection
                this.memoryMonitor = new MemoryMonitor();
            }
            
            createThrottle() {
                return (func, delay) => {
                    let timeoutId;
                    let lastExecTime = 0;
                    return (...args) => {
                        const currentTime = Date.now();
                        
                        if (currentTime - lastExecTime > delay) {
                            func(...args);
                            lastExecTime = currentTime;
                        } else {
                            clearTimeout(timeoutId);
                            timeoutId = setTimeout(() => {
                                func(...args);
                                lastExecTime = Date.now();
                            }, delay - (currentTime - lastExecTime));
                        }
                    };
                };
            }
        }
        
        🛡️ SECURITY & VALIDATION ENGINE:
        class SecurityEngine {
            constructor() {
                this.inputSanitizer = new InputSanitizer();
                this.xssProtection = new XSSProtection();
                this.csrfProtection = new CSRFProtection();
                this.rateLimiter = new RateLimiter();
            }
            
            sanitizeInput(input, type = 'text') {
                return this.inputSanitizer.sanitize(input, type);
            }
            
            validateInput(input, rules) {
                const validator = new InputValidator(rules);
                return validator.validate(input);
            }
            
            preventXSS(content) {
                return this.xssProtection.sanitize(content);
            }
        }
        
        📱 MOBILE OPTIMIZATION ENGINE:
        class MobileOptimizer {
            constructor() {
                this.touchHandler = new TouchGestureHandler();
                this.orientationHandler = new OrientationHandler();
                this.batteryMonitor = new BatteryMonitor();
                this.networkMonitor = new NetworkMonitor();
                
                this.setupMobileOptimizations();
            }
            
            setupMobileOptimizations() {
                // Touch gesture recognition
                this.touchHandler.registerGestures(['tap', 'doubleTap', 'swipe', 'pinch', 'rotate']);
                
                // Device orientation handling
                this.orientationHandler.onOrientationChange(this.handleOrientationChange.bind(this));
                
                // Network-aware loading
                this.networkMonitor.onConnectionChange(this.adjustQuality.bind(this));
                
                // Battery-aware performance
                this.batteryMonitor.onBatteryLow(this.reducePowerConsumption.bind(this));
            }
            
            handleOrientationChange(orientation) {
                // Adjust UI for new orientation
                this.adjustLayoutForOrientation(orientation);
                this.optimizeRenderingForOrientation(orientation);
            }
        }
        
        🎯 ACCESSIBILITY ENGINE:
        class AccessibilityEngine {
            constructor() {
                this.screenReaderSupport = new ScreenReaderSupport();
                this.keyboardNavigation = new KeyboardNavigation();
                this.focusManager = new FocusManager();
                this.contrastChecker = new ContrastChecker();
                this.voiceControl = new VoiceControl();
                
                this.setupAccessibility();
            }
            
            setupAccessibility() {
                // Dynamic ARIA updates
                this.ariaUpdater = new ARIAUpdater();
                
                // Keyboard navigation
                this.keyboardNavigation.setupTabOrder();
                this.keyboardNavigation.registerShortcuts();
                
                // Focus management
                this.focusManager.trapFocus();
                this.focusManager.manageSkipLinks();
                
                // High contrast mode detection
                this.detectHighContrastMode();
            }
            
            announceToScreenReader(message, priority = 'polite') {
                this.screenReaderSupport.announce(message, priority);
            }
        }
        
        🧠 AI INTEGRATION ENGINE:
        class AIIntegrationEngine {
            constructor() {
                this.modelLoader = new MLModelLoader();
                this.inferenceEngine = new InferenceEngine();
                this.dataPreprocessor = new DataPreprocessor();
                this.predictionCache = new PredictionCache();
                
                this.setupAI();
            }
            
            async loadModel(modelUrl, modelType = 'tensorflow') {
                return await this.modelLoader.load(modelUrl, modelType);
            }
            
            async predict(inputData, modelName) {
                const preprocessedData = this.dataPreprocessor.process(inputData);
                const cachedResult = this.predictionCache.get(preprocessedData);
                
                if (cachedResult) {
                    return cachedResult;
                }
                
                const prediction = await this.inferenceEngine.run(modelName, preprocessedData);
                this.predictionCache.set(preprocessedData, prediction);
                
                return prediction;
            }
        }
        """
        
        return mandatory_js
    
    def _create_js_prompt(self, request: AnalyzedRequest) -> str:
        """🎯 КОМПАКТНЫЙ ПРОМПТ: Создает JavaScript промпт под лимит 6000 токенов"""
        
        project_type_value = request.project_type.value if request.project_type else 'веб-приложение'
        features_str = ', '.join(request.features[:3])  # Ограничиваем количество фич
        
        return f"""Создай JavaScript для {project_type_value}.

Требования:
- Функции: {features_str}
- ES6+ синтаксис, чистый код
- Обработка событий DOM
- Responsive дизайн поддержка

Обязательные возможности:
- Навигация между экранами
- Локальное сохранение данных
- Анимации и переходы
- Обработка ошибок

Создай полнофункциональный JavaScript код."""
    
    def _generate_with_ai(self, prompt: str, task_type: str = 'code', progress_callback=None, target_file=None) -> str:
        """Генерирует код с помощью AI или продвинутых fallback'ов"""

        try:
            # AI generation logic would go here
            pass
        except Exception as e:
            print(f"Error in _generate_with_ai: {e}")

        js_code = """
        class ErrorBoundary {
            static wrap(fn, context = 'unknown') {
                try {
                    return fn();
                } catch (error) {
                    this.handleError(error, context);
                    return this.getGracefulFallback(context);
                }
            }
        }
        
        # 3. 🔄 REACTIVE PROGRAMMING:
        
        class ReactiveSystem {
            constructor() {
                this.observables = new Map();
                this.subscribers = new Set();
            }
            
            subscribe(event, callback) {
                // Observable pattern implementation
            }
        }
        
        // Advanced JavaScript architecture with error handling and performance optimization
        """
        return js_code

    def _generate_with_ai_duplicate(self, prompt: str, task_type: str = 'code', progress_callback=None, target_file=None) -> str:
        """Генерирует код с помощью AI или продвинутых fallback'ов"""
        
        try:
            if self.default_ai == 'groq' and self.groq_api_key:
                if progress_callback:
                    progress_callback("🤖 Подключаюсь к AI сервису...", 5)
                print(f"🤖 Вызываем Groq API...")
                # РЕВОЛЮЦИОННЫЙ ПОДХОД: ВСЕГДА ждем полноценный GROQ ответ, никогда не используем fallback
                attempt = 1
                max_attempts = 10  # Максимум 10 попыток для получения качественного ответа
                
                while attempt <= max_attempts:
                    content = self._call_groq_api_for_code(prompt, model=self.models['groq']['code'])
                    print(f"📝 Groq попытка {attempt}: вернул {len(content) if content else 0} символов")
                    
                    if content and len(content.strip()) > 100:  # Требуем минимум 100 символов для революционного кода
                        print(f"🚀 РЕВОЛЮЦИОННЫЙ РЕЗУЛЬТАТ GROQ получен! {len(content)} символов")
                        if progress_callback:
                            progress_callback("✅ Получен революционный ответ от AI!", 100)
                        # Небольшая задержка между запросами для предотвращения rate limiting
                        time.sleep(2)
                        return content
                    else:
                        print(f"⏳ Попытка {attempt}/{max_attempts}: результат короткий, повторяем через 15 секунд...")
                        if progress_callback:
                            progress_callback(f"⏳ Ожидаем качественный ответ от AI... попытка {attempt}/{max_attempts}", 20 + (attempt * 8))
                        time.sleep(15)  # Ждем 15 секунд перед повторной попыткой
                        attempt += 1
                
                # Если после 10 попыток всё еще не получили результат, попробуем с другой моделью
                print("🔄 Переключаемся на резервную модель GROQ...")
                content = self._call_groq_api_for_code(prompt, model=self.models['groq']['smart'])
                if content and len(content.strip()) > 50:
                    return content
        except Exception as e:
            print(f"❌ КРИТИЧЕСКАЯ ОШИБКА AI генерации: {e}")
            # В случае критической ошибки попробуем еще раз через 30 секунд
            print("🔄 Критическая ошибка - ждем 30 секунд и пробуем снова...")
            time.sleep(30)
            if self.default_ai == 'groq' and self.groq_api_key:
                content = self._call_groq_api_for_code(prompt, model=self.models['groq']['smart'])
                if content:
                    return content
            
        # ТОЛЬКО В КРАЙНЕМ СЛУЧАЕ - если GROQ полностью недоступен
        print("🚨 АВАРИЙНЫЙ РЕЖИМ: GROQ недоступен, создаю базовую структуру...")
        return f"// АВАРИЙНЫЙ РЕЖИМ - GROQ недоступен\\nconsole.log('Приложение в аварийном режиме');\\n// Требуется восстановление подключения к GROQ"
    
    def _generate_intelligent_fallback(self, prompt: str, task_type: str, progress_callback=None, target_file=None) -> str:
        """Интеллектуальная генерация кода на основе анализа промпта с прогрессом"""
        import time
        import random
        
        # Имитируем время генерации AI (5-15 секунд)
        delay = random.uniform(5, 15)
        print(f"⏳ Генерация займет примерно {delay:.1f} секунд...")
        
        # Отправляем уведомления о прогрессе
        if progress_callback:
            if 'HTML' in prompt.upper():
                progress_callback("🎨 Создаю HTML структуру...", 10)
            elif 'CSS' in prompt.upper():
                progress_callback("✨ Генерирую стили CSS...", 50)
            elif 'JAVASCRIPT' in prompt.upper():
                progress_callback("⚡ Программирую логику JavaScript...", 80)
        
        # Симулируем прогресс генерации
        steps = 5
        for i in range(steps):
            time.sleep(delay / steps)
            if progress_callback:
                progress = 10 + (80 * (i + 1) / steps)
                if 'HTML' in prompt.upper():
                    messages = [
                        "🔨 Создаю базовую структуру...",
                        "🎨 Добавляю интерфейсные элементы...",
                        "🔧 Настраиваю компоненты...",
                        "✨ Оптимизирую структуру...",
                        "🎯 Завершаю HTML разметку..."
                    ]
                elif 'CSS' in prompt.upper():
                    messages = [
                        "🎨 Создаю базовые стили...",
                        "✨ Добавляю анимации...",
                        "🌈 Настраиваю цветовую схему...",
                        "📱 Адаптирую под мобильные...",
                        "🎭 Полирую визуальные эффекты..."
                    ]
                elif 'JAVASCRIPT' in prompt.upper():
                    messages = [
                        "⚡ Создаю базовую логику...",
                        "🧠 Программирую алгоритмы...",
                        "🔄 Добавляю интерактивность...",
                        "🛡️ Обрабатываю ошибки...",
                        "🎯 Оптимизирую производительность..."
                    ]
                else:
                    messages = ["🔨 Генерирую код..."] * 5
                
                progress_callback(messages[i], progress)
        
        # Анализируем промпт для определения контекста
        prompt_lower = prompt.lower()
        
        # Определяем тип файла на основе task_type и контекста
        if task_type == 'code':
            # Первый приоритет - используем target_file если передан
            if target_file:
                if target_file == 'index.html':
                    result = self._generate_smart_html(prompt)
                elif target_file == 'styles.css':
                    result = self._generate_smart_css(prompt)
                elif target_file == 'script.js':
                    result = self._generate_smart_javascript(prompt)
                else:
                    # Определяем по расширению файла
                    if target_file.endswith('.html'):
                        result = self._generate_smart_html(prompt)
                    elif target_file.endswith('.css'):
                        result = self._generate_smart_css(prompt)
                    elif target_file.endswith('.js'):
                        result = self._generate_smart_javascript(prompt)
                    else:
                        result = self._generate_smart_html(prompt)  # default fallback
            else:
                # Второй приоритет - используем логику определения по содержимому промпта (старая логика)
                # НО более осторожно - избегаем ложных срабатываний
                if 'JAVASCRIPT' in prompt.upper() and 'script.js' in prompt and 'HTML' not in prompt.upper()[:100]:
                    result = self._generate_smart_javascript(prompt)
                elif 'CSS' in prompt.upper() and 'styles.css' in prompt and 'HTML' not in prompt.upper()[:100]:
                    result = self._generate_smart_css(prompt)
                elif 'HTML' in prompt.upper():
                    result = self._generate_smart_html(prompt)
                else:
                    # Fallback - определяем по ключевым словам в содержимом промпта
                    if any(word in prompt_lower for word in ['js', 'javascript', 'логика', 'функция', 'событие']):
                        result = self._generate_smart_javascript(prompt)
                    elif any(word in prompt_lower for word in ['css', 'стили', 'style', 'цвета', 'анимация']):
                        result = self._generate_smart_css(prompt)
                    else:
                        result = self._generate_smart_html(prompt)
        else:
            result = self._generate_fallback_code(task_type)
        
        if progress_callback:
            progress_callback("✅ Генерация завершена!", 100)
        
        return result
    
    def _generate_smart_html(self, prompt: str) -> str:
        """Генерирует умный HTML на основе промпта"""
        prompt_lower = prompt.lower()
        
        # Определяем тип приложения по ключевым словам
        if any(word in prompt_lower for word in ['калькулятор', 'calculator', 'вычисления', 'математика']):
            return self._get_advanced_calculator_html()
        elif any(word in prompt_lower for word in ['змейка', 'snake', 'игра', 'game']):
            return self._get_snake_html()
        elif any(word in prompt_lower for word in ['наставник', 'ии наставник', 'ai mentor', '3д', '3d', 'голограмма']):
            return self._get_ai_mentor_html()
        elif any(word in prompt_lower for word in ['idle', 'рпг', 'rpg', 'приключение', 'уровни']):
            return self._get_idle_rpg_html()
        else:
            return self._get_simple_app_html()
    
    def _get_ai_mentor_html(self) -> str:
        """Генерирует HTML для AI наставника с 3D аватаром"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Наставник 3D</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="app-container">
        <header class="header">
            <h1>🤖 AI Наставник 3D</h1>
            <div class="mentor-selector">
                <label>Выберите наставника:</label>
                <select id="mentorSelect">
                    <option value="elon">🚀 Илон Маск</option>
                    <option value="jobs">💻 Стив Джобс</option>
                    <option value="gates">🌍 Билл Гейтс</option>
                    <option value="bezos">📦 Джефф Безос</option>
                    <option value="buffett">💰 Уоррен Баффет</option>
                </select>
            </div>
        </header>
        
        <div class="main-content">
            <div class="mentor-avatar">
                <div id="avatar3d" class="avatar-container">
                    <div class="avatar-placeholder">
                        <div class="face">😊</div>
                        <div class="loading">Загрузка 3D модели...</div>
                    </div>
                </div>
                <div class="mentor-info">
                    <h3 id="mentorName">Илон Маск</h3>
                    <p id="mentorDescription">Предприниматель, основатель Tesla и SpaceX</p>
                </div>
            </div>
            
            <div class="chat-interface">
                <div class="chat-messages" id="chatMessages">
                    <div class="ai-message">
                        <strong>AI Наставник:</strong> Привет! Я готов поделиться опытом и знаниями. О чем хотите поговорить?
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <textarea id="userInput" placeholder="Задайте вопрос своему наставнику..."></textarea>
                    <button id="sendBtn" onclick="sendMessage()">Отправить</button>
                </div>
            </div>
        </div>
        
        <div class="features-panel">
            <h4>Возможности:</h4>
            <ul>
                <li>💬 Реалистичные диалоги</li>
                <li>🎯 Персональные советы</li>
                <li>📊 Анализ ситуаций</li>
                <li>🚀 Стратегии развития</li>
                <li>💡 Инновационные идеи</li>
            </ul>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_idle_rpg_html(self) -> str:
        """Генерирует HTML для idle RPG игры"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Idle RPG Adventure</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="game-container">
        <header class="game-header">
            <h1>⚔️ Idle RPG Adventure</h1>
            <div class="game-stats">
                <div class="stat">
                    <span>💰 Золото:</span>
                    <span id="gold">100</span>
                </div>
                <div class="stat">
                    <span>💎 Кристаллы:</span>
                    <span id="crystals">0</span>
                </div>
                <div class="stat">
                    <span>⚡ Энергия:</span>
                    <span id="energy">100/100</span>
                </div>
            </div>
        </header>
        
        <div class="game-main">
            <div class="character-panel">
                <div class="character-avatar">
                    <img id="characterImg" src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNDAiIGZpbGw9IiM0Mjg1RjQiLz4KPHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNDAiIGZpbGw9IiM0Mjg1RjQiLz4KPHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNTAiIGN5PSI1MCIgcj0iNDAiIGZpbGw9IiM0Mjg1RjQiLz4=" alt="Герой">
                </div>
                
                <div class="character-stats">
                    <h3>🏆 Герой</h3>
                    <div class="level">Уровень: <span id="level">1</span></div>
                    
                    <div class="stat-bar">
                        <label>❤️ Здоровье:</label>
                        <div class="progress-bar">
                            <div id="healthBar" class="progress-fill health" style="width: 100%"></div>
                        </div>
                        <span id="healthText">100/100</span>
                    </div>
                    
                    <div class="stat-bar">
                        <label>⭐ Опыт:</label>
                        <div class="progress-bar">
                            <div id="expBar" class="progress-fill exp" style="width: 0%"></div>
                        </div>
                        <span id="expText">0/100</span>
                    </div>
                    
                    <div class="primary-stats">
                        <div class="stat-item">
                            <span>⚔️ Атака:</span>
                            <span id="attack">10</span>
                        </div>
                        <div class="stat-item">
                            <span>🛡️ Защита:</span>
                            <span id="defense">5</span>
                        </div>
                        <div class="stat-item">
                            <span>💨 Скорость:</span>
                            <span id="speed">8</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="battle-area">
                <div class="enemy-section">
                    <div class="enemy-avatar">
                        <div id="enemySprite">👹</div>
                    </div>
                    <div class="enemy-info">
                        <h4 id="enemyName">Гоблин</h4>
                        <div class="enemy-health-bar">
                            <div id="enemyHealthBar" class="progress-fill enemy-health" style="width: 100%"></div>
                        </div>
                        <span id="enemyHealthText">50/50</span>
                    </div>
                </div>
                
                <div class="battle-controls">
                    <button id="attackBtn" class="action-btn attack-btn" onclick="attack()">⚔️ Атаковать</button>
                    <button id="defendBtn" class="action-btn defend-btn" onclick="defend()">🛡️ Защищаться</button>
                    <button id="skillBtn" class="action-btn skill-btn" onclick="useSkill()">💫 Навык</button>
                </div>
                
                <div class="battle-log" id="battleLog">
                    <div class="log-entry">Начинается битва с Гоблином!</div>
                </div>
            </div>
            
            <div class="upgrades-panel">
                <h4>🏪 Улучшения</h4>
                <div class="upgrade-item">
                    <span>⚔️ Улучшить меч</span>
                    <span class="cost">50 💰</span>
                    <button onclick="upgradeSword()">Купить</button>
                </div>
                <div class="upgrade-item">
                    <span>🛡️ Лучшая броня</span>
                    <span class="cost">75 💰</span>
                    <button onclick="upgradeArmor()">Купить</button>
                </div>
                <div class="upgrade-item">
                    <span>💊 Зелье здоровья</span>
                    <span class="cost">25 💰</span>
                    <button onclick="buyPotion()">Купить</button>
                </div>
            </div>
        </div>
        
        <div class="achievements">
            <h4>🏆 Достижения</h4>
            <div class="achievement locked">
                <span>🥇 Первая победа</span>
                <span class="requirement">Победить 1 врага</span>
            </div>
            <div class="achievement locked">
                <span>💰 Богач</span>
                <span class="requirement">Накопить 1000 золота</span>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_advanced_calculator_html(self) -> str:
        """Генерирует продвинутый калькулятор"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Научный Калькулятор</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="calculator-container">
        <div class="calculator">
            <div class="display">
                <div class="history" id="history"></div>
                <input type="text" id="display" readonly value="0">
            </div>
            
            <div class="buttons">
                <div class="row">
                    <button class="btn function" onclick="clearAll()">C</button>
                    <button class="btn function" onclick="clearEntry()">CE</button>
                    <button class="btn function" onclick="backspace()">⌫</button>
                    <button class="btn operator" onclick="operation('/')">÷</button>
                </div>
                
                <div class="row">
                    <button class="btn function" onclick="operation('sqrt')">√</button>
                    <button class="btn function" onclick="operation('square')">x²</button>
                    <button class="btn function" onclick="operation('power')">x^y</button>
                    <button class="btn operator" onclick="operation('*')">×</button>
                </div>
                
                <div class="row">
                    <button class="btn number" onclick="number('7')">7</button>
                    <button class="btn number" onclick="number('8')">8</button>
                    <button class="btn number" onclick="number('9')">9</button>
                    <button class="btn operator" onclick="operation('-')">−</button>
                </div>
                
                <div class="row">
                    <button class="btn number" onclick="number('4')">4</button>
                    <button class="btn number" onclick="number('5')">5</button>
                    <button class="btn number" onclick="number('6')">6</button>
                    <button class="btn operator" onclick="operation('+')">+</button>
                </div>
                
                <div class="row">
                    <button class="btn number" onclick="number('1')">1</button>
                    <button class="btn number" onclick="number('2')">2</button>
                    <button class="btn number" onclick="number('3')">3</button>
                    <button class="btn equals" onclick="calculate()" rowspan="2">=</button>
                </div>
                
                <div class="row">
                    <button class="btn number zero" onclick="number('0')">0</button>
                    <button class="btn number" onclick="number('.')">.</button>
                    <button class="btn function" onclick="toggleSign()">±</button>
                </div>
            </div>
            
            <div class="scientific-panel">
                <h4>Научные функции</h4>
                <div class="scientific-buttons">
                    <button class="btn function" onclick="operation('sin')">sin</button>
                    <button class="btn function" onclick="operation('cos')">cos</button>
                    <button class="btn function" onclick="operation('tan')">tan</button>
                    <button class="btn function" onclick="operation('log')">log</button>
                    <button class="btn function" onclick="operation('ln')">ln</button>
                    <button class="btn function" onclick="operation('pi')">π</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _generate_smart_css(self, prompt: str) -> str:
        """Генерирует CSS на основе промпта"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['наставник', 'ai mentor', '3d']):
            return self._get_ai_mentor_css()
        elif any(word in prompt_lower for word in ['idle', 'rpg', 'игра']):
            return self._get_idle_rpg_css()
        elif any(word in prompt_lower for word in ['калькулятор', 'calculator']):
            return self._get_calculator_css()
        else:
            return self._get_generic_css()
    
    def _generate_smart_javascript(self, prompt: str) -> str:
        """Генерирует JavaScript на основе промпта"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['наставник', 'ai mentor', '3d']):
            return self._get_ai_mentor_js()
        elif any(word in prompt_lower for word in ['idle', 'rpg', 'игра']):
            return self._get_idle_rpg_js()
        elif any(word in prompt_lower for word in ['калькулятор', 'calculator']):
            return self._get_calculator_js()
        else:
            return self._get_generic_js()
    
    def _get_calculator_css(self) -> str:
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
}

.calculator-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.calculator {
    width: 400px;
}

.display {
    background: #000;
    color: #fff;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    text-align: right;
}

.history {
    font-size: 14px;
    color: #888;
    min-height: 20px;
    margin-bottom: 10px;
}

#display {
    background: transparent;
    border: none;
    color: #fff;
    font-size: 32px;
    width: 100%;
    text-align: right;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-bottom: 20px;
}

.row {
    display: contents;
}

.btn {
    height: 70px;
    border: none;
    border-radius: 15px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

.btn.number {
    background: #333;
    color: #fff;
}

.btn.operator {
    background: #ff9500;
    color: #fff;
}

.btn.function {
    background: #a6a6a6;
    color: #000;
}

.btn.equals {
    background: #ff9500;
    color: #fff;
    grid-row: span 2;
}

.btn.zero {
    grid-column: span 2;
}

.scientific-panel {
    background: rgba(0,0,0,0.1);
    padding: 15px;
    border-radius: 10px;
    margin-top: 15px;
}

.scientific-panel h4 {
    color: #fff;
    margin-bottom: 10px;
    text-align: center;
}

.scientific-buttons {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
}

.scientific-buttons .btn {
    height: 50px;
    font-size: 16px;
}'''
    
    def _get_calculator_js(self) -> str:
        return '''let display = document.getElementById('display');
let history = document.getElementById('history');
let currentOperation = null;
let previousOperand = null;
let waitingForOperand = false;

function number(digit) {
    if (waitingForOperand) {
        display.value = digit;
        waitingForOperand = false;
    } else {
        display.value = display.value === '0' ? digit : display.value + digit;
    }
}

function operation(nextOperator) {
    const inputValue = parseFloat(display.value);

    if (previousOperand === null) {
        previousOperand = inputValue;
    } else if (currentOperation) {
        const currentValue = previousOperand || 0;
        const newValue = performCalculation[currentOperation](currentValue, inputValue);

        display.value = String(newValue);
        previousOperand = newValue;
    }

    waitingForOperand = true;
    currentOperation = nextOperator;
    
    // Добавляем в историю
    if (nextOperator !== '=') {
        history.textContent = previousOperand + ' ' + getOperatorSymbol(nextOperator);
    }
}

function calculate() {
    const inputValue = parseFloat(display.value);

    if (previousOperand !== null && currentOperation) {
        const newValue = performCalculation[currentOperation](previousOperand, inputValue);
        
        history.textContent = previousOperand + ' ' + getOperatorSymbol(currentOperation) + ' ' + inputValue + ' =';
        display.value = String(newValue);
        
        previousOperand = null;
        currentOperation = null;
        waitingForOperand = true;
    }
}

const performCalculation = {
    '/': (firstOperand, secondOperand) => firstOperand / secondOperand,
    '*': (firstOperand, secondOperand) => firstOperand * secondOperand,
    '+': (firstOperand, secondOperand) => firstOperand + secondOperand,
    '-': (firstOperand, secondOperand) => firstOperand - secondOperand,
    'sqrt': (operand) => Math.sqrt(operand),
    'square': (operand) => operand * operand,
    'power': (firstOperand, secondOperand) => Math.pow(firstOperand, secondOperand),
    'sin': (operand) => Math.sin(operand * Math.PI / 180),
    'cos': (operand) => Math.cos(operand * Math.PI / 180),
    'tan': (operand) => Math.tan(operand * Math.PI / 180),
    'log': (operand) => Math.log10(operand),
    'ln': (operand) => Math.log(operand),
    'pi': () => Math.PI,
    '=': (firstOperand, secondOperand) => secondOperand
};

function getOperatorSymbol(op) {
    const symbols = {
        '/': '÷',
        '*': '×',
        '+': '+',
        '-': '−',
        'sqrt': '√',
        'square': 'x²',
        'power': '^'
    };
    return symbols[op] || op;
}

function clearAll() {
    display.value = '0';
    history.textContent = '';
    previousOperand = null;
    currentOperation = null;
    waitingForOperand = false;
}

function clearEntry() {
    display.value = '0';
}

function backspace() {
    display.value = display.value.slice(0, -1) || '0';
}

function toggleSign() {
    display.value = String(-parseFloat(display.value));
}

// Обработка клавиатурного ввода
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    if (key >= '0' && key <= '9' || key === '.') {
        number(key);
    } else if (key === '+' || key === '-' || key === '*' || key === '/') {
        operation(key);
    } else if (key === 'Enter' || key === '=') {
        calculate();
    } else if (key === 'Escape') {
        clearAll();
    } else if (key === 'Backspace') {
        backspace();
    }
});

console.log('🧮 Научный калькулятор загружен! Поддерживает клавиатурный ввод.');'''
    
    def _get_snake_html(self) -> str:
        """Генерирует HTML для игры змейка"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Змейка</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h1>🐍 Змейка</h1>
            <div class="game-stats">
                <div class="stat">Счет: <span id="score">0</span></div>
                <div class="stat">Рекорд: <span id="highScore">0</span></div>
                <div class="stat">Уровень: <span id="level">1</span></div>
            </div>
        </div>
        
        <div class="game-board-container">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
            <div class="game-overlay" id="gameOverlay">
                <div class="start-screen" id="startScreen">
                    <h2>🎮 Добро пожаловать!</h2>
                    <p>Используйте WASD или стрелки для управления</p>
                    <button onclick="startGame()">Начать игру</button>
                </div>
                <div class="game-over-screen" id="gameOverScreen" style="display: none;">
                    <h2>💀 Игра окончена!</h2>
                    <p>Ваш счет: <span id="finalScore">0</span></p>
                    <button onclick="restartGame()">Играть снова</button>
                </div>
            </div>
        </div>
        
        <div class="controls">
            <div class="control-buttons">
                <button onclick="pauseGame()" id="pauseBtn">⏸️ Пауза</button>
                <button onclick="toggleSound()" id="soundBtn">🔊 Звук</button>
            </div>
            
            <div class="mobile-controls">
                <div class="control-row">
                    <button class="control-btn" onclick="changeDirection('up')">↑</button>
                </div>
                <div class="control-row">
                    <button class="control-btn" onclick="changeDirection('left')">←</button>
                    <button class="control-btn" onclick="changeDirection('down')">↓</button>
                    <button class="control-btn" onclick="changeDirection('right')">→</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_ai_mentor_css(self) -> str:
        """CSS для AI наставника"""  
        return '''/* AI Mentor 3D Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    color: white;
    margin: 0;
    padding: 20px;
}

.app-container {
    max-width: 1200px;
    margin: 0 auto;
}

.header h1 {
    text-align: center;
    font-size: 2.5rem;
    margin-bottom: 30px;
}

.main-content {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 30px;
}

.mentor-avatar {
    text-align: center;
}

.avatar-container {
    width: 200px;
    height: 200px;
    margin: 0 auto 20px;
    background: linear-gradient(45deg, #667eea, #764ba2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.chat-interface {
    background: rgba(255,255,255,0.1);
    border-radius: 15px;
    padding: 20px;
}

.chat-messages {
    height: 300px;
    overflow-y: auto;
    margin-bottom: 20px;
    padding: 15px;
    background: rgba(0,0,0,0.2);
    border-radius: 10px;
}'''
    
    def _get_ai_mentor_js(self) -> str:
        """JavaScript для AI наставника"""
        return '''const mentors = {
    'elon': { name: 'Илон Маск', avatar: '🚀' },
    'jobs': { name: 'Стив Джобс', avatar: '💻' }
};

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (message) {
        addMessage('user', message);
        setTimeout(() => addMessage('ai', 'Интересная мысль! Расскажите больше.'), 1000);
        input.value = '';
    }
}

function addMessage(sender, text) {
    const chat = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.innerHTML = `<strong>${sender === 'user' ? 'Вы' : 'AI'}:</strong> ${text}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('🤖 AI Mentor загружен');
});'''

    def _get_generic_css(self) -> str:
        return '''body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    margin: 0;
    padding: 20px;
    color: white;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.app-container {
    background: rgba(255,255,255,0.1);
    padding: 40px;
    border-radius: 20px;
    text-align: center;
    max-width: 600px;
}

button {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 25px;
    cursor: pointer;
    margin: 10px;
    font-size: 16px;
}'''

    def _get_generic_js(self) -> str:
        return '''document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Приложение загружено!');
});

function showMessage(msg) {
    alert(msg);
}

function changeBackground() {
    document.body.style.background = 'linear-gradient(135deg, #ff6b6b, #4ecdc4)';
}'''

    def _get_simple_app_html(self) -> str:
        """Генерирует простое приложение"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Простое приложение</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        <header class="app-header">
            <h1>🚀 Простое приложение</h1>
            <p>Добро пожаловать в наше приложение!</p>
        </header>
        
        <main class="app-main">
            <div class="feature-section">
                <h2>✨ Особенности</h2>
                <div class="features-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🎨</div>
                        <h3>Красивый дизайн</h3>
                        <p>Современный и привлекательный интерфейс</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <h3>Быстрая работа</h3>
                        <p>Оптимизированная производительность</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📱</div>
                        <h3>Адаптивность</h3>
                        <p>Работает на всех устройствах</p>
                    </div>
                </div>
            </div>
            
            <div class="action-section">
                <h2>🎯 Действия</h2>
                <div class="action-buttons">
                    <button class="action-btn primary" onclick="startApp()">
                        <span>🚀 Начать</span>
                    </button>
                    <button class="action-btn secondary" onclick="showInfo()">
                        <span>ℹ️ Информация</span>
                    </button>
                    <button class="action-btn tertiary" onclick="showSettings()">
                        <span>⚙️ Настройки</span>
                    </button>
                </div>
            </div>
        </main>
        
        <footer class="app-footer">
            <p>© 2024 Простое приложение. Создано с любовью ❤️</p>
        </footer>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''

    def _generate_fallback_code(self, file_type: str) -> str:
        """Генерирует базовый код если AI недоступен"""
        
        if file_type == 'calculator_html':
            return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Калькулятор</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="calculator">
        <div class="display">
            <input type="text" id="display" readonly value="0">
        </div>
        <div class="buttons">
            <button class="btn clear" onclick="clearDisplay()">AC</button>
            <button class="btn" onclick="deleteLast()">⌫</button>
            <button class="btn" onclick="appendToDisplay('%')">%</button>
            <button class="btn operator" onclick="appendToDisplay('/')">÷</button>
            
            <button class="btn number" onclick="appendToDisplay('7')">7</button>
            <button class="btn number" onclick="appendToDisplay('8')">8</button>
            <button class="btn number" onclick="appendToDisplay('9')">9</button>
            <button class="btn operator" onclick="appendToDisplay('*')">×</button>
            
            <button class="btn number" onclick="appendToDisplay('4')">4</button>
            <button class="btn number" onclick="appendToDisplay('5')">5</button>
            <button class="btn number" onclick="appendToDisplay('6')">6</button>
            <button class="btn operator" onclick="appendToDisplay('-')">-</button>
            
            <button class="btn number" onclick="appendToDisplay('1')">1</button>
            <button class="btn number" onclick="appendToDisplay('2')">2</button>
            <button class="btn number" onclick="appendToDisplay('3')">3</button>
            <button class="btn operator" onclick="appendToDisplay('+')">+</button>
            
            <button class="btn number zero" onclick="appendToDisplay('0')">0</button>
            <button class="btn" onclick="appendToDisplay('.')">.</button>
            <button class="btn equals" onclick="calculate()">=</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>'''
        
        elif file_type == 'html':
=======
        Пользовательские требования дизайна:
        - Стиль дизайна: {', '.join(request.design_requirements)}
        - Дополнительные функции стилизации: {', '.join(project_requirements['additional_features'])}
        
        Технические требования CSS:
        - Полная адаптивность (mobile-first подход)
        - Современные CSS3 свойства (flexbox, grid, custom properties)
        - Плавные анимации и micro-interactions
        - Кроссбраузерная совместимость
        - Высокая производительность (оптимизированные селекторы)
        - Accessibility compliance (контрастность, фокус)
        - Progressive enhancement
        
        Цветовая схема и типографика:
        - Современная цветовая палитра с контрастными акцентами
        - Читаемые шрифты с правильной иерархией
        - Consistency в spacing и sizing
        
        ВАЖНО: По умолчанию показывай только главный экран (#main-screen.active), 
        остальные экраны должны быть скрыты (.screen:not(.active)).
        
        Создай детальную и качественную CSS структуру. Верни только чистый CSS код без объяснений.
        """
    
    def _create_js_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации JavaScript"""
        
        # Получаем детальные требования для конкретного типа проекта
        project_requirements = self._get_project_specific_requirements(request)
        
        mandatory_navigation_logic = """
        ОБЯЗАТЕЛЬНАЯ НАВИГАЦИОННАЯ СИСТЕМА (всегда включай):
        
        1. Функция переключения экранов:
        function showScreen(screenId) {
            // Скрыть все экраны с анимацией
            document.querySelectorAll('.screen').forEach(screen => {
                screen.classList.remove('active');
            });
            // Показать нужный экран с анимацией
            setTimeout(() => {
                document.getElementById(screenId).classList.add('active');
            }, 150);
        }
        
        2. Обработчики кнопок навигации:
        - Кнопка "Начать/Открыть" → showScreen('app-screen') + инициализация основного функционала
        - Кнопка "Настройки" → showScreen('settings-screen') + загрузка настроек
        - Кнопка "Назад" → showScreen('main-screen') + сохранение состояния
        
        3. Инициализация при загрузке:
        document.addEventListener('DOMContentLoaded', function() {
            // Показать главный экран по умолчанию
            showScreen('main-screen');
            // Настроить обработчики навигации
            setupNavigation();
            // Загрузить сохраненные данные
            loadSavedData();
        });
        
        4. Основной функционал приложения должен активироваться только после нажатия "Начать".
        """
        
        return f"""
        Создай профессиональный JavaScript для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        {mandatory_navigation_logic}
        
        {project_requirements['js_specifics']}
        
        Пользовательские функции для реализации:
        {', '.join(request.features)}
        
        Дополнительные возможности:
        {', '.join(project_requirements['additional_features'])}
        
        Технические требования JavaScript:
        - Современный ES6+ синтаксис (arrow functions, const/let, modules)
        - Event-driven архитектура
        - Обработка ошибок (try-catch блоки)
        - Валидация пользовательского ввода
        - Локальное хранение данных (localStorage/sessionStorage)
        - Адаптивное поведение и отзывчивость
        - Performance optimization (debouncing, throttling)
        - Accessibility support (keyboard navigation, ARIA)
        
        Структура кода:
        - Модульная организация (разделение на функции/классы)
        - Комментарии для сложных алгоритмов
        - Константы для магических чисел
        - Обработка различных состояний приложения
        
        ВАЖНО: НЕ запускай основной функционал сразу! Сначала пользователь должен 
        увидеть главную страницу и нажать "Начать". Весь основной код должен быть 
        инкапсулирован в функции и классы.
        
        Создай детальную и функциональную JavaScript структуру. Верни только чистый JavaScript код без объяснений.
        """
    
    def _generate_with_ai(self, prompt: str, task_type: str = 'code') -> str:
        """Генерирует код с помощью AI"""
        
        try:
            if self.default_ai == 'groq' and self.groq_api_key:
                content = self._call_groq_api_for_code(prompt, model=self.models['groq']['code'])
                if content and len(content.strip()) > 50:  # Проверяем что получили достаточно контента
                    return content
        except Exception as e:
            print(f"Ошибка AI генерации: {e}")
            pass
        
        # Fallback - простой шаблон
        if task_type == 'code':
            # Определяем тип файла по промпту
            if 'HTML' in prompt.upper() or 'INDEX.HTML' in prompt.upper():
                return self._generate_fallback_code('html')
            elif 'CSS' in prompt.upper() or 'STYLES' in prompt.upper():
                return self._generate_fallback_code('css') 
            elif 'JAVASCRIPT' in prompt.upper() or 'SCRIPT' in prompt.upper():
                return self._generate_fallback_code('js')
        
        return self._generate_fallback_code(task_type)
    
    def _generate_fallback_code(self, file_type: str) -> str:
        """Генерирует базовый код если AI недоступен"""
        
        if file_type == 'html':
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
            return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated App</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Главная страница -->
    <div id="main-screen" class="screen active">
        <div class="nav-header">
            <button class="btn-secondary" onclick="showScreen('settings-screen')">⚙️ Настройки</button>
        </div>
        <div class="main-content">
            <h1>🎉 Добро пожаловать!</h1>
            <p>Ваше приложение создано с помощью AI</p>
            <button class="btn-primary" onclick="showScreen('app-screen')">🚀 Начать</button>
        </div>
    </div>

    <!-- Экран настроек -->
    <div id="settings-screen" class="screen">
        <div class="nav-header">
            <button class="btn-secondary" onclick="showScreen('main-screen')">← Назад</button>
        </div>
        <div class="main-content">
            <h2>⚙️ Настройки</h2>
            <div class="settings-panel">
                <p>Настройки пока не реализованы</p>
            </div>
        </div>
    </div>

    <!-- Основное приложение -->
    <div id="app-screen" class="screen">
        <div class="nav-header">
            <button class="btn-secondary" onclick="showScreen('main-screen')">🏠 Главная</button>
            <button class="btn-secondary" onclick="showScreen('settings-screen')">⚙️ Настройки</button>
        </div>
        <div class="main-content">
            <div class="app-area">
                <h2>🎮 Основное приложение</h2>
                <p>Здесь будет ваш основной функционал</p>
            </div>
        </div>
    </div>

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
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
}

/* Screen System */
.screen {
    display: none;
    min-height: 100vh;
    padding: 20px;
    animation: fadeIn 0.3s ease-in-out;
}

.screen.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Navigation */
.nav-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
    padding: 15px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Content */
.main-content {
    max-width: 800px;
    margin: 0 auto;
    text-align: center;
    padding: 40px 20px;
}

.main-content h1 {
    font-size: 2.5rem;
    margin-bottom: 20px;
    color: #2c3e50;
}

.main-content h2 {
    font-size: 2rem;
    margin-bottom: 20px;
    color: #34495e;
}

/* Buttons */
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 15px 30px;
    border-radius: 25px;
    font-size: 1.2rem;
    cursor: pointer;
    margin: 10px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.btn-secondary {
    background: rgba(52, 73, 94, 0.8);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    font-size: 1rem;
    cursor: pointer;
    margin: 5px;
    transition: all 0.3s ease;
}

.btn-secondary:hover {
    background: rgba(52, 73, 94, 1);
    transform: scale(1.05);
}

/* Settings Panel */
.settings-panel {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
}

/* App Area */
.app-area {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    margin-top: 20px;
}

/* Mobile Responsive */
@media (max-width: 768px) {
    .nav-header {
        flex-direction: column;
        gap: 10px;
    }
    
    .main-content h1 {
        font-size: 2rem;
    }
    
    .btn-primary {
        padding: 12px 25px;
        font-size: 1.1rem;
    }
}'''
        else:  # JavaScript
            return '''// AI Generated JavaScript with Navigation System
document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded successfully!');
    
    // Initialize navigation system
    initializeNavigation();
    
    // Show main screen by default
    showScreen('main-screen');
});

// Navigation System
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        console.log(`Switched to ${screenId}`);
    }
}

function initializeNavigation() {
    // Add click handlers for navigation buttons
    document.addEventListener('click', function(e) {
        const button = e.target;
        
        // Handle navigation based on button text/data
        if (button.matches('.btn-primary') && button.textContent.includes('Начать')) {
            showScreen('app-screen');
        } else if (button.textContent.includes('Настройки')) {
            showScreen('settings-screen');
        } else if (button.textContent.includes('Назад') || button.textContent.includes('Главная')) {
            showScreen('main-screen');
        }
    });
}

// App functionality - only activates after user clicks "Start"
function startApp() {
    console.log('App started!');
    // Add your main app functionality here
    // This function is called when user reaches app-screen
}

// Settings functionality
function initializeSettings() {
    console.log('Settings initialized');
    // Add settings logic here
}'''
    
    def _generate_modifications(self, current_files: Dict[str, str], analysis: AnalyzedRequest) -> Dict[str, str]:
        """Генерирует модификации существующего проекта"""
        
        modified_files = current_files.copy()
<<<<<<< HEAD

        # Анализируем что нужно изменить и генерируем с AI
        try:
            if isinstance(current_files, dict):
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
            else:
                print(f"⚠️ Ошибка: current_files не является словарем: {type(current_files)}")
                return {}
        except AttributeError as e:
            print(f"⚠️ Ошибка доступа к current_files.items(): {e}")
            return {}

=======
        
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
        
>>>>>>> 7976a00e07f65908bec962e8dd4b0dc605312a62
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
    
    def generate_project_recommendations(self, project_data: Dict[str, str], project_type: ProjectType = None) -> Dict[str, Any]:
        """Генерирует рекомендации для улучшения существующего проекта"""
        
        recommendations = {
            'ui_improvements': [],
            'functionality_suggestions': [],
            'technical_enhancements': [],
            'user_experience': [],
            'performance_optimizations': [],
            'accessibility_improvements': []
        }
        
        # Анализируем код проекта
        html_content = project_data.get('index.html', '')
        css_content = project_data.get('styles.css', '')
        js_content = project_data.get('script.js', '')
        
        # UI улучшения
        if 'dark mode' not in css_content.lower() and 'theme' not in css_content.lower():
            recommendations['ui_improvements'].append({
                'title': 'Темная тема',
                'description': 'Добавить переключатель темной/светлой темы для лучшего пользовательского опыта',
                'priority': 'medium',
                'implementation': 'Добавить toggle в настройки и CSS переменные для цветов'
            })
        
        if 'loading' not in html_content.lower() and 'spinner' not in css_content.lower():
            recommendations['ui_improvements'].append({
                'title': 'Индикаторы загрузки',
                'description': 'Добавить красивые индикаторы загрузки для лучшего UX',
                'priority': 'low',
                'implementation': 'CSS анимации и JavaScript для показа/скрытия'
            })
        
        if 'animation' not in css_content.lower():
            recommendations['ui_improvements'].append({
                'title': 'Микро-анимации',
                'description': 'Добавить плавные анимации для кнопок и переходов',
                'priority': 'medium',
                'implementation': 'CSS transitions и keyframe анимации'
            })
        
        # Функциональные предложения
        if project_type == ProjectType.IDLE_GAME or project_type == ProjectType.GAME:
            if 'achievement' not in js_content.lower():
                recommendations['functionality_suggestions'].append({
                    'title': 'Система достижений',
                    'description': 'Добавить достижения за различные игровые действия',
                    'priority': 'high',
                    'implementation': 'JavaScript объект с достижениями и проверкой условий'
                })
            
            if 'leaderboard' not in js_content.lower():
                recommendations['functionality_suggestions'].append({
                    'title': 'Таблица лидеров',
                    'description': 'Локальная таблица рекордов игроков',
                    'priority': 'medium',
                    'implementation': 'localStorage для хранения и сортировки результатов'
                })
            
            if 'sound' not in js_content.lower() and 'audio' not in html_content.lower():
                recommendations['functionality_suggestions'].append({
                    'title': 'Звуковые эффекты',
                    'description': 'Добавить звуки для игровых действий',
                    'priority': 'low',
                    'implementation': 'Web Audio API или HTML5 audio элементы'
                })
        
        # Технические улучшения  
        if 'localStorage' not in js_content.lower():
            recommendations['technical_enhancements'].append({
                'title': 'Локальное сохранение',
                'description': 'Автоматическое сохранение прогресса пользователя',
                'priority': 'high',
                'implementation': 'localStorage API для сохранения состояния'
            })
        
        if 'offline' not in html_content.lower():
            recommendations['technical_enhancements'].append({
                'title': 'Офлайн поддержка',
                'description': 'Service Worker для работы без интернета',
                'priority': 'medium',
                'implementation': 'PWA технологии и кэширование ресурсов'
            })
        
        if 'viewport' not in html_content.lower() or '@media' not in css_content.lower():
            recommendations['technical_enhancements'].append({
                'title': 'Мобильная оптимизация',
                'description': 'Улучшить адаптивность для мобильных устройств',
                'priority': 'high',
                'implementation': 'Responsive design и touch-friendly элементы'
            })
        
        # Медиа и аудио улучшения
        if 'audio' not in html_content.lower() and 'sound' not in js_content.lower():
            recommendations['functionality_suggestions'].append({
                'title': 'Звуковые эффекты',
                'description': 'Добавить фоновую музыку и звуки взаимодействия',
                'priority': 'medium',
                'implementation': 'HTML5 Audio API или Web Audio API'
            })
        
        if 'video' not in html_content.lower() and project_type != ProjectType.MEDIA_PLAYER:
            recommendations['functionality_suggestions'].append({
                'title': 'Видео контент',
                'description': 'Добавить возможность просмотра/записи видео',
                'priority': 'low',
                'implementation': 'HTML5 Video API и MediaRecorder'
            })
        
        if 'three.js' not in js_content.lower() and 'webgl' not in js_content.lower():
            recommendations['functionality_suggestions'].append({
                'title': '3D элементы',
                'description': 'Добавить 3D графику для более впечатляющего интерфейса',
                'priority': 'low',
                'implementation': 'Three.js библиотека для 3D рендеринга'
            })
        
        # База данных улучшения
        if 'indexeddb' not in js_content.lower() and 'supabase' not in js_content.lower():
            recommendations['technical_enhancements'].append({
                'title': 'Улучшенное хранение данных',
                'description': 'Использовать IndexedDB или облачную БД вместо localStorage',
                'priority': 'medium',
                'implementation': 'IndexedDB для локального хранения или Supabase для облака'
            })
        
        if 'backup' not in js_content.lower():
            recommendations['technical_enhancements'].append({
                'title': 'Резервное копирование',
                'description': 'Автоматическое создание бэкапов пользовательских данных',
                'priority': 'medium',
                'implementation': 'JSON экспорт/импорт или синхронизация с облаком'
            })
        
        # UX улучшения
        if 'tooltip' not in css_content.lower():
            recommendations['user_experience'].append({
                'title': 'Подсказки',
                'description': 'Всплывающие подсказки для элементов интерфейса',
                'priority': 'medium',
                'implementation': 'CSS псевдоэлементы или JavaScript tooltips'
            })
        
        if 'shortcut' not in js_content.lower() and 'keydown' not in js_content.lower():
            recommendations['user_experience'].append({
                'title': 'Горячие клавиши',
                'description': 'Клавиатурные сочетания для основных действий',
                'priority': 'low',
                'implementation': 'Event listeners для keydown событий'
            })
        
        # Производительность
        if js_content.count('getElementById') > 10:
            recommendations['performance_optimizations'].append({
                'title': 'Кэширование DOM элементов',
                'description': 'Сохранять ссылки на часто используемые элементы',
                'priority': 'medium',
                'implementation': 'Переменные для хранения DOM references'
            })
        
        if 'requestAnimationFrame' not in js_content.lower() and ('setInterval' in js_content.lower() or 'setTimeout' in js_content.lower()):
            recommendations['performance_optimizations'].append({
                'title': 'Оптимизация анимаций',
                'description': 'Использовать requestAnimationFrame вместо setInterval',
                'priority': 'medium',
                'implementation': 'Замена timers на requestAnimationFrame'
            })
        
        # Доступность
        if 'alt=' not in html_content.lower():
            recommendations['accessibility_improvements'].append({
                'title': 'Альтернативный текст',
                'description': 'Добавить alt атрибуты для изображений',
                'priority': 'high',
                'implementation': 'alt="" для всех img элементов'
            })
        
        if 'aria-' not in html_content.lower():
            recommendations['accessibility_improvements'].append({
                'title': 'ARIA атрибуты',
                'description': 'Улучшить доступность для screen readers',
                'priority': 'medium',
                'implementation': 'aria-label, aria-describedby, role атрибуты'
            })
        
        # Подсчитываем общий приоритет
        total_recommendations = sum(len(category) for category in recommendations.values())
        high_priority_count = sum(
            1 for category in recommendations.values() 
            for rec in category if rec.get('priority') == 'high'
        )
        
        return {
            'recommendations': recommendations,
            'summary': {
                'total_suggestions': total_recommendations,
                'high_priority': high_priority_count,
                'improvement_areas': [key.replace('_', ' ').title() for key, value in recommendations.items() if value],
                'next_steps': [
                    'Выберите 1-2 улучшения с высоким приоритетом',
                    'Начните с простых UI изменений',
                    'Постепенно добавляйте более сложные функции',
                    'Тестируйте каждое изменение перед добавлением следующего'
                ]
            }
        }
    
    def get_contextual_suggestions(self, user_message: str, project_history: List[Dict] = None) -> List[str]:
        """Генерирует контекстные предложения на основе сообщения пользователя"""
        
        message_lower = user_message.lower()
        suggestions = []
        
        # Предложения на основе ключевых слов
        if any(word in message_lower for word in ['игра', 'game', 'играть']):
            suggestions.extend([
                'Создать idle-игру с прокачкой персонажа',
                'Разработать аркадную игру',
                'Сделать головоломку или квиз',
                'Создать симулятор кликера'
            ])
        
        elif any(word in message_lower for word in ['сайт', 'website', 'веб', 'лендинг']):
            suggestions.extend([
                'Создать современный лендинг',
                'Разработать корпоративный сайт',
                'Сделать портфолио',
                'Создать интернет-магазин'
            ])
        
        elif any(word in message_lower for word in ['портфолио', 'резюме', 'cv']):
            suggestions.extend([
                'Создать интерактивное портфолио',
                'Добавить галерею работ',
                'Интегрировать контактную форму',
                'Добавить скачивание резюме'
            ])
        
        elif any(word in message_lower for word in ['магазин', 'shop', 'ecommerce']):
            suggestions.extend([
                'Создать каталог товаров',
                'Добавить корзину покупок',
                'Интегрировать платежную систему',
                'Создать личный кабинет покупателя'
            ])
        
        elif any(word in message_lower for word in ['музыка', 'music', 'аудио', 'плеер']):
            suggestions.extend([
                'Создать музыкальный плеер',
                'Разработать аудиозапись с микрофона',
                'Сделать эквалайзер',
                'Создать подкаст плеер'
            ])
        
        elif any(word in message_lower for word in ['видео', 'video', 'фильм', 'ютуб']):
            suggestions.extend([
                'Создать видео плеер',
                'Разработать видеоредактор',
                'Сделать стриминг приложение',
                'Создать видеозапись с камеры'
            ])
        
        elif any(word in message_lower for word in ['3d', '3д', 'трёхмерный', 'трехмерный']):
            suggestions.extend([
                'Создать 3D просмотрщик моделей',
                'Разработать 3D игру',
                'Сделать 3D редактор',
                'Создать VR/AR приложение'
            ])
        
        elif any(word in message_lower for word in ['база', 'database', 'данные', 'бд']):
            suggestions.extend([
                'Создать CRUD приложение',
                'Разработать систему управления данными',
                'Сделать аналитику данных',
                'Создать базу знаний'
            ])
        
        elif any(word in message_lower for word in ['запись', 'recording', 'микрофон', 'камера']):
            suggestions.extend([
                'Создать приложение записи экрана',
                'Разработать диктофон',
                'Сделать видеоблог платформу',
                'Создать стриминг студию'
            ])
        
        # Общие предложения если нет специфических
        if not suggestions:
            suggestions = [
                'Создать интерактивное приложение',
                'Разработать веб-игру с 3D элементами',
                'Сделать медиа-плеер с записью',
                'Создать портфолио с базой данных',
                'Разработать музыкальное приложение',
                'Создать видео-редактор в браузере',
                'Сделать 3D просмотрщик моделей',
                'Создать приложение с AI функциями'
            ]
        
        return suggestions[:4]  # Возвращаем максимум 4 предложения