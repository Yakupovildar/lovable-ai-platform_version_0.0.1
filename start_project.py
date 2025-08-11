
#!/usr/bin/env python3
import subprocess
import threading
import time
import os

def start_backend():
    """Запуск backend сервера"""
    print("🚀 Запускаю Backend сервер...")
    os.chdir('backend')
    subprocess.run(['python', 'app.py'])

def start_frontend():
    """Запуск frontend сервера"""
    print("🌐 Запускаю Frontend сервер...")
    time.sleep(2)  # Даем backend время на запуск
    subprocess.run(['python', 'serve_frontend.py'])

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Lovable AI Platform - Полный запуск")
    print("=" * 50)
    
    # Запускаем backend в отдельном потоке
    backend_thread = threading.Thread(target=start_backend)
    backend_thread.daemon = True
    backend_thread.start()
    
    # Запускаем frontend в основном потоке
    start_frontend()
