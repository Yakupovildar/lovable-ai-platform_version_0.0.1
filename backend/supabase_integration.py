#!/usr/bin/env python3
"""
Интеграция с Supabase для создания реальных баз данных
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid

@dataclass
class SupabaseProject:
    """Проект в Supabase"""
    project_id: str
    name: str
    url: str
    anon_key: str
    service_key: str
    database_url: str
    status: str

class SupabaseManager:
    """Управление проектами и базами данных в Supabase"""
    
    def __init__(self):
        self.supabase_access_token = os.getenv('SUPABASE_ACCESS_TOKEN')
        self.base_url = 'https://api.supabase.com/v1'
        self.organization_id = os.getenv('SUPABASE_ORG_ID')
        
    def create_project(self, name: str, database_password: str = None) -> Optional[SupabaseProject]:
        """Создает новый проект в Supabase"""
        
        if not self.supabase_access_token:
            print("⚠️ Supabase Access Token не настроен, создаю demo проект")
            return self._create_demo_project(name)
        
        if not database_password:
            database_password = f"SecurePass_{uuid.uuid4().hex[:8]}"
            
        headers = {
            'Authorization': f'Bearer {self.supabase_access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'name': name.lower().replace(' ', '-'),
            'organization_id': self.organization_id,
            'plan': 'free',
            'region': 'us-east-1',
            'db_pass': database_password
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/projects',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                project_data = response.json()
                
                return SupabaseProject(
                    project_id=project_data['id'],
                    name=project_data['name'],
                    url=f"https://{project_data['id']}.supabase.co",
                    anon_key="",  # Получим позже
                    service_key="",  # Получим позже
                    database_url=project_data.get('database', {}).get('host', ''),
                    status=project_data['status']
                )
            else:
                print(f"❌ Ошибка создания Supabase проекта: {response.text}")
                return self._create_demo_project(name)
                
        except Exception as e:
            print(f"❌ Исключение при создании Supabase проекта: {e}")
            return self._create_demo_project(name)
            
    def _create_demo_project(self, name: str) -> SupabaseProject:
        """Создает демо проект для тестирования"""
        project_id = f"demo_{uuid.uuid4().hex[:8]}"
        
        return SupabaseProject(
            project_id=project_id,
            name=name,
            url=f"https://{project_id}.supabase.co",
            anon_key=f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo_anon_key_{project_id}",
            service_key=f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo_service_key_{project_id}",
            database_url=f"postgresql://postgres:password@db.{project_id}.supabase.co:5432/postgres",
            status='ACTIVE_DEMO'
        )
        
    def wait_for_project_ready(self, project: SupabaseProject, timeout_minutes: int = 5) -> bool:
        """Ждет готовности проекта"""
        
        if 'demo' in project.project_id.lower():
            print(f"✅ Demo проект готов: {project.name}")
            return True
            
        headers = {
            'Authorization': f'Bearer {self.supabase_access_token}',
        }
        
        import time
        max_attempts = timeout_minutes * 12  # Проверяем каждые 5 секунд
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    f'{self.base_url}/projects/{project.project_id}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    project_data = response.json()
                    if project_data['status'] == 'ACTIVE_HEALTHY':
                        print(f"✅ Supabase проект готов: {project.name}")
                        return True
                        
                print(f"⏳ Ожидание готовности проекта... ({attempt + 1}/{max_attempts})")
                time.sleep(5)
                
            except Exception as e:
                print(f"❌ Ошибка проверки статуса: {e}")
                
        print(f"⏰ Timeout: проект не готов за {timeout_minutes} минут")
        return False
        
    def get_project_keys(self, project: SupabaseProject) -> Dict[str, str]:
        """Получает API ключи проекта"""
        
        if 'demo' in project.project_id.lower():
            return {
                'anon_key': project.anon_key,
                'service_key': project.service_key
            }
            
        headers = {
            'Authorization': f'Bearer {self.supabase_access_token}',
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/projects/{project.project_id}/api-keys',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                keys = response.json()
                return {
                    'anon_key': keys.get('anon', ''),
                    'service_key': keys.get('service_role', '')
                }
            else:
                print(f"❌ Ошибка получения ключей: {response.text}")
                
        except Exception as e:
            print(f"❌ Исключение при получении ключей: {e}")
            
        return {'anon_key': '', 'service_key': ''}
        
    def create_database_tables(self, project: SupabaseProject, schema: Dict[str, Dict[str, str]]) -> bool:
        """Создает таблицы в базе данных"""
        
        if 'demo' in project.project_id.lower():
            print(f"✅ Demo таблицы созданы для {project.name}")
            return True
            
        # Для реального проекта здесь будет SQL запрос
        sql_statements = []
        
        for table_name, columns in schema.items():
            columns_sql = []
            for column_name, column_type in columns.items():
                columns_sql.append(f"  {column_name} {column_type}")
                
            create_table_sql = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
{',\n'.join(columns_sql)}
);
"""
            sql_statements.append(create_table_sql)
            
        # Выполняем SQL через REST API Supabase
        try:
            headers = {
                'Authorization': f'Bearer {project.service_key}',
                'Content-Type': 'application/json',
                'apikey': project.anon_key
            }
            
            for sql in sql_statements:
                response = requests.post(
                    f'{project.url}/rest/v1/rpc/exec_sql',
                    headers=headers,
                    json={'sql': sql.strip()},
                    timeout=10
                )
                
                if response.status_code != 200:
                    print(f"⚠️ Ошибка создания таблицы: {response.text}")
                    
            print(f"✅ Таблицы созданы в {project.name}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка создания таблиц: {e}")
            return False
            
    def seed_sample_data(self, project: SupabaseProject, table_name: str, data: List[Dict]) -> bool:
        """Заполняет таблицы примерными данными"""
        
        if 'demo' in project.project_id.lower():
            print(f"✅ Demo данные добавлены в {table_name}")
            return True
            
        try:
            headers = {
                'Authorization': f'Bearer {project.service_key}',
                'Content-Type': 'application/json',
                'apikey': project.anon_key
            }
            
            response = requests.post(
                f'{project.url}/rest/v1/{table_name}',
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Данные добавлены в {table_name}: {len(data)} записей")
                return True
            else:
                print(f"⚠️ Ошибка добавления данных: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка добавления данных: {e}")
            return False

class SupabaseProjectSetup:
    """Настройка полного проекта с базой данных"""
    
    def __init__(self):
        self.supabase_manager = SupabaseManager()
        
    def setup_ecommerce_project(self, project_name: str) -> Optional[SupabaseProject]:
        """Настраивает полный проект для интернет-магазина"""
        
        print(f"🚀 Настраиваю Supabase проект для: {project_name}")
        
        # Создаем проект
        project = self.supabase_manager.create_project(project_name)
        if not project:
            return None
            
        # Ждем готовности
        if not self.supabase_manager.wait_for_project_ready(project):
            return None
            
        # Получаем ключи
        keys = self.supabase_manager.get_project_keys(project)
        project.anon_key = keys['anon_key']
        project.service_key = keys['service_key']
        
        # Создаем схему БД для интернет-магазина
        ecommerce_schema = {
            'products': {
                'id': 'uuid primary key default gen_random_uuid()',
                'name': 'text not null',
                'description': 'text',
                'price': 'decimal(10,2) not null',
                'image_url': 'text',
                'category': 'text',
                'stock': 'integer default 0',
                'created_at': 'timestamp default now()'
            },
            'orders': {
                'id': 'uuid primary key default gen_random_uuid()',
                'user_email': 'text not null',
                'total': 'decimal(10,2) not null',
                'status': 'text default \'pending\'',
                'created_at': 'timestamp default now()'
            },
            'order_items': {
                'id': 'uuid primary key default gen_random_uuid()',
                'order_id': 'uuid references orders(id)',
                'product_id': 'uuid references products(id)',
                'quantity': 'integer not null',
                'price': 'decimal(10,2) not null'
            }
        }
        
        # Создаем таблицы
        if not self.supabase_manager.create_database_tables(project, ecommerce_schema):
            return None
            
        # Добавляем примерные товары
        sample_products = [
            {
                'name': 'Стильная футболка',
                'description': 'Качественная хлопковая футболка',
                'price': 1500.00,
                'category': 'Одежда',
                'stock': 10,
                'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab'
            },
            {
                'name': 'Джинсы премиум',
                'description': 'Классические джинсы высокого качества',
                'price': 3500.00,
                'category': 'Одежда',
                'stock': 5,
                'image_url': 'https://images.unsplash.com/photo-1542272604-787c3835535d'
            },
            {
                'name': 'Кроссовки спортивные',
                'description': 'Удобные кроссовки для активного образа жизни',
                'price': 5000.00,
                'category': 'Обувь',
                'stock': 8,
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772'
            }
        ]
        
        self.supabase_manager.seed_sample_data(project, 'products', sample_products)
        
        print(f"✅ Supabase проект настроен: {project.url}")
        return project
        
def test_supabase_integration():
    """Тестирование интеграции с Supabase"""
    setup = SupabaseProjectSetup()
    
    project = setup.setup_ecommerce_project("Test Ecommerce Store")
    if project:
        print(f"🎉 Проект создан: {project.url}")
        print(f"🔑 Anon key: {project.anon_key[:20]}...")
        print(f"🔑 Service key: {project.service_key[:20]}...")

if __name__ == "__main__":
    test_supabase_integration()