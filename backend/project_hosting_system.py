#!/usr/bin/env python3
"""
Система хостинга и превью приложений
Создает уникальные URL, QR коды, облачное хранение
"""

import os
import json
import uuid
import qrcode
import io
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sqlite3
import hashlib

# Database configuration - ЕДИНАЯ база данных для всех экземпляров
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.db')

class ProjectHostingSystem:
    """Система для хостинга и демонстрации созданных приложений"""
    
    def __init__(self):
        self.projects_dir = Path("hosted_projects")
        self.projects_dir.mkdir(exist_ok=True)
        self.base_url = os.getenv('BASE_URL', 'http://127.0.0.1:5002')
        
        # Определяем среду выполнения
        self.is_railway = os.getenv('RAILWAY_ENVIRONMENT_ID') is not None
        self.is_production = os.getenv('NODE_ENV') == 'production' or self.is_railway
        
        if self.is_railway:
            print("🚂 Running on Railway - using optimized configuration")
        
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных для хостинга"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hosted_projects (
                project_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                project_name TEXT NOT NULL,
                project_type TEXT NOT NULL,
                files TEXT NOT NULL,
                created_at REAL NOT NULL,
                last_accessed REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                is_public BOOLEAN DEFAULT 1,
                custom_domain TEXT NULL,
                qr_code TEXT NULL,
                thumbnail TEXT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def host_project(self, project_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Размещает проект в облаке и создает уникальный URL"""
        
        # Генерируем уникальный ID
        project_id = self.generate_project_id()
        
        # Создаем директорию для проекта
        project_path = self.projects_dir / project_id
        project_path.mkdir(exist_ok=True)
        
        # Сохраняем файлы проекта
        files = project_data.get('files', {})
        self.save_project_files(project_path, files)
        
        # Генерируем QR код
        qr_code_data = self.generate_qr_code(project_id)
        
        # Создаем thumbnail
        try:
            if isinstance(files, dict):
                thumbnail_data = self.generate_thumbnail(files.get('index.html', ''))
            elif isinstance(files, list):
                # Ищем index.html в списке файлов
                index_html_content = ''
                for item in files:
                    if isinstance(item, dict):
                        if item.get('name') == 'index.html' or item.get('filename') == 'index.html':
                            index_html_content = item.get('content', '')
                            break
                    elif isinstance(item, str) and 'index.html' in item:
                        index_html_content = item
                        break
                thumbnail_data = self.generate_thumbnail(index_html_content)
            else:
                print(f"⚠️ Неизвестный тип files для thumbnail: {type(files)}")
                thumbnail_data = self.generate_thumbnail('')
        except Exception as e:
            print(f"⚠️ Ошибка создания thumbnail: {e}")
            thumbnail_data = self.generate_thumbnail('')
        
        # Сохраняем в базу данных с retry механизмом для Railway
        max_retries = 3
        for attempt in range(max_retries):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                
                # Убеждаемся что таблица существует
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS hosted_projects (
                        project_id TEXT PRIMARY KEY,
                        user_id TEXT NOT NULL,
                        project_name TEXT NOT NULL,
                        project_type TEXT NOT NULL,
                        files TEXT NOT NULL,
                        created_at REAL NOT NULL,
                        last_accessed REAL NOT NULL,
                        access_count INTEGER DEFAULT 0,
                        is_public BOOLEAN DEFAULT 1,
                        custom_domain TEXT NULL,
                        qr_code TEXT NULL,
                        thumbnail TEXT NULL
                    )
                ''')
                
                cursor.execute('''
                    INSERT OR REPLACE INTO hosted_projects 
                    (project_id, user_id, project_name, project_type, files, created_at, 
                     last_accessed, qr_code, thumbnail)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    project_id,
                    user_id,
                    project_data.get('name', 'Unnamed Project'),
                    project_data.get('type', 'web_app'),
                    json.dumps(files),
                    datetime.now().timestamp(),
                    datetime.now().timestamp(),
                    qr_code_data,
                    thumbnail_data
                ))
                
                conn.commit()
                
                # Проверяем что проект действительно сохранился
                cursor.execute('SELECT project_id FROM hosted_projects WHERE project_id = ?', (project_id,))
                if cursor.fetchone():
                    print(f"✅ Project {project_id} successfully saved to database (attempt {attempt + 1})")
                    conn.close()
                    break
                else:
                    raise Exception("Project not found after insert")
                    
            except Exception as e:
                print(f"⚠️ Database save attempt {attempt + 1} failed: {e}")
                if 'conn' in locals():
                    conn.close()
                if attempt == max_retries - 1:
                    print(f"❌ Failed to save project {project_id} after {max_retries} attempts")
                    # На Railway продолжаем работу даже если база не сохранилась
                    # так как есть fallback при обслуживании
                else:
                    import time
                    time.sleep(0.1)  # Небольшая пауза перед retry
        
        # Возвращаем информацию о размещенном проекте
        return {
            'project_id': project_id,
            'live_url': f"{self.base_url}/app/{project_id}",
            'preview_url': f"{self.base_url}/preview/{project_id}",
            'qr_code': qr_code_data,
            'thumbnail': thumbnail_data,
            'files_hosted': len(files),
            'hosting_status': 'active'
        }
    
    def generate_project_id(self) -> str:
        """Генерирует уникальный читаемый ID проекта"""
        # Генерируем короткий но уникальный ID
        timestamp = str(int(datetime.now().timestamp()))[-6:]  # Последние 6 цифр времени
        random_part = str(uuid.uuid4())[:6]  # Первые 6 символов UUID
        
        return f"{timestamp}-{random_part}"
    
    def save_project_files(self, project_path: Path, files: Dict[str, str]):
        """Сохраняет файлы проекта на диск"""
        try:
            if isinstance(files, dict):
                for filename, content in files.items():
                    file_path = project_path / filename

                    # Создаем поддиректории если нужно
                    file_path.parent.mkdir(parents=True, exist_ok=True)

                    # Записываем содержимое файла
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
            else:
                print(f"⚠️ Ошибка: files не является словарем: {type(files)}")
                print(f"⚠️ Получены данные: {files}")
                # Если это список, попробуем обработать как список файлов
                if isinstance(files, list):
                    for i, item in enumerate(files):
                        if isinstance(item, dict) and 'name' in item and 'content' in item:
                            filename = item['name']
                            content = item['content']
                            file_path = project_path / filename
                            file_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                        else:
                            print(f"⚠️ Неизвестный формат файла в позиции {i}: {item}")
        except AttributeError as e:
            print(f"⚠️ Ошибка доступа к files.items(): {e}")
            print(f"⚠️ Тип данных: {type(files)}")
            print(f"⚠️ Содержимое: {files}")
            return

    def _save_single_file(self, project_path: Path, filename: str, content: str):
        """Вспомогательная функция для сохранения одного файла"""
        file_path = project_path / filename

        # Создаем поддиректории если нужно
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Сохраняем файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_qr_code(self, project_id: str) -> str:
        """Генерирует QR код для приложения"""
        app_url = f"{self.base_url}/app/{project_id}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        qr.add_data(app_url)
        qr.make(fit=True)
        
        # Создаем изображение QR кода
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Конвертируем в base64 для хранения
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return f"data:image/png;base64,{qr_code_base64}"
    
    def generate_thumbnail(self, html_content: str) -> str:
        """Генерирует thumbnail превью приложения"""
        # Простая генерация thumbnail на основе типа приложения
        # В реальной системе здесь был бы headless браузер
        
        if 'game' in html_content.lower() or 'canvas' in html_content.lower():
            thumbnail_type = '🎮'
        elif 'shop' in html_content.lower() or 'store' in html_content.lower():
            thumbnail_type = '🛒'
        elif 'portfolio' in html_content.lower():
            thumbnail_type = '💼'
        elif 'blog' in html_content.lower():
            thumbnail_type = '📝'
        elif 'dashboard' in html_content.lower():
            thumbnail_type = '📊'
        else:
            thumbnail_type = '🌐'
        
        # Создаем простой SVG thumbnail
        svg_thumbnail = f'''
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="300" height="200" fill="url(#grad1)" rx="10"/>
            <text x="150" y="100" font-family="Arial" font-size="48" fill="white" 
                  text-anchor="middle" dominant-baseline="central">{thumbnail_type}</text>
            <text x="150" y="160" font-family="Arial" font-size="14" fill="white" 
                  text-anchor="middle">AI Generated App</text>
        </svg>
        '''
        
        # Конвертируем SVG в base64
        thumbnail_base64 = base64.b64encode(svg_thumbnail.encode('utf-8')).decode('utf-8')
        
        return f"data:image/svg+xml;base64,{thumbnail_base64}"
    
    def get_project_stats(self, project_id: str) -> Dict[str, Any]:
        """Получает статистику проекта"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT project_name, project_type, created_at, last_accessed, 
                   access_count, is_public
            FROM hosted_projects 
            WHERE project_id = ?
        ''', (project_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'project_name': result[0],
                'project_type': result[1],
                'created_at': datetime.fromtimestamp(result[2]),
                'last_accessed': datetime.fromtimestamp(result[3]),
                'access_count': result[4],
                'is_public': bool(result[5]),
                'age_days': (datetime.now() - datetime.fromtimestamp(result[2])).days
            }
        
        return None
    
    def update_access_stats(self, project_id: str):
        """Обновляет статистику доступа к проекту"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE hosted_projects 
            SET last_accessed = ?, access_count = access_count + 1
            WHERE project_id = ?
        ''', (datetime.now().timestamp(), project_id))
        
        conn.commit()
        conn.close()
    
    def get_user_projects(self, user_id: str) -> List[Dict[str, Any]]:
        """Получает все проекты пользователя"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT project_id, project_name, project_type, created_at, 
                   access_count, thumbnail
            FROM hosted_projects 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        projects = []
        for result in results:
            projects.append({
                'project_id': result[0],
                'project_name': result[1],
                'project_type': result[2],
                'created_at': datetime.fromtimestamp(result[3]).strftime('%d.%m.%Y %H:%M'),
                'access_count': result[4],
                'thumbnail': result[5],
                'live_url': f"{self.base_url}/app/{result[0]}",
                'preview_url': f"{self.base_url}/preview/{result[0]}"
            })
        
        return projects
    
    def delete_project(self, project_id: str, user_id: str) -> bool:
        """Удаляет проект пользователя"""
        # Проверяем права доступа
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id FROM hosted_projects WHERE project_id = ?
        ''', (project_id,))
        
        result = cursor.fetchone()
        
        if not result or result[0] != user_id:
            conn.close()
            return False
        
        # Удаляем из базы данных
        cursor.execute('''
            DELETE FROM hosted_projects WHERE project_id = ?
        ''', (project_id,))
        
        conn.commit()
        conn.close()
        
        # Удаляем файлы с диска
        project_path = self.projects_dir / project_id
        if project_path.exists():
            import shutil
            shutil.rmtree(project_path)
        
        return True
    
    def cleanup_old_projects(self, days_old: int = 30):
        """Очистка старых неиспользуемых проектов"""
        cutoff_time = datetime.now() - timedelta(days=days_old)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Находим старые проекты
        cursor.execute('''
            SELECT project_id FROM hosted_projects 
            WHERE last_accessed < ? AND access_count < 5
        ''', (cutoff_time.timestamp(),))
        
        old_projects = cursor.fetchall()
        
        for (project_id,) in old_projects:
            # Удаляем файлы
            project_path = self.projects_dir / project_id
            if project_path.exists():
                import shutil
                shutil.rmtree(project_path)
            
            # Удаляем из базы
            cursor.execute('''
                DELETE FROM hosted_projects WHERE project_id = ?
            ''', (project_id,))
        
        conn.commit()
        conn.close()
        
        return len(old_projects)

class ProjectPreviewGenerator:
    """Генератор превью для проектов в чате"""
    
    def __init__(self, hosting_system: ProjectHostingSystem):
        self.hosting = hosting_system
    
    def generate_chat_preview(self, project_data: Dict[str, Any]) -> str:
        """Генерирует HTML превью для отображения в чате"""
        
        project_id = project_data.get('id', project_data.get('project_id', 'unknown'))
        project_name = project_data.get('name', 'Unnamed Project')
        live_url = project_data.get('hosted_url', project_data.get('live_url', '#'))
        
        # Debugging: Log the project_data to see what's being passed
        print(f"🔍 Preview generation - project_data keys: {list(project_data.keys())}")
        print(f"🔍 Preview generation - hosted_url: {project_data.get('hosted_url', 'NOT_FOUND')}")
        print(f"🔍 Preview generation - live_url: {project_data.get('live_url', 'NOT_FOUND')}")
        print(f"🔍 Preview generation - final live_url: {live_url}")
        
        thumbnail = project_data.get('thumbnail', '')
        
        preview_html = f'''
        <div class="project-preview-card" style="
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 16px;
            margin: 16px 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #1f2937;
        ">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                <div style="
                    width: 48px; 
                    height: 48px; 
                    border-radius: 8px;
                    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 20px;
                ">🎉</div>
                <div>
                    <h3 style="color: #1f2937; margin: 0; font-size: 16px; font-weight: 600;">
                        {project_name}
                    </h3>
                    <p style="color: #6b7280; margin: 4px 0 0 0; font-size: 14px;">
                        Приложение готово к использованию!
                    </p>
                </div>
            </div>
            
            <div class="preview-actions" style="
                display: flex; 
                gap: 8px; 
                flex-wrap: wrap;
                margin-top: 12px;
            ">
                <a href="{live_url}" target="_blank" style="
                    background: linear-gradient(135deg, #8b5cf6, #06b6d4);
                    color: white;
                    padding: 10px 20px;
                    border-radius: 25px;
                    text-decoration: none;
                    font-weight: bold;
                    font-size: 14px;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                    transition: transform 0.2s ease;
                ">
                    🚀 Запустить приложение
                </a>
                
                <button onclick="showQRCode('{project_id}')" style="
                    background: #f1f5f9;
                    color: #374151;
                    border: 1px solid #d1d5db;
                    padding: 8px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                ">
                    📱 QR код
                </button>
                
                <button onclick="shareProject('{live_url}')" style="
                    background: #f1f5f9;
                    color: #374151;
                    border: 1px solid #d1d5db;
                    padding: 8px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                ">
                    🔗 Поделиться
                </button>
            </div>
            
            <div style="
                margin-top: 12px;
                padding-top: 12px;
                border-top: 1px solid #e5e7eb;
                font-size: 12px;
                color: #9ca3af;
            ">
                💡 Приложение размещено в облаке и доступно по ссылке
            </div>
        </div>
        '''
        
        return preview_html
    
    def generate_mobile_qr_modal(self, project_id: str, qr_code: str) -> str:
        """Генерирует модальное окно с QR кодом"""
        
        return f'''
        <div id="qr-modal-{project_id}" class="qr-modal" style="
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
        ">
            <div style="
                background: #ffffff;
                padding: 30px;
                border-radius: 15px;
                text-align: center;
                max-width: 300px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
            ">
                <h3 style="color: #333; margin-bottom: 20px;">
                    📱 Отсканируйте QR код
                </h3>
                
                <img src="{qr_code}" alt="QR Code" style="
                    width: 200px;
                    height: 200px;
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    border-radius: 10px;
                ">
                
                <p style="color: #666; font-size: 14px; margin-bottom: 20px;">
                    Откройте камеру телефона и наведите на код
                </p>
                
                <button onclick="closeQRModal('{project_id}')" style="
                    background: #333;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 25px;
                    cursor: pointer;
                    font-size: 14px;
                ">
                    Закрыть
                </button>
            </div>
        </div>
        '''