
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
            "игры": ["игра", "game", "геймс", "играть", "gaming", "геймплей", "аркада", "симулятор", "idle", "rpg", "стрелялка", "платформер"],
            "социальные": ["соцсеть", "чат", "мессенджер", "общение", "друзья", "инстаграм", "тикток", "знакомства", "дейтинг", "форум"],
            "бизнес": ["работа", "офис", "компания", "crm", "erp", "управление", "бизнес", "продажи", "клиенты", "корпоративный"],
            "магазин": ["торговля", "продавать", "покупать", "ecommerce", "интернет-магазин", "маркетплейс", "товары", "онлайн-магазин"],
            "финансы": ["деньги", "платежи", "банк", "карты", "кошелек", "криптовалюта", "инвестиции", "бюджет", "финтех"],
            "здоровье": ["фитнес", "спорт", "тренировки", "диета", "медицина", "врач", "здоровье", "wellness", "медитация"],
            "образование": ["учеба", "обучение", "курсы", "школа", "университет", "знания", "изучать", "учить", "онлайн-курсы"],
            "развлечения": ["музыка", "видео", "фильмы", "сериалы", "подкасты", "стриминг", "контент", "медиа", "развлечение"],
            "утилиты": ["инструмент", "помощник", "калькулятор", "погода", "заметки", "переводчик", "сканер", "органайзер"],
            "путешествия": ["туризм", "отпуск", "поездки", "отели", "билеты", "карты", "навигация", "гид", "путешествие"]
        }
        
        # Продвинутые паттерны распознавания намерений
        self.intent_patterns = {
            "создать_приложение": [
                r"(создай|сделай|разработай|построй|запрограммируй).*(приложение|app|апп|программу)",
                r"(хочу|нужно|требуется).*(приложение|app|апп|сайт|программу)",
                r"(мобильное|mobile).*(приложение|app)",
                r"можешь.*(создать|сделать).*(приложение|app|сайт)",
                r"(нужна|нужен).*(программа|приложение|сайт)",
                r"давай.*(создадим|сделаем|разработаем)"
            ],
            "улучшить_проект": [
                r"(улучши|доработай|добавь|измени|модернизируй).*(проект|приложение|app|сайт)",
                r"(можно|нужно).*(добавить|изменить|улучшить|доработать)",
                r"(новые|дополнительные).*(функции|возможности|фичи|фишки)",
                r"(обнови|апдейт|версия).*(приложение|проект)"
            ],
            "получить_совет": [
                r"(посоветуй|подскажи|помоги|что лучше|как выбрать)",
                r"(какое|какую|какой).*(приложение|проект|идею|направление)",
                r"(не знаю|сомневаюсь|выбрать|определиться)",
                r"(что думаешь|мнение|совет)"
            ],
            "узнать_тренды": [
                r"(тренды|популярно|модно|актуально|в моде)",
                r"(что сейчас|сейчас популярно|в тренде|востребовано)",
                r"(рынок|статистика|аналитика|исследование)",
                r"(что пользуется спросом|что качают|что скачивают)"
            ],
            "монетизация": [
                r"(заработать|доход|деньги|прибыль|монетизация)",
                r"(сколько можно заработать|доходность|окупаемость)",
                r"(как зарабатывать|схемы заработка|бизнес-модель)"
            ]
        }
        
        # Эмоциональные реакции для более живого общения
        self.emotional_responses = {
            "восторг": [
                "🚀 ВАУ! Это потрясающая идея!",
                "🔥 Невероятно! Я в восторге от вашей задумки!",
                "✨ Гениально! Такого еще не было!",
                "💎 Это будет бриллиант среди приложений!",
                "⚡ Фантастика! Это взорвет рынок!",
                "🌟 Офигенно! Это будущее индустрии!"
            ],
            "поддержка": [
                "💪 Отлично! Мы обязательно это сделаем!",
                "🎯 Точно! Это отличное направление!",
                "👍 Супер! Я вижу огромный потенциал!",
                "⚡ Да! Это изменит все!",
                "🏆 Прекрасный выбор! Будет хит!",
                "💫 Замечательно! Пользователи полюбят это!"
            ],
            "уверенность": [
                "🏆 100% получится! Я создам что-то невероятное!",
                "🎉 Без проблем! Это будет шедевр!",
                "🌟 Конечно! Результат превзойдет ожидания!",
                "💫 Легко! Создадим что-то революционное!",
                "🔥 Определенно! Сделаем лучше всех конкурентов!",
                "⚡ Само собой! Это будет топовый продукт!"
            ],
            "мотивация": [
                "🚀 Вперед к успеху! Создаем будущее!",
                "💡 Гениальная идея заслуживает гениального воплощения!",
                "🎯 Цель ясна, результат будет потрясающим!",
                "💎 Из хорошей идеи сделаем бриллиант!",
                "🔥 Зажгем этот рынок нашим продуктом!"
            ]
        }
        
        # Креативные предложения для вдохновения
        self.creative_suggestions = {
            "игры": [
                "🎮 AR-игра с реальными объектами",
                "🏆 Турнирная система с призами",
                "🤖 AI-соперник, который учится",
                "🌍 Глобальные онлайн-битвы",
                "💎 NFT-предметы в игре",
                "🎭 Персонализированные аватары",
                "🔄 Процедурно генерируемые уровни",
                "🎵 Музыкальные элементы геймплея"
            ],
            "социальные": [
                "🎭 AI-аватары пользователей",
                "🎵 Музыкальные комнаты для общения",
                "📸 AR-фильтры в реальном времени",
                "🏠 Виртуальные пространства для встреч",
                "💝 Система подарков и наград",
                "🎪 Тематические сообщества",
                "📱 Истории с интерактивными элементами",
                "🌐 Глобальные чаты по интересам"
            ],
            "бизнес": [
                "🤖 AI-помощник для продаж",
                "📊 Предсказательная аналитика",
                "🔄 Автоматизация всех процессов",
                "📱 Мобильный офис в кармане",
                "🌐 Интеграция с 100+ сервисами",
                "📈 Real-time дашборды",
                "🎯 Автоматический lead scoring",
                "💬 Интеллектуальные чат-боты"
            ],
            "магазин": [
                "🛒 Персонализированные рекомендации",
                "📱 AR-примерка товаров",
                "🤖 AI-консультант покупателей",
                "📦 Умная логистика и доставка",
                "💳 One-click покупки",
                "🎁 Геймифицированная программа лояльности",
                "📊 Predictive inventory management",
                "🔄 Социальная торговля"
            ]
        }

        # База знаний о трендах и возможностях
        self.market_insights = {
            "2024_trends": [
                "🤖 AI-first приложения доминируют",
                "🔄 Real-time функциональность - стандарт",
                "🎨 Персонализация на основе поведения",
                "🌍 Суперапп подход набирает обороты", 
                "🔐 Privacy-by-design архитектура",
                "📱 Progressive Web Apps заменяют нативные",
                "🎮 Геймификация в нетрадиционных областях",
                "🌱 Sustainable tech решения"
            ],
            "revenue_models": {
                "freemium": "85% пользователей бесплатно, 5-15% платят $5-50/месяц",
                "subscription": "Средний ARPU $10-100/месяц, retention 85%+",
                "marketplace": "Комиссия 5-15%, потенциал масштабирования огромный",
                "advertising": "$1-10 CPM в зависимости от ниши",
                "premium": "Разовые покупки $1-50, высокая маржа"
            }
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
        
        # Определяем сложность
        complexity = self._detect_complexity(message_lower)
        
        # Анализ монетизационных намерений
        monetization_interest = self._detect_monetization_interest(message_lower)
        
        return {
            "intent": intent,
            "app_type": app_type,
            "emotion": emotion,
            "requirements": requirements,
            "urgency": urgency,
            "platform_preferences": platform_prefs,
            "complexity": complexity,
            "monetization_interest": monetization_interest,
            "confidence": self._calculate_confidence(message, intent, app_type),
            "raw_message": message,
            "processed_message": message_lower
        }

    def _classify_intent(self, message: str) -> str:
        """Классифицирует намерение пользователя"""
        
        # Проверяем каждый паттерн
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message):
                    return intent
        
        # Дополнительный анализ по ключевым словам
        create_keywords = ["создай", "сделай", "хочу", "нужно", "разработай", "построй"]
        if any(word in message for word in create_keywords):
            return "создать_приложение"
        
        improve_keywords = ["улучши", "добавь", "доработай", "измени", "обнови"]
        if any(word in message for word in improve_keywords):
            return "улучшить_проект"
        
        advice_keywords = ["посоветуй", "подскажи", "помоги", "что лучше"]
        if any(word in message for word in advice_keywords):
            return "получить_совет"
        
        trend_keywords = ["тренды", "популярно", "модно", "рынок", "статистика"]
        if any(word in message for word in trend_keywords):
            return "узнать_тренды"
        
        money_keywords = ["заработать", "доход", "деньги", "прибыль", "монетизация"]
        if any(word in message for word in money_keywords):
            return "монетизация"
        
        return "общий_вопрос"

    def _extract_app_type(self, message: str) -> str:
        """Извлекает тип приложения из сообщения"""
        
        # Подсчитываем совпадения для каждой категории
        category_scores = {}
        
        for category, synonyms in self.app_synonyms.items():
            score = 0
            for synonym in synonyms:
                if synonym in message:
                    # Длинные синонимы получают больший вес
                    weight = len(synonym.split("_")) if "_" in synonym else len(synonym) // 3
                    score += max(1, weight)
            
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        # Контекстный анализ для специфичных случаев
        game_indicators = ["змейка", "тетрис", "арканоид", "шутер", "rpg", "idle", "аркада"]
        if any(word in message for word in game_indicators):
            return "игры"
        
        social_indicators = ["чат", "общение", "друзья", "знакомства", "соцсеть"]
        if any(word in message for word in social_indicators):
            return "социальные"
        
        business_indicators = ["crm", "erp", "продажи", "клиенты", "сотрудники"]
        if any(word in message for word in business_indicators):
            return "бизнес"
        
        ecommerce_indicators = ["магазин", "товары", "продавать", "покупать", "корзина"]
        if any(word in message for word in ecommerce_indicators):
            return "магазин"
        
        return "утилиты"  # По умолчанию

    def _detect_emotion(self, message: str) -> str:
        """Определяет эмоциональную окраску сообщения"""
        
        # Восторженные слова
        excited_words = ["круто", "офигенно", "потрясающе", "невероятно", "фантастика", "супер"]
        if any(word in message for word in excited_words):
            return "восторг"
        
        # Срочность и энтузиазм
        urgent_excited = ["хочу", "срочно", "быстро", "скорее", "немедленно", "прямо сейчас"]
        if any(word in message for word in urgent_excited):
            return "восторг"
        
        # Позитивные слова
        positive_words = ["отлично", "классно", "хорошо", "нравится", "люблю", "обожаю"]
        if any(word in message for word in positive_words):
            return "поддержка"
        
        # Неуверенность
        uncertain_words = ["не знаю", "сомневаюсь", "может быть", "возможно", "не уверен", "думаю"]
        if any(word in message for word in uncertain_words):
            return "поддержка"  # Поддерживаем неуверенных пользователей
        
        # Мотивационные слова
        motivational_words = ["давай", "вперед", "начнем", "делаем", "создаем"]
        if any(word in message for word in motivational_words):
            return "мотивация"
        
        return "уверенность"  # По умолчанию

    def _extract_requirements(self, message: str) -> List[str]:
        """Извлекает ключевые требования из сообщения"""
        
        requirements = []
        
        # Платформы
        platform_indicators = {
            "iOS поддержка": ["ios", "айфон", "iphone", "apple", "app store"],
            "Android поддержка": ["android", "андроид", "google play", "плей маркет"],
            "Веб-версия": ["веб", "web", "браузер", "сайт", "онлайн"],
            "PWA": ["pwa", "прогрессивное приложение", "гибридное"]
        }
        
        for req, indicators in platform_indicators.items():
            if any(indicator in message for indicator in indicators):
                requirements.append(req)
        
        # Функциональные требования
        feature_indicators = {
            "Онлайн функциональность": ["онлайн", "интернет", "облако", "синхронизация", "real-time"],
            "Офлайн режим": ["офлайн", "без интернета", "автономно", "локально"],
            "Система платежей": ["оплата", "платежи", "деньги", "покупки", "подписка"],
            "Система сообщений": ["чат", "сообщения", "общение", "переписка", "уведомления"],
            "Геолокация": ["карта", "геолокация", "gps", "местоположение", "навигация"],
            "AI-интеграция": ["ai", "искусственный интеллект", "нейросеть", "машинное обучение"],
            "Социальные функции": ["друзья", "подписчики", "лайки", "комментарии", "репосты"]
        }
        
        for req, indicators in feature_indicators.items():
            if any(indicator in message for indicator in indicators):
                requirements.append(req)
        
        # Дизайн требования
        design_indicators = {
            "Современный дизайн": ["красивый", "стильный", "современный", "модный", "трендовый"],
            "Темная тема": ["темная", "dark", "черная", "ночная"],
            "Минималистичный дизайн": ["минимализм", "простой", "чистый", "лаконичный"],
            "Анимации": ["анимации", "эффекты", "переходы", "интерактивный"]
        }
        
        for req, indicators in design_indicators.items():
            if any(indicator in message for indicator in indicators):
                requirements.append(req)
        
        return requirements

    def _detect_urgency(self, message: str) -> str:
        """Определяет уровень срочности"""
        
        urgent_words = ["срочно", "быстро", "скорее", "немедленно", "прямо сейчас", "вчера нужно было", "асап"]
        if any(word in message for word in urgent_words):
            return "высокая"
        
        relaxed_words = ["когда удобно", "не спешу", "качество важнее", "тщательно", "не торопясь"]
        if any(word in message for word in relaxed_words):
            return "низкая"
        
        return "средняя"

    def _extract_platform_preferences(self, message: str) -> List[str]:
        """Извлекает предпочтения по платформам"""
        
        platforms = []
        
        platform_keywords = {
            "iOS": ["ios", "айфон", "iphone", "apple", "app store"],
            "Android": ["android", "андроид", "google play", "плей маркет"],
            "Web": ["веб", "web", "браузер", "сайт", "онлайн"],
            "Desktop": ["десктоп", "компьютер", "windows", "mac", "linux"]
        }
        
        for platform, keywords in platform_keywords.items():
            if any(keyword in message for keyword in keywords):
                platforms.append(platform)
        
        # Специальные случаи
        if any(word in message for word in ["все платформы", "везде", "кроссплатформ", "универсальное"]):
            platforms = ["iOS", "Android", "Web"]
        
        if not platforms:
            platforms = ["iOS", "Android"]  # По умолчанию мобильные платформы
        
        return platforms

    def _detect_complexity(self, message: str) -> str:
        """Определяет сложность требуемого решения"""
        
        simple_words = ["простой", "базовый", "минимальный", "легкий", "быстрый", "несложный"]
        if any(word in message for word in simple_words):
            return "простая"
        
        complex_words = ["сложный", "продвинутый", "корпоративный", "enterprise", "профессиональный", "мощный"]
        if any(word in message for word in complex_words):
            return "сложная"
        
        return "средняя"

    def _detect_monetization_interest(self, message: str) -> bool:
        """Определяет интерес к монетизации"""
        
        money_keywords = ["заработать", "доход", "деньги", "прибыль", "монетизация", "бизнес", "продавать", "подписка"]
        return any(keyword in message for keyword in money_keywords)

    def _calculate_confidence(self, original_message: str, intent: str, app_type: str) -> float:
        """Рассчитывает уверенность в распознавании"""
        
        confidence = 0.5  # Базовая уверенность
        
        # Повышаем за четкие намерения
        if intent != "общий_вопрос":
            confidence += 0.2
        
        # Повышаем за определенный тип приложения
        if app_type != "утилиты":
            confidence += 0.15
        
        # Повышаем за длину сообщения (больше контекста)
        words_count = len(original_message.split())
        if words_count > 10:
            confidence += 0.15
        elif words_count > 5:
            confidence += 0.1
        
        # Повышаем за специфические ключевые слова
        specific_keywords = ["создай", "сделай", "хочу", "нужно", "приложение", "app"]
        keyword_matches = sum(1 for word in specific_keywords if word in original_message.lower())
        confidence += min(0.2, keyword_matches * 0.05)
        
        return min(confidence, 1.0)

    def generate_intelligent_response(self, user_message: str, context: Dict = None) -> Dict[str, Any]:
        """Генерирует интеллигентный ответ на запрос пользователя"""
        
        # Анализируем намерения
        understanding = self.understand_user_intent(user_message)
        
        intent = understanding["intent"]
        app_type = understanding["app_type"]
        emotion = understanding["emotion"]
        requirements = understanding["requirements"]
        urgency = understanding["urgency"]
        complexity = understanding["complexity"]
        
        # Выбираем эмоциональную реакцию
        emotional_start = random.choice(self.emotional_responses[emotion])
        
        # Генерируем основной ответ в зависимости от намерения
        if intent == "создать_приложение":
            response = self._generate_creation_response(
                emotional_start, app_type, requirements, urgency, complexity, understanding
            )
        elif intent == "улучшить_проект":
            response = self._generate_improvement_response(emotional_start, app_type, requirements)
        elif intent == "получить_совет":
            response = self._generate_advice_response(emotional_start, app_type, understanding)
        elif intent == "узнать_тренды":
            response = self._generate_trends_response(emotional_start, app_type)
        elif intent == "монетизация":
            response = self._generate_monetization_response(emotional_start, app_type)
        else:
            response = self._generate_general_response(emotional_start, app_type, understanding)
        
        # Добавляем метаинформацию
        response["understanding"] = understanding
        response["timestamp"] = datetime.now().isoformat()
        
        return response

    def _generate_creation_response(self, emotional_start: str, app_type: str, 
                                  requirements: List[str], urgency: str, complexity: str,
                                  understanding: Dict) -> Dict[str, Any]:
        """Генерирует ответ для создания приложения"""
        
        urgency_responses = {
            "высокая": "⚡ ПОНЯЛ! Работаю на максимальной скорости!",
            "средняя": "🎯 Отлично! Создаю качественное решение!",
            "низкая": "🏆 Прекрасно! Делаем идеальный продукт!"
        }
        
        complexity_info = {
            "простая": "быстрое и элегантное решение",
            "средняя": "сбалансированное решение с расширенными возможностями",
            "сложная": "мощное enterprise-решение с полным функционалом"
        }
        
        # Получаем креативные предложения для категории
        creative_features = self.creative_suggestions.get(app_type, [
            "🤖 AI-интеграция для умных функций",
            "📊 Продвинутая аналитика пользователей",
            "🔄 Real-time синхронизация данных",
            "📱 Кроссплатформенная совместимость"
        ])
        
        # Формируем список требований
        requirements_text = ""
        if requirements:
            requirements_text = f"\n\n✅ **Ваши требования учтены:**\n" + "\n".join([f"• {req}" for req in requirements[:6]])
        
        # Рассчитываем примерные доходы
        revenue_estimate = self._get_revenue_estimate(app_type, understanding.get("monetization_interest", False))
        
        message = f"""{emotional_start}

{urgency_responses[urgency]}

🚀 **Создаю {app_type} приложение ({complexity_info[complexity]}):**

✨ **Топ-возможности которые получите:**
{chr(10).join(random.sample(creative_features, min(5, len(creative_features))))}

💎 **В проект включено:**
• 📱 Полностью готовое приложение
• 🎨 Потрясающий современный дизайн
• ⚙️ Оптимизированная архитектура для роста
• 🔌 Готовые интеграции (платежи, аналитика, push)
• 💰 Настроенная монетизация
• 📖 Полная документация по запуску{requirements_text}

💵 **Потенциальный доход: {revenue_estimate}**
⏰ **Готово через: 15 минут!**

Начинаем создание вашего цифрового шедевра?"""

        suggestions = [
            "🚀 ДА! Создавать немедленно!",
            f"🎨 Показать дизайн для {app_type}",
            "💰 Детали монетизации",
            "📋 Полный список функций"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type,
            "complexity": complexity,
            "revenue_estimate": revenue_estimate
        }

    def _generate_improvement_response(self, emotional_start: str, app_type: str, requirements: List[str]) -> Dict[str, Any]:
        """Генерирует ответ для улучшения проекта"""
        
        improvements = [
            "🤖 AI-помощник нового поколения",
            "📊 Продвинутая аналитика и инсайты",
            "🔄 Real-time уведомления и синхронизация", 
            "💳 Интеграция всех популярных платежей",
            "🌍 Поддержка 50+ языков интерфейса",
            "📱 PWA-версия для веб-браузеров",
            "🔐 Биометрическая аутентификация",
            "⚡ Оптимизация скорости работы на 300%",
            "🎨 Обновление дизайна до трендов 2024",
            "📈 Система A/B тестирования",
            "🔔 Умные push-уведомления",
            "📊 Интеграция с популярными CRM"
        ]
        
        category_specific = self.creative_suggestions.get(app_type, [])
        if category_specific:
            improvements.extend(category_specific)
        
        selected_improvements = random.sample(improvements, min(6, len(improvements)))
        
        message = f"""{emotional_start}

🔧 **ПРОКАЧИВАЕМ ВАШ ПРОЕКТ ДО КОСМИЧЕСКОГО УРОВНЯ!**

🚀 **Топ-улучшения для {app_type} приложения:**

{chr(10).join(selected_improvements)}

💡 **Дополнительные возможности:**
• 🎨 Редизайн интерфейса в соответствии с трендами
• ⚡ Техническая оптимизация и ускорение
• 🔒 Усиление безопасности данных
• 📈 Настройка аналитики для роста бизнеса

🎯 **Результат:** Увеличение engagement на 200-500%
⏰ **Время доработки:** 10-15 минут

Какие улучшения добавляем первыми?"""

        suggestions = [
            "🤖 AI-функции",
            "🎨 Обновить дизайн",
            "⚡ Ускорить приложение", 
            "💰 Настроить монетизацию"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type,
            "improvements": selected_improvements
        }

    def _get_revenue_estimate(self, app_type: str, has_monetization_interest: bool) -> str:
        """Возвращает оценку потенциального дохода"""
        
        base_estimates = {
            "игры": "$2,000-25,000",
            "социальные": "$5,000-75,000",
            "бизнес": "$10,000-150,000",
            "магазин": "$8,000-200,000",
            "финансы": "$15,000-500,000",
            "здоровье": "$6,000-80,000",
            "образование": "$4,000-60,000",
            "развлечения": "$3,000-40,000",
            "утилиты": "$2,000-30,000",
            "путешествия": "$5,000-70,000"
        }
        
        estimate = base_estimates.get(app_type, "$3,000-50,000")
        
        if has_monetization_interest:
            estimate = estimate.replace("000", "000+")
        
        return f"{estimate}/месяц"

    def _generate_advice_response(self, emotional_start: str, app_type: str, understanding: Dict) -> Dict[str, Any]:
        """Генерирует ответ-совет"""
        
        advice_by_type = {
            "игры": "🎮 Игры - это всегда хит! Особенно с уникальной механикой и социальными элементами. Средний доход топ-10%: $50,000+/месяц",
            "социальные": "💬 Социальные приложения имеют огромный потенциал роста и вирусности. TikTok и Discord показали, что нишевые соцсети могут взорвать рынок",
            "бизнес": "💼 B2B приложения - самый стабильный доход через подписки. Средний LTV клиента: $500-5,000. Меньше конкуренции, выше лояльность",
            "магазин": "🛒 E-commerce - быстрорастущий рынок $6.2 трлн. С правильной нишей можно быстро масштабироваться до $100K+/месяц",
            "финансы": "💰 FinTech - один из самых прибыльных сегментов! Строгие требования, но маржи могут достигать 80%",
            "здоровье": "🏥 HealthTech переживает бум после пандемии. Рынок $400+ млрд, высокий спрос на персонализированные решения",
            "образование": "🎓 EdTech - будущее образования. Онлайн-курсы, персональные AI-тьюторы, VR-обучение - все в тренде",
            "утилиты": "🔧 Утилиты - стабильный спрос, простая монетизация. Фокус на решении конкретной болевой точки пользователей"
        }
        
        advice_text = advice_by_type.get(app_type, "✨ Любое приложение может стать успешным при правильном подходе и исполнении!")
        
        # Персонализированные рекомендации на основе сложности
        complexity = understanding.get("complexity", "средняя")
        complexity_advice = {
            "простая": "Начните с MVP, быстро выходите на рынок, итерируйтесь на основе обратной связи",
            "средняя": "Сбалансируйте функциональность и простоту. Добавьте 2-3 уникальные фичи для выделения",
            "сложная": "Подумайте о поэтапном релизе функций. Сначала core features, затем advanced возможности"
        }
        
        message = f"""{emotional_start}

🎯 **НАЙДЕМ ИДЕАЛЬНУЮ СТРАТЕГИЮ ДЛЯ ВАШЕГО УСПЕХА!**

💡 **Мой экспертный совет по {app_type}:**
{advice_text}

🎯 **Рекомендация по сложности ({complexity}):**
{complexity_advice[complexity]}

📈 **Топ-5 трендов которые стоит учесть:**
{chr(10).join(random.sample(self.market_insights["2024_trends"], 5))}

💰 **Лучшие модели монетизации для {app_type}:**
{self._get_monetization_advice(app_type)}

🚀 **Готов создать приложение по всем этим принципам?**"""

        suggestions = [
            f"💡 Создать {app_type} с этими советами",
            "📊 Подробный анализ рынка",
            "💰 Стратегия монетизации",
            "🎯 Помочь выбрать конкретную нишу"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type,
            "advice_category": "consultation"
        }

    def _get_monetization_advice(self, app_type: str) -> str:
        """Возвращает советы по монетизации для конкретного типа приложения"""
        
        advice = {
            "игры": "Freemium + внутриигровые покупки (87% доходов мобильных игр)",
            "социальные": "Реклама + премиум подписки (модель TikTok, Instagram)",
            "бизнес": "SaaS подписки + корпоративные тарифы (highest LTV)",
            "магазин": "Комиссии с продаж + listing fees (модель Amazon)",
            "финансы": "Transaction fees + premium features (очень высокие маржи)",
            "здоровье": "Подписки + персональные консультации",
            "образование": "Курсы + сертификации + корпоративные программы",
            "утилиты": "Freemium + advanced features (простая конверсия)"
        }
        
        return advice.get(app_type, "Freemium модель - самая универсальная для старта")

    def _generate_trends_response(self, emotional_start: str, app_type: str = None) -> Dict[str, Any]:
        """Генерирует ответ о трендах"""
        
        message = f"""{emotional_start}

📈 **ЭКСКЛЮЗИВНАЯ АНАЛИТИКА ТРЕНДОВ 2024!**

🔥 **Что взрывает рынок приложений:**

{chr(10).join(self.market_insights["2024_trends"])}

💰 **Самые прибыльные ниши с цифрами:**
• 🏥 **HealthTech**: $400 млрд рынок, рост 25%/год
• 💳 **FinTech**: $310 млрд рынок, маржи до 80%
• 🎓 **EdTech**: $350 млрд к 2025, boom онлайн-обучения
• 🛒 **Social Commerce**: $1.2 трлн к 2025
• 🤖 **AI-First Apps**: $1.8 трлн рынок к 2030

📊 **Модели монетизации и их эффективность:**
• **Freemium**: {self.market_insights["revenue_models"]["freemium"]}
• **Subscription**: {self.market_insights["revenue_models"]["subscription"]}
• **Marketplace**: {self.market_insights["revenue_models"]["marketplace"]}

🚀 **Готов создать трендовое приложение в горячей нише?**"""

        suggestions = [
            "🤖 AI-приложение",
            "🏥 HealthTech решение",
            "💳 FinTech продукт",
            "🎮 Игру с AI"
        ]
        
        if app_type:
            suggestions.insert(0, f"Создать трендовое {app_type} приложение")
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "trends_data": self.market_insights["2024_trends"]
        }

    def _generate_monetization_response(self, emotional_start: str, app_type: str) -> Dict[str, Any]:
        """Генерирует ответ о монетизации"""
        
        revenue_models = self.market_insights["revenue_models"]
        app_revenue = self._get_revenue_estimate(app_type, True)
        
        message = f"""{emotional_start}

💰 **СЕКРЕТЫ МОНЕТИЗАЦИИ МОБИЛЬНЫХ ПРИЛОЖЕНИЙ!**

🎯 **Для {app_type} приложений оптимально:**
{self._get_monetization_advice(app_type)}

📊 **Детальная разбивка всех моделей:**

💎 **Freemium**: {revenue_models["freemium"]}
🔄 **Subscription**: {revenue_models["subscription"]}  
🏪 **Marketplace**: {revenue_models["marketplace"]}
📺 **Advertising**: {revenue_models["advertising"]}
💎 **Premium**: {revenue_models["premium"]}

💡 **Секретные стратегии TOP-1% приложений:**
• 🎯 Комбинирование 2-3 моделей для максимизации дохода
• 📈 A/B тестирование цен каждые 2 недели
• 🎁 Геймификация покупок (увеличивает конверсию на 47%)
• 🤖 AI-персонализация предложений
• 📱 Cross-selling между различными продуктами

💵 **Ваш потенциал с {app_type}: {app_revenue}**

🚀 **Создаем приложение с интегрированной монетизацией?**"""

        suggestions = [
            f"💰 Создать {app_type} с монетизацией",
            "📊 A/B тест стратегии",  
            "🎯 Персонализированный план",
            "💎 Премиум-фичи"
        ]
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": suggestions,
            "app_type": app_type,
            "monetization_focus": True,
            "revenue_estimate": app_revenue
        }

    def _generate_general_response(self, emotional_start: str, app_type: str, understanding: Dict) -> Dict[str, Any]:
        """Генерирует общий ответ"""
        
        capabilities = [
            "📱 Любые мобильные приложения (iOS/Android/PWA)",
            "🌐 Веб-приложения любой сложности", 
            "🤖 AI-интеграция в каждый проект",
            "🎨 Дизайн уровня топовых студий мира",
            "💰 Настройка монетизации до $1M+/месяц",
            "🚀 Готовность к публикации в App Store/Google Play"
        ]
        
        # Персонализируем ответ на основе определенного типа
        if app_type != "утилиты":
            personalization = f"На основе нашего разговора вижу, что вас интересует **{app_type}** направление - отличный выбор!"
        else:
            personalization = "Готов помочь определиться с направлением и создать идеальное решение!"

        message = f"""{emotional_start}

💫 **ДОБРО ПОЖАЛОВАТЬ В БУДУЩЕЕ СОЗДАНИЯ ПРИЛОЖЕНИЙ!**

{personalization}

✨ **Мои суперспособности:**
{chr(10).join(capabilities)}

⚡ **Уникальные преимущества:**
• 🕐 Создание за 15 минут (вместо 6+ месяцев)
• 💡 AI подбирает оптимальные решения
• 🎯 Учитываю последние тренды рынка
• 💰 Интегрирую проверенные модели заработка
• 🔥 Качество уровня $100K+ проектов

🚀 **Готов создать что-то невероятное вместе?**
Расскажите подробнее о своей идее!"""

        base_suggestions = [
            "🎮 Создать игру",
            "💼 Бизнес-приложение", 
            "💬 Социальную сеть",
            "💡 Показать все возможности"
        ]
        
        # Персонализируем предложения
        if app_type != "утилиты":
            base_suggestions[0] = f"🚀 Создать {app_type} приложение"
        
        return {
            "type": "genius_response",
            "message": message,
            "suggestions": base_suggestions,
            "app_type": app_type,
            "personalized": app_type != "утилиты"
        }
