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

class ProjectHostingSystem:
    """Система для хостинга и демонстрации созданных приложений"""
    
    def __init__(self):
        self.projects_dir = Path("hosted_projects")
        self.projects_dir.mkdir(exist_ok=True)
        self.base_url = os.getenv('BASE_URL', 'https://web-production-d498d.up.railway.app')
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных для хостинга"""
        conn = sqlite3.connect('users.db')
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
        thumbnail_data = self.generate_thumbnail(files.get('index.html', ''))
        
        # Сохраняем в базу данных
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
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
            json.dumps(list(files.keys())),
            datetime.now().timestamp(),
            datetime.now().timestamp(),
            qr_code_data,
            thumbnail_data
        ))
        
        conn.commit()
        conn.close()
        
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
        for filename, content in files.items():
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
        conn = sqlite3.connect('users.db')
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
        conn = sqlite3.connect('users.db')
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
        conn = sqlite3.connect('users.db')
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
        conn = sqlite3.connect('users.db')
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
        
        conn = sqlite3.connect('users.db')
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
        
        project_id = project_data.get('project_id', 'unknown')
        project_name = project_data.get('name', 'Unnamed Project')
        live_url = project_data.get('live_url', '#')
        thumbnail = project_data.get('thumbnail', '')
        
        preview_html = f'''
        <div class="project-preview-card" style="
            background: linear-gradient(135deg, #1a1a1a, #2a2a2a);
            border: 2px solid #00ff88;
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
            max-width: 500px;
            font-family: 'Inter', sans-serif;
        ">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <img src="{thumbnail}" alt="Preview" style="
                    width: 60px; 
                    height: 40px; 
                    border-radius: 8px;
                    object-fit: cover;
                ">
                <div>
                    <h3 style="color: #00ffff; margin: 0; font-size: 18px;">
                        🎉 {project_name}
                    </h3>
                    <p style="color: #cccccc; margin: 5px 0 0 0; font-size: 14px;">
                        Приложение готово к использованию!
                    </p>
                </div>
            </div>
            
            <div class="preview-actions" style="
                display: flex; 
                gap: 10px; 
                flex-wrap: wrap;
                margin-top: 15px;
            ">
                <a href="{live_url}" target="_blank" style="
                    background: linear-gradient(45deg, #00ff88, #00ffff);
                    color: #000000;
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
                    background: rgba(255, 255, 255, 0.1);
                    color: #ffffff;
                    border: 1px solid #00ff88;
                    padding: 10px 15px;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 14px;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                ">
                    📱 QR код
                </button>
                
                <button onclick="shareProject('{live_url}')" style="
                    background: rgba(255, 255, 255, 0.1);
                    color: #ffffff;
                    border: 1px solid #00ff88;
                    padding: 10px 15px;
                    border-radius: 20px;
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
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid rgba(0, 255, 136, 0.3);
                font-size: 12px;
                color: #999999;
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