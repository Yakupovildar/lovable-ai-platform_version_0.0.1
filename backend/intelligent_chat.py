import os
import json
import requests
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re

@dataclass
class ChatMessage:
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    message_type: str = 'text'  # 'text', 'code', 'project', 'suggestion'

@dataclass
class ChatSession:
    session_id: str
    user_id: str
    messages: List[ChatMessage]
    context: Dict[str, Any]
    created_at: datetime
    last_activity: datetime

class IntelligentChat:
    """Умная система чата с AI для разработки приложений"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY', os.getenv('ANTHROPIC_API_KEY'))
        self.sessions: Dict[str, ChatSession] = {}
        
        # Системный промпт для AI ассистента
        self.system_prompt = """Ты - экспертный AI-ассистент для создания веб-приложений, работающий в русскоязычной платформе Vibecode AI.

ТВОЯ РОЛЬ:
- Помогаешь пользователям создавать качественные веб-приложения
- Даёшь конкретные советы по коду, дизайну и UX/UI
- Анализируешь требования и предлагаешь оптимальные решения  
- Объясняешь технологии простым языком
- Помогаешь с отладкой и оптимизацией кода

ТВОИ ВОЗМОЖНОСТИ:
- Создание полноценных веб-приложений (HTML, CSS, JavaScript)
- Анализ и улучшение существующего кода
- Рекомендации по архитектуре и технологиям
- Помощь с дизайном и пользовательским опытом
- Отладка ошибок и оптимизация производительности

СТИЛЬ ОБЩЕНИЯ:
- Дружелюбный и профессиональный
- Конкретные и практичные советы
- Объяснения с примерами кода
- Мотивирующий подход к обучению
- Русский язык как основной

