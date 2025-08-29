import os
import json
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class GeneratedFile:
    name: str
    content: str
    type: str  # 'html', 'css', 'js', 'json', 'md'

@dataclass
class ProjectResult:
    success: bool
    message: str
    files: List[GeneratedFile]
    structure: List[str]
    instructions: str
    project_type: str

class SmartAIGenerator:
    """Умный генератор кода с поддержкой различных AI API"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY', os.getenv('ANTHROPIC_API_KEY'))
        
    def analyze_project_requirements(self, description: str) -> Dict[str, Any]:
        """Анализирует описание проекта и определяет требования"""
        
        project_types = {
            'landing': ['лендинг', 'landing', 'сайт-визитка', 'одностраничник', 'промо'],
            'blog': ['блог', 'blog', 'новости', 'статьи', 'журнал', 'cms'],
            'ecommerce': ['магазин', 'shop', 'интернет-магазин', 'ecommerce', 'торговля', 'маркетплейс'],
            'portfolio': ['портфолио', 'portfolio', 'резюме', 'cv', 'галерея работ', 'творчество'],
            'dashboard': ['админка', 'dashboard', 'панель управления', 'аналитика', 'crm', 'система'],
            'game': ['игра', 'game', 'тетрис', 'змейка', 'пазл', 'аркада', 'квест', 'шутер'],
            'calculator': ['калькулятор', 'calculator', 'счётчик', 'конвертер', 'курсы валют'],
            'timer': ['таймер', 'timer', 'будильник', 'секундомер', 'помодоро', 'трекер'],
            'todo': ['todo', 'список дел', 'задачи', 'планировщик', 'органайзер', 'канбан'],
            'chat': ['чат', 'chat', 'мессенджер', 'общение', 'форум', 'комментарии'],
            'weather': ['погода', 'weather', 'прогноз', 'метео', 'климат'],
            'music': ['музыка', 'music', 'плеер', 'аудио', 'подкасты', 'радио'],
            'photo': ['фото', 'photo', 'галерея', 'изображения', 'instagram', 'фотосток'],
            'social': ['социальная сеть', 'social', 'лайки', 'посты', 'профиль', 'друзья', 'лайки и посты'],
            'education': ['обучение', 'курсы', 'education', 'школа', 'университет', 'тесты'],
            'fitness': ['фитнес', 'фитнес-тренировки', 'спорт', 'тренировки', 'здоровье', 'диета', 'калории', 'тренажерный зал'],
            'finance': ['финансы', 'бюджет', 'деньги', 'инвестиции', 'банк', 'кошелек'],
            'travel': ['путешествия', 'отели', 'билеты', 'туризм', 'карты', 'гид'],
            'food': ['еда', 'рецепты', 'ресторан', 'доставка', 'кафе', 'кулинария'],
            'booking': ['бронирование', 'запись', 'календарь', 'встречи', 'салон', 'врач'],
            'quiz': ['викторина', 'quiz', 'тест', 'опрос', 'голосование', 'квиз'],
            'streaming': ['видео', 'стриминг', 'youtube', 'трансляции', 'фильмы'],
            'crypto': ['криптовалюта', 'биткоин', 'blockchain', 'трейдинг', 'майнинг'],
            'ai': ['искусственный интеллект', 'ai', 'нейронные сети', 'чатбот', 'ml'],
            'dating': ['знакомства', 'dating', 'свидания', 'пары', 'любовь'],
            'news': ['новости', 'СМИ', 'журналистика', 'репортажи', 'события'],
            'real_estate': ['недвижимость', 'квартиры', 'аренда', 'продажа', 'риелтор'],
            'job': ['работа', 'вакансии', 'резюме', 'карьера', 'hh', 'рекрутинг']
        }
        
        description_lower = description.lower()
        detected_type = 'webapp'
        confidence = 0
        
        # Сначала ищем точные совпадения с весом
        type_scores = {}
        for proj_type, keywords in project_types.items():
            score = 0
            for keyword in keywords:
                if keyword in description_lower:
                    # Приоритет длинным ключевым словам
                    weight = len(keyword.split()) * 2 + 1
                    score += weight
            type_scores[proj_type] = score
        
        # Находим тип с максимальным весом
        if type_scores:
            best_type = max(type_scores, key=type_scores.get)
            if type_scores[best_type] > 0:
                detected_type = best_type
                confidence = type_scores[best_type]
        
        # Определяем технологии
        technologies = []
        if any(word in description_lower for word in ['react', 'vue', 'angular']):
            technologies.append('spa')
        if any(word in description_lower for word in ['bootstrap', 'tailwind']):
            technologies.append('framework')
        if any(word in description_lower for word in ['api', 'backend', 'сервер']):
            technologies.append('backend')
        
        # Определяем сложность
        complexity = 'simple'
        if len(description.split()) > 50 or 'сложн' in description_lower or 'много функций' in description_lower:
            complexity = 'complex'
        elif len(description.split()) > 20:
            complexity = 'medium'
            
        return {
            'project_type': detected_type,
            'confidence': confidence,
            'technologies': technologies,
            'complexity': complexity,
            'estimated_files': self._estimate_files(detected_type, complexity)
        }

    def _estimate_files(self, project_type: str, complexity: str) -> List[str]:
        """Оценивает необходимые файлы для проекта"""
        base_files = ['index.html', 'styles.css', 'script.js']
        
        file_structures = {
            'game': ['index.html', 'game.css', 'game.js', 'assets/sounds.js'],
            'dashboard': ['index.html', 'dashboard.css', 'dashboard.js', 'data.js', 'charts.js'],
            'ecommerce': ['index.html', 'products.html', 'cart.html', 'checkout.html', 'styles.css', 'shop.js', 'cart.js'],
            'social': ['index.html', 'profile.html', 'feed.html', 'social.css', 'social.js', 'api.js'],
            'education': ['index.html', 'courses.html', 'quiz.html', 'education.css', 'learning.js', 'progress.js'],
            'fitness': ['index.html', 'workout.html', 'tracker.html', 'fitness.css', 'fitness.js', 'health.js'],
            'finance': ['index.html', 'budget.html', 'transactions.html', 'finance.css', 'money.js', 'charts.js'],
            'travel': ['index.html', 'destinations.html', 'booking.html', 'travel.css', 'maps.js', 'booking.js'],
            'food': ['index.html', 'menu.html', 'recipes.html', 'food.css', 'recipes.js', 'nutrition.js'],
            'booking': ['index.html', 'calendar.html', 'appointments.html', 'booking.css', 'calendar.js', 'booking.js'],
            'streaming': ['index.html', 'player.html', 'playlist.html', 'video.css', 'player.js', 'streaming.js'],
            'chat': ['index.html', 'chat.html', 'rooms.html', 'chat.css', 'chat.js', 'socket.js'],
            'music': ['index.html', 'player.html', 'playlist.html', 'music.css', 'audio.js', 'player.js'],
            'weather': ['index.html', 'forecast.html', 'maps.html', 'weather.css', 'weather.js', 'api.js'],
            'crypto': ['index.html', 'portfolio.html', 'trading.html', 'crypto.css', 'trading.js', 'charts.js'],
            'ai': ['index.html', 'chat.html', 'models.html', 'ai.css', 'ai.js', 'neural.js'],
            'dating': ['index.html', 'profiles.html', 'matches.html', 'dating.css', 'matching.js', 'chat.js'],
            'news': ['index.html', 'articles.html', 'categories.html', 'news.css', 'feed.js', 'reader.js'],
            'real_estate': ['index.html', 'listings.html', 'search.html', 'realty.css', 'search.js', 'maps.js'],
            'job': ['index.html', 'jobs.html', 'resume.html', 'career.css', 'jobs.js', 'matching.js']
        }
        
        if project_type in file_structures:
            return file_structures[project_type]
        elif complexity == 'complex':
            return base_files + ['components.js', 'utils.js', 'config.js', 'api.js']
        elif complexity == 'medium':
            return base_files + ['utils.js']
        else:
            return base_files

    def generate_with_claude(self, description: str, project_analysis: Dict[str, Any]) -> ProjectResult:
        """Генерирует код используя Claude API"""
        
        if not self.claude_api_key:
            return self._fallback_generation(description, project_analysis)
            
        try:
            prompt = self._create_smart_prompt(description, project_analysis)
            
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.claude_api_key,
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                'model': 'claude-3-5-sonnet-20241022',
                'max_tokens': 4000,
                'temperature': 0.7,
                'messages': [
                    {
                        'role': 'user', 
                        'content': prompt
                    }
                ]
            }
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['content'][0]['text']
                return self._parse_ai_response(content, project_analysis)
            else:
                print(f"Claude API error: {response.status_code} - {response.text}")
                return self._fallback_generation(description, project_analysis)
                
        except Exception as e:
            print(f"Ошибка при обращении к Claude API: {e}")
            return self._fallback_generation(description, project_analysis)

    def generate_with_openai(self, description: str, project_analysis: Dict[str, Any]) -> ProjectResult:
        """Генерирует код используя OpenAI API"""
        
        if not self.openai_api_key:
            return self._fallback_generation(description, project_analysis)
            
        try:
            prompt = self._create_smart_prompt(description, project_analysis)
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.openai_api_key}'
            }
            
            payload = {
                'model': 'gpt-4',
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an expert web developer who creates high-quality, modern web applications.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': 4000,
                'temperature': 0.7
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                return self._parse_ai_response(content, project_analysis)
            else:
                print(f"OpenAI API error: {response.status_code} - {response.text}")
                return self._fallback_generation(description, project_analysis)
                
        except Exception as e:
            print(f"Ошибка при обращении к OpenAI API: {e}")
            return self._fallback_generation(description, project_analysis)

    def _create_smart_prompt(self, description: str, analysis: Dict[str, Any]) -> str:
        """Создает умный промпт для AI с учетом анализа проекта"""
        
        prompt = f"""Создай полноценное веб-приложение по следующему описанию:

