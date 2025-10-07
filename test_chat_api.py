#!/usr/bin/env python3
"""
Тестовый API сервер для прямого тестирования AI чата
"""

import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
sys.path.append('backend')

from backend.intelligent_chat import IntelligentChat

# Создаем Flask приложение
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

# Инициализируем AI чат
chat = IntelligentChat()

@app.route('/api/test-chat', methods=['POST'])
def test_chat():
    """Тестовый endpoint для чата без авторизации"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Требуется поле message',
                'status': 'error'
            }), 400
        
        message = data['message']
        session_id = data.get('session_id', 'default_test_session')
        
        # Получаем ответ от AI
        result = chat.chat(session_id, message)
        
        # Получаем предложения
        suggestions = chat.get_suggestions(session_id)
        
        # Возвращаем полный результат
        return jsonify({
            'status': 'success',
            'response': result['response'],
            'session_id': result['session_id'],
            'intent_analysis': result['intent_analysis'],
            'ai_provider': result['ai_provider'],
            'message_count': result['message_count'],
            'suggestions': suggestions,
            'timestamp': result['timestamp']
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Внутренняя ошибка сервера: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/chat-history/<session_id>', methods=['GET'])
def get_test_chat_history(session_id):
    """Получить историю чата"""
    try:
        session = chat.get_session(session_id)
        
        if not session:
            return jsonify({
                'error': 'Сессия не найдена',
                'status': 'error'
            }), 404
        
        # Форматируем сообщения для JSON
        messages = []
        for msg in session.messages:
            if msg.role != 'system':  # Исключаем системные сообщения
                messages.append({
                    'role': msg.role,
                    'content': msg.content,
                    'timestamp': msg.timestamp.isoformat(),
                    'message_type': msg.message_type
                })
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'messages': messages,
            'total_messages': len(messages),
            'created_at': session.created_at.isoformat(),
            'last_activity': session.last_activity.isoformat(),
            'context': session.context
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Ошибка получения истории: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/suggestions/<session_id>', methods=['GET'])
def get_suggestions(session_id):
    """Получить предложения для сессии"""
    try:
        suggestions = chat.get_suggestions(session_id)
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'session_id': session_id
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Ошибка получения предложений: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Получить статус системы"""
    return jsonify({
        'status': 'running',
        'ai_chat': 'active',
        'sessions_count': len(chat.sessions),
        'openai_available': chat.openai_api_key is not None,
        'claude_available': chat.claude_api_key is not None,
        'version': '2.0.0'
    })

@app.route('/test', methods=['GET'])
def test_page():
    """Простая тестовая страница"""
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Тест AI Чата</title>
        <style>
            body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ccc; height: 400px; overflow-y: scroll; padding: 10px; margin: 10px 0; }
            .message { margin: 10px 0; padding: 8px; border-radius: 8px; }
            .user { background: #e3f2fd; text-align: right; }
            .ai { background: #f1f8e9; }
            .input-area { display: flex; margin: 10px 0; }
            .input-area input { flex: 1; padding: 10px; }
            .input-area button { padding: 10px 20px; margin-left: 10px; }
            .suggestions { margin: 10px 0; }
            .suggestion { display: inline-block; margin: 5px; padding: 5px 10px; background: #f5f5f5; border-radius: 15px; cursor: pointer; border: 1px solid #ddd; }
            .status { background: #fff3e0; padding: 10px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>🤖 Тест AI Чата Lovable Platform</h1>
        
        <div class="status" id="status">
            <strong>Статус:</strong> <span id="status-text">Загрузка...</span>
        </div>
        
        <div class="chat-container" id="chat"></div>
        
        <div class="suggestions" id="suggestions">
            <strong>💡 Предложения:</strong>
        </div>
        
        <div class="input-area">
            <input type="text" id="messageInput" placeholder="Напишите сообщение..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Отправить</button>
            <button onclick="clearChat()">Очистить</button>
        </div>
        
        <script>
            const sessionId = 'test_web_session_' + Date.now();
            
            async function checkStatus() {
                try {
                    const response = await fetch('/api/status');
                    const status = await response.json();
                    document.getElementById('status-text').innerHTML = `
                        ✅ Работает | Сессий: ${status.sessions_count} | 
                        OpenAI: ${status.openai_available ? '✅' : '❌'} | 
                        Claude: ${status.claude_available ? '✅' : '❌'}
                    `;
                } catch (e) {
                    document.getElementById('status-text').textContent = '❌ Ошибка подключения';
                }
            }
            
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;
                
                // Показываем сообщение пользователя
                addMessage(message, 'user');
                input.value = '';
                
                try {
                    const response = await fetch('/api/test-chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message, session_id: sessionId })
                    });
                    
                    const result = await response.json();
                    
                    if (result.status === 'success') {
                        // Показываем ответ AI
                        addMessage(result.response, 'ai', result.ai_provider);
                        
                        // Обновляем предложения
                        updateSuggestions(result.suggestions);
                        
                        // Обновляем статус
                        checkStatus();
                    } else {
                        addMessage('Ошибка: ' + result.error, 'ai', 'error');
                    }
                } catch (e) {
                    addMessage('Ошибка сети: ' + e.message, 'ai', 'error');
                }
            }
            
            function addMessage(text, type, provider = '') {
                const chat = document.getElementById('chat');
                const div = document.createElement('div');
                div.className = `message ${type}`;
                
                if (type === 'ai' && provider) {
                    div.innerHTML = `<strong>🤖 AI (${provider}):</strong> ${text}`;
                } else if (type === 'user') {
                    div.innerHTML = `<strong>👤 Вы:</strong> ${text}`;
                } else {
                    div.textContent = text;
                }
                
                chat.appendChild(div);
                chat.scrollTop = chat.scrollHeight;
            }
            
            function updateSuggestions(suggestions) {
                const container = document.getElementById('suggestions');
                container.innerHTML = '<strong>💡 Предложения:</strong>';
                
                suggestions.forEach(suggestion => {
                    const span = document.createElement('span');
                    span.className = 'suggestion';
                    span.textContent = suggestion;
                    span.onclick = () => {
                        document.getElementById('messageInput').value = suggestion;
                        sendMessage();
                    };
                    container.appendChild(span);
                });
            }
            
            function clearChat() {
                document.getElementById('chat').innerHTML = '';
                document.getElementById('suggestions').innerHTML = '<strong>💡 Предложения:</strong>';
            }
            
            // Инициализация
            checkStatus();
            addMessage('Привет! Я AI-ассистент Lovable Platform. Расскажи, что хочешь создать?', 'ai', 'system');
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Запуск тестового AI чат сервера...")
    print("🌐 Откройте: http://127.0.0.1:5001/test")
    print("📡 API: http://127.0.0.1:5001/api/test-chat")
    print("💡 Для остановки нажмите Ctrl+C")
    
    app.run(
        host='127.0.0.1', 
        port=5001, 
        debug=False, 
        use_reloader=False
    )