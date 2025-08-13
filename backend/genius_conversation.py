
import re
import json
import random
from typing import Dict, List, Any, Tuple
from datetime import datetime

class GeniusConversationAI:
    """Гениальный диалоговый AI, понимающий любые запросы на создание приложений"""
    
    def __init__(self):
        # Огромная база синонимов и вариаций
        self.app_synonyms = {
            "игры": ["игра", "game", "геймс", "играть", "gaming", "геймплей", "аркада", "симулятор"],
            "социальные": ["соцсеть", "чат", "мессенджер", "общение", "друзья", "инстаграм", "тикток", "знакомства"],
            "бизнес": ["работа", "офис", "компания", "crm", "erp", "управление", "бизнес", "продажи", "клиенты"],
            "магазин": ["торговля", "продавать", "покупать", "ecommerce", "интернет-магазин", "маркетплейс", "товары"],
            "финансы": ["деньги", "платежи", "банк", "карты", "кошелек", "криптовалюта", "инвестиции", "бюджет"],
            "здоровье": ["фитнес", "спорт", "тренировки", "диета", "медицина", "врач", "здоровье", "wellness"],
            "образование": ["учеба", "обучение", "курсы", "школа", "университет", "знания", "изучать", "учить"],
            "развлечения": ["музыка", "видео", "фильмы", "сериалы", "подкасты", "стриминг", "контент", "медиа"],
            "утилиты": ["инструмент", "помощник", "калькулятор", "погода", "заметки", "переводчик", "сканер"],
            "путешествия": ["туризм", "отпуск", "поездки", "отели", "билеты", "карты", "навигация", "гид"]
        }
        
        # Продвинутые паттерны распознавания
        self.intent_patterns = {
            "создать_приложение": [
                r"(создай|сделай|разработай|построй|запрограммируй).*(приложение|app|апп)",
                r"(хочу|нужно|требуется).*(приложение|app|апп)",
                r"(мобильное|mobile).*(приложение|app)",
                r"можешь.*(создать|сделать).*(приложение|app)"
            ],
            "улучшить_проект": [
                r"(улучши|доработай|добавь|измени).*(проект|приложение|app)",
                r"(можно|нужно).*(добавить|изменить|улучшить)",
                r"(новые|дополнительные).*(функции|возможности|фичи)"
            ],
            "получить_совет": [
                r"(посоветуй|подскажи|помоги|что лучше)",
                r"(какое|какую|какой).*(приложение|проект|идею)",
                r"(не знаю|сомневаюсь|выбрать)"
            ],
            "узнать_тренды": [
                r"(тренды|популярно|модно|актуально)",
                r"(что сейчас|сейчас популярно|в тренде)",
                r"(рынок|статистика|аналитика)"
            ]
        }
        
        # Эмоциональные реакции для более живого общения
        self.emotional_responses = {
            "восторг": [
                "🚀 ВАУ! Это потрясающая идея!",
                "🔥 Невероятно! Я в восторге от вашей задумки!",
                "✨ Гениально! Такого еще не было!",
                "💎 Это будет бриллиант среди приложений!"
            ],
            "поддержка": [
                "💪 Отлично! Мы обязательно это сделаем!",
                "🎯 Точно! Это отличное направление!",
                "👍 Супер! Я вижу огромный потенциал!",
                "⚡ Да! Это изменит все!"
            ],
            "уверенность": [
                "🏆 100% получится! Я создам что-то невероятное!",
                "🎉 Без проблем! Это будет шедевр!",
                "🌟 Конечно! Результат превзойдет ожидания!",
                "💫 Легко! Создадим что-то революционное!"
            ]
        }
        
        # Креативные предложения для вдохновения
        self.creative_suggestions = {
            "игры": [
                "🎮 AR-игра с реальными объектами",
                "🏆 Турнирная система с призами",
                "🤖 AI-соперник, который учится",
                "🌍 Глобальные онлайн-битвы",
                "💎 NFT-предметы в игре"
            ],
            "социальные": [
                "🎭 AI-аватары пользователей",
                "🎵 Музыкальные комнаты для общения",
                "📸 AR-фильтры в реальном времени",
                "🏠 Виртуальные пространства для встреч",
                "💝 Система подарков и наград"
            ],
            "бизнес": [
                "🤖 AI-помощник для продаж",
                "📊 Предсказательная аналитика",
                "🔄 Автоматизация всех процессов",
                "📱 Мобильный офис в кармане",
                "🌐 Интеграция с 100+ сервисами"
            ]
        }

    def understand_user_intent(self, message: str) -> Dict[str, Any]:
        """Понимает намерения пользователя с помощью продвинутого NLP"""
        
        message_lower = message.lower()
        
        # Определяем основное намерение
        intent = self._classify_intent(message_lower)
        
        # Извлекаем тип приложения
        app_type = self._extract_app_type(message_lower)
        
        # Определяем эмоциональную окраску
        emotion = self._detect_emotion(message_lower)
        
        # Извлекаем ключевые требования
        requirements = self._extract_requirements(message_lower)
        
        # Определяем уровень срочности
        urgency = self._detect_urgency(message_lower)
        
        # Извлекаем предпочтения по платформе
        platform_prefs = self._extract_platform_preferences(message_lower)
        
        return {
            "intent": intent,
            "app_type": app_type,
            "emotion": emotion,
            "requirements": requirements,
            "urgency": urgency,
            "platform_preferences": platform_prefs,
            "confidence": self._calculate_confidence(message, intent, app_type)
        }

    def _classify_intent(self, message: str) -> str:
        """Классифицирует намерение пользователя"""
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return intent
        
        # Если прямых паттернов нет, анализируем ключевые слова
        create_keywords = ["создай", "сделай", "хочу", "нужно", "разработай"]
        if any(word in message for word in create_keywords):
            return "создать_приложение"
        
        return "общий_вопрос"

    def _extract_app_type(self, message: str) -> str:
        """Извлекает тип приложения из сообщения"""
        
        # Подсчитываем совпадения для каждой категории
        category_scores = {}
        
        for category, synonyms in self.app_synonyms.items():
            score = sum(1 for synonym in synonyms if synonym in message)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Возвращаем категорию с наибольшим количеством совпадений
            return max(category_scores, key=category_scores.get)
        
        # Если ничего не найдено, пытаемся найти по контексту
        if any(word in message for word in ["змейка", "тетрис", "арканоид"]):
            return "игры"
        elif any(word in message for word in ["чат", "общение", "друзья"]):
            return "социальные"
        elif any(word in message for word in ["продажи", "магазин", "товары"]):
            return "магазин"
        
        return "утилиты"  # По умолчанию

    def _detect_emotion(self, message: str) -> str:
        """Определяет эмоциональную окраску сообщения"""
        
        positive_words = ["круто", "отлично", "супер", "классно", "восторге", "обожаю", "люблю"]
        excited_words = ["хочу", "срочно", "быстро", "скорее", "немедленно", "прямо сейчас"]
        uncertain_words = ["не знаю", "сомневаюсь", "может быть", "возможно", "не уверен"]
        
        if any(word in message for word in excited_words):
            return "восторг"
        elif any(word in message for word in positive_words):
            return "поддержка"
        elif any(word in message for word in uncertain_words):
            return "поддержка"  # Помогаем неуверенным пользователям
        
        return "уверенность"

    def _extract_requirements(self, message: str) -> List[str]:
        """Извлекает ключевые требования из сообщения"""
        
        requirements = []
        
        # Платформы
        if any(word in message for word in ["ios", "айфон", "iphone"]):
            requirements.append("iOS поддержка")
        if any(word in message for word in ["android", "андроид"]):
            requirements.append("Android поддержка")
        if any(word in message for word in ["веб", "web", "браузер"]):
            requirements.append("Веб-версия")
        
        # Функции
        if any(word in message for word in ["онлайн", "интернет", "облако"]):
            requirements.append("Онлайн функциональность")
        if any(word in message for word in ["офлайн", "без интернета"]):
            requirements.append("Офлайн режим")
        if any(word in message for word in ["оплата", "платежи", "деньги"]):
            requirements.append("Система платежей")
        if any(word in message for word in ["чат", "сообщения", "общение"]):
            requirements.append("Система сообщений")
        if any(word in message for word in ["карта", "геолокация", "gps"]):
            requirements.append("Геолокация")
        
        # Дизайн
        if any(word in message for word in ["красивый", "стильный", "современный"]):
            requirements.append("Современный дизайн")
        if any(word in message for word in ["темная", "dark", "черная"]):
            requirements.append("Темная тема")
        if any(word in message for word in ["минимализм", "простой", "чистый"]):
            requirements.append("Минималистичный дизайн")
        
        return requirements

    def _detect_urgency(self, message: str) -> str:
        """Определяет уровень срочности"""
        
        urgent_words = ["срочно", "быстро", "скорее", "немедленно", "прямо сейчас", "вчера нужно было"]
        normal_words = ["когда удобно", "не спешу", "качество важнее", "тщательно"]
        
        if any(word in message for word in urgent_words):
            return "высокая"
        elif any(word in message for word in normal_words):
            return "низкая"
        
        return "средняя"

    def _extract_platform_preferences(self, message: str) -> List[str]:
        """Извлекает предпочтения по платформам"""
        
        platforms = []
        
        if any(word in message for word in ["ios", "айфон", "iphone", "apple"]):
            platforms.append("iOS")
        if any(word in message for word in ["android", "андроид", "google play"]):
            platforms.append("Android")
        if any(word in message for word in ["веб", "web", "браузер", "сайт"]):
            platforms.append("Web")
        if any(word in message for word in ["все платформы", "везде", "кроссплатформ"]):
            platforms = ["iOS", "Android", "Web"]
        
        if not platforms:
            platforms = ["iOS", "Android"]  # По умолчанию
        
        return platforms

    def _calculate_confidence(self, message: str, intent: str, app_type: str) -> float:
        """Рассчитывает уверенность в распознавании"""
        
        confidence = 0.5  # Базовая уверенность
        
        # Повышаем за четкие ключевые слова
        if intent != "общий_вопрос":
            confidence += 0.2
        
        if app_type != "утилиты":  # Если определили конкретный тип
            confidence += 0.2
        
        # Повышаем за длину сообщения (больше контекста)
        if len(message.split()) > 5:
            confidence += 0.1
        
        return min(confidence, 1.0)

    def generate_intelligent_response(self, user_message: str) -> Dict[str, Any]:
        """Генерирует интеллигентный ответ на запрос пользователя"""
        
        # Анализируем намерения
        understanding = self.understand_user_intent(user_message)
        
        intent = understanding["intent"]
        app_type = understanding["app_type"]
        emotion = understanding["emotion"]
        requirements = understanding["requirements"]
        urgency = understanding["urgency"]
        
        # Выбираем эмоциональную реакцию
        emotional_start = random.choice(self.emotional_responses[emotion])
        
        # Генерируем основной ответ в зависимости от намерения
        if intent == "создать_приложение":
            response = self._generate_creation_response(
                emotional_start, app_type, requirements, urgency
            )
        elif intent == "улучшить_проект":
            response = self._generate_improvement_response(emotional_start, app_type)
        elif intent == "получить_совет":
            response = self._generate_advice_response(emotional_start, app_type)
        elif intent == "узнать_тренды":
            response = self._generate_trends_response(emotional_start)
        else:
            response = self._generate_general_response(emotional_start, app_type)
        
        return response

    def _generate_creation_response(self, emotional_start: str, app_type: str, 
                                  requirements: List[str], urgency: str) -> Dict[str, Any]:
        """Генерирует ответ для создания приложения"""
        
        urgency_text = {
            "высокая": "⚡ Понял! Делаем на максимальной скорости!",
            "средняя": "🎯 Отлично! Создадим качественное решение!",
            "низкая": "🏆 Прекрасно! Сделаем идеальный продукт!"
        }
        
        features = self.creative_suggestions.get(app_type, [
            "🤖 AI-интеграция",
            "📊 Умная аналитика", 
            "🔄 Real-time обновления",
            "📱 Кроссплатформенность"
        ])
        
        requirements_text = ""
        if requirements:
            requirements_text = f"\n\n✅ **Ваши требования:**\n" + "\n".join([f"• {req}" for req in requirements])
        
        message = f"""{emotional_start}

{urgency_text[urgency]}

🚀 **Создаю {app_type} приложение с революционными возможностями:**

{chr(10).join(features[:4])}

💎 **Что получите:**
• 📱 Полностью готовое приложение
• 🎨 Потрясающий дизайн
• 💰 Готовые схемы монетизации ($5,000-50,000/месяц)
• 🚀 Инструкции по публикации в сторах{requirements_text}

⏰ **Готово через 15 минут!**

Начинаем создание?"""

        suggestions = [
            "🚀 ДА! Создавать немедленно!",
            f"🎨 Показать дизайн-варианты для {app_type}",
            "💰 Детали монетизации",
            "📋 Список всех функций"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type,
            "understanding": {
                "intent": "создать_приложение",
                "confidence": 0.95,
                "requirements": requirements
            }
        }

    def _generate_improvement_response(self, emotional_start: str, app_type: str) -> Dict[str, Any]:
        """Генерирует ответ для улучшения проекта"""
        
        improvements = [
            "🤖 AI-помощник для пользователей",
            "📊 Продвинутая аналитика поведения",
            "🔄 Real-time уведомления",
            "💳 Интеграция платежных систем",
            "🌍 Мультиязычная поддержка",
            "📱 PWA версия для веба"
        ]
        
        message = f"""{emotional_start}

🔧 **Отлично! Прокачаем ваш проект до космического уровня!**

🚀 **Топ улучшения для {app_type} приложения:**

{chr(10).join(random.sample(improvements, 4))}

💡 **Дополнительные возможности:**
• 🎨 Обновление дизайна до современных трендов
• ⚡ Оптимизация производительности на 300%
• 🔐 Усиление безопасности с биометрией
• 📈 Интеграция аналитики для роста бизнеса

Какие улучшения добавляем?"""

        suggestions = [
            "🤖 Добавить AI-функции",
            "🎨 Обновить дизайн",
            "⚡ Ускорить приложение",
            "💰 Настроить монетизацию"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type
        }

    def _generate_advice_response(self, emotional_start: str, app_type: str) -> Dict[str, Any]:
        """Генерирует ответ-совет"""
        
        advice_by_type = {
            "игры": "🎮 Игры - это всегда хит! Особенно с уникальной механикой и социальными элементами",
            "социальные": "💬 Социальные приложения имеют огромный потенциал роста и вирусности",
            "бизнес": "💼 Бизнес-приложения - стабильный доход через подписки и B2B продажи",
            "магазин": "🛒 E-commerce - быстрорастущий рынок с отличной монетизацией",
            "финансы": "💰 Финтех - один из самых прибыльных сегментов мобильных приложений"
        }
        
        advice_text = advice_by_type.get(app_type, "✨ Любое приложение может стать успешным при правильном подходе!")
        
        message = f"""{emotional_start}

🎯 **Давайте найдем идеальное решение для вас!**

💡 **Мой совет по {app_type}:**
{advice_text}

📊 **Топ-3 трендовых направления сейчас:**
1. 🤖 **AI-интеграция** - пользователи обожают умные функции
2. 🔄 **Real-time взаимодействие** - мгновенность = engagement  
3. 🎨 **Персонализация** - уникальный опыт для каждого

🚀 **Хотите узнать конкретные идеи для вашей ниши?**"""

        suggestions = [
            f"💡 Показать идеи для {app_type}",
            "📊 Анализ трендов рынка",
            "💰 Лучшие модели монетизации",
            "🎯 Помочь выбрать нишу"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type
        }

    def _generate_trends_response(self, emotional_start: str) -> Dict[str, Any]:
        """Генерирует ответ о трендах"""
        
        trends_2024 = [
            "🤖 **AI-интеграция** - каждое приложение должно быть умным",
            "🎮 **Геймификация** - превращаем скучные задачи в игру", 
            "🔄 **Real-time функции** - все должно работать мгновенно",
            "🌍 **Суперапп концепт** - одно приложение для всех нужд",
            "🎨 **Персонализация** - уникальный опыт для каждого",
            "🔐 **Privacy-first** - безопасность превыше всего"
        ]
        
        message = f"""{emotional_start}

📈 **Вот что взрывает рынок приложений в 2024!**

🔥 **Главные тренды:**

{chr(10).join(trends_2024)}

💰 **Самые прибыльные ниши:**
• 🏥 **HealthTech** - $350 млрд рынок
• 💳 **FinTech** - $310 млрд рынок  
• 🎓 **EdTech** - $400 млрд рынок
• 🛒 **E-commerce** - $6.2 трлн рынок

🚀 **Готов создать трендовое приложение?**"""

        suggestions = [
            "🤖 Создать AI-приложение",
            "🏥 HealthTech решение", 
            "💳 FinTech приложение",
            "🎮 Геймифицированное приложение"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions
        }

    def _generate_general_response(self, emotional_start: str, app_type: str) -> Dict[str, Any]:
        """Генерирует общий ответ"""
        
        message = f"""{emotional_start}

💫 **Я готов создать для вас невероятное приложение!**

🎯 **Что умею:**
• 📱 Любые мобильные приложения (iOS/Android)
• 🌐 Веб-приложения и PWA
• 🤖 AI-интеграция в любой проект
• 🎨 Современный дизайн любой сложности
• 💰 Настройка монетизации

⚡ **Скорость создания: 15 минут!**
💵 **Потенциал дохода: до $50,000/месяц**

Расскажите, что хотите создать?"""

        suggestions = [
            "🎮 Создать игру",
            "💼 Бизнес-приложение",
            "💬 Социальную сеть",
            "💡 Показать все возможности"
        ]
        
        return {
            "type": "genius_response", 
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type
        }
