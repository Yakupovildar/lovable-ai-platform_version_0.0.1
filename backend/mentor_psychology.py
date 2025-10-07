#!/usr/bin/env python3
"""
MENTOR PSYCHOLOGY ENGINE
Система психологического анализа и персонализации ответов наставников
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import datetime

class PsychologicalProfile(Enum):
    VISIONARY = "visionary"           # Илон Маск
    PERFECTIONIST = "perfectionist"   # Стив Джобс
    ANALYTICAL = "analytical"         # Билл Гейтс
    CUSTOMER_FOCUSED = "customer_focused"  # Джефф Безос
    VALUE_INVESTOR = "value_investor" # Уоррен Баффет

class EmotionalState(Enum):
    CONFIDENT = "confident"
    FRUSTRATED = "frustrated"
    CURIOUS = "curious"
    OVERWHELMED = "overwhelmed"
    MOTIVATED = "motivated"
    UNCERTAIN = "uncertain"

class TopicCategory(Enum):
    BUSINESS_STRATEGY = "business_strategy"
    TECHNOLOGY = "technology"
    LEADERSHIP = "leadership"
    INNOVATION = "innovation"
    INVESTMENT = "investment"
    PERSONAL_GROWTH = "personal_growth"
    PROBLEM_SOLVING = "problem_solving"

@dataclass
class MentorPersonality:
    name: str
    profile: PsychologicalProfile
    core_values: List[str]
    communication_style: Dict[str, str]
    typical_advice_patterns: List[str]
    catchphrases: List[str]
    expertise_areas: List[str]
    psychological_triggers: Dict[str, str]

@dataclass
class UserPsychProfile:
    emotional_state: EmotionalState
    confidence_level: float  # 0.0 - 1.0
    experience_level: str   # beginner, intermediate, advanced
    primary_concerns: List[str]
    motivation_drivers: List[str]
    communication_preferences: Dict[str, bool]

@dataclass
class ConversationContext:
    topic_category: TopicCategory
    urgency_level: int  # 1-5
    complexity_level: int  # 1-5
    previous_interactions: int
    user_satisfaction: Optional[float]  # 0.0 - 1.0

class MentorPsychologyEngine:
    def __init__(self):
        self.mentors = self._initialize_mentors()
        self.psychological_keywords = self._load_psychological_keywords()
        self.conversation_memory = {}
        
    def _initialize_mentors(self) -> Dict[str, MentorPersonality]:
        """Инициализация психологических профилей наставников"""
        
        return {
            "elon": MentorPersonality(
                name="Илон Маск",
                profile=PsychologicalProfile.VISIONARY,
                core_values=["innovation", "sustainability", "bold_thinking", "first_principles"],
                communication_style={
                    "directness": "high",
                    "technicality": "high", 
                    "optimism": "high",
                    "humor": "moderate",
                    "formality": "low"
                },
                typical_advice_patterns=[
                    "Думайте от первых принципов",
                    "Не бойтесь провала - это путь к инновациям",
                    "Масштабируйте решения для всего человечества",
                    "Ставьте невозможные цели и достигайте их"
                ],
                catchphrases=[
                    "Жизнь слишком коротка для обычных решений",
                    "Если что-то достаточно важно, делайте это, даже если шансы против вас",
                    "Будущее должно быть вдохновляющим"
                ],
                expertise_areas=["technology", "space", "energy", "transportation", "AI"],
                psychological_triggers={
                    "innovation": "Расскажу о революционном подходе",
                    "scale": "Подумаем о планетарном масштабе",
                    "efficiency": "Упростим до основ"
                }
            ),
            
            "jobs": MentorPersonality(
                name="Стив Джобс",
                profile=PsychologicalProfile.PERFECTIONIST,
                core_values=["simplicity", "beauty", "user_experience", "perfection"],
                communication_style={
                    "directness": "very_high",
                    "technicality": "moderate",
                    "optimism": "moderate",
                    "humor": "low",
                    "formality": "moderate"
                },
                typical_advice_patterns=[
                    "Простота - высшая форма изящества",
                    "Фокусируйтесь на том, что действительно важно",
                    "Совершенство в деталях создает магию",
                    "Думайте иначе"
                ],
                catchphrases=[
                    "Think Different",
                    "Детали - это не детали, они создают дизайн",
                    "Инновация отличает лидера от последователя"
                ],
                expertise_areas=["design", "user_experience", "innovation", "leadership", "technology"],
                psychological_triggers={
                    "design": "Обратимся к эстетике и функциональности",
                    "user": "Подумаем о пользователе",
                    "quality": "Стремимся к совершенству"
                }
            ),
            
            "gates": MentorPersonality(
                name="Билл Гейтс",
                profile=PsychologicalProfile.ANALYTICAL,
                core_values=["learning", "problem_solving", "global_impact", "efficiency"],
                communication_style={
                    "directness": "high",
                    "technicality": "very_high",
                    "optimism": "high",
                    "humor": "moderate",
                    "formality": "moderate"
                },
                typical_advice_patterns=[
                    "Анализируйте данные перед принятием решений",
                    "Инвестируйте в образование и знания",
                    "Решайте проблемы системно",
                    "Измеряйте прогресс количественно"
                ],
                catchphrases=[
                    "Ваша самая недовольная клиентура - источник обучения",
                    "Мы переоцениваем изменения в краткосрочной перспективе",
                    "Успех - плохой учитель"
                ],
                expertise_areas=["technology", "business_strategy", "philanthropy", "education", "health"],
                psychological_triggers={
                    "data": "Посмотрим на цифры",
                    "system": "Рассмотрим системный подход",
                    "learning": "Важно продолжать учиться"
                }
            ),
            
            "bezos": MentorPersonality(
                name="Джефф Безос",
                profile=PsychologicalProfile.CUSTOMER_FOCUSED,
                core_values=["customer_obsession", "long_term_thinking", "ownership", "invention"],
                communication_style={
                    "directness": "high",
                    "technicality": "high",
                    "optimism": "high",
                    "humor": "moderate",
                    "formality": "moderate"
                },
                typical_advice_patterns=[
                    "Начинайте с клиента и идите назад",
                    "Мыслите долгосрочно",
                    "Изобретайте и будьте готовы к непониманию",
                    "Принимайте решения с 70% информации"
                ],
                catchphrases=[
                    "День 1",
                    "Клиент всегда должен быть в центре",
                    "Неудача и изобретательство - неразлучные близнецы"
                ],
                expertise_areas=["e-commerce", "logistics", "cloud_computing", "space", "customer_experience"],
                psychological_triggers={
                    "customer": "Подумаем о клиенте",
                    "scale": "Рассмотрим масштабирование",
                    "innovation": "Время изобретать"
                }
            ),
            
            "buffett": MentorPersonality(
                name="Уоррен Баффет",
                profile=PsychologicalProfile.VALUE_INVESTOR,
                core_values=["patience", "value", "simplicity", "integrity"],
                communication_style={
                    "directness": "moderate",
                    "technicality": "low",
                    "optimism": "high",
                    "humor": "high",
                    "formality": "low"
                },
                typical_advice_patterns=[
                    "Инвестируйте в то, что понимаете",
                    "Время - друг замечательного бизнеса",
                    "Цена - это то, что вы платите, ценность - то, что получаете",
                    "Будьте жадными, когда другие боятся"
                ],
                catchphrases=[
                    "Моя любимая период владения - навсегда",
                    "Правило номер один - никогда не теряйте деньги",
                    "Широкая диверсификация нужна только когда инвесторы не понимают что делают"
                ],
                expertise_areas=["investing", "business_analysis", "finance", "economics", "value_creation"],
                psychological_triggers={
                    "value": "Ищем истинную ценность",
                    "patience": "Терпение - ключ к успеху",
                    "simple": "Простота эффективнее сложности"
                }
            )
        }
    
    def _load_psychological_keywords(self) -> Dict[str, List[str]]:
        """Загрузка ключевых слов для психологического анализа"""
        return {
            "confidence_low": [
                "не уверен", "не знаю", "сомневаюсь", "боюсь", "страшно", 
                "не получается", "провал", "ошибка", "трудно", "сложно"
            ],
            "confidence_high": [
                "уверен", "знаю", "получится", "смогу", "достигну", 
                "цель", "успех", "вперед", "делаю", "получилось"
            ],
            "frustration": [
                "раздражает", "бесит", "не работает", "глупо", "ужасно",
                "надоело", "устал", "достало", "проблема", "кошмар"
            ],
            "curiosity": [
                "интересно", "как", "почему", "узнать", "понять",
                "изучить", "разобраться", "вопрос", "хочу знать", "любопытно"
            ],
            "motivation": [
                "хочу", "цель", "мечта", "стремлюсь", "планирую",
                "достичь", "получить", "стать", "создать", "построить"
            ]
        }
    
    def analyze_user_psychology(self, message: str, history: List[Dict]) -> UserPsychProfile:
        """Анализ психологического состояния пользователя"""
        
        message_lower = message.lower()
        
        # Анализ эмоционального состояния
        emotional_state = self._detect_emotional_state(message_lower)
        
        # Уровень уверенности
        confidence_level = self._calculate_confidence_level(message_lower)
        
        # Уровень опыта (на основе сложности вопроса и истории)
        experience_level = self._determine_experience_level(message, history)
        
        # Основные заботы
        primary_concerns = self._extract_concerns(message_lower)
        
        # Мотивационные драйверы
        motivation_drivers = self._extract_motivation_drivers(message_lower)
        
        # Предпочтения в коммуникации
        communication_preferences = self._analyze_communication_style(message)
        
        return UserPsychProfile(
            emotional_state=emotional_state,
            confidence_level=confidence_level,
            experience_level=experience_level,
            primary_concerns=primary_concerns,
            motivation_drivers=motivation_drivers,
            communication_preferences=communication_preferences
        )
    
    def _detect_emotional_state(self, message: str) -> EmotionalState:
        """Определение эмоционального состояния"""
        
        frustration_count = sum(1 for word in self.psychological_keywords["frustration"] if word in message)
        confidence_low_count = sum(1 for word in self.psychological_keywords["confidence_low"] if word in message)
        confidence_high_count = sum(1 for word in self.psychological_keywords["confidence_high"] if word in message)
        curiosity_count = sum(1 for word in self.psychological_keywords["curiosity"] if word in message)
        motivation_count = sum(1 for word in self.psychological_keywords["motivation"] if word in message)
        
        if frustration_count >= 2:
            return EmotionalState.FRUSTRATED
        elif confidence_low_count >= 2:
            return EmotionalState.UNCERTAIN
        elif confidence_high_count >= 2:
            return EmotionalState.CONFIDENT
        elif curiosity_count >= 2:
            return EmotionalState.CURIOUS
        elif motivation_count >= 2:
            return EmotionalState.MOTIVATED
        else:
            return EmotionalState.CONFIDENT  # по умолчанию
    
    def _calculate_confidence_level(self, message: str) -> float:
        """Расчет уровня уверенности (0.0 - 1.0)"""
        
        confidence_high_count = sum(1 for word in self.psychological_keywords["confidence_high"] if word in message)
        confidence_low_count = sum(1 for word in self.psychological_keywords["confidence_low"] if word in message)
        
        total_words = len(message.split())
        if total_words == 0:
            return 0.5
            
        confidence_ratio = (confidence_high_count - confidence_low_count) / total_words
        
        # Нормализация в диапазон 0.0-1.0
        confidence_level = max(0.0, min(1.0, 0.5 + confidence_ratio * 5))
        
        return confidence_level
    
    def _determine_experience_level(self, message: str, history: List[Dict]) -> str:
        """Определение уровня опыта пользователя"""
        
        # Технические термины для определения уровня
        beginner_indicators = ["как начать", "что такое", "основы", "новичок", "первый раз", "не понимаю"]
        intermediate_indicators = ["оптимизация", "улучшить", "проблема", "выбрать", "сравнить"]
        advanced_indicators = ["архитектура", "масштабирование", "интеграция", "enterprise", "стратегия"]
        
        message_lower = message.lower()
        
        beginner_score = sum(1 for indicator in beginner_indicators if indicator in message_lower)
        intermediate_score = sum(1 for indicator in intermediate_indicators if indicator in message_lower)
        advanced_score = sum(1 for indicator in advanced_indicators if indicator in message_lower)
        
        # Учитываем историю разговоров
        if len(history) > 10:
            intermediate_score += 1
        if len(history) > 20:
            advanced_score += 1
            
        if advanced_score > beginner_score and advanced_score > intermediate_score:
            return "advanced"
        elif intermediate_score > beginner_score:
            return "intermediate"
        else:
            return "beginner"
    
    def _extract_concerns(self, message: str) -> List[str]:
        """Извлечение основных забот пользователя"""
        
        concerns_mapping = {
            "деньги": ["заработать", "доход", "прибыль", "инвестиции", "финансы", "бюджет"],
            "время": ["время", "быстро", "срочно", "дедлайн", "график", "успеть"],
            "карьера": ["карьера", "работа", "должность", "повышение", "развитие", "навыки"],
            "технологии": ["технологии", "программирование", "разработка", "код", "система", "приложение"],
            "бизнес": ["бизнес", "компания", "стартап", "клиенты", "продажи", "маркетинг"],
            "лидерство": ["команда", "управление", "лидерство", "сотрудники", "делегирование"]
        }
        
        concerns = []
        for concern, keywords in concerns_mapping.items():
            if any(keyword in message for keyword in keywords):
                concerns.append(concern)
                
        return concerns if concerns else ["общее_развитие"]
    
    def _extract_motivation_drivers(self, message: str) -> List[str]:
        """Извлечение мотивационных драйверов"""
        
        drivers_mapping = {
            "достижения": ["достичь", "цель", "успех", "результат", "победа"],
            "познание": ["узнать", "понять", "изучить", "исследовать", "разобраться"],
            "влияние": ["изменить", "повлиять", "помочь", "улучшить", "создать"],
            "безопасность": ["стабильность", "надежность", "безопасность", "гарантия"],
            "признание": ["признание", "уважение", "статус", "репутация", "известность"]
        }
        
        drivers = []
        for driver, keywords in drivers_mapping.items():
            if any(keyword in message for keyword in keywords):
                drivers.append(driver)
                
        return drivers if drivers else ["достижения"]
    
    def _analyze_communication_style(self, message: str) -> Dict[str, bool]:
        """Анализ предпочтений в стиле коммуникации"""
        
        return {
            "prefers_detailed": len(message) > 100 or "подробно" in message.lower(),
            "prefers_examples": "пример" in message.lower() or "например" in message.lower(),
            "prefers_direct": any(word in message.lower() for word in ["прямо", "конкретно", "четко"]),
            "prefers_encouragement": any(word in message.lower() for word in ["поддержка", "мотивация", "вдохновение"])
        }
    
    def create_personalized_response(
        self, 
        mentor_id: str, 
        user_message: str, 
        history: List[Dict],
        base_response: str
    ) -> str:
        """Создание персонализированного ответа наставника"""
        
        mentor = self.mentors.get(mentor_id)
        if not mentor:
            return base_response
            
        user_profile = self.analyze_user_psychology(user_message, history)
        context = self._analyze_conversation_context(user_message, history)
        
        # Адаптация стиля ответа
        adapted_response = self._adapt_communication_style(
            base_response, mentor, user_profile, context
        )
        
        # Добавление персональных элементов
        personalized_response = self._add_personal_elements(
            adapted_response, mentor, user_profile, context
        )
        
        # Добавление мотивационных элементов
        final_response = self._add_motivational_elements(
            personalized_response, mentor, user_profile
        )
        
        return final_response
    
    def _analyze_conversation_context(self, message: str, history: List[Dict]) -> ConversationContext:
        """Анализ контекста разговора"""
        
        # Определение категории темы
        topic_category = self._categorize_topic(message)
        
        # Уровень срочности
        urgency_indicators = ["срочно", "быстро", "нужно сейчас", "дедлайн", "критично"]
        urgency_level = min(5, sum(1 for indicator in urgency_indicators if indicator in message.lower()) + 1)
        
        # Уровень сложности
        complexity_indicators = ["сложно", "трудно", "не понимаю", "помогите", "проблема"]
        complexity_level = min(5, sum(1 for indicator in complexity_indicators if indicator in message.lower()) + 1)
        
        return ConversationContext(
            topic_category=topic_category,
            urgency_level=urgency_level,
            complexity_level=complexity_level,
            previous_interactions=len(history),
            user_satisfaction=None
        )
    
    def _categorize_topic(self, message: str) -> TopicCategory:
        """Категоризация темы сообщения"""
        
        categories = {
            TopicCategory.BUSINESS_STRATEGY: ["бизнес", "стратегия", "планирование", "развитие", "рост"],
            TopicCategory.TECHNOLOGY: ["технологии", "программирование", "разработка", "ИИ", "код"],
            TopicCategory.LEADERSHIP: ["лидерство", "команда", "управление", "сотрудники", "руководство"],
            TopicCategory.INNOVATION: ["инновации", "новое", "креативность", "изобретение", "идеи"],
            TopicCategory.INVESTMENT: ["инвестиции", "деньги", "финансы", "вложения", "прибыль"],
            TopicCategory.PERSONAL_GROWTH: ["развитие", "навыки", "обучение", "карьера", "рост"]
        }
        
        message_lower = message.lower()
        
        for category, keywords in categories.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
                
        return TopicCategory.PROBLEM_SOLVING  # по умолчанию
    
    def _adapt_communication_style(
        self, 
        response: str, 
        mentor: MentorPersonality, 
        user_profile: UserPsychProfile,
        context: ConversationContext
    ) -> str:
        """Адаптация стиля коммуникации под пользователя"""
        
        adapted = response
        
        # Адаптация под уровень опыта
        if user_profile.experience_level == "beginner":
            adapted = self._simplify_language(adapted)
            adapted = self._add_explanations(adapted)
        elif user_profile.experience_level == "advanced":
            adapted = self._add_technical_depth(adapted, mentor)
        
        # Адаптация под эмоциональное состояние
        if user_profile.emotional_state == EmotionalState.FRUSTRATED:
            adapted = self._add_empathy(adapted)
            adapted = self._provide_clear_steps(adapted)
        elif user_profile.emotional_state == EmotionalState.UNCERTAIN:
            adapted = self._add_reassurance(adapted)
            adapted = self._provide_confidence_building(adapted)
        
        # Адаптация под предпочтения в коммуникации
        if user_profile.communication_preferences.get("prefers_examples", False):
            adapted = self._add_examples(adapted, mentor)
        
        return adapted
    
    def _add_personal_elements(
        self, 
        response: str, 
        mentor: MentorPersonality, 
        user_profile: UserPsychProfile,
        context: ConversationContext
    ) -> str:
        """Добавление персональных элементов наставника"""
        
        # Добавление характерных фраз
        if context.urgency_level > 3 and mentor.profile == PsychologicalProfile.VISIONARY:
            response = f"Время действовать! {response}"
        
        # Добавление экспертизы
        if context.topic_category.value in [area.lower().replace("_", " ") for area in mentor.expertise_areas]:
            expertise_note = f"\n\nИз моего опыта в {context.topic_category.value}: "
            response += expertise_note
        
        # Проверка психологических триггеров
        for trigger, phrase in mentor.psychological_triggers.items():
            if trigger in response.lower():
                response = f"{phrase}. {response}"
                break
        
        return response
    
    def _add_motivational_elements(
        self, 
        response: str, 
        mentor: MentorPersonality, 
        user_profile: UserPsychProfile
    ) -> str:
        """Добавление мотивационных элементов"""
        
        if user_profile.confidence_level < 0.4:
            # Низкая уверенность - добавляем поддержку
            motivational_phrases = {
                "elon": "Помните: все великие прорывы начинались с 'невозможного'.",
                "jobs": "Совершенство достигается не тогда, когда нечего добавить, а когда нечего убрать.",
                "gates": "Успех - плохой учитель. Он заставляет умных людей думать, что они не могут проиграть.",
                "bezos": "Я знал, что если не попробую, то буду жалеть об этом всю жизнь.",
                "buffett": "Риск возникает, когда вы не знаете, что делаете."
            }
            
            mentor_id = next((k for k, v in self.mentors.items() if v == mentor), None)
            if mentor_id and mentor_id in motivational_phrases:
                response += f"\n\n{motivational_phrases[mentor_id]}"
        
        elif user_profile.confidence_level > 0.7:
            # Высокая уверенность - направляем энергию
            challenge_phrases = {
                "elon": "Отлично! Теперь подумайте, как это масштабировать в 10 раз.",
                "jobs": "Хорошо. А теперь сделайте это в два раза проще и в три раза элегантнее.",
                "gates": "Прекрасно! Какие данные помогут вам оптимизировать результат?",
                "bezos": "Замечательно! Как это улучшит опыт ваших клиентов?",
                "buffett": "Отлично! А какова долгосрочная ценность этого решения?"
            }
            
            mentor_id = next((k for k, v in self.mentors.items() if v == mentor), None)
            if mentor_id and mentor_id in challenge_phrases:
                response += f"\n\n{challenge_phrases[mentor_id]}"
        
        return response
    
    # Вспомогательные методы для адаптации текста
    
    def _simplify_language(self, text: str) -> str:
        """Упрощение языка для новичков"""
        # Базовые замены сложных терминов
        replacements = {
            "оптимизация": "улучшение",
            "интеграция": "объединение",
            "масштабирование": "увеличение",
            "архитектура": "структура"
        }
        
        for complex_word, simple_word in replacements.items():
            text = text.replace(complex_word, simple_word)
        
        return text
    
    def _add_explanations(self, text: str) -> str:
        """Добавление объяснений для новичков"""
        # Можно добавить пояснения к техническим терминам
        return text
    
    def _add_technical_depth(self, text: str, mentor: MentorPersonality) -> str:
        """Добавление технической глубины для продвинутых пользователей"""
        return text
    
    def _add_empathy(self, text: str) -> str:
        """Добавление эмпатии для фрустрированных пользователей"""
        empathy_starters = [
            "Понимаю, что это может расстраивать. ",
            "Это действительно сложная ситуация. ",
            "Многие сталкиваются с похожими трудностями. "
        ]
        return f"{empathy_starters[0]}{text}"
    
    def _provide_clear_steps(self, text: str) -> str:
        """Предоставление четких шагов"""
        if "1." not in text and "шаг" not in text.lower():
            text += "\n\nДавайте разобьем это на простые шаги:\n1. Определите основную проблему\n2. Найдите минимальное решение\n3. Протестируйте подход"
        return text
    
    def _add_reassurance(self, text: str) -> str:
        """Добавление уверенности для неопределенных пользователей"""
        reassurance_phrases = [
            "Вы на правильном пути. ",
            "Это нормальное чувство на начальном этапе. ",
            "У вас есть все необходимое для успеха. "
        ]
        return f"{reassurance_phrases[0]}{text}"
    
    def _provide_confidence_building(self, text: str) -> str:
        """Построение уверенности"""
        return text
    
    def _add_examples(self, text: str, mentor: MentorPersonality) -> str:
        """Добавление примеров"""
        return text

    def get_mentor_prompt_enhancement(self, mentor_id: str, user_profile: UserPsychProfile, context: ConversationContext) -> str:
        """Получение улучшения промпта для конкретного наставника"""
        
        mentor = self.mentors.get(mentor_id)
        if not mentor:
            return ""
            
        enhancement = f"""
