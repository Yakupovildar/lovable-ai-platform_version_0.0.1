#!/usr/bin/env python3
"""
Скрипт инициализации базы данных для проектов
"""

import sqlite3
import os

def init_database():
    """Создает таблицу hosted_projects если её нет"""
    
    db_path = 'users.db'
    
    print("🔧 Инициализация базы данных...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу hosted_projects
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hosted_projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id TEXT UNIQUE NOT NULL,
            user_id TEXT NOT NULL,
            project_name TEXT NOT NULL,
            project_type TEXT NOT NULL,
            description TEXT DEFAULT 'AI Generated Project',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'active',
            file_path TEXT,
            file_size INTEGER DEFAULT 0,
            download_count INTEGER DEFAULT 0
        )
    ''')
    
    # Создаем индекс для быстрого поиска по пользователю
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_hosted_projects_user_id 
        ON hosted_projects(user_id)
    ''')
    
    # Создаем индекс для поиска по project_id
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_hosted_projects_project_id 
        ON hosted_projects(project_id)
    ''')
    
    conn.commit()
    
    # Проверяем что таблица создалась
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hosted_projects'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        print("✅ Таблица hosted_projects успешно создана")
        
        # Подсчитаем количество проектов
        cursor.execute("SELECT COUNT(*) FROM hosted_projects")
        count = cursor.fetchone()[0]
        print(f"📊 Найдено проектов: {count}")
        
    else:
        print("❌ Ошибка создания таблицы hosted_projects")
    
    conn.close()

if __name__ == "__main__":
    init_database()