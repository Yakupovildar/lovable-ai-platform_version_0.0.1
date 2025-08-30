#!/usr/bin/env python3
"""
Диалоговая AI система для интерактивной разработки проектов
Конкурирует с Lovable.dev chat interface
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from intelligent_chat import IntelligentChat

@dataclass
class ChatMessage:
    """Сообщение в чате"""
    id: str
    role: str  # 'user', 'assistant', 'system'
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = None

@dataclass 
class ProjectContext:
    """Контекст проекта для AI"""
    project_id: str
    name: str
    description: str
    project_type: str
    framework: str
    files: Dict[str, str]
    database_schema: Dict[str, Any]
    deployment_info: Dict[str, Any]
    history: List[Dict[str, Any]]

class ProjectAIChatBot:
    """AI бот для интерактивной разработки проектов"""
    
    def __init__(self):
        # Используем только бесплатные AI сервисы (GigaChat, Yandex GPT)
        self.intelligent_chat = IntelligentChat()
        self.active_sessions = {}  # session_id -> conversation
        
        # Системный промпт для проектного AI
        self.system_prompt = """
Ты - экспертный AI Full-Stack разработчик, аналог Lovable.dev.
Ты помогаешь создавать и дорабатывать реальные React/Next.js приложения.

ВОЗМОЖНОСТИ:
- Создание компонентов и страниц
- Модификация существующего кода
- Добавление новых функций
- Исправление ошибок
- Настройка базы данных Supabase
- Интеграция с API
- Стилизация с Tailwind CSS
- Mobile-responsive дизайн

СТИЛЬ ОБЩЕНИЯ:
- Конкретные технические решения
- Пошаговые инструкции
- Код с объяснениями
- Предложения улучшений
- Вопросы для уточнения требований

ПОМНИ: Ты работаешь с реальными проектами, которые будут развернуты и использованы.
"""

    def create_chat_session(self, project_context: ProjectContext) -> str:
        """Создает новую сессию чата для проекта"""
        session_id = f"chat_{uuid.uuid4().hex[:12]}"
        
        self.active_sessions[session_id] = {
            'project_context': project_context,
            'messages': [
                ChatMessage(
                    id=str(uuid.uuid4()),
                    role='system',
                    content=self.system_prompt,
                    timestamp=datetime.now()
                ),
                ChatMessage(
                    id=str(uuid.uuid4()),
                    role='assistant', 
                    content=f"""🚀 Привет! Я AI разработчик для проекта "{project_context.name}".

📋 **Что я знаю о проекте:**
- Тип: {project_context.project_type}
- Фреймворк: {project_context.framework}
- Файлов: {len(project_context.files)}
- База данных: {'Настроена' if project_context.database_schema else 'Не настроена'}

💬 **Что я могу сделать:**
- Добавить новые компоненты
- Изменить существующий код
- Исправить ошибки
- Улучшить дизайн
- Настроить функционал
- Оптимизировать производительность