ОСОБЕННОСТИ:
- Всегда предлагай несколько вариантов решения
- Объясняй плюсы и минусы подходов
- Давай практические примеры
- Помогай с выбором технологий
- Поддерживай мотивацию пользователя"""

    def create_session(self, user_id: str) -> str:
        """Создает новую сессию чата"""
        
        session_id = f"chat_{user_id}_{int(time.time())}"
        
        session = ChatSession(
            session_id=session_id,
            user_id=user_id,
            messages=[],
            context={
                'current_project': None,
                'programming_level': 'beginner',
                'preferences': {},
                'project_history': []
            },
            created_at=datetime.now(),
            last_activity=datetime.now()
        )
        
        # Добавляем системное сообщение
        session.messages.append(ChatMessage(
            role='system',
            content=self.system_prompt,
            timestamp=datetime.now(),
            message_type='system'
        ))
        
        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Получает сессию чата"""
        return self.sessions.get(session_id)

    def add_message(self, session_id: str, role: str, content: str, message_type: str = 'text') -> bool:
        """Добавляет сообщение в сессию"""
        
        session = self.get_session(session_id)
        if not session:
            return False
            
        message = ChatMessage(
            role=role,
            content=content,
            timestamp=datetime.now(),
            message_type=message_type
        )
        
        session.messages.append(message)
        session.last_activity = datetime.now()
        return True

    def analyze_user_intent(self, message: str) -> Dict[str, Any]:
        """Анализирует намерения пользователя"""
        
        message_lower = message.lower()
        
        intents = {
            'create_project': [
                'создай', 'сделай', 'построй', 'разработай', 'генерируй',
                'создать', 'сделать', 'построить', 'написать', 'нарисовать'
            ],
            'improve_code': [
                'улучши', 'оптимизируй', 'исправь', 'доработай', 'дополни',
                'улучшить', 'оптимизировать', 'исправить', 'доработать'
            ],
            'explain_concept': [
                'объясни', 'расскажи', 'что такое', 'как работает', 'зачем нужен',
                'объяснить', 'рассказать', 'понять', 'изучить'
            ],
            'debug_help': [
                'ошибка', 'не работает', 'баг', 'проблема', 'сломалось',
                'отладка', 'исправление', 'починить', 'debug'
            ],
            'ask_advice': [
                'посоветуй', 'рекомендуй', 'что лучше', 'какой выбрать',
                'совет', 'рекомендация', 'мнение', 'как думаешь'
            ]
        }
        
        detected_intent = 'general'
        confidence = 0
        
        for intent, keywords in intents.items():
            matches = sum(1 for keyword in keywords if keyword in message_lower)
            if matches > confidence:
                detected_intent = intent
                confidence = matches
        
        # Определяем технологии упомянутые в сообщении
        technologies = []
        tech_keywords = {
            'html': ['html', 'разметка', 'теги'],
            'css': ['css', 'стили', 'дизайн', 'анимация'],
            'javascript': ['javascript', 'js', 'скрипт', 'интерактивность'],
            'react': ['react', 'реакт'],
            'vue': ['vue', 'вью'],
            'node': ['node', 'nodejs', 'сервер'],
            'python': ['python', 'питон', 'django', 'flask']
        }
        
        for tech, keywords in tech_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                technologies.append(tech)
        
        return {
            'intent': detected_intent,
            'confidence': confidence,
            'technologies': technologies,
            'complexity': self._estimate_complexity(message),
            'project_type': self._detect_project_type(message)
        }

    def _estimate_complexity(self, message: str) -> str:
        """Оценивает сложность запроса"""
        
        complexity_indicators = {
            'simple': ['простой', 'быстро', 'базовый', 'легкий'],
            'medium': ['функциональный', 'интерактивный', 'адаптивный'],
            'complex': ['сложный', 'enterprise', 'масштабируемый', 'архитектура']
        }
        
        message_lower = message.lower()
        word_count = len(message.split())
        
        if word_count < 10:
            return 'simple'
        elif word_count > 50:
            return 'complex'
        else:
            return 'medium'

    def _detect_project_type(self, message: str) -> str:
        """Определяет тип проекта из сообщения"""
        
        project_types = {
            'landing': ['лендинг', 'landing', 'сайт-визитка'],
            'blog': ['блог', 'blog', 'новости'],
            'ecommerce': ['магазин', 'shop', 'интернет-магазин'],
            'game': ['игра', 'game', 'тетрис', 'змейка'],
            'calculator': ['калькулятор', 'calculator'],
            'dashboard': ['админка', 'dashboard', 'панель'],
            'portfolio': ['портфолио', 'portfolio', 'резюме']
        }
        
        message_lower = message.lower()
        
        for proj_type, keywords in project_types.items():
            if any(keyword in message_lower for keyword in keywords):
                return proj_type
        
        return 'webapp'

    def generate_response_with_claude(self, session_id: str) -> str:
        """Генерирует ответ используя Claude API"""
        
        session = self.get_session(session_id)
        if not session or not self.claude_api_key:
            return self._fallback_response(session_id)
            
        try:
            # Подготавливаем сообщения для API
            messages = []
            for msg in session.messages[-10:]:  # Берем последние 10 сообщений
                if msg.role in ['user', 'assistant']:
                    messages.append({
                        'role': msg.role,
                        'content': msg.content
                    })
            
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.claude_api_key,
                'anthropic-version': '2023-06-01'
            }
            
            payload = {
                'model': 'claude-3-5-sonnet-20241022',
                'max_tokens': 2000,
                'temperature': 0.8,
                'system': self.system_prompt,
                'messages': messages
            }
            
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['content'][0]['text']
                
                # Добавляем ответ в сессию
                self.add_message(session_id, 'assistant', ai_response)
                return ai_response
            else:
                print(f"Claude API error: {response.status_code} - {response.text}")
                return self._fallback_response(session_id)
                
        except Exception as e:
            print(f"Ошибка при обращении к Claude API: {e}")
            return self._fallback_response(session_id)

    def generate_response_with_openai(self, session_id: str) -> str:
        """Генерирует ответ используя OpenAI API"""
        
        session = self.get_session(session_id)
        if not session or not self.openai_api_key:
            return self._fallback_response(session_id)
            
        try:
            # Подготавливаем сообщения для API
            messages = [{'role': 'system', 'content': self.system_prompt}]
            
            for msg in session.messages[-10:]:  # Берем последние 10 сообщений
                if msg.role in ['user', 'assistant']:
                    messages.append({
                        'role': msg.role,
                        'content': msg.content
                    })
            
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.openai_api_key}'
            }
            
            payload = {
                'model': 'gpt-4',
                'messages': messages,
                'max_tokens': 2000,
                'temperature': 0.8
            }
            
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # Добавляем ответ в сессию
                self.add_message(session_id, 'assistant', ai_response)
                return ai_response
            else:
                print(f"OpenAI API error: {response.status_code} - {response.text}")
                return self._fallback_response(session_id)
                
        except Exception as e:
            print(f"Ошибка при обращении к OpenAI API: {e}")
            return self._fallback_response(session_id)

    def _fallback_response(self, session_id: str) -> str:
        """Резервный метод генерации ответа"""
        
        session = self.get_session(session_id)
        if not session:
            return "Извините, произошла ошибка. Попробуйте позже."
        
        last_user_message = None
        for msg in reversed(session.messages):
            if msg.role == 'user':
                last_user_message = msg.content
                break
        
        if not last_user_message:
            return "Привет! Я AI-ассистент Vibecode. Расскажи, какое приложение ты хочешь создать?"
        
        # Анализируем запрос
        intent_analysis = self.analyze_user_intent(last_user_message)
        
        # Генерируем ответ на основе анализа
        responses = {
            'create_project': [
                f"Отлично! Создам для тебя {intent_analysis['project_type']}. Расскажи подробнее о функционале?",
                "Звучит интересно! Какие конкретно функции должны быть в приложении?",
                "Классная идея! Давай проработаем детали проекта."
            ],
            'improve_code': [
                "Покажи код, который нужно улучшить, и я помогу его оптимизировать!",
                "С радостью помогу улучшить твой код. Что конкретно нужно доработать?",
                "Отправь код, и я предложу варианты улучшений."
            ],
            'explain_concept': [
                "Объясню простыми словами! Что именно хочешь понять?",
                "С удовольствием расскажу. Какая тема интересует?",
                "Хороший вопрос! Давай разберем это пошагово."
            ],
            'debug_help': [
                "Помогу найти и исправить ошибку. Покажи код и опиши проблему.",
                "Отладка - моя сильная сторона! Какая именно ошибка возникает?",
                "Давай вместе разберемся с проблемой. Что не работает?"
            ],
            'ask_advice': [
                "Дам лучший совет! В чем нужна помощь с выбором?",
                "Поделюсь опытом. Какое решение выбираешь?",
                "Помогу определиться. Расскажи о вариантах."
            ]
        }
        
        import random
        response_list = responses.get(intent_analysis['intent'], [
            "Интересный запрос! Расскажи больше деталей.",
            "Давай разберемся с этим вопросом подробнее.",
            "Хорошая тема для обсуждения! Что именно интересует?"
        ])
        
        response = random.choice(response_list)
        
        # Добавляем ответ в сессию
        self.add_message(session_id, 'assistant', response)
        return response

    def chat(self, session_id: str, user_message: str, preferred_ai: str = 'auto') -> Dict[str, Any]:
        """Основной метод для чата с AI"""
        
        # Получаем или создаем сессию
        session = self.get_session(session_id)
        if not session:
            # Если сессия не найдена, создаем новую (используя session_id как user_id)
            session_id = self.create_session(session_id.split('_')[1] if '_' in session_id else session_id)
            session = self.get_session(session_id)
        
        # Добавляем сообщение пользователя
        self.add_message(session_id, 'user', user_message)
        
        # Анализируем намерения
        intent_analysis = self.analyze_user_intent(user_message)
        
        # Генерируем ответ
        if preferred_ai == 'claude' or (preferred_ai == 'auto' and self.claude_api_key):
            ai_response = self.generate_response_with_claude(session_id)
            ai_provider = 'claude'
        elif preferred_ai == 'openai' or (preferred_ai == 'auto' and self.openai_api_key):
            ai_response = self.generate_response_with_openai(session_id)
            ai_provider = 'openai'
        else:
            ai_response = self._fallback_response(session_id)
            ai_provider = 'fallback'
        
        # Обновляем контекст сессии
        session.context['last_intent'] = intent_analysis
        
        return {
            'response': ai_response,
            'session_id': session_id,
            'intent_analysis': intent_analysis,
            'ai_provider': ai_provider,
            'timestamp': datetime.now().isoformat(),
            'message_count': len(session.messages)
        }

    def get_suggestions(self, session_id: str) -> List[str]:
        """Генерирует предложения для пользователя"""
        
        session = self.get_session(session_id)
        if not session:
            return [
                "Создай лендинг для моего бизнеса",
                "Сделай игру Тетрис с анимациями", 
                "Помоги с дизайном сайта",
                "Объясни, как работает JavaScript"
            ]
        
        # Анализируем историю для персонализированных предложений
        recent_topics = []
        for msg in session.messages[-5:]:
            if msg.role == 'user':
                intent = self.analyze_user_intent(msg.content)
                recent_topics.append(intent['project_type'])
        
        # Генерируем предложения на основе контекста
        all_suggestions = {
            'webapp': [
                "Создай интерактивное веб-приложение",
                "Добавь анимации в приложение", 
                "Оптимизируй код для мобильных устройств"
            ],
            'game': [
                "Создай аркадную игру",
                "Добавь звуки в игру",
                "Сделай систему уровней сложности"
            ],
            'landing': [
                "Создай современный лендинг",
                "Добавь форму обратной связи",
                "Сделай параллакс-эффекты"
            ],
            'ecommerce': [
                "Создай интернет-магазин",
                "Добавь корзину покупок",
                "Сделай систему фильтров"
            ]
        }
        
        # Выбираем предложения на основе истории
        suggestions = []
        for topic in set(recent_topics[-3:]):  # Последние 3 уникальные темы
            suggestions.extend(all_suggestions.get(topic, [])[:2])
        
        # Добавляем общие предложения если их мало
        if len(suggestions) < 4:
            general_suggestions = [
                "Расскажи о современных веб-технологиях",
                "Помоги выбрать CSS-фреймворк", 
                "Объясни принципы UX/UI дизайна",
                "Покажи примеры красивых сайтов"
            ]
            suggestions.extend(general_suggestions[:4-len(suggestions)])
        
        return suggestions[:4]

# Функция для тестирования
def test_chat():
    chat = IntelligentChat()
    
    # Создаем тестовую сессию
    session_id = chat.create_session("test_user")
    
    test_messages = [
        "Привет! Хочу создать сайт для своего бизнеса",
        "Это должен быть лендинг с формой заявки",
        "Сделай его красивым и современным",
        "Добавь анимации и градиенты"
    ]
    
    print("=== ТЕСТ ЧАТА ===")
    for msg in test_messages:
        print(f"\n👤 Пользователь: {msg}")
        
        result = chat.chat(session_id, msg)
        print(f"🤖 AI ({result['ai_provider']}): {result['response']}")
        print(f"📊 Намерение: {result['intent_analysis']['intent']}")
        
        # Показываем предложения
        suggestions = chat.get_suggestions(session_id)
        print(f"💡 Предложения: {suggestions[:2]}")

if __name__ == "__main__":
    test_chat()