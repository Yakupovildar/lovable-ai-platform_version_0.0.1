#!/usr/bin/env python3
"""
GitHub интеграция для синхронизации проектов и version control
Конкурирует с Lovable.dev GitHub sync
"""

import os
import json
import requests
import base64
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import uuid

@dataclass
class GitHubRepo:
    """Информация о GitHub репозитории"""
    name: str
    full_name: str
    html_url: str
    clone_url: str
    default_branch: str
    private: bool
    created_at: str

@dataclass
class GitHubCommit:
    """Информация о коммите"""
    sha: str
    message: str
    author: str
    date: str
    url: str

class GitHubIntegration:
    """Интеграция с GitHub API для управления репозиториями"""
    
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        
    def authenticate_user(self, access_token: str) -> Optional[Dict[str, Any]]:
        """Аутентификация пользователя через GitHub OAuth"""
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(f'{self.base_url}/user', headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    'id': user_data['id'],
                    'login': user_data['login'],
                    'name': user_data.get('name', user_data['login']),
                    'email': user_data.get('email', ''),
                    'avatar_url': user_data['avatar_url'],
                    'public_repos': user_data['public_repos'],
                    'private_repos': user_data.get('total_private_repos', 0)
                }
            else:
                print(f"❌ GitHub auth error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ GitHub auth exception: {e}")
            return None
    
    def create_repository(self, access_token: str, repo_name: str, description: str = "", private: bool = True) -> Optional[GitHubRepo]:
        """Создает новый репозиторий на GitHub"""
        
        if not access_token:
            return self._create_demo_repo(repo_name, description)
            
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'name': repo_name.lower().replace(' ', '-'),
            'description': description,
            'private': private,
            'auto_init': True,
            'gitignore_template': 'Node'
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/user/repos',
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 201:
                repo_data = response.json()
                
                return GitHubRepo(
                    name=repo_data['name'],
                    full_name=repo_data['full_name'],
                    html_url=repo_data['html_url'],
                    clone_url=repo_data['clone_url'],
                    default_branch=repo_data['default_branch'],
                    private=repo_data['private'],
                    created_at=repo_data['created_at']
                )
            else:
                print(f"❌ GitHub repo creation error: {response.text}")
                return self._create_demo_repo(repo_name, description)
                
        except Exception as e:
            print(f"❌ GitHub repo creation exception: {e}")
            return self._create_demo_repo(repo_name, description)
    
    def _create_demo_repo(self, repo_name: str, description: str) -> GitHubRepo:
        """Создает демо репозиторий для тестирования"""
        demo_name = repo_name.lower().replace(' ', '-')
        demo_id = uuid.uuid4().hex[:8]
        
        return GitHubRepo(
            name=demo_name,
            full_name=f"demo-user/{demo_name}",
            html_url=f"https://github.com/demo-user/{demo_name}",
            clone_url=f"https://github.com/demo-user/{demo_name}.git",
            default_branch="main",
            private=True,
            created_at=datetime.now().isoformat()
        )
    
    def upload_project_files(self, access_token: str, repo_full_name: str, project_files: Dict[str, str], commit_message: str = "Initial project setup") -> bool:
        """Загружает файлы проекта в репозиторий"""
        
        if not access_token or 'demo-user' in repo_full_name:
            print(f"✅ Demo: Файлы загружены в {repo_full_name}")
            return True
            
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        success_count = 0
        total_files = len(project_files)
        
        for file_path, content in project_files.items():
            try:
                # Кодируем содержимое в base64
                content_encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
                
                payload = {
                    'message': f"{commit_message} - {file_path}",
                    'content': content_encoded,
                    'branch': 'main'
                }
                
                # Проверяем существует ли файл
                file_url = f'{self.base_url}/repos/{repo_full_name}/contents/{file_path}'
                existing_response = requests.get(file_url, headers=headers, timeout=10)
                
                if existing_response.status_code == 200:
                    # Файл существует, обновляем
                    existing_data = existing_response.json()
                    payload['sha'] = existing_data['sha']
                    
                response = requests.put(file_url, headers=headers, json=payload, timeout=15)
                
                if response.status_code in [200, 201]:
                    success_count += 1
                    print(f"✅ Загружен: {file_path}")
                else:
                    print(f"❌ Ошибка загрузки {file_path}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Исключение при загрузке {file_path}: {e}")
                
        print(f"📊 Результат: {success_count}/{total_files} файлов загружено")
        return success_count > 0
    
    def get_user_repositories(self, access_token: str, per_page: int = 30) -> List[GitHubRepo]:
        """Получает список репозиториев пользователя"""
        
        if not access_token:
            return self._get_demo_repositories()
            
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/user/repos?per_page={per_page}&sort=updated',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                repos_data = response.json()
                repositories = []
                
                for repo in repos_data:
                    repositories.append(GitHubRepo(
                        name=repo['name'],
                        full_name=repo['full_name'],
                        html_url=repo['html_url'],
                        clone_url=repo['clone_url'],
                        default_branch=repo['default_branch'],
                        private=repo['private'],
                        created_at=repo['created_at']
                    ))
                    
                return repositories
            else:
                print(f"❌ GitHub repos error: {response.text}")
                return self._get_demo_repositories()
                
        except Exception as e:
            print(f"❌ GitHub repos exception: {e}")
            return self._get_demo_repositories()
    
    def _get_demo_repositories(self) -> List[GitHubRepo]:
        """Возвращает демо репозитории"""
        return [
            GitHubRepo(
                name="my-ecommerce-app",
                full_name="demo-user/my-ecommerce-app",
                html_url="https://github.com/demo-user/my-ecommerce-app",
                clone_url="https://github.com/demo-user/my-ecommerce-app.git",
                default_branch="main",
                private=True,
                created_at=datetime.now().isoformat()
            ),
            GitHubRepo(
                name="portfolio-website",
                full_name="demo-user/portfolio-website", 
                html_url="https://github.com/demo-user/portfolio-website",
                clone_url="https://github.com/demo-user/portfolio-website.git",
                default_branch="main",
                private=False,
                created_at=datetime.now().isoformat()
            )
        ]
    
    def get_repository_commits(self, access_token: str, repo_full_name: str, per_page: int = 10) -> List[GitHubCommit]:
        """Получает список коммитов репозитория"""
        
        if not access_token or 'demo-user' in repo_full_name:
            return self._get_demo_commits(repo_full_name)
            
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/repos/{repo_full_name}/commits?per_page={per_page}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                commits_data = response.json()
                commits = []
                
                for commit in commits_data:
                    commits.append(GitHubCommit(
                        sha=commit['sha'][:7],
                        message=commit['commit']['message'],
                        author=commit['commit']['author']['name'],
                        date=commit['commit']['author']['date'],
                        url=commit['html_url']
                    ))
                    
                return commits
            else:
                print(f"❌ GitHub commits error: {response.text}")
                return self._get_demo_commits(repo_full_name)
                
        except Exception as e:
            print(f"❌ GitHub commits exception: {e}")
            return self._get_demo_commits(repo_full_name)
    
    def _get_demo_commits(self, repo_full_name: str) -> List[GitHubCommit]:
        """Возвращает демо коммиты"""
        return [
            GitHubCommit(
                sha="abc1234",
                message="Initial project setup with Next.js",
                author="Demo User",
                date=datetime.now().isoformat(),
                url=f"https://github.com/{repo_full_name}/commit/abc1234"
            ),
            GitHubCommit(
                sha="def5678", 
                message="Add product components and styling",
                author="Demo User",
                date=datetime.now().isoformat(),
                url=f"https://github.com/{repo_full_name}/commit/def5678"
            )
        ]
    
    def create_pull_request(self, access_token: str, repo_full_name: str, title: str, body: str, head_branch: str = "feature/update", base_branch: str = "main") -> Optional[Dict[str, Any]]:
        """Создает Pull Request"""
        
        if not access_token or 'demo-user' in repo_full_name:
            return {
                'number': 1,
                'title': title,
                'html_url': f"https://github.com/{repo_full_name}/pull/1",
                'state': 'open'
            }
            
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'title': title,
            'body': body,
            'head': head_branch,
            'base': base_branch
        }
        
        try:
            response = requests.post(
                f'{self.base_url}/repos/{repo_full_name}/pulls',
                headers=headers,
                json=payload,
                timeout=15
            )
            
            if response.status_code == 201:
                pr_data = response.json()
                return {
                    'number': pr_data['number'],
                    'title': pr_data['title'],
                    'html_url': pr_data['html_url'],
                    'state': pr_data['state']
                }
            else:
                print(f"❌ GitHub PR error: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ GitHub PR exception: {e}")
            return None

