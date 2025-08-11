
import spacy
import nltk
from textblob import TextBlob
from langdetect import detect
import random
import time
import json
from datetime import datetime, timedelta
from collections import defaultdict
import re
from faker import Faker

# Инициализация библиотек
try:
    nlp = spacy.load("ru_core_news_sm")
    print("✅ spaCy модель ru_core_news_sm загружена успешно")
except (OSError, IOError):
    print("⚠️ Модель spaCy ru_core_news_sm не найдена")
    print("💡 Используем базовые функции без NLP анализа")
    print("🔧 Для установки выполните: python -m spacy download ru_core_news_sm --break-system-packages")
    nlp = None

fake = Faker('ru_RU')

class SuperSmartAI:
    def __init__(self):
        self.user_profiles = {}
        self.conversation_memory = defaultdict(list)
        self.emotional_states = ['excited', 'helpful', 'encouraging', 'confident', 'friendly']
        self.current_emotion = 'friendly'
        
        # Персонализированные приветствия
        self.greetings = {
            'morning': [
                "Доброе утро! ☀️ Отличное время для создания чего-то потрясающего!",
                "Утро - лучшее время для новых идей! 🌅 Что будем создавать?",
                "Привет! Начинаем день с создания крутого приложения? ⚡"
            ],
            'day': [
                "Привет! 👋 Готов превратить вашу идею в реальность!",
                "Добро пожаловать! 🎯 Давайте создадим что-то невероятное!",
                "Здравствуйте! 🚀 Время создавать приложения мечты!"
            ],
            'evening': [
                "Добрый вечер! 🌆 Идеальное время для творчества!",
                "Вечер - время для вдохновения! ✨ Что создаем?",
                "Привет! 🎨 Вечером всегда рождаются лучшие идеи!"
            ]
        }
        
        # Эмоциональные реакции
        self.excitement_phrases = [
            "Вау! Это звучит потрясающе! 🔥",
            "Блестящая идея! 💎",
            "Это будет хит! 🎯",
            "Обожаю такие проекты! ⚡",
            "Получится бомба! 💥"
        ]
        
        self.encouragement_phrases = [
            "Вы на правильном пути! 👍",
            "Отличное решение! ✨",
            "Так держать! 🚀",
            "Вы молодец! 🌟",
            "Продолжайте в том же духе! 💪"
        ]
        
        # Комплименты и мотивация
        self.compliments = [
            "У вас отличный вкус! 🎨",
            "Вы настоящий визионер! 👁️",
            "Чувствую предпринимательскую жилку! 💼",
            "Вы думаете как успешный разработчик! 💻",
            "Это мышление настоящего инноватора! 🚀"
        ]
        
        # Истории успеха для мотивации
        self.success_stories = [
            {
                "app": "Простая игра змейка",
                "result": "15,000 скачиваний за месяц",
                "revenue": "$2,300",
                "time": "2 недели разработки"
            },
            {
                "app": "TODO планировщик",
                "result": "B2B контракт на $50,000",
                "revenue": "$50,000",
                "time": "1 месяц"
            },
            {
                "app": "Фитнес трекер",
                "result": "Покупка крупной компанией",
                "revenue": "$150,000",
                "time": "3 месяца"
            }
        ]
        
        # Тренды и инсайты
        self.market_insights = {
            "games": {
                "trend": "📈 +127% рост за год",
                "opportunity": "Казуальные игры показывают рекордные результаты",
                "tip": "Добавьте социальные функции - это увеличивает retention на 340%!"
            },
            "productivity": {
                "trend": "📊 +89% спрос в B2B",
                "opportunity": "Компании готовы платить $100+ за пользователя в месяц",
                "tip": "Интеграция с популярными сервисами увеличивает конверсию в 5 раз!"
            },
            "health": {
                "trend": "💪 +156% рост после пандемии",
                "opportunity": "Персонализированные решения - золотая жила",
                "tip": "AI-рекомендации повышают retention до 85%!"
            }
        }

    def analyze_user_message(self, message, user_id="default"):
        """Продвинутый анализ сообщения пользователя"""
        analysis = {
            'sentiment': self.get_sentiment(message),
            'emotion': self.detect_emotion(message),
            'intent': self.classify_intent(message),
            'entities': self.extract_entities(message),
            'complexity': self.assess_complexity(message),
            'urgency': self.detect_urgency(message),
            'experience_level': self.assess_experience_level(message)
        }
        
        # Обновляем профиль пользователя
        self.update_user_profile(user_id, message, analysis)
        
        return analysis

    def get_sentiment(self, text):
        """Анализ тональности"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            if polarity > 0.3:
                return "positive"
            elif polarity < -0.3:
                return "negative"
            else:
                return "neutral"
        except:
            return "neutral"

    def detect_emotion(self, text):
        """Определение эмоции в тексте"""
        text_lower = text.lower()
        
        emotions = {
            'excited': ['круто', 'отлично', 'супер', 'потрясающе', 'вау', '!'],
            'frustrated': ['не получается', 'проблема', 'ошибка', 'не работает'],
            'curious': ['как', 'почему', 'что такое', 'расскажи', 'объясни'],
            'confident': ['знаю', 'умею', 'делал', 'опыт', 'понимаю'],
            'uncertain': ['не знаю', 'не уверен', 'возможно', 'может быть']
        }
        
        for emotion, keywords in emotions.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return 'neutral'

    def classify_intent(self, text):
        """Классификация намерений пользователя"""
        text_lower = text.lower()
        
        intents = {
            'create_game': ['игра', 'игру', 'змейка', 'тетрис', 'аркада'],
            'create_app': ['приложение', 'app', 'todo', 'планировщик'],
            'get_advice': ['совет', 'рекомендация', 'что лучше', 'помоги выбрать'],
            'learn_market': ['тренд', 'рынок', 'популярно', 'востребовано'],
            'monetization': ['заработать', 'деньги', 'доход', 'монетизация'],
            'technical_help': ['как сделать', 'проблема', 'ошибка', 'не работает']
        }
        
        for intent, keywords in intents.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        return 'general_chat'

    def extract_entities(self, text):
        """Извлечение именованных сущностей"""
        entities = {
            'technologies': [],
            'app_types': [],
            'platforms': [],
            'timeframes': []
        }
        
        # Расширенное извлечение ключевых слов
        tech_keywords = ['react', 'python', 'javascript', 'html', 'css', 'flutter', 'vue', 'angular', 'node', 'django', 'flask']
        app_keywords = ['игра', 'игру', 'приложение', 'сайт', 'платформа', 'app', 'website']
        platform_keywords = ['ios', 'android', 'web', 'мобильн', 'desktop']
        time_keywords = ['день', 'неделя', 'месяц', 'быстро', 'срочно', 'сегодня']
        
        text_lower = text.lower()
        
        # Извлекаем технологии
        for keyword in tech_keywords:
            if keyword in text_lower:
                entities['technologies'].append(keyword.title())
        
        # Извлекаем типы приложений
        for keyword in app_keywords:
            if keyword in text_lower:
                entities['app_types'].append(keyword)
        
        # Извлекаем платформы
        for keyword in platform_keywords:
            if keyword in text_lower:
                entities['platforms'].append(keyword)
                
        # Извлекаем временные рамки
        for keyword in time_keywords:
            if keyword in text_lower:
                entities['timeframes'].append(keyword)
        
        # Используем spaCy если доступен
        if nlp:
            try:
                doc = nlp(text)
                for ent in doc.ents:
                    if ent.label_ in ['ORG', 'PRODUCT']:
                        entities['technologies'].append(ent.text)
            except Exception as e:
                print(f"⚠️ Ошибка spaCy анализа: {e}")
        
        # Удаляем дубликаты
        for key in entities:
            entities[key] = list(set(entities[key]))
        
        return entities

    def assess_complexity(self, text):
        """Оценка сложности запроса"""
        complexity_indicators = {
            'simple': ['простой', 'базовый', 'начальный', 'легкий'],
            'medium': ['обычный', 'средний', 'стандартный'],
            'complex': ['сложный', 'продвинутый', 'профессиональный', 'enterprise']
        }
        
        text_lower = text.lower()
        for level, indicators in complexity_indicators.items():
            if any(ind in text_lower for ind in indicators):
                return level
        
        # По умолчанию оцениваем по длине и количеству требований
        if len(text) > 200 or text.count(',') > 3:
            return 'complex'
        elif len(text) > 50:
            return 'medium'
        else:
            return 'simple'

    def detect_urgency(self, text):
        """Определение срочности"""
        urgent_keywords = ['срочно', 'быстро', 'сегодня', 'сейчас', 'немедленно']
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in urgent_keywords):
            return 'high'
        elif any(word in text_lower for word in ['скоро', 'завтра', 'на днях']):
            return 'medium'
        else:
            return 'low'

    def assess_experience_level(self, text):
        """Оценка уровня опыта пользователя"""
        beginner_indicators = ['новичок', 'начинаю', 'не знаю', 'первый раз', 'учусь']
        expert_indicators = ['опыт', 'работал', 'знаю', 'делал', 'профессионал']
        
        text_lower = text.lower()
        
        if any(ind in text_lower for ind in expert_indicators):
            return 'expert'
        elif any(ind in text_lower for ind in beginner_indicators):
            return 'beginner'
        else:
            return 'intermediate'

    def update_user_profile(self, user_id, message, analysis):
        """Обновление профиля пользователя"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'first_interaction': datetime.now(),
                'messages_count': 0,
                'interests': [],
                'experience_level': 'beginner',
                'preferred_complexity': 'simple',
                'sentiment_history': [],
                'project_types': [],
                'time_of_day_preference': self.get_time_of_day()
            }
        
        profile = self.user_profiles[user_id]
        profile['messages_count'] += 1
        profile['sentiment_history'].append(analysis['sentiment'])
        
        # Обновляем уровень опыта
        if analysis['experience_level'] == 'expert':
            profile['experience_level'] = 'expert'
        elif analysis['experience_level'] == 'intermediate' and profile['experience_level'] == 'beginner':
            profile['experience_level'] = 'intermediate'
        
        # Запоминаем интересы
        for app_type in analysis['entities']['app_types']:
            if app_type not in profile['project_types']:
                profile['project_types'].append(app_type)

    def get_time_of_day(self):
        """Определение времени дня"""
        hour = datetime.now().hour
        if 5 <= hour < 12:
            return 'morning'
        elif 12 <= hour < 18:
            return 'day'
        else:
            return 'evening'

    def generate_personalized_response(self, message, user_id="default"):
        """Генерация персонализированного ответа"""
        analysis = self.analyze_user_message(message, user_id)
        profile = self.user_profiles.get(user_id, {})
        
        # Выбираем стиль ответа на основе анализа
        response_style = self.choose_response_style(analysis, profile)
        
        # Генерируем ответ
        if analysis['intent'] == 'create_game':
            return self.generate_game_response(analysis, profile, response_style)
        elif analysis['intent'] == 'create_app':
            return self.generate_app_response(analysis, profile, response_style)
        elif analysis['intent'] == 'get_advice':
            return self.generate_advice_response(analysis, profile, response_style)
        elif analysis['intent'] == 'learn_market':
            return self.generate_market_response(analysis, profile, response_style)
        elif analysis['intent'] == 'monetization':
            return self.generate_monetization_response(analysis, profile, response_style)
        else:
            return self.generate_general_response(analysis, profile, response_style)

    def choose_response_style(self, analysis, profile):
        """Выбор стиля ответа"""
        style = {
            'tone': 'friendly',
            'complexity': 'medium',
            'enthusiasm': 'medium',
            'personalization': 'medium'
        }
        
        # Адаптируем под эмоции
        if analysis['emotion'] == 'excited':
            style['enthusiasm'] = 'high'
            style['tone'] = 'excited'
        elif analysis['emotion'] == 'frustrated':
            style['tone'] = 'supportive'
            style['enthusiasm'] = 'low'
        
        # Адаптируем под опыт
        experience = profile.get('experience_level', 'beginner')
        if experience == 'expert':
            style['complexity'] = 'high'
        elif experience == 'beginner':
            style['complexity'] = 'simple'
        
        return style

    def generate_game_response(self, analysis, profile, style):
        """Генерация ответа для создания игр"""
        excitement = random.choice(self.excitement_phrases)
        insight = self.market_insights['games']
        compliment = random.choice(self.compliments)
        
        time_greeting = self.get_contextual_greeting(profile)
        
        response = f"{time_greeting}\n\n{excitement} {compliment}\n\n"
        
        response += f"🎮 **Игры сейчас - это золотая жила!**\n\n"
        response += f"📊 **Актуальные данные:** {insight['trend']}\n"
        response += f"💡 **Возможность:** {insight['opportunity']}\n"
        response += f"🔥 **Секрет успеха:** {insight['tip']}\n\n"
        
        # Добавляем историю успеха
        success_story = random.choice([s for s in self.success_stories if 'игра' in s['app']])
        response += f"✨ **История успеха:** Один наш клиент создал '{success_story['app']}' и получил {success_story['result']} за {success_story['time']}. Заработок: {success_story['revenue']}!\n\n"
        
        response += "🚀 **Что создаем?**\n"
        response += "• 🐍 **Змейка** - проще не бывает, а результат впечатляет!\n"
        response += "• 🧩 **Тетрис** - классика, которая никогда не устареет\n"
        response += "• 🎯 **Уникальная механика** - давайте придумаем что-то новое!\n\n"
        
        if style['enthusiasm'] == 'high':
            response += "Я уже вижу, как ваша игра становится хитом! 🌟 Начинаем?"
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "🐍 Создать змейку прямо сейчас!",
                "🧩 Сделать тетрис с твистом",
                "💡 Придумать уникальную игру",
                "📊 Показать еще статистику"
            ]
        }

    def generate_app_response(self, analysis, profile, style):
        """Генерация ответа для создания приложений"""
        encouragement = random.choice(self.encouragement_phrases)
        insight = self.market_insights['productivity']
        
        response = f"{encouragement}\n\n"
        response += f"📱 **Приложения продуктивности - это тренд будущего!**\n\n"
        response += f"📈 **Рыночные данные:** {insight['trend']}\n"
        response += f"💰 **Потенциал:** {insight['opportunity']}\n"
        response += f"🎯 **Лайфхак:** {insight['tip']}\n\n"
        
        # Персонализация под опыт
        if profile.get('experience_level') == 'expert':
            response += "💼 **Для профессионала как вы** рекомендую начать с MVP и быстро выйти на рынок!\n\n"
        else:
            response += "🎓 **Для начала** создадим красивое и функциональное приложение, которое можно сразу показывать клиентам!\n\n"
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "📝 TODO с AI-помощником",
                "📊 Трекер привычек",
                "💰 Финансовый планировщик",
                "⏱️ Тайм-менеджер"
            ]
        }

    def generate_advice_response(self, analysis, profile, style):
        """Генерация советов"""
        compliment = random.choice(self.compliments)
        
        response = f"{compliment}\n\n"
        response += "🎯 **Мой персональный совет на основе трендов 2024:**\n\n"
        
        # Адаптируем совет под профиль
        if profile.get('messages_count', 0) == 1:
            response += "🚀 **Для первого проекта** рекомендую:\n"
            response += "1. 🎮 **Простую игру** - быстрый результат и wow-эффект\n"
            response += "2. 📱 **TODO-приложение** - всегда востребовано\n"
            response += "3. 🛠️ **Утилиту** - решает конкретную проблему\n\n"
        
        response += "💡 **Секрет успеха:** Начните с простого, но идеального продукта. Лучше сделать одну функцию отлично, чем десять посредственно!\n\n"
        
        # Добавляем инсайт
        response += "📊 **Актуальная статистика:** 87% успешных приложений начинались как простые MVP, которые потом развивались на основе отзывов пользователей."
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "🎮 Начать с игры",
                "📱 Создать приложение",
                "📊 Изучить рынок подробнее",
                "💰 Узнать о монетизации"
            ]
        }

    def generate_market_response(self, analysis, profile, style):
        """Генерация ответа о рынке"""
        response = "📊 **Эксклюзивная аналитика рынка мобильных приложений:**\n\n"
        
        for category, data in self.market_insights.items():
            response += f"🔸 **{category.title()}:** {data['trend']}\n"
            response += f"   {data['opportunity']}\n\n"
        
        response += "🎯 **Моя рекомендация:** Выбирайте направление, которое вам близко. Страсть к проекту - 50% успеха!\n\n"
        
        response += "✨ **Бонус:** Наш сервис помогает создавать приложения в 10 раз быстрее обычного. Что раньше занимало месяцы, теперь делается за часы!"
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "🎮 Изучить игровой рынок",
                "📱 Узнать о продуктивности",
                "💪 Исследовать фитнес-тренды",
                "🚀 Начать создавать!"
            ]
        }

    def generate_monetization_response(self, analysis, profile, style):
        """Генерация ответа о монетизации"""
        excitement = random.choice(self.excitement_phrases)
        
        response = f"{excitement}\n\n"
        response += "💰 **Стратегии монетизации, которые реально работают:**\n\n"
        
        response += "🥇 **ТОП-3 модели:**\n"
        response += "1. 📺 **Freemium + Реклама** - 70% разработчиков выбирают это\n"
        response += "2. 💎 **Подписка** - стабильный доход, высокая прибыль\n"
        response += "3. 🛒 **Покупки в приложении** - отлично для игр\n\n"
        
        # Добавляем конкретные цифры
        response += "📈 **Реальные цифры доходности:**\n"
        response += "• Простая игра: $500-2,000/месяц\n"
        response += "• TODO-приложение: $1,000-5,000/месяц\n"
        response += "• Фитнес-трекер: $2,000-10,000/месяц\n\n"
        
        response += "🎯 **Секрет:** Комбинируйте модели! Бесплатная версия + премиум функции + небольшая реклама = максимальный доход."
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "💡 Выбрать модель для моего проекта",
                "📊 Посчитать потенциальный доход",
                "🚀 Создать MVP для тестирования",
                "📈 Изучить кейсы успеха"
            ]
        }

    def generate_general_response(self, analysis, profile, style):
        """Генерация общего ответа"""
        time_greeting = self.get_contextual_greeting(profile)
        
        response = f"{time_greeting}\n\n"
        response += "💫 **Добро пожаловать в будущее создания приложений!**\n\n"
        response += "🚀 **Что особенного в нашем сервисе:**\n"
        response += "• ⚡ Создание приложений за минуты, не месяцы\n"
        response += "• 🎨 Профессиональный дизайн автоматически\n"
        response += "• 📱 Готовность к публикации в сторах\n"
        response += "• 💰 Встроенные стратегии монетизации\n\n"
        
        if profile.get('messages_count', 0) > 3:
            response += "👋 Вижу, вы уже не первый раз здесь! Готовы создать что-то потрясающее?"
        else:
            response += "🎯 С чего начнем ваш путь к успеху?"
        
        return {
            "type": "ai_response",
            "message": response,
            "suggestions": [
                "🎮 Создать игру",
                "📱 Разработать приложение",
                "📊 Изучить тренды",
                "💰 Узнать о заработке"
            ]
        }

    def get_contextual_greeting(self, profile):
        """Получение контекстного приветствия"""
        time_of_day = self.get_time_of_day()
        greetings = self.greetings[time_of_day]
        
        # Персонализация на основе истории
        if profile.get('messages_count', 0) > 5:
            return "С возвращением! 🌟 " + random.choice(greetings)
        else:
            return random.choice(greetings)
