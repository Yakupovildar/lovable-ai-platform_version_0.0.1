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
    MEDIA_PLAYER = "media_player"
    VIDEO_EDITOR = "video_editor"
    MUSIC_APP = "music_app"
    THREE_D_GAME = "3d_game"
    THREE_D_VIEWER = "3d_viewer"
    DATABASE_APP = "database_app"
    RECORDING_APP = "recording_app"

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
            ProjectType.GAME: ['игра', 'game', 'игру', 'тетрис', 'змейка', 'арканоид', 'clicker', 'кликер'],
            ProjectType.IDLE_GAME: ['idle', 'айдл', 'инкремент', 'clicker heroes', 'cookie clicker'],
            ProjectType.CALCULATOR: ['калькулятор', 'calculator', 'счетчик'],
            ProjectType.TODO_APP: ['todo', 'список дел', 'задачи', 'планировщик'],
            ProjectType.CHAT_APP: ['чат', 'chat', 'мессенджер'],
            ProjectType.WEATHER_APP: ['погода', 'weather', 'прогноз погоды'],
            ProjectType.MEDIA_PLAYER: ['плеер', 'player', 'музыка', 'music', 'видео', 'video', 'медиаплеер'],
            ProjectType.VIDEO_EDITOR: ['видеоредактор', 'video editor', 'монтаж', 'editing'],
            ProjectType.MUSIC_APP: ['музыкальное приложение', 'music app', 'аудио', 'audio'],
            ProjectType.THREE_D_GAME: ['3d игра', '3d game', '3д', 'трехмерный', 'трёхмерный', 'webgl'],
            ProjectType.THREE_D_VIEWER: ['3d просмотрщик', '3d viewer', '3d модели', 'three.js'],
            ProjectType.DATABASE_APP: ['база данных', 'database', 'бд', 'crud', 'данные'],
            ProjectType.RECORDING_APP: ['запись', 'recording', 'диктофон', 'recorder', 'микрофон', 'камера'],
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
    
    def _get_project_specific_requirements(self, request: AnalyzedRequest) -> Dict[str, str]:
        """Возвращает детальные требования для конкретного типа проекта"""
        
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
            
        # Добавляем общие требования качества
        for key in requirements:
            if key.endswith('_specifics'):
                requirements[key] += '''
                
                ОБЩИЕ ТРЕБОВАНИЯ КАЧЕСТВА:
                - Профессиональный код с комментариями
                - Семантическая HTML разметка
                - Современные веб-стандарты
                - Кроссбраузерная совместимость
                - Доступность (accessibility)
                - Производительность и оптимизация
                '''
        
        return requirements
    
    def _create_html_prompt(self, request: AnalyzedRequest) -> str:
        """Создает промпт для генерации HTML"""
        
        # Получаем детальные требования для конкретного типа проекта
        project_requirements = self._get_project_specific_requirements(request)
        
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
        
        return f"""
        Создай профессиональные CSS стили для {request.project_type.value if request.project_type else 'веб-приложения'}.
        
        {mandatory_css_structure}
        
        {project_requirements['css_specifics']}
        
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