Что хочешь добавить или изменить в проекте?""",
                    timestamp=datetime.now()
                )
            ],
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        return session_id
    
    def send_message(self, session_id: str, user_message: str) -> Dict[str, Any]:
        """Отправляет сообщение в чат и получает ответ AI"""
        
        if session_id not in self.active_sessions:
            return {'error': 'Session not found'}
            
        session = self.active_sessions[session_id]
        project_context = session['project_context']
        
        # Добавляем сообщение пользователя
        user_msg = ChatMessage(
            id=str(uuid.uuid4()),
            role='user',
            content=user_message,
            timestamp=datetime.now()
        )
        session['messages'].append(user_msg)
        
        # Генерируем ответ AI
        try:
            ai_response = self._generate_ai_response(session, user_message)
            
            # Добавляем ответ AI
            ai_msg = ChatMessage(
                id=str(uuid.uuid4()),
                role='assistant',
                content=ai_response['content'],
                timestamp=datetime.now(),
                metadata=ai_response.get('metadata', {})
            )
            session['messages'].append(ai_msg)
            session['last_activity'] = datetime.now()
            
            return {
                'success': True,
                'message': asdict(ai_msg),
                'actions': ai_response.get('actions', [])
            }
            
        except Exception as e:
            error_msg = ChatMessage(
                id=str(uuid.uuid4()),
                role='assistant',
                content=f"❌ Произошла ошибка: {str(e)}\nПожалуйста, попробуйте переформулировать запрос.",
                timestamp=datetime.now()
            )
            session['messages'].append(error_msg)
            
            return {
                'success': False,
                'message': asdict(error_msg),
                'error': str(e)
            }
    
    def _generate_ai_response(self, session: Dict, user_message: str) -> Dict[str, Any]:
        """Генерирует ответ AI на основе контекста проекта"""
        
        project_context = session['project_context']
        recent_messages = session['messages'][-10:]  # Последние 10 сообщений
        
        # Определяем тип запроса
        request_type = self._analyze_request_type(user_message)
        
        if request_type == 'code_modification':
            return self._handle_code_modification(project_context, user_message)
        elif request_type == 'new_feature':
            return self._handle_new_feature(project_context, user_message)
        elif request_type == 'bug_fix':
            return self._handle_bug_fix(project_context, user_message)
        elif request_type == 'design_improvement':
            return self._handle_design_improvement(project_context, user_message)
        else:
            return self._handle_general_question(project_context, user_message, recent_messages)
    
    def _analyze_request_type(self, message: str) -> str:
        """Анализирует тип запроса пользователя"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['добавь', 'создай', 'новый', 'новая']):
            return 'new_feature'
        elif any(word in message_lower for word in ['измени', 'поправь', 'отредактируй']):
            return 'code_modification'  
        elif any(word in message_lower for word in ['ошибка', 'не работает', 'исправь']):
            return 'bug_fix'
        elif any(word in message_lower for word in ['дизайн', 'стиль', 'красивее']):
            return 'design_improvement'
        else:
            return 'general_question'
    
    def _handle_code_modification(self, context: ProjectContext, message: str) -> Dict[str, Any]:
        """Обработка запросов на изменение кода"""
        
        # Используем intelligent chat для анализа
        intelligent_response = self.intelligent_chat.get_response(
            f"Проект: {context.name} ({context.project_type})\nЗапрос: {message}"
        )
        
        return {
            'content': f"""🔧 **Изменение кода**

{intelligent_response}

**Следующие шаги:**
1. Проверь изменения в файлах
2. Протестируй функционал
3. При необходимости попроси дополнительные правки

💡 Хочешь что-то еще изменить?""",
            'actions': ['code_update'],
            'metadata': {
                'type': 'code_modification',
                'affected_files': self._extract_relevant_files(context, message)
            }
        }
    
    def _handle_new_feature(self, context: ProjectContext, message: str) -> Dict[str, Any]:
        """Обработка запросов на новые функции"""
        
        return {
            'content': f"""✨ **Новая функция**

Отличная идея! Для проекта "{context.name}" я могу добавить эту функцию.

**Что нужно сделать:**
1. Создать новые компоненты
2. Добавить API endpoints (если нужно)
3. Обновить базу данных (при необходимости)
4. Настроить роутинг
5. Добавить стили

**Уточни пожалуйста:**
- Где должна располагаться эта функция?
- Нужна ли авторизация для доступа?
- Какие данные должны сохраняться?

Готов начать разработку! 🚀""",
            'actions': ['feature_development'],
            'metadata': {
                'type': 'new_feature',
                'complexity': 'medium'
            }
        }
    
    def _handle_bug_fix(self, context: ProjectContext, message: str) -> Dict[str, Any]:
        """Обработка запросов на исправление ошибок"""
        
        return {
            'content': f"""🐛 **Исправление ошибки**

Понятно! Давай разберемся с проблемой в проекте "{context.name}".

**Для диагностики мне нужно знать:**
1. В каком файле/компоненте происходит ошибка?
2. Какое поведение ожидается?
3. Есть ли сообщения об ошибках в консоли?
4. На каком этапе проявляется проблема?

**План действий:**
1. Анализ кода
2. Выявление причины
3. Исправление
4. Тестирование

Поделись деталями, и я быстро все исправлю! 🔧""",
            'actions': ['bug_analysis'],
            'metadata': {
                'type': 'bug_fix',
                'priority': 'high'
            }
        }
    
    def _handle_design_improvement(self, context: ProjectContext, message: str) -> Dict[str, Any]:
        """Обработка запросов на улучшение дизайна"""
        
        return {
            'content': f"""🎨 **Улучшение дизайна**

Отлично! Сделаем проект "{context.name}" еще красивее и удобнее.

**Варианты улучшений:**
- 📱 Mobile-responsive дизайн
- 🌈 Современная цветовая палитра  
- ✨ Анимации и микроинтеракции
- 🖼️ Улучшенная типографика
- 🎯 UX оптимизация

**Что конкретно хочешь улучшить:**
- Общий стиль страниц?
- Определенный компонент?
- Мобильную версию?
- Цвета и шрифты?

Расскажи свое видение, и я воплощу его в коде! 🚀""",
            'actions': ['design_update'],
            'metadata': {
                'type': 'design_improvement',
                'framework': context.framework
            }
        }
    
    def _handle_general_question(self, context: ProjectContext, message: str, recent_messages: List) -> Dict[str, Any]:
        """Обработка общих вопросов"""
        
        intelligent_response = self.intelligent_chat.get_response(message)
        
        return {
            'content': f"""💬 **Консультация**

{intelligent_response}

**Могу помочь с:**
- Добавлением новых функций
- Изменением существующего кода
- Исправлением ошибок
- Улучшением дизайна
- Оптимизацией производительности
- Настройкой интеграций

Что хочешь сделать дальше?""",
            'metadata': {
                'type': 'consultation'
            }
        }
    
    def _extract_relevant_files(self, context: ProjectContext, message: str) -> List[str]:
        """Извлекает релевантные файлы на основе сообщения"""
        relevant_files = []
        message_lower = message.lower()
        
        for filename in context.files.keys():
            if any(keyword in filename.lower() for keyword in message_lower.split()):
                relevant_files.append(filename)
                
        return relevant_files[:5]  # Максимум 5 файлов
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Получает историю чата"""
        if session_id not in self.active_sessions:
            return []
            
        messages = self.active_sessions[session_id]['messages']
        return [asdict(msg) for msg in messages if msg.role != 'system']
    
    def update_project_context(self, session_id: str, updated_context: ProjectContext):
        """Обновляет контекст проекта в сессии"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['project_context'] = updated_context

