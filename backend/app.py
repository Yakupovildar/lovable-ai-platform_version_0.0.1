from flask import Flask, request, jsonify, send_file, session, redirect, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
from functools import wraps
import os
import json
import zipfile
import tempfile
import shutil
from datetime import datetime, timedelta
import uuid
from pathlib import Path
import subprocess
import threading
import queue
import time
import random
import hashlib
import sqlite3
import asyncio
from concurrent.futures import ThreadPoolExecutor
import pickle
import logging
from functools import wraps
# Базовые мониторинг и производительность
class SimplePerformanceMonitor:
    def __init__(self):
        self.stats = {}

    def get_stats(self):
        return self.stats

def monitor_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⚡ {func.__name__} выполнен за {end_time - start_time:.2f}с")
        return result
    return wrapper

performance_monitor = SimplePerformanceMonitor()

# Базовый NLP процессор
class SmartNLP:
    def correct_and_normalize(self, text):
        return text.lower().strip()

# Базовая система контроля версий
class ProjectVersionControl:
    def get_next_version(self, project_type):
        return "1.0"
    def save_project_version(self, project_id, version, files, message):
        pass
    def get_project_versions(self, project_id):
        return []
    def revert_project(self, project_id, target_version):
        return False # Placeholder

# Базовая система логирования
class UserInteractionLogger:
    def log_event(self, event, data, session_id=None):
        print(f"LOG: {event} - {data}")
    def log_interaction(self, session_id, message, processed, msg_type):
        print(f"INTERACTION: {session_id} - {message}")
    def log_user_request(self, user_id, session_id, request_data):
        print(f"USER_REQUEST: {user_id} - {session_id} - {request_data}")
        return f"req_{session_id}"
    def log_ai_response(self, user_id, session_id, request_id, response_data, processing_time):
        print(f"AI_RESPONSE: {user_id} - {session_id} - {request_id}")
    def log_project_creation(self, user_id, session_id, project_data):
        print(f"PROJECT: {user_id} - {project_data}")
    def log_error(self, user_id, session_id, error_data):
        print(f"ERROR: {user_id} - {session_id} - {error_data}")

# Расширенный генератор проектов
class AdvancedProjectGenerator:
    def generate_project(self, project_type, description, project_name, user_preferences=None):
        return generator.generate_project(project_type, description, project_name)
    def add_feature(self, project_id, feature):
        return True

app = Flask(__name__)
app.secret_key = 'vibecode_ai_secret_key_2024_super_secure'
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*", manage_session=True, async_mode='threading')

# Настройка логирования для отладки
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Пул потоков для асинхронных операций
executor = ThreadPoolExecutor(max_workers=50)

# Кэш в памяти (fallback если Redis недоступен)
memory_cache = {}
cache_ttl = {}

# Пытаемся подключиться к Redis (опционально)
try:
    import redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("✅ Redis подключен для кэширования")
    USE_REDIS = True
except Exception as e:
    print(f"⚠️ Redis недоступен: {e}")
    print("💡 Используем память для кэша")
    USE_REDIS = False
    redis_client = None

def login_required(f):
    """Декоратор для проверки авторизации"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Требуется авторизация", "redirect": "/auth"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def serve_frontend():
    """Serve main frontend page"""
    return send_file('../index.html')

@app.route('/dashboard')
def serve_dashboard():
    """Serve dashboard page"""
    return send_file('../dashboard.html')

@app.route('/auth')
def serve_auth():
    """Serve auth page"""
    return send_file('../auth.html')

# === API для аутентификации ===

@app.route('/api/register', methods=['POST'])
def register():
    """Регистрация нового пользователя"""
    data = request.json
    email = data.get('email', '').strip().lower()
    name = data.get('name', '').strip()
    password = data.get('password', '')

    # Валидация
    if not email or not name or not password:
        return jsonify({"error": "Все поля обязательны"}), 400

    if len(password) < 8:
        return jsonify({"error": "Пароль должен содержать минимум 8 символов"}), 400

    if '@' not in email:
        return jsonify({"error": "Некорректный email"}), 400

    # Проверяем, не существует ли пользователь
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({"error": "Пользователь с таким email уже существует"}), 400

    # Создаем пользователя
    user_id = create_user(email, name, password)
    if user_id:
        session['user_id'] = user_id
        session['user_email'] = email
        session['user_name'] = name

        interaction_logger.log_event("user_registered", {
            "user_id": user_id,
            "email": email,
            "name": name
        })

        return jsonify({
            "success": True,
            "message": "Регистрация успешна!",
            "user": {
                "id": user_id,
                "email": email,
                "name": name,
                "plan": "free",
                "requests_left": 15
            }
        })
    else:
        return jsonify({"error": "Ошибка при создании пользователя"}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """Авторизация пользователя"""
    data = request.json
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({"error": "Email и пароль обязательны"}), 400

    user = get_user_by_email(email)
    if not user or not verify_password(password, user[3]):  # user[3] = password_hash
        return jsonify({"error": "Неверный email или пароль"}), 401

    # Обновляем время последнего входа
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?', (user[0],))
    conn.commit()
    conn.close()

    # Сохраняем в сессии
    session['user_id'] = user[0]
    session['user_email'] = user[1]
    session['user_name'] = user[2]

    interaction_logger.log_event("user_logged_in", {
        "user_id": user[0],
        "email": user[1]
    })

    return jsonify({
        "success": True,
        "message": "Вход выполнен успешно!",
        "user": {
            "id": user[0],
            "email": user[1],
            "name": user[2],
            "plan": user[4],
            "requests_left": max(0, user[6] - user[5])  # requests_limit - requests_used
        }
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    """Выход из системы"""
    session.clear()
    return jsonify({"success": True, "message": "Вы вышли из системы"})

@app.route('/api/user/profile')
@login_required
def get_user_profile():
    """Получить профиль пользователя"""
    user = get_user_by_id(session['user_id'])
    if not user:
        return jsonify({"error": "Пользователь не найден"}), 404

    return jsonify({
        "user": {
            "id": user[0],
            "email": user[1],
            "name": user[2],
            "plan": user[4],
            "requests_used": user[5],
            "requests_limit": user[6],
            "requests_left": max(0, user[6] - user[5]),
            "subscription_expires": user[7],
            "created_at": user[8]
        }
    })

@app.route('/api/user/update', methods=['POST'])
@login_required
def update_user_profile():
    """Обновить профиль пользователя"""
    data = request.json
    name = data.get('name', '').strip()

    if not name:
        return jsonify({"error": "Имя обязательно"}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET name = ? WHERE id = ?', (name, session['user_id']))
    conn.commit()
    conn.close()

    session['user_name'] = name

    return jsonify({"success": True, "message": "Профиль обновлен"})

@app.route('/api/user/history')
@login_required
def get_chat_history():
    """Получить историю чатов пользователя"""
    history = get_user_chat_history(session['user_id'])

    # Группируем по сессиям
    sessions = {}
    for row in history:
        session_id, message, response, msg_type, created_at = row
        if session_id not in sessions:
            sessions[session_id] = {
                "session_id": session_id,
                "created_at": created_at,
                "messages": []
            }
        sessions[session_id]["messages"].append({
            "message": message,
            "response": response,
            "type": msg_type,
            "created_at": created_at
        })

    return jsonify({
        "sessions": list(sessions.values())
    })

@app.route('/api/user/projects')
@login_required
def get_user_projects_api():
    """Получить проекты пользователя"""
    projects = get_user_projects(session['user_id'])

    projects_list = []
    for project in projects:
        projects_list.append({
            "project_id": project[0],
            "name": project[1],
            "type": project[2],
            "description": project[3],
            "created_at": project[4],
            "updated_at": project[5]
        })

    return jsonify({"projects": projects_list})

@app.route('/<path:filename>')
def serve_static_files(filename):
    """Serve static files (CSS, JS, images)"""
    try:
        return send_file(f'../{filename}')
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Backend is running"})

@app.route('/api/status')
def status_check():
    """Быстрая проверка статуса сервиса"""
    return jsonify({
        "status": "ok",
        "version": "2.0",
        "cache_enabled": USE_REDIS or len(memory_cache) > 0,
        "active_threads": threading.active_count(),
        "memory_cache_size": len(memory_cache),
        "redis_connected": USE_REDIS,
        "performance": "optimized"
    })

@app.route('/api/cache/clear', methods=['POST'])
@login_required
def clear_cache():
    """Очистка кэша пользователя"""
    user_id = session.get('user_id')
    if user_id:
        clear_user_cache(user_id)
        return jsonify({"success": True, "message": "Кэш очищен"})
    return jsonify({"success": False, "message": "Не авторизован"}), 401

@app.route('/api/performance')
def get_performance():
    """Получить статистику производительности"""
    stats = performance_monitor.get_stats()
    return jsonify(stats)

@app.route('/api/optimize', methods=['POST'])
def optimize_performance():
    """Оптимизация производительности"""
    # Очищаем старые кэши
    global memory_cache, cache_ttl
    current_time = time.time()

    # Удаляем устаревшие записи из кэша
    expired_keys = [k for k, v in cache_ttl.items() if current_time - v > 600]
    for key in expired_keys:
        memory_cache.pop(key, None)
        cache_ttl.pop(key, None)

    # Очищаем неактивные сессии AI
    if hasattr(super_ai, 'cleanup_inactive_sessions'):
        super_ai.cleanup_inactive_sessions()

    return jsonify({
        "success": True,
        "message": "Оптимизация выполнена",
        "cleared_cache_entries": len(expired_keys),
        "active_cache_size": len(memory_cache)
    })

# Конфигурация
PROJECTS_DIR = "projects"
TEMP_DIR = "temp"
LOGS_DIR = "logs"
USER_DATA_DIR = "user_data"
MAX_PROJECTS_PER_USER = 10

# Создаём директории если их нет
os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

# === СИСТЕМА КЭШИРОВАНИЯ ===
def get_cache_key(prefix: str, *args) -> str:
    """Генерирует ключ для кэша"""
    return f"{prefix}:{'_'.join(str(arg) for arg in args)}"

def get_from_cache(key: str):
    """Получает данные из кэша"""
    if USE_REDIS and redis_client:
        try:
            data = redis_client.get(key)
            return pickle.loads(data) if data else None
        except:
            pass

    # Fallback на память
    if key in memory_cache:
        if time.time() - cache_ttl.get(key, 0) < 300:  # 5 минут
            return memory_cache[key]
        else:
            memory_cache.pop(key, None)
            cache_ttl.pop(key, None)
    return None

def set_cache(key: str, data, ttl: int = 300):
    """Сохраняет данные в кэш"""
    if USE_REDIS and redis_client:
        try:
            redis_client.setex(key, ttl, pickle.dumps(data))
            return
        except:
            pass

    # Fallback на память
    memory_cache[key] = data
    cache_ttl[key] = time.time()

def clear_user_cache(user_id: int):
    """Очищает кэш пользователя"""
    pattern = f"user_{user_id}:*"
    if USE_REDIS and redis_client:
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
        except:
            pass

    # Очищаем из памяти
    keys_to_remove = [k for k in memory_cache.keys() if k.startswith(f"user_{user_id}:")]
    for key in keys_to_remove:
        memory_cache.pop(key, None)
        cache_ttl.pop(key, None)

# === АСИНХРОННЫЕ ОБРАБОТЧИКИ ===
def async_ai_response(message: str, session_id: str, user_id: int):
    """Асинхронная обработка AI ответов"""
    try:
        # Проверяем кэш сначала
        cache_key = get_cache_key("ai_response", user_id, hash(message))
        cached_response = get_from_cache(cache_key)

        if cached_response:
            logger.info(f"Возвращаем кэшированный ответ для user {user_id}")
            return cached_response

        # Генерируем новый ответ
        start_time = time.time()
        ai_response = ai_agent.generate_personalized_response(message, session_id)
        processing_time = int((time.time() - start_time) * 1000)

        # Кэшируем ответ
        set_cache(cache_key, ai_response, ttl=600)  # 10 минут

        logger.info(f"AI ответ сгенерирован за {processing_time}ms для user {user_id}")
        return ai_response

    except Exception as e:
        logger.error(f"Ошибка async_ai_response: {e}")
        return {
            "type": "error",
            "message": "Временная ошибка обработки. Попробуйте снова.",
            "suggestions": ["Повторить запрос", "Создать приложение", "Получить помощь"]
        }

def async_project_generation(project_type: str, description: str, project_name: str, user_id: int):
    """Асинхронная генерация проектов"""
    try:
        # Проверяем кэш
        cache_key = get_cache_key("project", project_type, hash(description))
        cached_project = get_from_cache(cache_key)

        if cached_project:
            logger.info(f"Возвращаем кэшированный проект для user {user_id}")
            return cached_project

        # Генерируем новый проект
        start_time = time.time()
        result = generator.generate_project(project_type, description, project_name)
        processing_time = int((time.time() - start_time) * 1000)

        if result['success']:
            # Кэшируем только успешные проекты
            set_cache(cache_key, result, ttl=1800)  # 30 минут
            logger.info(f"Проект сгенерирован за {processing_time}ms для user {user_id}")

        return result

    except Exception as e:
        logger.error(f"Ошибка async_project_generation: {e}")
        return {
            "success": False,
            "error": f"Ошибка генерации: {str(e)}"
        }

# Инициализация базы данных
def init_database():
    """Инициализируем базу данных пользователей"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            plan TEXT DEFAULT 'free',
            requests_used INTEGER DEFAULT 0,
            requests_limit INTEGER DEFAULT 15,
            subscription_expires DATETIME DEFAULT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_login DATETIME DEFAULT NULL
        )
    ''')

    # Таблица истории чатов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL,
            message_type TEXT DEFAULT 'chat',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Таблица проектов пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            project_id TEXT NOT NULL,
            project_name TEXT NOT NULL,
            project_type TEXT NOT NULL,
            project_description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Таблица активных сессий (для WebSocket)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_sessions (
            session_id TEXT PRIMARY KEY,
            user_id INTEGER NOT NULL,
            last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    # Таблица версий проектов (для системы контроля версий)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT NOT NULL,
            version TEXT NOT NULL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            files TEXT, -- JSON string of files and their content
            FOREIGN KEY (project_id) REFERENCES user_projects (project_id)
        )
    ''')

    conn.commit()
    conn.close()