ОПИСАНИЕ ПРОЕКТА: {description}

ТЕХНИЧЕСКАЯ ИНФОРМАЦИЯ:
- Тип проекта: {analysis['project_type']}
- Сложность: {analysis['complexity']}  
- Необходимые файлы: {', '.join(analysis['estimated_files'])}

ТРЕБОВАНИЯ К КОДУ:
1. Используй современные веб-технологии (HTML5, CSS3, ES6+)
2. Сделай код чистым, хорошо структурированным и комментированным
3. Добавь интерактивность и плавные анимации
4. Обеспечь полную адаптивность под все устройства
5. Используй семантичную разметку и доступность
6. Добавь обработку ошибок и валидацию
7. Сделай дизайн современным и привлекательным

ОСОБЫЕ ТРЕБОВАНИЯ для {analysis['project_type']}:
{self._get_project_specific_requirements(analysis['project_type'])}

ФОРМАТ ОТВЕТА:
Предоставь код в следующем формате:

===FILE: filename.html===
[HTML код]
===END===

===FILE: filename.css===  
[CSS код]
===END===

===FILE: filename.js===
[JavaScript код]  
===END===

===INSTRUCTIONS===
[Краткие инструкции по использованию]
===END===

Создай функциональное, красивое и интерактивное приложение с вниманием к деталям!"""

        return prompt

    def _get_project_specific_requirements(self, project_type: str) -> str:
        """Возвращает специфические требования для типа проекта"""
        
        requirements = {
            'landing': """
            - Создай привлекательный hero-раздел с призывом к действию
            - Добавь секции: О нас, Услуги, Преимущества, Контакты  
            - Используй современные градиенты и микроанимации
            - Добавь форму обратной связи с валидацией
            """,
            'game': """
            - Реализуй полноценную игровую механику
            - Добавь систему очков и уровней
            - Используй Canvas для рендеринга
            - Добавь звуковые эффекты (если возможно)
            - Сделай управление интуитивным
            """,
            'dashboard': """
            - Создай боковое меню навигации
            - Добавь интерактивные графики и чарты
            - Используй таблицы с сортировкой и фильтрацией
            - Добавь систему уведомлений
            - Сделай тёмную тему
            """,
            'ecommerce': """
            - Создай каталог товаров с фильтрами
            - Добавь корзину покупок с сохранением в localStorage
            - Реализуй поиск по товарам
            - Добавь модальные окна для деталей товара
            - Сделай адаптивную сетку товаров
            """,
            'portfolio': """
            - Создай галерею работ с модальными окнами
            - Добавь фильтры по категориям
            - Реализуй плавные переходы между секциями
            - Добавь форму контактов
            - Сделай параллакс-эффекты
            """,
            'social': """
            - Создай ленту новостей с постами
            - Добавь систему лайков и комментариев
            - Реализуй профили пользователей
            - Добавь поиск и фильтры друзей
            - Сделай чат между пользователями
            """,
            'education': """
            - Создай каталог курсов с прогрессом
            - Добавь систему тестирования и викторин
            - Реализуй трекинг обучения
            - Добавь видеоплеер для уроков
            - Сделай сертификаты достижений
            """,
            'fitness': """
            - Создай трекер тренировок и упражнений
            - Добавь календарь занятий
            - Реализуй счётчик калорий
            - Добавь графики прогресса
            - Сделай таймеры для упражнений
            """,
            'finance': """
            - Создай трекер доходов и расходов
            - Добавь категории транзакций
            - Реализуй бюджетирование
            - Добавь графики и аналитику
            - Сделай экспорт данных
            """,
            'travel': """
            - Создай поиск и бронирование отелей
            - Добавь карты и маршруты
            - Реализуй планировщик поездок
            - Добавь отзывы и рейтинги
            - Сделай конвертер валют
            """,
            'food': """
            - Создай каталог рецептов с поиском
            - Добавь планировщик меню
            - Реализуй список покупок
            - Добавь таймеры приготовления
            - Сделай калькулятор калорий
            """,
            'streaming': """
            - Создай видеоплеер с плейлистами
            - Добавь систему рекомендаций
            - Реализуй поиск контента
            - Добавь комментарии и лайки
            - Сделай адаптивное качество видео
            """,
            'chat': """
            - Создай реалтайм чат с комнатами
            - Добавь эмодзи и стикеры
            - Реализуй файловые вложения
            - Добавь уведомления
            - Сделай приватные сообщения
            """,
            'crypto': """
            - Создай портфолио криптовалют
            - Добавь графики цен в реальном времени
            - Реализуй калькулятор прибыли
            - Добавь новости рынка
            - Сделай алерты по ценам
            """,
            'ai': """
            - Создай чат-интерфейс с AI
            - Добавь разные модели ИИ
            - Реализуй генерацию контента
            - Добавь историю диалогов
            - Сделай настройки параметров
            """
        }
        
        return requirements.get(project_type, """
        - Сосредоточься на функциональности и пользовательском опыте
        - Добавь интерактивные элементы и анимации
        - Обеспечь быструю загрузку и оптимизацию
        """)

    def _parse_ai_response(self, content: str, analysis: Dict[str, Any]) -> ProjectResult:
        """Парсит ответ от AI и создает объект ProjectResult"""
        
        files = []
        instructions = ""
        
        try:
            # Извлекаем файлы
            file_pattern = r'===FILE: (.+?)===\n(.*?)\n===END==='
            file_matches = re.findall(file_pattern, content, re.DOTALL)
            
            for filename, file_content in file_matches:
                file_type = filename.split('.')[-1].lower()
                files.append(GeneratedFile(
                    name=filename.strip(),
                    content=file_content.strip(),
                    type=file_type
                ))
            
            # Извлекаем инструкции
            instructions_pattern = r'===INSTRUCTIONS===\n(.*?)\n===END==='
            instructions_match = re.search(instructions_pattern, content, re.DOTALL)
            if instructions_match:
                instructions = instructions_match.group(1).strip()
            
            # Если файлы не найдены через парсинг, пытаемся извлечь код другим способом
            if not files:
                files = self._extract_code_blocks(content, analysis)
            
            if not files:
                return self._fallback_generation("", analysis)
                
            return ProjectResult(
                success=True,
                message="Проект успешно создан с помощью AI!",
                files=files,
                structure=[f.name for f in files],
                instructions=instructions or "Откройте index.html в браузере для просмотра приложения.",
                project_type=analysis['project_type']
            )
            
        except Exception as e:
            print(f"Ошибка парсинга ответа AI: {e}")
            return self._fallback_generation("", analysis)

    def _extract_code_blocks(self, content: str, analysis: Dict[str, Any]) -> List[GeneratedFile]:
        """Извлекает блоки кода из ответа AI альтернативным способом"""
        
        files = []
        
        # Пытаемся найти блоки кода с языками
        code_patterns = [
            (r'```html\n(.*?)\n```', 'index.html', 'html'),
            (r'```css\n(.*?)\n```', 'styles.css', 'css'), 
            (r'```javascript\n(.*?)\n```', 'script.js', 'js'),
            (r'```js\n(.*?)\n```', 'script.js', 'js')
        ]
        
        for pattern, default_name, file_type in code_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            for i, match in enumerate(matches):
                filename = default_name if i == 0 else f"{file_type}{i+1}.{file_type}"
                files.append(GeneratedFile(
                    name=filename,
                    content=match.strip(),
                    type=file_type
                ))
        
        return files

    def _fallback_generation(self, description: str, analysis: Dict[str, Any]) -> ProjectResult:
        """Резервный метод генерации когда AI API недоступны"""
        
        from enhanced_ai_services import SmartAI
        
        smart_ai = SmartAI()
        result = smart_ai.generate_project_response(analysis['project_type'], description)
        
        files = []
        for filename, content in result.get('files', {}).items():
            file_type = filename.split('.')[-1].lower()
            files.append(GeneratedFile(
                name=filename,
                content=content,
                type=file_type
            ))
        
        return ProjectResult(
            success=True,
            message="Проект создан с помощью встроенного AI (резервный режим)",
            files=files,
            structure=result.get('structure', []),
            instructions=result.get('instructions', ''),
            project_type=analysis['project_type']
        )

    def generate_project(self, description: str, preferred_ai: str = 'auto') -> ProjectResult:
        """Главный метод для генерации проекта"""
        
        # Анализируем требования проекта
        analysis = self.analyze_project_requirements(description)
        
        print(f"🔍 Анализ проекта:")
        print(f"   Тип: {analysis['project_type']}")
        print(f"   Сложность: {analysis['complexity']}")
        print(f"   Файлы: {analysis['estimated_files']}")
        
        # Выбираем AI сервис
        if preferred_ai == 'claude' or (preferred_ai == 'auto' and self.claude_api_key):
            print("🧠 Генерирую с помощью Claude AI...")
            return self.generate_with_claude(description, analysis)
        elif preferred_ai == 'openai' or (preferred_ai == 'auto' and self.openai_api_key):
            print("🧠 Генерирую с помощью OpenAI GPT-4...")
            return self.generate_with_openai(description, analysis)
        else:
            print("🧠 Генерирую с помощью встроенного AI...")
            return self._fallback_generation(description, analysis)

# Функция для тестирования
def test_generator():
    generator = SmartAIGenerator()
    
    test_descriptions = [
        "Создай красивый лендинг для IT-компании с современным дизайном",
        "Сделай игру Тетрис с анимациями и звуками",
        "Нужен интернет-магазин для продажи одежды",
        "Создай портфолио для веб-дизайнера с галереей работ"
    ]
    
    for desc in test_descriptions:
        print(f"\n{'='*60}")
        print(f"Тест: {desc}")
        print('='*60)
        
        result = generator.generate_project(desc)
        print(f"Успех: {result.success}")
        print(f"Файлов: {len(result.files)}")
        print(f"Структура: {result.structure}")
        print(f"Инструкции: {result.instructions[:100]}...")

if __name__ == "__main__":
    test_generator()