def test_ai_chat():
    """Тестирование AI чат системы"""
    
    # Создаем тестовый контекст проекта
    test_context = ProjectContext(
        project_id="test_123",
        name="E-commerce Store", 
        description="Интернет-магазин с корзиной",
        project_type="ecommerce",
        framework="nextjs",
        files={
            "pages/index.js": "// Home page",
            "components/ProductCard.js": "// Product component",
            "styles/globals.css": "/* Global styles */"
        },
        database_schema={"products": {}, "orders": {}},
        deployment_info={},
        history=[]
    )
    
    # Инициализируем чат
    chat_bot = ProjectAIChatBot()
    session_id = chat_bot.create_chat_session(test_context)
    
    print(f"🤖 Сессия создана: {session_id}")
    
    # Тестовые сообщения
    test_messages = [
        "Добавь корзину товаров",
        "Измени цвет кнопок на синий",
        "У меня не работает форма заказа", 
        "Сделай дизайн современнее"
    ]
    
    for message in test_messages:
        print(f"\n👤 Пользователь: {message}")
        response = chat_bot.send_message(session_id, message)
        
        if response['success']:
            print(f"🤖 AI: {response['message']['content'][:200]}...")
        else:
            print(f"❌ Ошибка: {response['error']}")

if __name__ == "__main__":
    test_ai_chat()