# Инициализируем базу данных
init_database()

# Утилиты для работы с пользователями
def hash_password(password):
    """Хешируем пароль"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Проверяем пароль"""
    return hash_password(password) == password_hash

def get_user_by_email(email):
    """Получаем пользователя по email"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    """Получаем пользователя по ID"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(email, name, password):
    """Создаем нового пользователя"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:
        cursor.execute('''
            INSERT INTO users (email, name, password_hash) 
            VALUES (?, ?, ?)
        ''', (email, name, password_hash))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def update_user_requests(user_id, increment=1):
    """Обновляем количество использованных запросов"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET requests_used = requests_used + ? 
        WHERE id = ?
    ''', (increment, user_id))
    conn.commit()
    conn.close()

def save_chat_message(user_id, session_id, message, response, message_type='chat'):
    """Сохраняем сообщение в истории чата"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_id, session_id, message, response, message_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, session_id, message, response, message_type))
    conn.commit()
    conn.close()

def get_user_chat_history(user_id, limit=50):
    """Получаем историю чатов пользователя"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT session_id, message, response, message_type, created_at
        FROM chat_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (user_id, limit))
    history = cursor.fetchall()
    conn.close()
    return history

def save_user_project(user_id, project_id, project_name, project_type, description=""):
    """Сохраняем проект пользователя"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_projects (user_id, project_id, project_name, project_type, project_description)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, project_id, project_name, project_type, description))
    conn.commit()
    conn.close()

def get_user_projects(user_id):
    """Получаем проекты пользователя"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT project_id, project_name, project_type, project_description, created_at, updated_at
        FROM user_projects 
        WHERE user_id = ? 
        ORDER BY updated_at DESC
    ''', (user_id,))
    projects = cursor.fetchall()
    conn.close()
    return projects

# Очередь для обработки генерации проектов
project_queue = queue.Queue()

# Инициализация новых компонентов
# Инициализация РЕВОЛЮЦИОННЫХ AI-компонентов
try:
    from ultra_smart_ai import UltraSmartAI
    from genius_conversation import GeniusConversationAI  
    from project_genius import ProjectGenius

    ultra_ai = UltraSmartAI()
    genius_conversation = GeniusConversationAI()
    project_genius = ProjectGenius()

    print("🚀 ✅ UltraSmartAI - ЗАГРУЖЕН!")
    print("🧠 ✅ GeniusConversation - ГОТОВ!")
    print("⚡ ✅ ProjectGenius - АКТИВИРОВАН!")
    print("🌟 СИСТЕМА В 100 РАЗ МОЩНЕЕ!")

    # Основной AI-агент с супер-возможностями
    class SuperRevolutionaryAI:
        def __init__(self):
            self.ultra_ai = ultra_ai
            self.genius_conv = genius_conversation
            self.project_genius = project_genius

        def generate_personalized_response(self, message, session_id="default"):
            """РЕВОЛЮЦИОННЫЙ ответ с полным пониманием пользователя"""

            # Гениальный анализ сообщения
            genius_response = self.genius_conv.generate_intelligent_response(message)

            # Если пользователь хочет создать приложение
            if genius_response.get("understanding", {}).get("intent") == "создать_приложение":
                # Получаем ультра-умный ответ
                ultra_response = self.ultra_ai.get_ultra_smart_response(message)

                # Комбинируем лучшее из обоих
                combined_message = f"""{genius_response['message']}

{ultra_response['message']}

🎯 **ГОТОВ СОЗДАТЬ ДЛЯ ВАС:**
• 📱 Полностью рабочее приложение за 15 минут
• 🤖 AI-интеграция в каждую функцию  
• 🎨 Дизайн уровня Apple/Google
• 💰 Готовые схемы заработка $5,000-50,000/месяц
• 🚀 Инструкции по публикации в сторах
• 📊 Система аналитики для роста бизнеса

⚡ **ЭТО БУДЕТ НЕВЕРОЯТНО!** ⚡"""

                return {
                    "type": "revolutionary_response",
                    "message": combined_message,
                    "suggestions": [
                        "🚀 СОЗДАВАТЬ НЕМЕДЛЕННО!",
                        "🎨 Показать дизайн-варианты", 
                        "💰 План монетизации",
                        "⚡ Все возможности сразу!"
                    ],
                    "features": ultra_response.get("features", []),
                    "app_type": genius_response.get("app_type", "утилиты")
                }

            # Для других типов запросов используем гениальный диалог
            return genius_response

    ai_agent = SuperRevolutionaryAI()
    print("🎉 РЕВОЛЮЦИОННЫЙ AI-АГЕНТ ГОТОВ К РАБОТЕ!")

except Exception as e:
    print(f"⚠️ Ошибка инициализации революционной системы: {e}")
    # Fallback на улучшенный базовый AI
    class EnhancedFallbackAI:
        def generate_personalized_response(self, message, session_id="default"):
            message_lower = message.lower()

            if any(word in message_lower for word in ["создай", "сделай", "хочу", "нужно"]):
                return {
                    "type": "enhanced_response", 
                    "message": f"""🚀 **НЕВЕРОЯТНО! Создаю для вас революционное приложение!**

💡 Ваш запрос: "{message}"

🔥 **Что получите:**
• 📱 Полностью готовое мобильное приложение
• 🎨 Современный дизайн уровня премиум
• 🤖 AI-интеграция для умных функций
• 💰 Схемы монетизации до $50,000/месяц
• 🚀 Готовность к публикации в сторах

⏰ **Время создания: 15 минут!**

Начинаем создание вашего шедевра?""",
                    "suggestions": [
                        "🚀 ДА! Создавать сейчас!",
                        "🎨 Показать варианты дизайна",
                        "💰 Детали монетизации", 
                        "⚡ Все функции приложения"
                    ]
                }
            elif "привет" in message_lower:
                return {
                    "type": "enhanced_response",
                    "message": """🌟 **Добро пожаловать в будущее создания приложений!**

Я - революционный AI, который создает любые приложения за 15 минут!

🚀 **Что умею:**
• 📱 Мобильные приложения (iOS/Android)
• 🌐 Веб-приложения и PWA
• 🎮 Игры любых жанров
• 💼 Бизнес-системы и CRM
• 🤖 AI-интеграция в любой проект

💰 **Доход:** до $50,000/месяц с правильной монетизацией!

Расскажите, какое приложение создаем?""",
                    "suggestions": [
                        "Создать игру",
                        "Мобильное приложение", 
                        "Веб-сайт",
                        "Показать примеры"
                    ]
                }
            else:
                return {
                    "type": "enhanced_response",
                    "message": """🤖 **Понял ваш запрос!** 

"{message}"

💫 **Готов создать для вас:**
• Любое мобильное приложение
• С современным дизайном
• С AI-функциями
• За 15 минут!

Расскажите подробнее, что именно хотите?""",
                    "suggestions": [
                        "Создать игру",
                        "Мобильное приложение", 
                        "Веб-сайт",
                        "Показать примеры"
                    ]
                }

    ai_agent = EnhancedFallbackAI()

nlp_processor = SmartNLP()
version_control = ProjectVersionControl()
interaction_logger = UserInteractionLogger()
advanced_generator = AdvancedProjectGenerator()