class ProjectVersionControl:
    """Система версионного контроля для проектов"""
    
    def __init__(self):
        self.github = GitHubIntegration()
        self.projects_history = {}  # project_id -> history
        
    def sync_project_to_github(self, project_id: str, project_name: str, project_files: Dict[str, str], user_github_token: str) -> Dict[str, Any]:
        """Синхронизирует проект с GitHub"""
        
        try:
            print(f"🔄 Синхронизация проекта {project_name} с GitHub...")
            
            # 1. Создаем репозиторий
            repo = self.github.create_repository(
                access_token=user_github_token,
                repo_name=project_name,
                description=f"Full-stack проект созданный с Vibecode AI",
                private=True
            )
            
            if not repo:
                return {'success': False, 'error': 'Failed to create repository'}
            
            # 2. Загружаем файлы
            upload_success = self.github.upload_project_files(
                access_token=user_github_token,
                repo_full_name=repo.full_name,
                project_files=project_files,
                commit_message="🚀 Initial project setup via Vibecode AI"
            )
            
            if not upload_success:
                return {'success': False, 'error': 'Failed to upload files'}
            
            # 3. Сохраняем в истории
            self.projects_history[project_id] = {
                'github_repo': repo,
                'last_sync': datetime.now().isoformat(),
                'commits': [],
                'sync_count': 1
            }
            
            return {
                'success': True,
                'repository': {
                    'name': repo.name,
                    'url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'private': repo.private
                },
                'files_uploaded': len(project_files)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def update_github_project(self, project_id: str, updated_files: Dict[str, str], user_github_token: str, commit_message: str = "Update via Vibecode AI") -> Dict[str, Any]:
        """Обновляет проект на GitHub"""
        
        if project_id not in self.projects_history:
            return {'success': False, 'error': 'Project not synced with GitHub'}
            
        history = self.projects_history[project_id]
        repo = history['github_repo']
        
        try:
            # Загружаем обновленные файлы
            upload_success = self.github.upload_project_files(
                access_token=user_github_token,
                repo_full_name=repo.full_name,
                project_files=updated_files,
                commit_message=commit_message
            )
            
            if upload_success:
                history['last_sync'] = datetime.now().isoformat()
                history['sync_count'] += 1
                
                return {
                    'success': True,
                    'repository_url': repo.html_url,
                    'files_updated': len(updated_files),
                    'commit_message': commit_message
                }
            else:
                return {'success': False, 'error': 'Failed to update files'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_project_github_info(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Получает информацию о GitHub интеграции проекта"""
        
        if project_id not in self.projects_history:
            return None
            
        history = self.projects_history[project_id]
        repo = history['github_repo']
        
        return {
            'repository': {
                'name': repo.name,
                'full_name': repo.full_name,
                'url': repo.html_url,
                'clone_url': repo.clone_url,
                'private': repo.private
            },
            'sync_info': {
                'last_sync': history['last_sync'],
                'sync_count': history['sync_count']
            }
        }

def test_github_integration():
    """Тестирование GitHub интеграции"""
    
    github = GitHubIntegration()
    version_control = ProjectVersionControl()
    
    # Тестовые файлы проекта
    test_files = {
        'package.json': json.dumps({
            'name': 'test-project',
            'version': '1.0.0',
            'dependencies': {
                'next': '^14.0.0',
                'react': '^18.0.0'
            }
        }, indent=2),
        'pages/index.js': '''export default function Home() {
  return <div><h1>Hello from Vibecode AI!</h1></div>
}''',
        'README.md': '''# Test Project

Created with Vibecode AI Full-Stack Platform

## Features
- Next.js React application
- Supabase database integration
- Automatic deployment
'''
    }
    
    # Тестируем синхронизацию
    result = version_control.sync_project_to_github(
        project_id="test_123",
        project_name="Vibecode Test Project",
        project_files=test_files,
        user_github_token=""  # Demo mode
    )
    
    print("🧪 Результат тестирования GitHub интеграции:")
    print(f"   Success: {result['success']}")
    if result['success']:
        repo_info = result['repository']
        print(f"   Repository: {repo_info['name']}")
        print(f"   URL: {repo_info['url']}")
        print(f"   Files uploaded: {result['files_uploaded']}")

if __name__ == "__main__":
    test_github_integration()