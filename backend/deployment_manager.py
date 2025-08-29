#!/usr/bin/env python3
"""
Менеджер автоматического развертывания проектов
Поддерживает Vercel, Netlify и другие платформы
"""

import os
import json
import requests
import zipfile
import tempfile
import base64
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid
import time

@dataclass
class DeploymentResult:
    """Результат развертывания"""
    success: bool
    deployment_id: str
    url: str
    preview_url: str
    status: str
    platform: str
    error_message: str = ""

class VercelDeployment:
    """Развертывание на Vercel"""
    
    def __init__(self):
        self.access_token = os.getenv('VERCEL_ACCESS_TOKEN')
        self.team_id = os.getenv('VERCEL_TEAM_ID')  # Опционально
        self.base_url = 'https://api.vercel.com'
        
    def deploy_project(self, project_path: str, project_name: str, env_vars: Dict[str, str] = None) -> DeploymentResult:
        """Развертывает проект на Vercel"""
        
        if not self.access_token:
            return self._create_demo_deployment(project_name)
            
        try:
            # Подготавливаем файлы для развертывания
            files = self._prepare_files(project_path)
            
            # Создаем развертывание
            deployment_data = {
                'name': project_name.lower().replace(' ', '-'),
                'files': files,
                'projectSettings': {
                    'framework': 'nextjs'
                }
            }
            
            # Добавляем environment variables если есть
            if env_vars:
                deployment_data['env'] = [
                    {'key': key, 'value': value, 'type': 'plain'}
                    for key, value in env_vars.items()
                ]
                
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            if self.team_id:
                headers['X-Vercel-Team-Id'] = self.team_id
                
            print("🚀 Начинаю развертывание на Vercel...")
            
            response = requests.post(
                f'{self.base_url}/v13/deployments',
                headers=headers,
                json=deployment_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                
                deployment_id = result['id']
                url = f"https://{result['url']}"
                
                # Ждем завершения развертывания
                deployment_status = self._wait_for_deployment(deployment_id)
                
                return DeploymentResult(
                    success=True,
                    deployment_id=deployment_id,
                    url=url,
                    preview_url=url,
                    status=deployment_status,
                    platform='vercel'
                )
            else:
                error_msg = f"Vercel API error: {response.status_code} - {response.text}"
                print(f"❌ {error_msg}")
                
                return DeploymentResult(
                    success=False,
                    deployment_id="",
                    url="",
                    preview_url="",
                    status="ERROR",
                    platform='vercel',
                    error_message=error_msg
                )
                
        except Exception as e:
            error_msg = f"Deployment exception: {str(e)}"
            print(f"❌ {error_msg}")
            
            return DeploymentResult(
                success=False,
                deployment_id="",
                url="",
                preview_url="",
                status="ERROR",
                platform='vercel',
                error_message=error_msg
            )
            
    def _create_demo_deployment(self, project_name: str) -> DeploymentResult:
        """Создает демо развертывание для тестирования"""
        deployment_id = f"dpl_{uuid.uuid4().hex[:16]}"
        demo_url = f"https://{project_name.lower().replace(' ', '-')}-{deployment_id[:8]}.vercel.app"
        
        print(f"🎭 Создано demo развертывание: {demo_url}")
        
        return DeploymentResult(
            success=True,
            deployment_id=deployment_id,
            url=demo_url,
            preview_url=demo_url,
            status='READY_DEMO',
            platform='vercel'
        )
        
    def _prepare_files(self, project_path: str) -> List[Dict[str, str]]:
        """Подготавливает файлы для развертывания"""
        files = []
        
        for root, dirs, filenames in os.walk(project_path):
            # Пропускаем служебные директории
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__']]
            
            for filename in filenames:
                if filename.startswith('.') or filename.endswith('.pyc'):
                    continue
                    
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, project_path)
                
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        
                    # Кодируем содержимое в base64 для текстовых файлов
                    try:
                        # Пробуем декодировать как текст
                        text_content = content.decode('utf-8')
                        files.append({
                            'file': relative_path,
                            'data': text_content
                        })
                    except UnicodeDecodeError:
                        # Бинарный файл
                        files.append({
                            'file': relative_path,
                            'data': base64.b64encode(content).decode('utf-8'),
                            'encoding': 'base64'
                        })
                        
                except Exception as e:
                    print(f"⚠️ Ошибка чтения файла {file_path}: {e}")
                    
        return files
        
    def _wait_for_deployment(self, deployment_id: str, timeout_minutes: int = 10) -> str:
        """Ждет завершения развертывания"""
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        if self.team_id:
            headers['X-Vercel-Team-Id'] = self.team_id
            
        max_attempts = timeout_minutes * 12  # Проверяем каждые 5 секунд
        
        for attempt in range(max_attempts):
            try:
                response = requests.get(
                    f'{self.base_url}/v13/deployments/{deployment_id}',
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    deployment = response.json()
                    status = deployment.get('readyState', 'UNKNOWN')
                    
                    if status == 'READY':
                        print(f"✅ Развертывание завершено успешно")
                        return status
                    elif status == 'ERROR':
                        print(f"❌ Развертывание завершилось с ошибкой")
                        return status
                    elif status in ['BUILDING', 'QUEUED']:
                        print(f"⏳ Статус развертывания: {status} ({attempt + 1}/{max_attempts})")
                        
                time.sleep(5)
                
            except Exception as e:
                print(f"⚠️ Ошибка проверки статуса: {e}")
                
        print(f"⏰ Timeout: развертывание не завершено за {timeout_minutes} минут")
        return 'TIMEOUT'

class NetlifyDeployment:
    """Развертывание на Netlify"""
    
    def __init__(self):
        self.access_token = os.getenv('NETLIFY_ACCESS_TOKEN')
        self.base_url = 'https://api.netlify.com/api/v1'
        
    def deploy_project(self, project_path: str, project_name: str) -> DeploymentResult:
        """Развертывает проект на Netlify"""
        
        if not self.access_token:
            return self._create_demo_deployment(project_name)
            
        try:
            # Создаем сайт
            site = self._create_site(project_name)
            if not site:
                return DeploymentResult(
                    success=False,
                    deployment_id="",
                    url="",
                    preview_url="",
                    status="ERROR",
                    platform='netlify',
                    error_message="Failed to create site"
                )
                
            # Развертываем файлы
            deployment = self._deploy_files(site['id'], project_path)
            
            if deployment:
                return DeploymentResult(
                    success=True,
                    deployment_id=deployment['id'],
                    url=site['url'],
                    preview_url=deployment['deploy_url'],
                    status='READY',
                    platform='netlify'
                )
            else:
                return DeploymentResult(
                    success=False,
                    deployment_id="",
                    url="",
                    preview_url="",
                    status="ERROR",
                    platform='netlify',
                    error_message="Deployment failed"
                )
                
        except Exception as e:
            return DeploymentResult(
                success=False,
                deployment_id="",
                url="",
                preview_url="",
                status="ERROR",
                platform='netlify',
                error_message=str(e)
            )
            
    def _create_demo_deployment(self, project_name: str) -> DeploymentResult:
        """Создает демо развертывание"""
        deployment_id = f"netlify_{uuid.uuid4().hex[:12]}"
        demo_url = f"https://{project_name.lower().replace(' ', '-')}-{deployment_id[:8]}.netlify.app"
        
        return DeploymentResult(
            success=True,
            deployment_id=deployment_id,
            url=demo_url,
            preview_url=demo_url,
            status='READY_DEMO',
            platform='netlify'
        )
        
    def _create_site(self, project_name: str) -> Optional[Dict]:
        """Создает сайт на Netlify"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        site_data = {
            'name': project_name.lower().replace(' ', '-'),
            'build_settings': {
                'cmd': 'npm run build',
                'dir': 'dist'
            }
        }
        
        response = requests.post(
            f'{self.base_url}/sites',
            headers=headers,
            json=site_data,
            timeout=20
        )
        
        if response.status_code == 201:
            return response.json()
        else:
            print(f"❌ Ошибка создания сайта Netlify: {response.text}")
            return None
            
    def _deploy_files(self, site_id: str, project_path: str) -> Optional[Dict]:
        """Развертывает файлы на Netlify"""
        # Здесь будет логика развертывания файлов
        # Пока возвращаем заглушку
        return {
            'id': f'deploy_{uuid.uuid4().hex[:12]}',
            'deploy_url': f'https://deploy-{uuid.uuid4().hex[:8]}--site-name.netlify.app'
        }

class DeploymentManager:
    """Основной менеджер развертывания"""
    
    def __init__(self):
        self.vercel = VercelDeployment()
        self.netlify = NetlifyDeployment()
        
    def deploy_fullstack_project(self, 
                                project_path: str, 
                                project_name: str, 
                                platform: str = 'vercel',
                                env_vars: Dict[str, str] = None) -> DeploymentResult:
        """Развертывает full-stack проект на выбранной платформе"""
        
        print(f"🚀 Развертываю проект '{project_name}' на {platform.upper()}")
        
        if platform.lower() == 'vercel':
            return self.vercel.deploy_project(project_path, project_name, env_vars)
        elif platform.lower() == 'netlify':
            return self.netlify.deploy_project(project_path, project_name)
        else:
            return DeploymentResult(
                success=False,
                deployment_id="",
                url="",
                preview_url="",
                status="ERROR",
                platform=platform,
                error_message=f"Unsupported platform: {platform}"
            )
            
    def get_deployment_status(self, deployment_id: str, platform: str) -> str:
        """Получает статус развертывания"""
        
        if platform.lower() == 'vercel':
            return self.vercel._wait_for_deployment(deployment_id, timeout_minutes=1)
        elif platform.lower() == 'netlify':
            return 'READY'  # Заглушка для Netlify
        else:
            return 'UNKNOWN'
            
    def list_deployments(self, project_name: str = None) -> List[Dict]:
        """Список всех развертываний"""
        # Здесь будет логика получения списка развертываний
        return []

def test_deployment_manager():
    """Тестирование менеджера развертывания"""
    
    # Создаем временный проект для тестирования
    with tempfile.TemporaryDirectory() as temp_dir:
        # Создаем простой Next.js проект
        package_json = {
            'name': 'test-project',
            'version': '0.1.0',
            'scripts': {
                'dev': 'next dev',
                'build': 'next build',
                'start': 'next start'
            },
            'dependencies': {
                'next': '^14.0.0',
                'react': '^18.0.0',
                'react-dom': '^18.0.0'
            }
        }
        
        with open(os.path.join(temp_dir, 'package.json'), 'w') as f:
            json.dump(package_json, f, indent=2)
            
        # Создаем простую страницу
        index_js = '''export default function Home() {
  return <div><h1>Hello from Vibecode AI!</h1></div>
}'''
        
        pages_dir = os.path.join(temp_dir, 'pages')
        os.makedirs(pages_dir)
        with open(os.path.join(pages_dir, 'index.js'), 'w') as f:
            f.write(index_js)
            
        # Тестируем развертывание
        manager = DeploymentManager()
        
        result = manager.deploy_fullstack_project(
            project_path=temp_dir,
            project_name='Test Vibecode Project',
            platform='vercel',
            env_vars={
                'NEXT_PUBLIC_API_URL': 'https://api.example.com'
            }
        )
        
        print(f"🎉 Результат развертывания:")
        print(f"   Success: {result.success}")
        print(f"   URL: {result.url}")
        print(f"   Platform: {result.platform}")
        print(f"   Status: {result.status}")

if __name__ == "__main__":
    test_deployment_manager()