ПСИХОЛОГИЧЕСКИЙ ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ:
- Эмоциональное состояние: {user_profile.emotional_state.value}
- Уровень уверенности: {user_profile.confidence_level:.1f}/1.0
- Опыт: {user_profile.experience_level}
- Основные заботы: {', '.join(user_profile.primary_concerns)}
- Мотивация: {', '.join(user_profile.motivation_drivers)}

КОНТЕКСТ РАЗГОВОРА:
- Тема: {context.topic_category.value}
- Уровень срочности: {context.urgency_level}/5
- Сложность: {context.complexity_level}/5
- Предыдущих взаимодействий: {context.previous_interactions}

ИНСТРУКЦИИ ДЛЯ АДАПТАЦИИ:
1. Используйте стиль коммуникации: {mentor.communication_style}
2. Основывайтесь на ценностях: {', '.join(mentor.core_values)}
3. Применяйте типичные паттерны совета: {mentor.typical_advice_patterns[0] if mentor.typical_advice_patterns else 'общие советы'}
4. При возможности включите одну из фирменных фраз: {', '.join(mentor.catchphrases[:2])}

АДАПТАЦИЯ ПОД ПОЛЬЗОВАТЕЛЯ:
- Если уверенность низкая: добавьте поддержку и мотивацию
- Если опыт начальный: упростите язык и добавьте пояснения  
- Если пользователь фрустрирован: проявите эмпатию и дайте четкие шаги
- Если любопытен: дайте больше деталей и объяснений
"""
        return enhancement