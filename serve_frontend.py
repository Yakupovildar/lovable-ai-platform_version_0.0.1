#!/usr/bin/env python3
import http.server
import socketserver
import os
import webbrowser
from urllib.parse import urlparse
import subprocess
import time
import threading
import requests

PORT = 8000
BACKEND_PORT = 5000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def end_headers(self):
        # Добавляем CORS заголовки
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def check_backend():
    """Проверяет, запущен ли backend"""
    try:
        response = requests.get('http://0.0.0.0:5000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Запускает backend в отдельном процессе"""
    try:
        print("🚀 Запускаю backend...")
        subprocess.Popen(['python', 'backend/app.py'], cwd='.')

        # Ждем запуска backend
        for i in range(30):  # 30 секунд максимум
            if check_backend():
                print("✅ Backend успешно запущен!")
                return True
            time.sleep(1)
            print(f"⏳ Ожидание backend... ({i+1}/30)")

        print("❌ Backend не запустился за 30 секунд")
        return False
    except Exception as e:
        print(f"❌ Ошибка запуска backend: {e}")
        return False

if __name__ == '__main__':
    print("🌐 Запускаю Lovable AI Platform...")
    print("=" * 50)

    # Проверяем и запускаем backend если нужно
    if not check_backend():
        print("🔄 Backend не найден, запускаю...")
        backend_started = start_backend()
        if not backend_started:
            print("⚠️  Backend не запустился, чат может не работать")
    else:
        print("✅ Backend уже запущен!")

    print("🌐 Frontend server running at http://0.0.0.0:8000")
    print("🔗 Backend API running at http://0.0.0.0:5000")
    print("💡 Откройте браузер и перейдите по ссылке выше")
    print("=" * 50)

    with socketserver.TCPServer(("0.0.0.0", PORT), MyHTTPRequestHandler) as httpd:
        httpd.serve_forever()