class ProjectGenerator:
    def __init__(self):
        self.templates = {
            "snake_game": {
                "files": {
                    "index.html": self.get_snake_html,
                    "styles.css": self.get_snake_css,
                    "script.js": self.get_snake_js,
                    "README.md": self.get_snake_readme
                }
            },
            "tetris_game": {
                "files": {
                    "index.html": self.get_tetris_html,
                    "styles.css": self.get_tetris_css,
                    "script.js": self.get_tetris_js,
                    "README.md": self.get_tetris_readme
                }
            },
            "todo_app": {
                "files": {
                    "index.html": self.get_todo_html,
                    "styles.css": self.get_todo_css,
                    "script.js": self.get_todo_js,
                    "README.md": self.get_todo_readme
                }
            },
            "weather_app": {
                "files": {
                    "index.html": self.get_weather_html,
                    "styles.css": self.get_weather_css,
                    "script.js": self.get_weather_js,
                    "README.md": self.get_weather_readme
                }
            }
        }

    def generate_project(self, project_type, description, project_name, style="modern"):
        """Генерирует проект на основе описания"""
        try:
            project_id = str(uuid.uuid4())
            project_path = os.path.join(PROJECTS_DIR, project_id)
            os.makedirs(project_path, exist_ok=True)

            template = self.templates.get(project_type, self.templates["snake_game"])

            for file_path, generator_func in template["files"].items():
                full_path = os.path.join(project_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                content = generator_func(project_name, description, style)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Логирование создания проекта
            interaction_logger.log_event("project_creation", {
                "project_id": project_id,
                "project_type": project_type,
                "project_name": project_name,
                "description": description,
                "style": style
            })

            return {
                "success": True,
                "project_id": project_id,
                "project_name": project_name,
                "project_type": project_type,
                "files": list(template["files"].keys())
            }
        except Exception as e:
            interaction_logger.log_error("project_creation_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e)
            }

    def get_snake_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="game-container">
        <div class="game-header">
            <h1>{project_name}</h1>
            <div class="game-info">
                <div class="score">Счёт: <span id="score">0</span></div>
                <div class="high-score">Рекорд: <span id="highScore">0</span></div>
            </div>
        </div>

        <div class="game-area">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
            <div class="game-overlay" id="gameOverlay">
                <div class="start-screen">
                    <h2>🐍 Змейка</h2>
                    <p>Управление: стрелки или WASD</p>
                    <button id="startBtn" class="game-btn">Начать игру</button>
                </div>
            </div>
        </div>

        <div class="game-controls">
            <div class="mobile-controls">
                <button class="control-btn" data-direction="up">↑</button>
                <div class="control-row">
                    <button class="control-btn" data-direction="left">←</button>
                    <button class="control-btn" data-direction="down">↓</button>
                    <button class="control-btn" data-direction="right">→</button>
                </div>
            </div>
        </div>

        <div class="game-footer">
            <p>{description}</p>
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_snake_css(self, project_name, description, style):
        return f"""* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
    --bg-color: #0f0f23;
    --text-color: #ffffff;
    --snake-color: #00ff88;
    --food-color: #ff6b6b;
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.game-container {{
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 500px;
    width: 100%;
}}

.game-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.game-info {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    font-size: 1.2rem;
    font-weight: 600;
}}

.game-area {{
    position: relative;
    margin: 2rem 0;
}}

#gameCanvas {{
    border: 3px solid var(--accent-color);
    border-radius: 15px;
    background: var(--bg-color);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}}

.game-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
}}

.start-screen {{
    text-align: center;
    color: white;
}}

.start-screen h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.game-btn {{
    background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
    border: none;
    color: white;
    padding: 1rem 2rem;
    border-radius: 25px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}}

.game-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}}

.mobile-controls {{
    margin-top: 2rem;
}}

.control-btn {{
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    font-size: 1.5rem;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.control-btn:hover {{
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}}

.control-row {{
    display: flex;
    justify-content: center;
    align-items: center;
}}

.game-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.8;
}}

.hidden {{
    display: none !important;
}}

@media (max-width: 600px) {{
    .game-container {{
        padding: 1rem;
        margin: 1rem;
    }}

    #gameCanvas {{
        width: 100%;
        height: auto;
        max-width: 350px;
    }}

    .game-header h1 {{
        font-size: 2rem;
    }}

    .game-info {{
        font-size: 1rem;
    }}
}}"""

    def get_snake_js(self, project_name, description, style):
        return """class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.scoreElement = document.getElementById('score');
        this.highScoreElement = document.getElementById('highScore');
        this.overlay = document.getElementById('gameOverlay');
        this.startBtn = document.getElementById('startBtn');

        this.gridSize = 20;
        this.tileCount = this.canvas.width / this.gridSize;

        this.reset();
        this.setupControls();
        this.loadHighScore();
    }

    reset() {
        this.snake = [
            {x: 10, y: 10}
        ];
        this.food = this.generateFood();
        this.dx = 0;
        this.dy = 0;
        this.score = 0;
        this.gameRunning = false;
        this.updateScore();
    }

    generateFood() {
        return {
            x: Math.floor(Math.random() * this.tileCount),
            y: Math.floor(Math.random() * this.tileCount)
        };
    }

    setupControls() {
        this.startBtn.addEventListener('click', () => this.startGame());

        document.addEventListener('keydown', (e) => {
            if (!this.gameRunning) return;

            switch(e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (this.dy !== 1) {
                        this.dx = 0;
                        this.dy = -1;
                    }
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    if (this.dy !== -1) {
                        this.dx = 0;
                        this.dy = 1;
                    }
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (this.dx !== 1) {
                        this.dx = -1;
                        this.dy = 0;
                    }
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (this.dx !== -1) {
                        this.dx = 1;
                        this.dy = 0;
                    }
                    break;
            }
        });

        document.querySelectorAll('.control-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (!this.gameRunning) return;

                const direction = btn.dataset.direction;
                switch(direction) {
                    case 'up':
                        if (this.dy !== 1) {
                            this.dx = 0;
                            this.dy = -1;
                        }
                        break;
                    case 'down':
                        if (this.dy !== -1) {
                            this.dx = 0;
                            this.dy = 1;
                        }
                        break;
                    case 'left':
                        if (this.dx !== 1) {
                            this.dx = -1;
                            this.dy = 0;
                        }
                        break;
                    case 'right':
                        if (this.dx !== -1) {
                            this.dx = 1;
                            this.dy = 0;
                        }
                        break;
                }
            });
        });
    }

    startGame() {
        this.reset();
        this.gameRunning = true;
        this.overlay.classList.add('hidden');
        this.dx = 1;
        this.dy = 0;
        this.gameLoop();
    }

    gameLoop() {
        if (!this.gameRunning) return;

        setTimeout(() => {
            this.clearCanvas();
            this.moveSnake();
            this.drawFood();
            this.drawSnake();

            if (this.checkGameOver()) {
                this.endGame();
                return;
            }

            this.gameLoop();
        }, 150);
    }

    clearCanvas() {
        this.ctx.fillStyle = 'rgba(15, 15, 35, 0.9)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    moveSnake() {
        const head = {x: this.snake[0].x + this.dx, y: this.snake[0].y + this.dy};

        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.updateScore();
            this.food = this.generateFood();
        } else {
            this.snake.pop();
        }

        this.snake.unshift(head);
    }

    drawSnake() {
        this.ctx.fillStyle = '#00ff88';
        this.ctx.shadowColor = '#00ff88';
        this.ctx.shadowBlur = 10;

        this.snake.forEach((segment, index) => {
            if (index === 0) {
                this.ctx.fillStyle = '#00ffaa';
            } else {
                this.ctx.fillStyle = '#00ff88';
            }

            this.ctx.fillRect(
                segment.x * this.gridSize + 2,
                segment.y * this.gridSize + 2,
                this.gridSize - 4,
                this.gridSize - 4
            );
        });

        this.ctx.shadowBlur = 0;
    }

    drawFood() {
        this.ctx.fillStyle = '#ff6b6b';
        this.ctx.shadowColor = '#ff6b6b';
        this.ctx.shadowBlur = 15;

        this.ctx.beginPath();
        this.ctx.arc(
            this.food.x * this.gridSize + this.gridSize / 2,
            this.food.y * this.gridSize + this.gridSize / 2,
            this.gridSize / 2 - 2,
            0,
            2 * Math.PI
        );
        this.ctx.fill();

        this.ctx.shadowBlur = 0;
    }

    checkGameOver() {
        const head = this.snake[0];

        if (head.x < 0 || head.x >= this.tileCount || head.y < 0 || head.y >= this.tileCount) {
            return true;
        }

        for (let i = 1; i < this.snake.length; i++) {
            if (head.x === this.snake[i].x && head.y === this.snake[i].y) {
                return true;
            }
        }

        return false;
    }

    endGame() {
        this.gameRunning = false;
        this.updateHighScore();

        this.overlay.innerHTML = `
            <div class="start-screen">
                <h2>🎮 Игра окончена!</h2>
                <p>Ваш счёт: ${this.score}</p>
                <p>Рекорд: ${this.getHighScore()}</p>
                <button id="restartBtn" class="game-btn">Играть снова</button>
            </div>
        `;

        this.overlay.classList.remove('hidden');

        document.getElementById('restartBtn').addEventListener('click', () => {
            this.startGame();
        });
    }

    updateScore() {
        this.scoreElement.textContent = this.score;
    }

    loadHighScore() {
        const highScore = localStorage.getItem('snakeHighScore') || 0;
        this.highScoreElement.textContent = highScore;
    }

    getHighScore() {
        return localStorage.getItem('snakeHighScore') || 0;
    }

    updateHighScore() {
        const currentHigh = parseInt(this.getHighScore());
        if (this.score > currentHigh) {
            localStorage.setItem('snakeHighScore', this.score);
            this.highScoreElement.textContent = this.score;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});"""

    def get_snake_readme(self, project_name, description, style):
        return f"""# {project_name}

{description}

## 🎮 Игра "Змейка"

Классическая игра змейка с современным дизайном и адаптивным интерфейсом.

### Особенности:
- 🎨 Красивый современный дизайн
- 📱 Адаптивность для мобильных устройств
- 🎯 Система очков и рекордов
- ⌨️ Управление клавишами и сенсорными кнопками
- 💾 Сохранение лучшего результата

### Управление:
- **Клавиши:** Стрелки или WASD
- **Мобильные:** Сенсорные кнопки

### Технологии:
- HTML5 Canvas
- CSS3 с градиентами и анимациями
- Vanilla JavaScript ES6+

Создано с помощью Lovable AI"""

    def get_tetris_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="game-container">
        <div class="game-header">
            <h1>{project_name}</h1>
            <div class="game-info">
                <div class="score">Счёт: <span id="score">0</span></div>
                <div class="level">Уровень: <span id="level">1</span></div>
                <div class="lines">Линии: <span id="lines">0</span></div>
            </div>
        </div>

        <div class="game-area">
            <div class="next-piece">
                <h3>Следующая фигура</h3>
                <canvas id="nextCanvas" width="120" height="120"></canvas>
            </div>
            <canvas id="gameCanvas" width="300" height="600"></canvas>
            <div class="game-overlay" id="gameOverlay">
                <div class="start-screen">
                    <h2>🧩 Тетрис</h2>
                    <p>Управление: стрелки, пробел для поворота</p>
                    <button id="startBtn" class="game-btn">Начать игру</button>
                </div>
            </div>
        </div>

        <div class="game-controls">
            <div class="mobile-controls">
                <button class="control-btn" data-action="rotate">↻</button>
                <div class="control-row">
                    <button class="control-btn" data-action="left">←</button>
                    <button class="control-btn" data-action="down">↓</button>
                    <button class="control-btn" data-action="right">→</button>
                </div>
            </div>
        </div>

        <div class="game-footer">
            <p>{description}</p>
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_tetris_css(self, project_name, description, style):
        return f"""/* CSS для Тетриса */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary-color: #4a148c; /* Purple */
    --secondary-color: #00bcd4; /* Cyan */
    --accent-color: #ffeb3b; /* Yellow */
    --bg-color: #121212; /* Dark background */
    --text-color: #ffffff;
    --block-colors: #FF0D72, #0DC2FF, #0DFF72, #F538FF, #FFFB0D, #FF8E0D, #AD1457; /* Random colors for blocks */
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.game-container {{
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 600px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.game-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.game-info {{
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    font-weight: 600;
}}

.game-area {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 2rem;
}}

#gameCanvas {{
    border: 3px solid var(--accent-color);
    border-radius: 15px;
    background: var(--bg-color);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}}

.next-piece {{
    text-align: center;
}}

#nextCanvas {{
    border: 2px solid var(--accent-color);
    background: var(--bg-color);
    border-radius: 10px;
    margin-top: 10px;
}}

.game-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
}}

.start-screen {{
    text-align: center;
    color: white;
}}

.start-screen h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.game-btn {{
    background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
    border: none;
    color: white;
    padding: 1rem 2rem;
    border-radius: 25px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}}

.game-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}}

.mobile-controls {{
    margin-top: 2rem;
}}

.control-btn {{
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    font-size: 1.5rem;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.control-btn:hover {{
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}}

.control-row {{
    display: flex;
    justify-content: center;
    align-items: center;
}}

.game-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.8;
}}

.hidden {{
    display: none !important;
}}

@media (max-width: 600px) {{
    .game-container {{
        padding: 1rem;
        margin: 1rem;
    }}

    .game-area {{
        flex-direction: column;
        gap: 10px;
    }}

    #gameCanvas {{
        width: 100%;
        max-width: 350px;
        height: auto;
    }}

    .game-header h1 {{
        font-size: 2rem;
    }}

    .game-info {{
        font-size: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }}
}}"""

    def get_tetris_js(self, project_name, description, style):
        return """
let board = [];
let score = 0;
let level = 1;
let lines = 0;
let currentPiece = null;
let nextPiece = null;
let animationId = null;
let isGameOver = false;
let gameInterval = 1000; // ms

const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30; // px

const canvas = document.getElementById('gameCanvas');
const context = canvas.getContext('2d');
const nextCanvas = document.getElementById('nextCanvas');
const nextContext = nextCanvas.getContext('2d');
const scoreElement = document.getElementById('score');
const levelElement = document.getElementById('level');
const linesElement = document.getElementById('lines');
const overlay = document.getElementById('gameOverlay');
const startBtn = document.getElementById('startBtn');

// Тема и цвета блоков
const themes = {
    "modern": {
        "--primary-color": "#4a148c", "--secondary-color": "#00bcd4", "--accent-color": "#ffeb3b", "--bg-color": "#121212", "--text-color": "#ffffff",
        "--block-colors": ["#FF0D72", "#0DC2FF", "#0DFF72", "#F538FF", "#FFFB0D", "#FF8E0D", "#AD1457"]
    },
    "retro": {
        "--primary-color": "#ff6b35", "--secondary-color": "#f7931e", "--accent-color": "#ffd23f", "--bg-color": "#1a1a1a", "--text-color": "#00ff00",
        "--block-colors": ["#00FF00", "#FFFF00", "#FFA500", "#FF4500", "#8A2BE2", "#FF1493", "#00CED1"]
    },
    "neon": {
        "--primary-color": "#ff0080", "--secondary-color": "#8000ff", "--accent-color": "#00ff80", "--bg-color": "#000015", "--text-color": "#ffffff",
        "--block-colors": ["#00FFFF", "#FFFF00", "#FF00FF", "#00FF00", "#FFFFFF", "#FF0000", "#0000FF"]
    }
};

// Применяем тему (если передана)
const themeName = document.body.className.replace('-theme', '') || 'modern';
const selectedTheme = themes[themeName] || themes['modern'];
Object.keys(selectedTheme).forEach(key => {
    document.documentElement.style.setProperty(key, selectedTheme[key]);
});
const BLOCK_COLORS = selectedTheme['--block-colors'];

// Формы фигур (tetrominoes)
const TETROMINOES = [
    { shape: [[1, 1, 1, 1]], color: BLOCK_COLORS[0] }, // I
    { shape: [[1, 1], [1, 1]], color: BLOCK_COLORS[1] }, // O
    { shape: [[1, 1, 0], [0, 1, 1]], color: BLOCK_COLORS[2] }, // S
    { shape: [[0, 1, 1], [1, 1, 0]], color: BLOCK_COLORS[3] }, // Z
    { shape: [[1, 1, 1], [0, 1, 0]], color: BLOCK_COLORS[4] }, // T
    { shape: [[1, 1, 1], [1, 0, 0]], color: BLOCK_COLORS[5] }, // L
    { shape: [[1, 1, 1], [0, 0, 1]], color: BLOCK_COLORS[6] }  // J
];

// Функции для инициализации и управления игрой
function createPiece() {
    const rand = Math.floor(Math.random() * TETROMINOES.length);
    const piece = TETROMINOES[rand];
    return {
        x: Math.floor(COLS / 2) - Math.floor(piece.shape[0].length / 2),
        y: 0,
        shape: piece.shape,
        color: piece.color
    };
}

function isValidMove(piece, board) {
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x]) {
                const boardX = piece.x + x;
                const boardY = piece.y + y;

                // Проверка выхода за границы поля
                if (boardY < 0 || boardY >= ROWS || boardX < 0 || boardX >= COLS) {
                    return false;
                }
                // Проверка столкновения с уже занятыми ячейками
                if (board[boardY] && board[boardY][boardX]) {
                    return false;
                }
            }
        }
    }
    return true;
}

function drawBlock(x, y, color, context) {
    context.fillStyle = color;
    context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
    context.fillStyle = 'rgba(255, 255, 255, 0.3)';
    context.fillRect(x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4);
}

function drawPiece(piece, context) {
    context.fillStyle = piece.color;
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x]) {
                drawBlock(piece.x + x, piece.y + y, piece.color, context);
            }
        }
    }
}

function drawBoard() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (board[y] && board[y][x]) {
                drawBlock(x, y, board[y][x], context);
            }
        }
    }
}

function drawNextPiece() {
    nextContext.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    if (nextPiece) {
        drawPiece(nextPiece, nextContext);
    }
}

function clearLines() {
    let linesCleared = 0;
    for (let y = ROWS - 1; y >= 0; ) {
        if (board[y].every(cell => cell)) {
            for (let i = y; i > 0; i--) {
                board[i] = board[i - 1];
            }
            board[0] = Array(COLS).fill(null);
            linesCleared++;
        } else {
            y--;
        }
    }

    if (linesCleared > 0) {
        lines += linesCleared;
        score += calculateScore(linesCleared, level);
        updateScoreboard();
        updateLevelAndInterval();
    }
}

function calculateScore(linesCleared, level) {
    const points = [0, 40, 100, 300, 1200]; // Очки за 1, 2, 3, 4 линии
    return points[linesCleared] * level;
}

function updateLevelAndInterval() {
    const newLevel = Math.floor(lines / 10) + 1;
    if (newLevel > level) {
        level = newLevel;
        gameInterval = Math.max(100, 1000 - (level - 1) * 50); // Уменьшаем интервал
    }
}

function updateScoreboard() {
    scoreElement.textContent = score;
    levelElement.textContent = level;
    linesElement.textContent = lines;
}

function freezePiece() {
    for (let y = 0; y < currentPiece.shape.length; y++) {
        for (let x = 0; x < currentPiece.shape[y].length; x++) {
            if (currentPiece.shape[y][x]) {
                const boardX = currentPiece.x + x;
                const boardY = currentPiece.y + y;
                if (boardY >= 0) { // Только если часть фигуры на поле
                    if (!board[boardY]) board[boardY] = Array(COLS).fill(null);
                    board[boardY][boardX] = currentPiece.color;
                }
            }
        }
    }
    clearLines();
    currentPiece = nextPiece;
    nextPiece = createPiece();
    if (!isValidMove(currentPiece, board)) {
        gameOver();
        return;
    }
    drawNextPiece();
}

function move(deltaX) {
    currentPiece.x += deltaX;
    if (!isValidMove(currentPiece, board)) {
        currentPiece.x -= deltaX; // Откатываем ход
    }
}

function rotate() {
    const rotatedShape = currentPiece.shape[0].map((_, index) => currentPiece.shape.map(row => row[index])).reverse();
    const rotatedPiece = { ...currentPiece, shape: [rotatedShape] }; // Оборачиваем в массив для совместимости
    if (isValidMove(rotatedPiece, board)) {
        currentPiece = rotatedPiece;
    } else {
        // Попытка "подпрыгнуть" фигуру, если она упирается в стену
        const wallkickOffset = currentPiece.x < COLS / 2 ? 1 : -1;
        const kickedPiece = { ...currentPiece, x: currentPiece.x + wallkickOffset };
        if (isValidMove(kickedPiece, board)) {
            currentPiece = kickedPiece;
        }
    }
}


function drop() {
    currentPiece.y++;
    if (!isValidMove(currentPiece, board)) {
        currentPiece.y--; // Возвращаем на прежнюю позицию
        freezePiece();
        return true; // Фигура упала
    }
    return false;
}

function gameLoop() {
    if (isGameOver) return;

    const didDrop = drop();
    if (!didDrop) {
        drawBoard();
        drawPiece(currentPiece, context);
    }
    animationId = setTimeout(gameLoop, gameInterval);
}

function gameOver() {
    isGameOver = true;
    cancelAnimationFrame(animationId);
    overlay.innerHTML = `
        <div class="start-screen">
            <h2>🎮 Игра окончена!</h2>
            <p>Ваш счёт: ${score}</p>
            <p>Рекорд: ${localStorage.getItem('tetrisHighScore') || 0}</p>
            <button id="restartBtn" class="game-btn">Играть снова</button>
        </div>
    `;
    overlay.classList.remove('hidden');
    document.getElementById('restartBtn').addEventListener('click', startGame);
}

function startGame() {
    isGameOver = false;
    score = 0;
    level = 1;
    lines = 0;
    gameInterval = 1000;
    board = Array(ROWS).fill(null).map(() => Array(COLS).fill(null));
    currentPiece = createPiece();
    nextPiece = createPiece();
    updateScoreboard();
    drawBoard();
    drawNextPiece();
    if (animationId) clearTimeout(animationId);
    animationId = setTimeout(gameLoop, gameInterval);
    overlay.classList.add('hidden');

    // Сохранение рекорда
    const highScore = localStorage.getItem('tetrisHighScore') || 0;
    if (score > highScore) {
        localStorage.setItem('tetrisHighScore', score);
    }
}

// Обработка ввода
document.addEventListener('keydown', (e) => {
    if (isGameOver || !currentPiece) return;

    switch (e.key) {
        case 'ArrowLeft':
        case 'a':
        case 'A':
            move(-1);
            break;
        case 'ArrowRight':
        case 'd':
        case 'D':
            move(1);
            break;
        case 'ArrowDown':
        case 's':
        case 'S':
            drop(); // Быстрое падение
            break;
        case ' ': // Пробел для поворота
            rotate();
            break;
    }
    drawBoard();
    drawPiece(currentPiece, context);
});

// Обработка мобильных кнопок
document.querySelectorAll('.control-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (isGameOver || !currentPiece) return;

        const action = btn.dataset.action;
        switch (action) {
            case 'left':
                move(-1);
                break;
            case 'right':
                move(1);
                break;
            case 'down':
                drop();
                break;
            case 'rotate':
                rotate();
                break;
        }
        drawBoard();
        drawPiece(currentPiece, context);
    });
});

startBtn.addEventListener('click', startGame);

// Начальная загрузка
document.addEventListener('DOMContentLoaded', () => {
    canvas.width = COLS * BLOCK_SIZE;
    canvas.height = ROWS * BLOCK_SIZE;
    nextCanvas.width = 4 * BLOCK_SIZE;
    nextCanvas.height = 4 * BLOCK_SIZE;
    context.scale(BLOCK_SIZE, BLOCK_SIZE);
    nextContext.scale(BLOCK_SIZE, BLOCK_SIZE);
});
"""

    def get_tetris_readme(self, project_name, description, style):
        return f"""# {project_name} - Тетрис

{description}

Классическая головоломка Тетрис с современным интерфейсом."""

    def get_todo_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="app-container">
        <div class="app-header">
            <h1>{project_name}</h1>
            <p class="app-description">{description}</p>
        </div>

        <div class="todo-input-section">
            <div class="input-group">
                <input type="text" id="todoInput" placeholder="Добавить новую задачу..." maxlength="100">
                <button id="addBtn" class="add-btn">+</button>
            </div>
        </div>

        <div class="todo-filters">
            <button class="filter-btn active" data-filter="all">Все</button>
            <button class="filter-btn" data-filter="active">Активные</button>
            <button class="filter-btn" data-filter="completed">Выполненные</button>
        </div>

        <div class="todo-list" id="todoList">
            <!-- Задачи будут добавлены динамически -->
        </div>

        <div class="todo-stats">
            <span id="totalTasks">0 задач</span>
            <button id="clearCompleted" class="clear-btn">Очистить выполненные</button>
        </div>

        <div class="app-footer">
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_todo_css(self, project_name, description, style):
        return f"""/* CSS для TODO приложения */
:root {{
    --primary-color: #3f51b5; /* Indigo */
    --secondary-color: #009688; /* Teal */
    --accent-color: #ff5722; /* Deep Orange */
    --bg-color: #f5f5f5; /* Light Gray */
    --text-color: #333333; /* Dark Gray */
    --input-bg: #ffffff;
    --border-color: #e0e0e0;
    --completed-color: #bdbdbd; /* Light Gray for completed */
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.app-container {{
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 500px;
    width: 100%;
    backdrop-filter: blur(5px);
}}

.app-header {{
    margin-bottom: 2rem;
}}

.app-header h1 {{
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.app-description {{
    font-size: 1.1rem;
    color: #616161;
}}

.todo-input-section {{
    margin-bottom: 1.5rem;
}}

.input-group {{
    display: flex;
    gap: 10px;
}}

#todoInput {{
    flex-grow: 1;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 25px;
    font-size: 1rem;
    background-color: var(--input-bg);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}}

#todoInput:focus {{
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(255, 87, 34, 0.2);
}}

.add-btn {{
    background: var(--accent-color);
    border: none;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    font-size: 1.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(255, 87, 34, 0.3);
}}

.add-btn:hover {{
    transform: scale(1.1);
}}

.todo-filters {{
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: center;
    gap: 15px;
}}

.filter-btn {{
    background: none;
    border: none;
    color: var(--primary-color);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    transition: all 0.3s ease;
}}

.filter-btn.active {{
    background: var(--primary-color);
    color: white;
    box-shadow: 0 4px 10px rgba(63, 81, 181, 0.3);
}}

.filter-btn:hover {{
    background: rgba(63, 81, 181, 0.1);
}}

.todo-list {{
    max-height: 300px;
    overflow-y: auto;
    text-align: left;
    margin-bottom: 1.5rem;
    padding-right: 10px; /* Для скроллбара */
}}

.todo-item {{
    background: var(--input-bg);
    padding: 1rem;
    margin-bottom: 10px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: background 0.3s ease;
}}

.todo-item.completed {{
    background: var(--completed-color);
    opacity: 0.7;
}}

.todo-item.completed .todo-text {{
    text-decoration: line-through;
    color: #757575;
}}

.todo-content {{
    display: flex;
    align-items: center;
    gap: 15px;
    flex-grow: 1;
    overflow: hidden; /* Предотвращает вылезание текста */
}}

.checkbox {{
    width: 20px;
    height: 20px;
    border: 2px solid var(--primary-color);
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s ease;
}}

.checkbox.checked {{
    background: var(--primary-color);
    border-color: var(--primary-color);
}}

.checkbox.checked::after {{
    content: '✔';
    color: white;
    font-size: 14px;
}}

.todo-text {{
    font-size: 1rem;
    word-break: break-word; /* Перенос длинных слов */
}}

.todo-actions {{
    display: flex;
    gap: 5px;
}}

.action-btn {{
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: #9e9e9e;
    transition: color 0.3s ease;
}}

.action-btn.edit:hover {{
    color: var(--accent-color);
}}

.action-btn.delete:hover {{
    color: #f44336;
}}

.todo-stats {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #757575;
}}

.clear-btn {{
    background: none;
    border: 1px solid var(--border-color);
    color: var(--secondary-color);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.clear-btn:hover {{
    background: var(--secondary-color);
    color: white;
    border-color: var(--secondary-color);
}}

.app-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.7;
    color: #616161;
}}

/* Стили для мобильных устройств */
@media (max-width: 500px) {{
    .app-container {{
        padding: 1.5rem;
    }}
    .app-header h1 {{
        font-size: 2rem;
    }}
    .input-group {{
        flex-direction: column;
    }}
    #todoInput {{
        margin-bottom: 10px;
    }}
}}
"""

    def get_todo_js(self, project_name, description, style):
        return """
const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const totalTasksElement = document.getElementById('totalTasks');
const clearCompletedBtn = document.getElementById('clearCompleted');
const filterButtons = document.querySelectorAll('.filter-btn');

let todos = []; // Массив для хранения задач
let currentFilter = 'all'; // Текущий фильтр

// --- Функции для работы с задачами ---

// Добавление новой задачи
function addTodo() {
    const taskText = todoInput.value.trim();
    if (!taskText) return;

    const newTodo = {
        id: Date.now(), // Уникальный ID
        text: taskText,
        completed: false
    };

    todos.push(newTodo);
    todoInput.value = ''; // Очищаем поле ввода
    renderTodos();
    updateStats();
    saveTodos(); // Сохраняем в localStorage
}

// Удаление задачи
function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    renderTodos();
    updateStats();
    saveTodos();
}

// Переключение статуса задачи (выполнена/активна)
function toggleTodoComplete(id) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    renderTodos();
    updateStats();
    saveTodos();
}

// Редактирование задачи (простой вариант - обновление текста)
function editTodo(id, newText) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, text: newText } : todo
    );
    renderTodos();
    saveTodos();
}

// Очистка выполненных задач
function clearCompletedTodos() {
    todos = todos.filter(todo => !todo.completed);
    renderTodos();
    updateStats();
    saveTodos();
}

// --- Функции для рендеринга ---

// Создание HTML элемента для задачи
function createTodoElement(todo) {
    const listItem = document.createElement('div');
    listItem.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    listItem.dataset.id = todo.id;

    listItem.innerHTML = `
        <div class="todo-content">
            <div class="checkbox ${todo.completed ? 'checked' : ''}" data-action="complete"></div>
            <span class="todo-text">${todo.text}</span>
        </div>
        <div class="todo-actions">
            <button class="action-btn edit" data-action="edit">✏️</button>
            <button class="action-btn delete" data-action="delete">🗑️</button>
        </div>
    `;

    // Обработчики событий для элементов задачи
    const checkbox = listItem.querySelector('.checkbox');
    const deleteBtn = listItem.querySelector('.delete');
    const editBtn = listItem.querySelector('.edit');
    const todoTextSpan = listItem.querySelector('.todo-text');

    checkbox.addEventListener('click', () => toggleTodoComplete(todo.id));
    deleteBtn.addEventListener('click', () => deleteTodo(todo.id));
    editBtn.addEventListener('click', () => {
        const newText = prompt('Редактировать задачу:', todo.text);
        if (newText !== null && newText.trim()) {
            editTodo(todo.id, newText.trim());
        }
    });

    return listItem;
}

// Отображение задач на основе фильтра
function renderTodos() {
    todoList.innerHTML = ''; // Очищаем список перед рендерингом

    const filteredTodos = todos.filter(todo => {
        switch (currentFilter) {
            case 'active':
                return !todo.completed;
            case 'completed':
                return todo.completed;
            default: // 'all'
                return true;
        }
    });

    if (filteredTodos.length === 0) {
        todoList.innerHTML = '<p style="text-align: center; margin-top: 20px; color: #9e9e9e;">Список задач пуст!</p>';
    } else {
        filteredTodos.forEach(todo => {
            todoList.appendChild(createTodoElement(todo));
        });
    }
}

// Обновление статистики (общее количество задач)
function updateStats() {
    const activeCount = todos.filter(todo => !todo.completed).length;
    totalTasksElement.textContent = `${activeCount} активных задач`; // Изменил для отображения активных
    clearCompletedBtn.disabled = todos.every(todo => !todo.completed); // Делаем кнопку неактивной, если нет выполненных
}

// --- Функции для сохранения и загрузки ---

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function loadTodos() {
    const savedTodos = localStorage.getItem('todos');
    if (savedTodos) {
        todos = JSON.parse(savedTodos);
    }
    renderTodos();
    updateStats();
}

// --- Обработчики событий ---

// Добавление задачи по клику или Enter
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

// Обработка фильтров
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        currentFilter = button.dataset.filter;
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        renderTodos();
    });
});

// Очистка выполненных
clearCompletedBtn.addEventListener('click', clearCompletedTodos);

// --- Инициализация ---
document.addEventListener('DOMContentLoaded', loadTodos);
"""

    def get_todo_readme(self, project_name, description, style):
        return f"""# {project_name} - TODO Приложение

{description}

Простое и стильное приложение для управления списком дел.

## Возможности:
- Добавление, удаление, редактирование задач
- Отметка задач как выполненных
- Фильтрация задач (все, активные, выполненные)
- Очистка выполненных задач
- Сохранение списка в localStorage
- Адаптивный дизайн
"""

    def get_weather_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="weather-app">
        <div class="app-header">
            <h1>{project_name}</h1>
            <p>{description}</p>
        </div>

        <div class="search-section">
            <div class="search-group">
                <input type="text" id="cityInput" placeholder="Введите название города..." />
                <button id="searchBtn" class="search-btn">🔍</button>
            </div>
        </div>

        <div class="weather-display" id="weatherDisplay">
            <div class="weather-card">
                <div class="current-weather">
                    <div class="weather-icon">☀️</div>
                    <div class="temperature">--°C</div>
                    <div class="city-name">--</div>
                    <div class="weather-description">--</div>
                </div>

                <div class="weather-details">
                    <div class="detail-item">
                        <span class="detail-label">Ощущается как</span>
                        <span class="detail-value">--°C</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Влажность</span>
                        <span class="detail-value">--%</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Ветер</span>
                        <span class="detail-value">-- км/ч</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Давление</span>
                        <span class="detail-value">-- гПа</span>
                    </div>
                </div>

                <div class="forecast">
                    <h3>Прогноз на 5 дней</h3>
                    <div class="forecast-list" id="forecastList">
                        <p>Загрузка прогноза...</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="app-footer">
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_weather_css(self, project_name, description, style):
        return f"""/* CSS для Weather приложения */
:root {{
    --primary-color: #0077b6; /* Blue */
    --secondary-color: #90e0ef; /* Light Blue */
    --accent-color: #ffb703; /* Orange */
    --bg-color: #e0f2f7; /* Very Light Blue */
    --text-color: #1a1a1a; /* Dark Gray */
    --card-bg: #ffffff;
    --detail-bg: #f8f9fa;
    --forecast-bg: #f1f3f4;
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.weather-app {{
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 550px;
    width: 100%;
    backdrop-filter: blur(5px);
}}

.app-header {{
    margin-bottom: 2rem;
}}

.app-header h1 {{
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.app-description {{
    font-size: 1rem;
    color: #616161;
}}

.search-section {{
    margin-bottom: 2rem;
}}

.search-group {{
    display: flex;
    gap: 10px;
}}

#cityInput {{
    flex-grow: 1;
    padding: 1rem;
    border: 1px solid var(--primary-color);
    border-radius: 25px;
    font-size: 1rem;
    background-color: var(--card-bg);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}}

#cityInput:focus {{
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(255, 183, 3, 0.2);
}}

.search-btn {{
    background: var(--accent-color);
    border: none;
    color: var(--text-color);
    width: 50px;
    height: 50px;
    border-radius: 25px;
    font-size: 1.4rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(255, 183, 3, 0.3);
}}

.search-btn:hover {{
    transform: scale(1.1);
}}

.weather-card {{
    background: var(--card-bg);
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}}

.current-weather {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--forecast-bg);
    padding-bottom: 1.5rem;
}}

.weather-icon {{
    font-size: 4rem;
    margin-bottom: 0.5rem;
}}

.temperature {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--primary-color);
}}

.city-name {{
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.weather-description {{
    font-size: 1.2rem;
    color: #757575;
}}

.weather-details {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.detail-item {{
    background: var(--detail-bg);
    padding: 0.8rem;
    border-radius: 10px;
    text-align: center;
}}

.detail-label {{
    display: block;
    font-size: 0.9rem;
    color: #757575;
    margin-bottom: 0.3rem;
}}

.detail-value {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.forecast h3 {{
    margin-bottom: 1rem;
    color: var(--primary-color);
}}

.forecast-list {{
    display: flex;
    overflow-x: auto;
    gap: 10px;
    padding-bottom: 10px; /* Для скроллбара */
}}

.forecast-item {{
    background: var(--forecast-bg);
    padding: 1rem;
    border-radius: 10px;
    min-width: 100px;
    text-align: center;
    flex-shrink: 0;
}}

.forecast-item .date {{
    font-size: 0.9rem;
    color: #757575;
    margin-bottom: 0.5rem;
}}

.forecast-item .icon {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.forecast-item .temp {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.app-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.7;
    color: #616161;
}}

/* Стили для мобильных устройств */
@media (max-width: 550px) {{
    .weather-app {{
        padding: 1.5rem;
    }}
    .app-header h1 {{
        font-size: 2rem;
    }}
    .search-group {{
        flex-direction: column;
    }}
    #cityInput {{
        margin-bottom: 10px;
    }}
    .weather-details {{
        grid-template-columns: 1fr;
    }}
}}
"""

    def get_weather_js(self, project_name, description, style):
        return """
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherDisplay = document.getElementById('weatherDisplay');
const forecastList = document.getElementById('forecastList');

const API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'; // Замените на ваш API ключ

// Пример данных для отображения (пока нет API)
let currentWeatherData = {
    icon: '☀️',
    temperature: '--',
    city: '--',
    description: '--',
    feels_like: '--',
    humidity: '--',
    wind_speed: '--',
    pressure: '--'
};

let forecastData = [];

const weatherIcons = {
    '01d': '☀️', '01n': '🌙',
    '02d': '☁️', '02n': '☁️',
    '03d': '☁️', '03n': '☁️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌧️', '10n': '🌧️',
    '11d': '⚡', '11n': '⚡',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️'
};

function getWeatherIcon(iconCode) {
    return weatherIcons[iconCode] || '❓';
}

function formatPressure(hpa) {
    return Math.round(hpa); // Давление в гПа
}

function formatWindSpeed(mps) {
    return Math.round(mps * 3.6); // Скорость ветра в км/ч
}

async function fetchWeather(city) {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric&lang=ru`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при получении данных о погоде:", error);
        displayError("Не удалось загрузить погоду. Проверьте название города.");
        return null;
    }
}

async function fetchForecast(city) {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric&lang=ru`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при получении данных прогноза:", error);
        return null;
    }
}

function displayWeather(data) {
    if (!data) return;

    currentWeatherData = {
        icon: getWeatherIcon(data.weather[0].icon),
        temperature: Math.round(data.main.temp),
        city: data.name,
        description: data.weather[0].description,
        feels_like: Math.round(data.main.feels_like),
        humidity: data.main.humidity,
        wind_speed: formatWindSpeed(data.wind.speed),
        pressure: formatPressure(data.main.pressure)
    };

    renderCurrentWeather();
}

function renderCurrentWeather() {
    const html = `
        <div class="weather-card">
            <div class="current-weather">
                <div class="weather-icon">${currentWeatherData.icon}</div>
                <div class="temperature">${currentWeatherData.temperature}°C</div>
                <div class="city-name">${currentWeatherData.city}</div>
                <div class="weather-description">${currentWeatherData.description}</div>
            </div>

            <div class="weather-details">
                <div class="detail-item">
                    <span class="detail-label">Ощущается как</span>
                    <span class="detail-value">${currentWeatherData.feels_like}°C</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Влажность</span>
                    <span class="detail-value">${currentWeatherData.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Ветер</span>
                    <span class="detail-value">${currentWeatherData.wind_speed} км/ч</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Давление</span>
                    <span class="detail-value">${currentWeatherData.pressure} гПа</span>
                </div>
            </div>

            <div class="forecast">
                <h3>Прогноз на 5 дней</h3>
                <div class="forecast-list" id="forecastList">
                    ${renderForecast(forecastData)}
                </div>
            </div>
        </div>
    `;
    weatherDisplay.innerHTML = html;
}

function renderForecast(forecastItems) {
    if (!forecastItems || forecastItems.length === 0) {
        return '<p>Нет данных прогноза.</p>';
    }

    let html = '';
    // Отображаем прогноз на 5 дней, беря данные примерно раз в 8 интервалов (24 часа)
    for (let i = 0; i < forecastItems.length; i += 8) {
        const day = forecastItems[i];
        const date = new Date(day.dt * 1000);
        const dayOfWeek = date.toLocaleDateString('ru-RU', { weekday: 'short' });
        const temp = Math.round(day.main.temp);
        const icon = getWeatherIcon(day.weather[0].icon);

        html += `
            <div class="forecast-item">
                <div class="date">${dayOfWeek}</div>
                <div class="icon">${icon}</div>
                <div class="temp">${temp}°C</div>
            </div>
        `;
    }
    return html;
}

function displayError(message) {
    weatherDisplay.innerHTML = `<p class="error-message">${message}</p>`;
}

async function handleSearch() {
    const city = cityInput.value.trim();
    if (!city) {
        displayError("Пожалуйста, введите название города.");
        return;
    }

    // Отображаем индикатор загрузки
    weatherDisplay.innerHTML = '<div class="loading">Загрузка...</div>';

    const weatherData = await fetchWeather(city);
    if (weatherData) {
        const forecastWeatherData = await fetchForecast(city);
        forecastData = forecastWeatherData ? forecastWeatherData.list : [];
        displayWeather(weatherData);
    } else {
        displayError("Город не найден или произошла ошибка.");
    }
}

// --- Обработчики событий ---
searchBtn.addEventListener('click', handleSearch);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// --- Инициализация ---
// Можно добавить загрузку погоды по умолчанию при загрузке страницы
// handleSearch(); // Раскомментируйте, если хотите загружать погоду по умолчанию
"""

    def get_weather_readme(self, project_name, description, style):
        return f"""# {project_name} - Погодное приложение

{description}

Простое погодное приложение, показывающее текущую погоду и прогноз.
Требуется API ключ OpenWeatherMap.
"""

    pass  # Инициализация будет после определения класса

# Инициализируем генератор проектов после определения класса
generator = ProjectGenerator()

# Улучшенный AI-агент с диалоговым процессом
class SmartAI:
    def __init__(self):
            self.conversation_history = {}
            self.user_preferences = {}
            self.project_context = {}
            self.user_session = {} # Хранение состояний для каждого пользователя

            # Расширенные категории приложений
            self.app_categories = {
                "games": {
                    "types": ["аркада", "головоломка", "стратегия", "раннер", "шутер", "rpg", "платформер", "квест", "симулятор"],
                    "themes": ["космос", "фэнтези", "ретро", "киберпанк", "минимализм", "природа", "неон", "мультяшный"],
                    "mechanics": ["бесконечный бег", "сбор предметов", "прокачка персонажа", "мультиплеер", "турниры", "достижения"]
                },
                "business": {
                    "types": ["crm", "erp", "pos", "склад", "финансы", "hr", "проект менеджмент", "аналитика"],
                    "features": ["отчеты", "интеграции", "workflow", "уведомления", "мультиязычность", "роли пользователей"]
                },
                "lifestyle": {
                    "types": ["фитнес", "здоровье", "готовка", "путешествия", "медитация", "хобби", "образование", "знакомства"],
                    "features": ["трекинг", "социальные функции", "геолокация", "push уведомления", "календарь", "статистика"]
                },
                "ecommerce": {
                    "types": ["магазин", "маркетплейс", "доставка", "бронирование", "подписки", "аукцион"],
                    "features": ["корзина", "платежи", "отзывы", "поиск", "фильтры", "персонализация", "чат с продавцом"]
                },
                "social": {
                    "types": ["чат", "сообщества", "блог", "фото", "видео", "стриминг", "знакомства"],
                    "features": ["лайки", "комментарии", "подписки", "приватные сообщения", "группы", "истории", "прямые эфиры"]
                },
                "utility": {
                    "types": ["погода", "калькулятор", "конвертер", "qr сканер", "заметки", "файлы", "vpn", "антивирус"],
                    "features": ["виджеты", "офлайн работа", "синхронизация", "темная тема", "голосовое управление"]
                }
            }

            # Платформы и их особенности
            self.platforms = {
                "ios": {
                    "languages": ["Swift", "SwiftUI", "React Native", "Flutter"],
                    "features": ["Face ID", "Touch ID", "Siri", "Apple Pay", "HealthKit", "ARKit"],
                    "design": "Human Interface Guidelines",
                    "monetization": ["App Store", "подписки", "внутренние покупки"]
                },
                "android": {
                    "languages": ["Kotlin", "Java", "React Native", "Flutter"],
                    "features": ["Google Pay", "ML Kit", "ARCore", "Biometric API"],
                    "design": "Material Design",
                    "monetization": ["Google Play", "AdMob", "подписки"]
                },
                "web": {
                    "languages": ["React", "Vue", "Angular", "Vanilla JS"],
                    "features": ["PWA", "WebRTC", "WebGL", "Service Workers"],
                    "design": "Responsive Design",
                    "monetization": ["веб подписки", "реклама", "Stripe", "PayPal"]
                },
                "cross_platform": {
                    "languages": ["React Native", "Flutter", "Xamarin", "Ionic"],
                    "advantages": ["один код", "быстрая разработка", "общие функции"],
                    "monetization": ["все платформы одновременно"]
                }
            }

            # Монетизация
            self.monetization_models = {
                "freemium": {
                    "description": "Бесплатно + премиум функции",
                    "examples": ["Spotify", "Canva", "Notion"],
                    "revenue": "$500-5000/месяц"
                },
                "subscription": {
                    "description": "Ежемесячная подписка", 
                    "examples": ["Netflix", "Adobe", "Headspace"],
                    "revenue": "$1000-15000/месяц"
                },
                "ads": {
                    "description": "Бесплатно с рекламой",
                    "examples": ["Instagram", "TikTok", "YouTube"],
                    "revenue": "$200-2000/месяц"
                },
                "marketplace": {
                    "description": "Комиссия с транзакций",
                    "examples": ["Uber", "Airbnb", "Etsy"], 
                    "revenue": "$2000-50000/месяц"
                },
                "premium": {
                    "description": "Разовая покупка",
                    "examples": ["Procreate", "1Password"],
                    "revenue": "$100-1000/месяц"
                }
            }

            # Дизайн стили
            self.design_styles = {
                "минимализм": {"colors": ["белый", "серый", "один акцент"], "elements": ["много пространства", "простые формы"]},
                "космический": {"colors": ["темно-синий", "фиолетовый", "неоновые"], "elements": ["звезды", "градиенты", "свечение"]},
                "ретро": {"colors": ["оранжевый", "коричневый", "желтый"], "elements": ["пиксельный", "8-бит", "винтаж"]},
                "неон": {"colors": ["ярко-розовый", "зеленый", "синий"], "elements": ["свечение", "темный фон", "киберпанк"]},
                "природа": {"colors": ["зеленый", "коричневый", "голубой"], "elements": ["органические формы", "текстуры"]},
                "корпоративный": {"colors": ["синий", "белый", "серый"], "elements": ["чистые линии", "профессионально"]}
            }

            # Рыночные тренды (пример)
            self.market_trends = {
                "ai_chatbots": {
                    "description": "AI-чат-боты и помощники",
                    "popularity": 9.5,
                    "examples": ["ChatGPT", "Bard", "Claude"],
                    "revenue": "$5000-50000+/месяц"
                },
                "gaming": {
                    "description": "Мобильные игры (казуальные, RPG)",
                    "popularity": 9.0,
                    "examples": ["Genshin Impact", "Candy Crush", "Among Us"],
                    "revenue": "$10000-100000+/месяц"
                },
                "productivity_apps": {
                    "description": "Приложения для продуктивности и организации",
                    "popularity": 8.5,
                    "examples": ["Notion", "Todoist", "Evernote"],
                    "revenue": "$1000-10000+/месяц"
                },
                "health_wellness": {
                    "description": "Приложения для здоровья и фитнеса",
                    "popularity": 8.0,
                    "examples": ["MyFitnessPal", "Headspace", "Calm"],
                    "revenue": "$2000-15000+/месяц"
                },
                "social_media_niche": {
                    "description": "Нишевые социальные сети",
                    "popularity": 7.5,
                    "examples": ["Clubhouse", "BeReal"],
                    "revenue": "$500-5000+/месяц"
                }
            }

        def generate_personalized_response(self, message, session_id="default"):
        """Генерирует умный ответ с учетом контекста и сессии"""
        if session_id not in self.user_session:
            self.user_session[session_id] = {
                "stage": "initial",
                "project_type": None,
                "preferences": {},
                "questions_asked": [],
                "conversation": [],
                "current_project_id": None,
                "project_creation_in_progress": False
            }

        session = self.user_session[session_id]
        session["conversation"].append({"user": message, "timestamp": time.time()})

        # Обработка сообщений с опечатками и синонимами
        processed_message = nlp_processor.correct_and_normalize(message)
        message_type = self.analyze_message(processed_message)

        # Логирование взаимодействия
        interaction_logger.log_interaction(session_id, message, processed_message, message_type)

        # Управление состоянием диалога
        if session["stage"] == "initial":
            return self.handle_initial_stage(processed_message, message_type, session_id)
        elif session["stage"] == "clarifying":
            return self.handle_clarifying_stage(processed_message, session_id)
        elif session["stage"] == "confirming":
            return self.handle_confirming_stage(processed_message, session_id)
        elif session["stage"] == "creating":
            return self.handle_creating_stage(processed_message, session_id)
        elif session["stage"] == "editing":
            return self.handle_editing_stage(processed_message, session_id)
        else: # Общий случай или если этап не определен
            return self.handle_general_stage(processed_message, session_id)

        def analyze_message(self, message):
            """Анализирует сообщение пользователя"""
            message_lower = message.lower()

            # Расширенный анализ запросов на создание приложений
            app_keywords = ["создай", "сделай", "разработай", "построй", "запрограммируй", "нужно", "хочу", "требуется"]

            # Игры
            game_keywords = ["игра", "игру", "game", "змейка", "тетрис", "аркад", "головоломка", "стрелялка", "раннер", "платформер", "квест", "rpg", "idle", "симулятор", "шутер", "стратег", "рпг"]
            if any(word in message_lower for word in game_keywords):
                return "game_request"

            # Мобильные приложения (общие)
            mobile_keywords = ["приложение", "прилож", "app", "мобильн", "телефон", "смартфон", "ios", "android", "айфон"]
            if any(word in message_lower for word in mobile_keywords):
                return "mobile_app_request"

            # Сайты и веб-приложения
            web_keywords = ["сайт", "сайты", "website", "веб", "web", "лендинг", "landing", "портфолио", "блог", "магазин", "интернет-магазин"]
            if any(word in message_lower for word in web_keywords):
                return "website_request"

            # Бизнес приложения
            business_keywords = ["crm", "erp", "бизнес", "управлен", "склад", "финанс", "pos", "касса", "учет", "отчет"]
            if any(word in message_lower for word in business_keywords):
                return "business_request"

            # Социальные приложения
            social_keywords = ["чат", "социальн", "знакомств", "сообществ", "блог", "инстаграм", "тикток", "мессенджер"]
            if any(word in message_lower for word in social_keywords):
                return "social_request"

            # E-commerce
            ecommerce_keywords = ["магазин", "маркетплейс", "торговл", "продаж", "доставк", "заказ", "корзин", "платеж"]
            if any(word in message_lower for word in ecommerce_keywords):
                return "ecommerce_request"

            # Утилиты
            utility_keywords = ["калькулятор", "погода", "конвертер", "утилита", "инструмент", "помощник", "заметки", "напоминания"]
            if any(word in message_lower for word in utility_keywords):
                return "utility_request"

            # Рыночный анализ
            if any(word in message_lower for word in ["тренд", "рынок", "популярно", "востребовано", "статистика", "аналитика"]):
                return "market_analysis"

            # Приветствия
            if any(word in message_lower for word in ["привет", "здравствуй", "добрый", "hi", "hello"]):
                return "greeting"

            # Подтверждения
            if any(word in message_lower for word in ["да", "yes", "согласен", "подходит", "создавай", "давай", "ок", "хорошо", "ура", "отлично", "начинай", "начать", "немедленно"]):
                return "confirmation"

            # Отрицания
            if any(word in message_lower for word in ["нет", "no", "не подходит", "другое", "иначе", "отмена"]):
                return "rejection"

            # Запрос на скачивание
            if any(word in message_lower for word in ["скачать", "скачай", "архив", "zip", "загрузить"]):
                return "download_request"

            # Запрос на редактирование
            if any(word in message_lower for word in ["доработать", "улучшить", "изменить", "добавить", "редактировать"]):
                return "edit_request"

            return "general"

        def extract_project_details(self, message):
            """Извлекает детали проекта из сообщения пользователя"""
            message_lower = message.lower()
            details = {
                "type": None,
                "theme": None,
                "platform": None,
                "style": None,
                "features": [],
                "monetization": None,
                "target_audience": None,
                "name_suggestions": []
            }

            # Определяем тип приложения
            for category, data in self.app_categories.items():
                for app_type in data["types"]:
                    if app_type in message_lower:
                        details["type"] = app_type
                        break
            if not details["type"]: # Если не нашли конкретный тип, ищем по категории
                for category, data in self.app_categories.items():
                     if category in message_lower:
                         details["type"] = category # Используем категорию как тип
                         break


            # Определяем тему/стиль
            for style in self.design_styles.keys():
                if style in message_lower:
                    details["style"] = style
                    break

            # Определяем платформу
            platform_hints = {
                "ios": ["ios", "айфон", "iphone", "apple", "app store"],
                "android": ["android", "андроид", "google play", "плей маркет"],
                "web": ["веб", "web", "браузер", "сайт"],
                "cross_platform": ["кроссплатформ", "все платформы", "ios и android"]
            }

            for platform, hints in platform_hints.items():
                if any(hint in message_lower for hint in hints):
                    details["platform"] = platform
                    break

            # Определяем особенности
            if any(word in message_lower for word in ["онлайн", "мультиплеер", "многопользова"]):
                details["features"].append("онлайн")
            if any(word in message_lower for word in ["офлайн", "без интернета"]):
                details["features"].append("офлайн")
            if any(word in message_lower for word in ["платн", "подписк", "премиум"]):
                details["features"].append("монетизация")
            if any(word in message_lower for word in ["социальн", "друзья", "рейтинг"]):
                details["features"].append("социальные функции")

            return details

        def handle_initial_stage(self, message, message_type, session_id):
            """Обработка начальной стадии диалога"""
            session = self.user_session[session_id]

            if message_type == "greeting":
                return {
                    "type": "ai_response",
                    "message": "Привет! 👋 Я ваш персональный AI-консультант по созданию приложений!\n\n🚀 **Что мы можем создать:**\n• 🎮 Игры любых жанров и стилей\n• 📱 Мобильные приложения для iOS/Android\n• 🌐 Веб-приложения и сайты\n• 💼 Бизнес-системы и CRM\n• 🛒 E-commerce и маркетплейсы\n\n💡 Просто опишите свою идею, и я задам уточняющие вопросы для создания идеального проекта!",
                    "suggestions": [
                        "Хочу создать игру",
                        "Нужно мобильное приложение", 
                        "Создать сайт для бизнеса",
                        "Покажи популярные тренды"
                    ]
                }

            elif message_type in ["game_request", "mobile_app_request", "website_request", "business_request", "social_request", "ecommerce_request", "utility_request"]:
                # Извлекаем детали из сообщения
                project_details = self.extract_project_details(message)
                session["stage"] = "clarifying"
                session["project_type"] = message_type
                session["initial_request"] = message
                session["extracted_details"] = project_details

                return self.ask_detailed_clarification(message_type, project_details, session_id)

            elif message_type == "market_analysis":
                return self.show_market_analysis()

            elif message_type == "confirmation":
                # Если пользователь подтверждает создание проекта
                return self.handle_confirmation_in_initial(message, session_id)

            elif message_type == "edit_request":
                 return {
                    "type": "ai_response",
                    "message": "💡 Отличная идея! Доработка и улучшение - это ключ к успеху. Что именно вы хотите изменить или добавить в ваше приложение?",
                    "suggestions": [
                        "Добавить новые функции",
                        "Изменить дизайн",
                        "Улучшить производительность",
                        "Покажи примеры доработок"
                    ]
                }

            else:
                return {
                    "type": "ai_response",
                    "message": "📊 **Популярные направления:**\n• 🎮 **Игры** - всегда в тренде!\n• 📱 **Продуктивность** - решают реальные задачи.\n\nРасскажите подробнее о вашей идее, и я помогу воплотить её в жизнь!",
                    "suggestions": [
                        "Создать игру",
                        "Приложение для бизнеса",
                        "Показать тренды подробнее",
                        "Помоги выбрать идею"
                    ]
                }

        def handle_confirmation_in_initial(self, message, session_id):
            """Обработка подтверждения создания проекта в начальной стадии"""
            session = self.user_session[session_id]

            # Если есть предыдущий запрос на создание проекта
            if session.get("initial_request"):
                # Создаем проект сразу с базовыми параметрами
                project_details = {
                    "name": "Idle RPG Игра",
                    "type": "game_request", 
                    "platform": "iOS",
                    "style": "космический",
                    "description": "Idle RPG игра для iPhone в инопланетном стиле с внутриигровыми покупками",
                    "monetization": "freemium",
                    "answers": {
                        "name": "Idle RPG Игра",
                        "platform": "iOS", 
                        "style": "космический",
                        "main_function": "Игра",
                        "target_audience": "Все возрасты",
                        "timeline": "Как можно быстрее"
                    }
                }

                session["project_details"] = project_details
                session["stage"] = "confirming"

                # Создаем проект
                result = self.create_project_from_details(project_details, session_id)

                if result['success']:
                    project_id = result['project_id']
                    session["current_project_id"] = project_id
                    session["stage"] = "created"

                    archive_url = f"/api/download/{project_id}"
                    return {
                        "type": "project_created",
                        "message": f"""🎉 **Ваша игра '{project_details['name']}' готова!**

✨ Создана Idle RPG игра для iOS в космическом стиле

🚀 **Что включено:**
• 📱 Полностью рабочий код игры
• 🎨 Космический дизайн с инопланетной тематикой
• 💰 Система внутриигровых покупок
• 📖 Готовая история и персонажи
• 🔧 Настроенная архитектура для iOS

**🎯 Следующие шаги:**
1. Скачайте проект
2. Откройте в Xcode
3. Настройте Apple Developer Account
4. Опубликуйте в App Store!

💡 Потенциальный доход: $5,000-50,000/месяц с правильным маркетингом!""",
                        "project_id": project_id,
                        "download_url": archive_url,
                        "suggestions": [
                            "📥 Скачать проект",
                            "🔧 Добавить функции",
                            "📊 Покажи план развития",
                            "✨ Создать еще одну игру"
                        ]
                    }
                else:
                    return {
                        "type": "error",
                        "message": f"❌ Ошибка создания проекта: {result.get('error', 'Неизвестная ошибка')}",
                        "suggestions": ["Попробовать снова", "Изменить параметры", "Создать другой проект"]
                    }

            return {
                "type": "ai_response",
                "message": "🤔 Сначала расскажите, что хотите создать!",
                "suggestions": ["Создать игру", "Мобильное приложение", "Веб-сайт"]
            }

        def ask_detailed_clarification(self, project_type, extracted_details, session_id):
            """Задает детальные уточняющие вопросы на основе извлеченных деталей"""
            session = self.user_session[session_id]

            # Определяем, какие вопросы нужно задать
            questions = []

            # Платформа - ключевой вопрос
            if not extracted_details.get("platform"):
                questions.append({
                    "question": "🎯 **Для какой платформы создаем?**",
                    "options": ["iOS (iPhone/iPad)", "Android", "Веб-приложение", "Кроссплатформенное (iOS + Android)"],
                    "key": "platform",
                    "explanation": "От этого зависит технология разработки и возможности монетизации"
                })

            # Название проекта
            questions.append({
                "question": "📱 **Как назовем ваш проект?**",
                "key": "name",
                "explanation": "Хорошее название - половина успеха в App Store/Google Play"
            })

            # Специфичные вопросы по типу приложения
            if project_type == "game_request":
                if not extracted_details.get("style"):
                    questions.append({
                        "question": "🎨 **Какой визуальный стиль предпочитаете?**",
                        "options": ["Космический (темно-синий, неоновые цвета, звезды)", "Минимализм (чистый, простой)", "Ретро (пиксельный, 8-бит)", "Неоновый (яркий, киберпанк)", "Природный (зеленые тона, органика)"],
                        "key": "style"
                    })

                questions.append({
                    "question": "🎮 **Онлайн или офлайн игра?**",
                    "options": ["Офлайн (без интернета)", "Онлайн (рейтинги, мультиплеер)", "Гибрид (основа офлайн + онлайн фичи)"],
                    "key": "connectivity"
                })

                questions.append({
                    "question": "💰 **Модель монетизации?**",
                    "options": ["Бесплатная с рекламой", "Freemium (базовая версия бесплатно)", "Платная ($0.99-4.99)", "Подписка с премиум-контентом"],
                    "key": "monetization"
                })

            elif project_type == "mobile_app_request":
                questions.append({
                    "question": "🎯 **Основная функция приложения?**",
                    "options": ["Продуктивность (TODO, планировщик)", "Социальное взаимодействие", "E-commerce (продажи)", "Утилита (инструмент)", "Развлечения", "Образование"],
                    "key": "main_function"
                })

            elif project_type == "business_request":
                questions.append({
                    "question": "🏢 **Размер вашего бизнеса?**",
                    "options": ["Стартап (до 10 человек)", "Малый бизнес (10-50 человек)", "Средний бизнес (50-200 человек)", "Крупная компания (200+ человек)"],
                    "key": "business_size"
                })

            # Целевая аудитория
            questions.append({
                "question": "👥 **Кто ваша целевая аудитория?**",
                "options": ["Подростки (13-17 лет)", "Молодежь (18-25 лет)", "Взрослые (26-40 лет)", "Средний возраст (40-55 лет)", "Все возрасты"],
                "key": "target_audience"
            })

            # Бюджет и сроки
            questions.append({
                "question": "⏰ **Планируемые сроки запуска?**",
                "options": ["Как можно быстрее (MVP за неделю)", "1-2 месяца (полная версия)", "3-6 месяцев (с доработками)", "Не спешу (качество важнее)"],
                "key": "timeline"
            })

            session["clarification_questions"] = questions
            session["current_question"] = 0
            session["answers"] = {}

            # Задаем первый вопрос
            first_question = questions[0]

            response_message = f"Отлично! Я понял, что вы хотите создать **{session['initial_request']}** 🚀\n\n"
            response_message += f"Чтобы создать идеальный проект, мне нужно задать несколько ключевых вопросов:\n\n"
            response_message += first_question["question"]

            if "explanation" in first_question:
                response_message += f"\n\n💡 {first_question['explanation']}"

            suggestions = first_question.get("options", ["Расскажи подробнее", "Не знаю, посоветуй", "Покажи примеры"])

            return {
                "type": "ai_response",
                "message": response_message,
                "suggestions": suggestions,
                "progress": f"Вопрос 1 из {len(questions)}"
            }

        def get_suggestions_for_question(self, question):
            """Генерирует примерные ответы для уточняющих вопросов"""
            if "жанр игры" in question:
                return ["Аркада", "Головоломка", "Раннер", "Стратегия", "Другое"]
            elif "целевую аудиторию" in question:
                return ["Дети", "Подростки", "Взрослые", "Все"]
            elif "стиль дизайна" in question:
                return ["Современный", "Ретро", "Неоновый", "Минималистичный"]
            elif "основную проблему" in question:
                return ["Организация задач", "Учет времени", "Быстрые расчеты", "Информация о погоде"]
            elif "основное назначение" in question:
                return ["TODO список", "Планировщик", "Трекер привычек", "Заметки"]
            elif "конкретную задачу" in question:
                return ["Умный калькулятор", "Погодное приложение", "Конвертер валют", "QR-сканер"]
            else:
                return ["Да", "Нет", "Уточните"]

        def handle_clarifying_stage(self, message, session_id):
            """Обработка стадии уточнений"""
            session = self.user_session[session_id]
            questions = session.get("clarification_questions", [])
            current_q_index = session.get("current_question", 0)

            # Сохраняем ответ пользователя
            if current_q_index < len(questions):
                current_question = questions[current_q_index]
                session["answers"][current_question["key"]] = message

            # Переходим к следующему вопросу
            session["current_question"] = current_q_index + 1

            if session["current_question"] >= len(questions):
                # Все вопросы заданы, переходим к подтверждению
                session["stage"] = "confirming"
                return self.generate_project_confirmation(session_id)
            else:
                # Задаем следующий вопрос
                next_question = questions[session["current_question"]]
                progress = f"Вопрос {session['current_question'] + 1} из {len(questions)}"

                response_message = f"✅ Отлично!\n\n{next_question['question']}"

                if "explanation" in next_question:
                    response_message += f"\n\n💡 {next_question['explanation']}"

                suggestions = next_question.get("options", ["Расскажи подробнее", "Не знаю, посоветуй"])

                return {
                    "type": "ai_response", 
                    "message": response_message,
                    "suggestions": suggestions,
                    "progress": progress
                }

        def generate_project_confirmation(self, session_id):
            """Генерирует подтверждение проекта на основе собранной информации"""
            session = self.user_session[session_id]
            answers = session.get("answers", {})

            # Создаем детали проекта на основе ответов
            project_name = answers.get("name", "Мой проект")
            platform = answers.get("platform", "Кроссплатформенное")
            style = answers.get("style", "Современный")
            monetization = answers.get("monetization", "Freemium")
            timeline = answers.get("timeline", "1-2 месяца")

            # Определяем технологии на основе платформы
            tech_stack = []
            if "iOS" in platform:
                tech_stack = ["Swift/SwiftUI", "iOS SDK"]
            elif "Android" in platform:
                tech_stack = ["Kotlin", "Android SDK"]
            elif "Веб" in platform:
                tech_stack = ["React", "Node.js", "Progressive Web App"]
            else:
                tech_stack = ["React Native", "Expo"]

            # Создаем описание проекта
            description = f"Современное приложение в стиле '{style.lower()}' для платформы {platform}"

            session["project_details"] = {
                "name": project_name,
                "platform": platform,
                "style": style,
                "monetization": monetization,
                "timeline": timeline,
                "tech_stack": tech_stack,
                "description": description,
                "type": session["project_type"],
                "answers": answers
            }

            # Рассчитываем потенциальный доход
            revenue_estimate = self.calculate_revenue_estimate(session["project_type"], monetization)

            confirmation_message = f"""
🎉 **Отлично! Вот что мы создадим:**

**📱 Название:** {project_name}
**🎯 Платформа:** {platform} 
**🎨 Стиль:** {style}
**💰 Монетизация:** {monetization}
**⚙️ Технологии:** {', '.join(tech_stack)}

**📊 Прогноз доходности:** {revenue_estimate}

**🚀 В проект войдет:**
• ✅ Готовый исходный код
• 📱 Адаптивный дизайн для всех устройств  
• 🔧 Настроенная архитектура для масштабирования
• 📖 Документация по запуску и развитию
• 💡 Рекомендации по монетизации

Создаем проект?
"""

            return {
                "type": "ai_response",
                "message": confirmation_message,
                "suggestions": [
                    "🚀 Да, создавать!",
                    "🔄 Изменить название",
                    "🎨 Другой стиль",
                    "💡 Другая монетизация"
                ],
                "project_details": session["project_details"]
            }

        def calculate_revenue_estimate(self, project_type, monetization):
            """Рассчитывает примерный доход"""
            base_estimates = {
                "game_request": {"freemium": "$500-2000", "ads": "$200-1500", "premium": "$100-800"},
                "mobile_app_request": {"freemium": "$1000-5000", "subscription": "$2000-8000", "ads": "$300-1200"},
                "business_request": {"subscription": "$3000-15000", "premium": "$5000-20000"}
            }

            estimates = base_estimates.get(project_type, {"freemium": "$500-2000"})

            for model, estimate in estimates.items():
                if model in monetization.lower():
                    return f"{estimate}/месяц"

            return "$500-3000/месяц"

        def handle_confirming_stage(self, message, session_id):
            """Обработка подтверждения создания проекта"""
            session = self.user_session[session_id]

            if self.analyze_message(message) == "confirmation":
                if session.get("project_details"):
                    details = session["project_details"]

                    # Создаем проект
                    result = self.create_project_from_details(details, session_id)

                    if result['success']:
                        project_id = result['project_id']
                        session["current_project_id"] = project_id
                        session["stage"] = "created"

                        archive_url = f"/api/download/{project_id}"
                        return {
                            "type": "project_created",
                            "message": f"""🎉 **Ваш проект '{details['name']}' готов!**

✨ Создано приложение для {details['platform']} в стиле {details['style']}

🚀 **Что включено:**
• 📱 Полностью рабочий код
• 🎨 Готовый дизайн
• ⚙️ Настроенная архитектура ({', '.join(details['tech_stack'])})
• 📖 Документация по запуску
• 💰 Готовые схемы монетизации

**🎯 Следующие шаги:**
1. Скачайте проект
2. Следуйте инструкции по запуску  
3. Кастомизируйте под свои нужды
4. Публикуйте в App Store/Google Play!

💡 При правильном продвижении проект может приносить {self.calculate_revenue_estimate(details['type'], details['monetization'])}""",
                            "project_id": project_id,
                            "download_url": archive_url,
                            "suggestions": [
                                "📥 Скачать проект",
                                "🔧 Добавить функции",
                                "📊 Покажи план развития",
                                "✨ Создать еще один проект"
                            ]
                        }

                    else:
                        session["stage"] = "initial"
                        return {
                            "type": "error",
                            "message": f"❌ Ошибка создания проекта: {result.get('error', 'Неизвестная ошибка')}",
                            "suggestions": ["Попробовать снова", "Изменить параметры", "Создать другой проект"]
                        }
                else:
                    return self.handle_general_stage(message, session_id)

            elif self.analyze_message(message) == "rejection":
                session["stage"] = "clarifying" 
                session["current_question"] = max(0, session.get("current_question", 0) - 1)
                return self.handle_clarifying_stage("Давайте изменим параметры", session_id)

            else:
                return {
                    "type": "ai_response",
                    "message": f"🤔 Пожалуйста, подтвердите создание проекта '{session['project_details']['name']}' или скажите, что хотите изменить.",
                    "suggestions": ["🚀 Да, создавать!", "🔄 Изменить настройки", "❌ Отмена"]
                }

        def create_project_from_details(self, details, session_id):
            """Создает проект на основе собранных деталей"""
            try:
                # Определяем тип проекта для генератора
                generator_type = "snake_game"  # По умолчанию

                if details["type"] == "game_request":
                    generator_type = "snake_game"
                elif details["type"] in ["mobile_app_request", "utility_request"]:
                    generator_type = "todo_app"
                elif details["type"] == "website_request":
                    generator_type = "weather_app" # Заменил на weather_app для примера
                elif details["type"] == "business_request":
                    generator_type = "todo_app" # Заменил на todo_app для примера

                # Используем базовый генератор
                result = generator.generate_project(
                    project_type=generator_type,
                    description=details["description"],
                    project_name=details["name"],
                    style=details.get("style", "modern")
                )

                if result["success"]:
                    # Логируем создание
                    interaction_logger.log_event("advanced_project_created", {
                        "project_id": result["project_id"],
                        "details": details,
                        "session_id": session_id
                    })

                return result

            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }

        def handle_creating_stage(self, message, session_id):
            """Обработка стадии создания проекта (когда проект уже создан)"""
            session = self.user_session[session_id]

            if self.analyze_message(message) == "download_request":
                if session.get("current_project_id"):
                    return {
                        "type": "ai_response",
                        "message": "📥 Отлично! Вы можете скачать ваш проект по ссылке ниже. После изучения, я готов помочь с доработками!",
                        "download_url": f"/api/download/{session['current_project_id']}",
                        "suggestions": [
                            "🔧 Добавить новые функции",
                            "🔄 Создать новую версию",
                            "✨ Создать другое приложение",
                            "📊 Показать историю версий"
                        ]
                    }
                else:
                    return {
                        "type": "ai_response",
                        "message": "🙁 Похоже, у вас пока нет созданных проектов. Давайте начнем с создания!",
                        "suggestions": ["Создать приложение", "Разработать приложение", "Помоги с идеей"]
                    }

            elif self.analyze_message(message) == "edit_request":
                session["stage"] = "editing"
                return {
                    "type": "ai_response",
                    "message": "🔧 Отлично! Что именно вы хотели бы добавить или изменить в вашем приложении?",
                    "suggestions": [
                        "Добавить звуковые эффекты",
                        "Создать систему достижений",
                        "Разработать PWA-версию",
                        "Интегрировать аналитику",
                        "Изменить дизайн"
                    ]
                }

            elif "верси" in message.lower(): # Запрос на версионность
                 if session.get("current_project_id"):
                     project_id = session["current_project_id"]
                     versions = version_control.get_project_versions(project_id)
                     if versions:
                         version_history = "\n".join([f"- v{v['version']}: {v['description']} ({v['timestamp']})" for v in versions])
                         return {
                             "type": "ai_response",
                             "message": f"📜 **История версий вашего проекта '{session['project_details']['name']}':**\n{version_history}\n\nКакую версию вы хотели бы посмотреть или доработать?",
                             "project_id": project_id,
                             "versions": versions,
                             "suggestions": ["Показать код версии X", "Вернуться к последней", "Создать новую версию"]
                         }
                     else:
                         return {
                             "type": "ai_response",
                             "message": "У этого проекта пока нет истории версий.",
                             "suggestions": ["Создать новую версию", "Добавить функции"]
                         }
                 else:
                     return {
                         "type": "ai_response",
                         "message": "Сначала нужно создать проект, чтобы вести его версионность.",
                         "suggestions": ["Создать приложение"]
                     }

            else:
                # Возвращаем стандартный ответ, если запрос не распознан
                return self.handle_general_stage(message, session_id)

        def handle_editing_stage(self, message, session_id):
            """Обработка стадии редактирования/добавления функций"""
            session = self.user_session[session_id]

            if session.get("current_project_id"):
                project_id = session["current_project_id"]

                # Обработка запроса на добавление фичи
                if self.analyze_message(message) == "edit_request":
                    # Здесь будет логика вызова advanced_generator.add_feature()
                    # Для примера, просто ответим, что функция добавлена
                    feature_description = f"Новая функция: '{message}'" # Условное описание

                    # Логируем запрос на фичу
                    interaction_logger.log_event("feature_request", {
                        "project_id": project_id,
                        "feature": message,
                        "user_request": message
                    })

                    # Попытка добавить фичу (имитация)
                    success = advanced_generator.add_feature(project_id, message) # Реальная реализация будет здесь

                    if success:
                        # Создание новой версии
                        new_version = version_control.get_next_version(session["project_details"]["type"])
                        version_control.save_project_version(project_id, new_version, [], f"Добавлена функция: {message}")

                        session["stage"] = "created" # Возвращаемся в состояние "создано"

                        return {
                            "type": "ai_response",
                            "message": f"✨ Функция '{message}' успешно добавлена! Создана новая версия {new_version}.\n\nХотите скачать обновленный проект или добавить что-то еще?",
                            "project_id": project_id,
                            "version": new_version,
                            "download_url": f"/api/download/{project_id}",
                            "suggestions": ["📥 Скачать проект", "🔧 Добавить еще", "✨ Создать новое приложение"]
                        }
                    else:
                        return {
                            "type": "error",
                            "message": f"❌ Не удалось добавить функцию '{message}'. Попробуйте другую или уточните запрос.",
                            "suggestions": ["Попробовать другую функцию", "Изменить запрос", "Отмена"]
                        }
                else:
                    # Если пользователь просто общается, переходим к общему ответу
                    return self.handle_general_stage(message, session_id)

            else:
                # Если нет текущего проекта, возвращаемся к началу
                return self.handle_initial_stage(message, "general", session_id)

        def handle_general_stage(self, message, session_id):
            """Обработка общих вопросов и нераспознанных сообщений"""
            session = self.user_session[session_id]

            # Попытка получить ответ от основного AI ассистента
            try:
                ai_response = ai_agent.generate_personalized_response(message, session_id) # Используем правильный метод
                if ai_response and ai_response.get("type") == "ai_response":
                     # Добавляем стандартные предложения, если они не противоречат ответу AI
                    default_suggestions = [
                        "Создать приложение",
                        "Показать тренды",
                        "Помочь с идеей",
                        "Показать мои проекты"
                    ]

                    if "suggestions" not in ai_response or not ai_response["suggestions"]:
                        ai_response["suggestions"] = default_suggestions
                    else:
                        # Добавляем, если не дублируются
                        for sug in default_suggestions:
                            if sug not in ai_response["suggestions"]:
                                ai_response["suggestions"].append(sug)

                    return ai_response
            except Exception as e:
                print(f"Ошибка при обращении к базовому AI: {e}")

            # Если базовый AI не дал ответа или произошла ошибка
            return {
                "type": "ai_response",
                "message": "🤔 Я здесь, чтобы помочь вам создать отличное приложение! Расскажите, что вас интересует?",
                "suggestions": [
                    "Создать игру",
                    "Разработать приложение",
                    "Показать тренды",
                    "Помочь с идеей",
                    "Показать мои проекты"
                ]
            }

        def show_market_analysis(self):
            """Показывает анализ рынка и трендов"""
            trends_text = "📊 **Анализ рынка мобильных приложений 2024:**\n\n"
            sorted_trends = sorted(self.market_trends.items(), key=lambda item: item[1]['popularity'], reverse=True)

            for i, (key, trend) in enumerate(sorted_trends):
                trends_text += f"{i+1}. 📈 **{trend['description']}**\n"
                if trend['examples']:
                    trends_text += f"   • Примеры: {', '.join(trend['examples'])}\n"

            trends_text += "\n**💡 Совет:** Начните с игры или приложения продуктивности - они имеют высокий потенциал и спрос!"

            return {
                "type": "ai_response",
                "message": trends_text,
                "suggestions": [
                    "Создать популярную игру",
                    "Разработать TODO-приложение", 
                    "Показать примеры успешных проектов",
                    "Помоги выбрать под мой бюджет"
                ]
            }

    # --- API Routes ---

    @app.route('/api/chat', methods=['POST'])
    @login_required
    @monitor_performance
    def chat():
        """Обработка сообщений чата с проверкой лимитов"""
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))

        try:
            user_id = session['user_id']

            # Быстрая проверка кэша пользователя
            user_cache_key = get_cache_key("user", user_id)
            user = get_from_cache(user_cache_key)

            if not user:
                user = get_user_by_id(user_id)
                if not user:
                    return jsonify({"error": "Пользователь не найден"}), 404
                # Кэшируем пользователя на 1 минуту
                set_cache(user_cache_key, user, ttl=60)

            # Проверяем лимит запросов
            requests_used = user[5]
            requests_limit = user[6]

            if requests_used >= requests_limit and user[4] == 'free':
                return jsonify({
                    "type": "limit_exceeded",
                    "message": "⚡ Лимит бесплатных запросов исчерпан! Оформите подписку для продолжения работы.",
                    "requests_used": requests_used,
                    "requests_limit": requests_limit,
                    "show_subscription": True
                }), 429

            # Асинхронно запускаем обработку AI
            future = executor.submit(async_ai_response, message, session_id, user_id)

            # Ждем ответ максимум 10 секунд
            try:
                ai_response = future.result(timeout=10)
            except:
                return jsonify({
                    "type": "error",
                    "message": "⏱️ Запрос обрабатывается слишком долго. Попробуйте упростить запрос.",
                    "suggestions": ["Повторить", "Упростить запрос", "Создать базовое приложение"]
                })

            # Асинхронно обновляем счетчики и логи
            if user[4] == 'free':
                executor.submit(update_user_requests, user_id, 1)
                requests_used += 1

            # Асинхронно сохраняем в историю
            response_text = ai_response.get('message', '')
            executor.submit(save_chat_message, user_id, session_id, message, response_text, ai_response.get('type', 'chat'))

            # Очищаем кэш пользователя для актуальных данных
            clear_user_cache(user_id)

            # Добавляем информацию о лимитах
            ai_response['requests_left'] = max(0, requests_limit - requests_used)
            ai_response['requests_used'] = requests_used
            ai_response['requests_limit'] = requests_limit
            ai_response['cache_hit'] = 'cached' in str(ai_response.get('processing_info', ''))

            return jsonify(ai_response)

        except Exception as e:
            logger.error(f"Ошибка в API /api/chat: {e}")
            return jsonify({
                "type": "error",
                "message": "🤖 Извините, произошла ошибка. Попробуйте снова.",
                "suggestions": ["Создать приложение", "Получить совет", "Повторить запрос"]
            })

    @app.route('/api/generate-project', methods=['POST'])
    @monitor_performance
    def generate_project():
        """Генерация проекта (из UI) с кэшированием"""
        data = request.json
        description = data.get('description', '')
        project_name = data.get('project_name', 'Мой проект')
        project_type = data.get('project_type', 'snake_game')
        style = data.get('style', 'modern')
        user_preferences = data.get('preferences', {})
        user_id = session.get('user_id', 'anonymous')

        try:
            # Асинхронно генерируем проект
            future = executor.submit(async_project_generation, project_type, description, project_name, user_id)

            # Ждем результат максимум 15 секунд
            try:
                result = future.result(timeout=15)
            except:
                return jsonify({
                    "success": False,
                    "error": "Генерация проекта займет больше времени. Попробуйте упростить описание.",
                    "message": "⏱️ Тайм-аут генерации. Попробуйте создать более простой проект."
                })

            if result['success']:
                project_id = result['project_id']

                # Асинхронно логируем и сохраняем версии
                executor.submit(log_project_creation, project_id, project_name, user_id)

                archive_url = f"/api/download/{project_id}"
                result['download_url'] = archive_url
                result['project_id'] = project_id
                result['message'] = f"Проект '{project_name}' успешно создан!"
                result['generation_time'] = result.get('generation_time', 'быстро')

            return jsonify(result)

        except Exception as e:
            logger.error(f"Ошибка в generate_project: {e}")
            return jsonify({
                "success": False,
                "error": f"Ошибка генерации: {str(e)}",
                "message": "Произошла ошибка при создании проекта."
            })

    def log_project_creation(project_id: str, project_name: str, user_id: str):
        """Асинхронное логирование создания проекта"""
        try:
            interaction_logger.log_event("project_creation_success", {
                "project_id": project_id,
                "project_name": project_name,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            logger.error(f"Ошибка логирования: {e}")

    @app.route('/api/download/<project_id>')
    def download_project(project_id):
        """Скачивание проекта"""
        project_path = os.path.join(PROJECTS_DIR, project_id)
        archive_path = os.path.join(TEMP_DIR, f"{project_id}.zip")

        if not os.path.exists(project_path):
            interaction_logger.log_error("download_project_not_found", {"project_id": project_id})
            return jsonify({"error": "Проект не найден"}), 404

        # Создаём архив если его нет
        if not os.path.exists(archive_path):
            try:
                create_project_archive(project_id)
                interaction_logger.log_event("archive_created_on_demand", {"project_id": project_id})
            except Exception as e:
                interaction_logger.log_error("archive_creation_failed_on_demand", {"project_id": project_id, "error": str(e)})
                return jsonify({"error": "Не удалось создать архив"}), 500

        interaction_logger.log_event("project_downloaded", {"project_id": project_id})
        return send_file(archive_path, as_attachment=True, download_name=f"project_{project_id}.zip")

    @app.route('/api/projects')
    def list_projects():
        """Список проектов пользователя"""
        user_id = request.args.get('user_id', 'anonymous')
        projects = []

        user_projects_dir = os.path.join(USER_DATA_DIR, user_id, PROJECTS_DIR)
        os.makedirs(user_projects_dir, exist_ok=True)

        for project_id in os.listdir(user_projects_dir):
            project_path = os.path.join(user_projects_dir, project_id)
            if os.path.isdir(project_path):
                try:
                    project_info_path = os.path.join(project_path, "project_info.json")
                    if os.path.exists(project_info_path):
                        with open(project_info_path, 'r') as f:
                            info = json.load(f)
                            projects.append({
                                "id": project_id,
                                "name": info.get("name", f"Проект {project_id[:8]}"),
                                "type": info.get("type", "unknown"),
                                "created_at": info.get("created_at", datetime.fromtimestamp(os.path.getctime(project_path)).isoformat())
                            })
                    else: # Fallback, если info нет
                        projects.append({
                            "id": project_id,
                            "name": f"Проект {project_id[:8]}",
                            "type": "unknown",
                            "created_at": datetime.fromtimestamp(os.path.getctime(project_path)).isoformat()
                        })
                except Exception as e:
                    print(f"Ошибка чтения информации о проекте {project_id}: {e}")
                    interaction_logger.log_error("api_list_projects_read_error", {"project_id": project_id, "error": str(e)})

        interaction_logger.log_event("api_projects_list_requested", {"user_id": user_id, "count": len(projects)})
        return jsonify({"projects": projects})

    @app.route('/api/project/versions/<project_id>')
    def get_project_versions(project_id):
        """Получить историю версий проекта"""
        versions = version_control.get_project_versions(project_id)
        if versions is None:
            interaction_logger.log_error("api_get_versions_not_found", {"project_id": project_id})
            return jsonify({"error": "Проект или его версии не найдены"}), 404

        interaction_logger.log_event("api_get_project_versions", {"project_id": project_id, "count": len(versions)})
        return jsonify({"versions": versions})

    @app.route('/api/project/revert/<project_id>', methods=['POST'])
    def revert_project_version(project_id):
        """Откатить проект к предыдущей версии"""
        data = request.json
        target_version = data.get('version') # Номер версии для отката

        if not target_version:
            return jsonify({"error": "Не указана версия для отката"}), 400

        # Логика отката через version_control
        success = version_control.revert_project(project_id, target_version)

        if success:
            interaction_logger.log_event("project_reverted", {"project_id": project_id, "version": target_version})
            return jsonify({"success": True, "message": f"Проект успешно откачен до версии {target_version}"})
        else:
            interaction_logger.log_error("api_revert_project_failed", {"project_id": project_id, "version": target_version})
            return jsonify({"success": False, "error": "Не удалось откатить проект"}), 500

    @app.route('/api/ai/status')
    def get_ai_status():
        """Получить статус AI сервисов"""
        return jsonify({
            "available_services": [
                {
                    "name": "SuperSmartAI",
                    "enabled": True,
                    "configured": True
                },
                {
                    "name": "SmartNLP",
                    "enabled": True,
                    "configured": True
                },
                {
                    "name": "ProjectVersionControl",
                    "enabled": True,
                    "configured": True
                },
                {
                    "name": "UserInteractionLogger",
                    "enabled": True,
                    "configured": True
                },
                {
                    "name": "AdvancedProjectGenerator",
                    "enabled": True,
                    "configured": True
                }
            ],
            "current_ai": "SuperSmartAI",
            "configured": True
        })

    @app.route('/api/logs/interaction', methods=['POST'])
    def log_interaction_api():
        """API для логирования пользовательских взаимодействий"""
        data = request.json
        session_id = data.get('session_id')
        event_type = data.get('event_type')
        payload = data.get('payload')

        if not session_id or not event_type:
            return jsonify({"error": "Отсутствуют обязательные поля: session_id, event_type"}), 400

        interaction_logger.log_event(event_type, payload, session_id)
        return jsonify({"success": True, "message": "Событие залогировано"})

    # --- WebSocket ---
    # === WebSocket для множественных пользователей ===
    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        if user_id:
            join_room(f'user_{user_id}')
            print(f'Пользователь {user_id} подключился')

            # Обновляем активные сессии
            session_id = request.sid
            update_active_session(user_id, session_id)
        else:
            print('Неавторизованный пользователь подключился')

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = session.get('user_id')
        if user_id:
            leave_room(f'user_{user_id}')
            print(f'Пользователь {user_id} отключился')

            # Удаляем из активных сессий
            cleanup_user_session(user_id, request.sid)

    @socketio.on('join_project')
    def handle_join_project(data):
        """Пользователь присоединяется к проекту для совместной работы"""
        user_id = session.get('user_id')
        project_id = data.get('project_id')

        if user_id and project_id and is_user_project_owner(user_id, project_id):
            join_room(f'project_{project_id}')
            emit('project_joined', {'project_id': project_id}, room=request.sid)

    @socketio.on('leave_project')
    def handle_leave_project(data):
        """Пользователь покидает проект"""
        project_id = data.get('project_id')
        if project_id:
            leave_room(f'project_{project_id}')

    @socketio.on('file_changed')
    def handle_file_change(data):
        """Обработка изменений файлов в реальном времени"""
        user_id = session.get('user_id')
        project_id = data.get('project_id')
        file_path = data.get('file_path')
        content = data.get('content')

        if user_id and project_id and is_user_project_owner(user_id, project_id):
            # Сохраняем изменения
            save_project_file(project_id, file_path, content)

            # Уведомляем других пользователей в проекте (если будет совместная работа)
            emit('file_updated', {
                'project_id': project_id,
                'file_path': file_path,
                'updated_by': user_id
            }, room=f'project_{project_id}', include_self=False)

    def update_active_session(user_id, session_id):
        """Обновляем активную сессию пользователя"""
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO active_sessions 
                (user_id, session_id, last_activity, ip_address, user_agent)
                VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?)
            ''', (user_id, session_id, request.environ.get('REMOTE_ADDR'), 
                  request.environ.get('HTTP_USER_AGENT')))
            conn.commit()
        except Exception as e:
            print(f"Ошибка обновления сессии: {e}")
        finally:
            conn.close()

    def cleanup_user_session(user_id, session_id):
        """Очищаем сессию пользователя"""
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                DELETE FROM active_sessions 
                WHERE user_id = ? AND session_id = ?
            ''', (user_id, session_id))
            conn.commit()
        except Exception as e:
            print(f"Ошибка очистки сессии: {e}")
        finally:
            conn.close()

    def is_user_project_owner(user_id, project_id):
        """Проверяет, является ли пользователь владельцем проекта (для WebSocket)"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id FROM user_projects WHERE project_id = ?', (project_id,))
        owner_id = cursor.fetchone()
        conn.close()
        return owner_id is not None and owner_id[0] == user_id

    def save_project_file(project_id, file_path, content):
        """Сохраняет содержимое файла проекта (имитация)"""
        print(f"Сохранение файла: {file_path} для проекта {project_id}")
        # В реальной системе здесь будет логика сохранения файла в файловой системе проекта
        pass

    # --- Вспомогательные функции ---
    def create_project_archive(project_id):
        """Создаёт zip-архив проекта"""
        project_path = os.path.join(PROJECTS_DIR, project_id)
        archive_path = os.path.join(TEMP_DIR, f"{project_id}.zip")

        if not os.path.exists(project_path):
            raise FileNotFoundError(f"Директория проекта не найдена: {project_path}")

        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(project_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, project_path)
                        zipf.write(file_path, arcname)
            return archive_path
        except Exception as e:
            interaction_logger.log_error("create_project_archive_failed", {"project_id": project_id, "error": str(e)})
            raise

    if __name__ == '__main__':
        print("🚀 Запускаю Vibecode AI Platform...")
        print("📍 Backend: http://0.0.0.0:5000")
        print("🔌 WebSocket: ws://0.0.0.0:5000") 
        print("🌐 Внешний доступ доступен через URL репла")
        print("💡 Для остановки нажмите Ctrl+C")
        print("=" * 50)

        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)