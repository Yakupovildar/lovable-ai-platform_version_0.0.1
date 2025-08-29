#!/usr/bin/env python3
"""
Система совместной работы и sharing для конкуренции с Lovable.dev
- Real-time collaboration
- Project sharing
- Team management
- Comments and feedback
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import socketio

@dataclass
class Collaborator:
    """Участник совместной работы"""
    user_id: str
    name: str
    email: str
    avatar_url: str
    role: str  # 'owner', 'editor', 'viewer'
    joined_at: datetime
    last_active: datetime
    online: bool = False

@dataclass
class ProjectComment:
    """Комментарий к проекту"""
    id: str
    project_id: str
    user_id: str
    user_name: str
    content: str
    created_at: datetime
    file_path: str = ""
    line_number: int = 0
    replies: List['ProjectComment'] = None

@dataclass
class ProjectShare:
    """Настройки публикации проекта"""
    project_id: str
    share_id: str
    visibility: str  # 'public', 'private', 'team'
    password: str = ""
    expires_at: Optional[datetime] = None
    view_count: int = 0
    allow_comments: bool = True
    allow_cloning: bool = False

class CollaborationManager:
    """Менеджер совместной работы"""
    
    def __init__(self):
        self.active_collaborators = {}  # project_id -> List[Collaborator]
        self.project_comments = {}  # project_id -> List[ProjectComment]
        self.project_shares = {}  # share_id -> ProjectShare
        self.real_time_changes = {}  # project_id -> List[changes]
        
        # Socket.IO для real-time обновлений
        self.sio = socketio.Server(cors_allowed_origins="*")
        
        # Настраиваем события
        self._setup_socket_events()
    
    def _setup_socket_events(self):
        """Настраивает Socket.IO события"""
        
        @self.sio.event
        def connect(sid, environ):
            print(f"📡 Collaborator connected: {sid}")
        
        @self.sio.event
        def disconnect(sid):
            print(f"📡 Collaborator disconnected: {sid}")
            self._remove_collaborator_from_all_projects(sid)
        
        @self.sio.event
        def join_project(sid, data):
            project_id = data.get('project_id')
            user_info = data.get('user_info', {})
            
            if project_id:
                self.sio.enter_room(sid, f"project_{project_id}")
                self._add_collaborator_to_project(project_id, sid, user_info)
                
                # Уведомляем других участников
                self.sio.emit('collaborator_joined', {
                    'user_info': user_info,
                    'timestamp': datetime.now().isoformat()
                }, room=f"project_{project_id}", skip_sid=sid)
        
        @self.sio.event
        def leave_project(sid, data):
            project_id = data.get('project_id')
            if project_id:
                self.sio.leave_room(sid, f"project_{project_id}")
                user_info = self._remove_collaborator_from_project(project_id, sid)
                
                # Уведомляем других участников
                self.sio.emit('collaborator_left', {
                    'user_info': user_info,
                    'timestamp': datetime.now().isoformat()
                }, room=f"project_{project_id}")
        
        @self.sio.event
        def code_change(sid, data):
            project_id = data.get('project_id')
            change_data = data.get('change')
            
            if project_id and change_data:
                # Сохраняем изменение
                self._save_real_time_change(project_id, change_data)
                
                # Транслируем другим участникам
                self.sio.emit('code_updated', {
                    'change': change_data,
                    'timestamp': datetime.now().isoformat()
                }, room=f"project_{project_id}", skip_sid=sid)
        
        @self.sio.event
        def add_comment(sid, data):
            project_id = data.get('project_id')
            comment_data = data.get('comment')
            
            if project_id and comment_data:
                comment = self._add_comment_to_project(project_id, comment_data)
                
                # Уведомляем всех участников
                self.sio.emit('comment_added', {
                    'comment': asdict(comment),
                    'timestamp': datetime.now().isoformat()
                }, room=f"project_{project_id}")
    
    def _add_collaborator_to_project(self, project_id: str, sid: str, user_info: Dict):
        """Добавляет участника к проекту"""
        if project_id not in self.active_collaborators:
            self.active_collaborators[project_id] = {}
        
        collaborator = Collaborator(
            user_id=user_info.get('user_id', sid),
            name=user_info.get('name', 'Anonymous'),
            email=user_info.get('email', ''),
            avatar_url=user_info.get('avatar_url', ''),
            role=user_info.get('role', 'viewer'),
            joined_at=datetime.now(),
            last_active=datetime.now(),
            online=True
        )
        
        self.active_collaborators[project_id][sid] = collaborator
        print(f"👥 {collaborator.name} joined project {project_id}")
    
    def _remove_collaborator_from_project(self, project_id: str, sid: str) -> Optional[Dict]:
        """Удаляет участника из проекта"""
        if project_id in self.active_collaborators and sid in self.active_collaborators[project_id]:
            collaborator = self.active_collaborators[project_id].pop(sid)
            print(f"👋 {collaborator.name} left project {project_id}")
            return asdict(collaborator)
        return None
    
    def _remove_collaborator_from_all_projects(self, sid: str):
        """Удаляет участника из всех проектов при отключении"""
        for project_id in list(self.active_collaborators.keys()):
            if sid in self.active_collaborators[project_id]:
                self._remove_collaborator_from_project(project_id, sid)
    
    def _save_real_time_change(self, project_id: str, change_data: Dict):
        """Сохраняет изменение в реальном времени"""
        if project_id not in self.real_time_changes:
            self.real_time_changes[project_id] = []
        
        change_data['timestamp'] = datetime.now().isoformat()
        change_data['id'] = str(uuid.uuid4())
        
        self.real_time_changes[project_id].append(change_data)
        
        # Храним только последние 100 изменений
        if len(self.real_time_changes[project_id]) > 100:
            self.real_time_changes[project_id] = self.real_time_changes[project_id][-100:]
    
    def _add_comment_to_project(self, project_id: str, comment_data: Dict) -> ProjectComment:
        """Добавляет комментарий к проекту"""
        if project_id not in self.project_comments:
            self.project_comments[project_id] = []
        
        comment = ProjectComment(
            id=str(uuid.uuid4()),
            project_id=project_id,
            user_id=comment_data.get('user_id', ''),
            user_name=comment_data.get('user_name', 'Anonymous'),
            content=comment_data.get('content', ''),
            file_path=comment_data.get('file_path', ''),
            line_number=comment_data.get('line_number', 0),
            created_at=datetime.now(),
            replies=[]
        )
        
        self.project_comments[project_id].append(comment)
        return comment
    
    def get_active_collaborators(self, project_id: str) -> List[Dict]:
        """Получает список активных участников проекта"""
        if project_id not in self.active_collaborators:
            return []
        
        return [asdict(collab) for collab in self.active_collaborators[project_id].values()]
    
    def get_project_comments(self, project_id: str) -> List[Dict]:
        """Получает комментарии проекта"""
        if project_id not in self.project_comments:
            return []
        
        return [asdict(comment) for comment in self.project_comments[project_id]]
    
    def get_real_time_changes(self, project_id: str, since: Optional[str] = None) -> List[Dict]:
        """Получает изменения в реальном времени"""
        if project_id not in self.real_time_changes:
            return []
        
        changes = self.real_time_changes[project_id]
        
        if since:
            # Фильтруем изменения после указанной метки времени
            changes = [change for change in changes if change['timestamp'] > since]
        
        return changes
    
    def create_project_share(self, project_id: str, settings: Dict) -> ProjectShare:
        """Создает публичную ссылку для проекта"""
        share_id = str(uuid.uuid4())[:12]
        
        project_share = ProjectShare(
            project_id=project_id,
            share_id=share_id,
            visibility=settings.get('visibility', 'public'),
            password=settings.get('password', ''),
            expires_at=settings.get('expires_at'),
            allow_comments=settings.get('allow_comments', True),
            allow_cloning=settings.get('allow_cloning', False)
        )
        
        self.project_shares[share_id] = project_share
        return project_share
    
    def get_project_share(self, share_id: str) -> Optional[ProjectShare]:
        """Получает настройки публикации по ID"""
        return self.project_shares.get(share_id)
    
    def update_share_view_count(self, share_id: str):
        """Увеличивает счетчик просмотров"""
        if share_id in self.project_shares:
            self.project_shares[share_id].view_count += 1
    
    def is_share_valid(self, share_id: str, password: str = "") -> bool:
        """Проверяет валидность публичной ссылки"""
        share = self.get_project_share(share_id)
        if not share:
            return False
        
        # Проверяем срок действия
        if share.expires_at and datetime.now() > share.expires_at:
            return False
        
        # Проверяем пароль
        if share.password and share.password != password:
            return False
        
        return True
    
    def get_socket_app(self):
        """Возвращает Socket.IO приложение для интеграции с Flask"""
        return socketio.WSGIApp(self.sio)

class ProjectSharingSystem:
    """Система публикации и sharing проектов"""
    
    def __init__(self, collaboration_manager: CollaborationManager):
        self.collaboration_manager = collaboration_manager
        self.public_projects = {}  # Публичные проекты
        
    def publish_project(self, project_id: str, project_data: Dict, settings: Dict) -> str:
        """Публикует проект для общего доступа"""
        
        # Создаем share
        project_share = self.collaboration_manager.create_project_share(project_id, settings)
        
        # Сохраняем публичную версию проекта
        public_project = {
            'project_id': project_id,
            'share_id': project_share.share_id,
            'name': project_data.get('name', 'Untitled Project'),
            'description': project_data.get('description', ''),
            'preview_image': project_data.get('preview_image', ''),
            'author': project_data.get('author', 'Anonymous'),
            'created_at': datetime.now().isoformat(),
            'tags': project_data.get('tags', []),
            'framework': project_data.get('framework', ''),
            'files_count': len(project_data.get('files', {})),
            'view_count': 0,
            'clone_count': 0,
            'settings': asdict(project_share)
        }
        
        self.public_projects[project_share.share_id] = public_project
        
        return project_share.share_id
    
    def get_public_project(self, share_id: str) -> Optional[Dict]:
        """Получает публичный проект по share_id"""
        return self.public_projects.get(share_id)
    
    def get_public_projects_list(self, limit: int = 20, offset: int = 0) -> List[Dict]:
        """Получает список публичных проектов"""
        projects = list(self.public_projects.values())
        
        # Сортируем по дате создания (новые сначала)
        projects.sort(key=lambda x: x['created_at'], reverse=True)
        
        # Применяем пагинацию
        return projects[offset:offset + limit]
    
    def clone_project(self, share_id: str, user_info: Dict) -> Optional[Dict]:
        """Клонирует публичный проект"""
        public_project = self.get_public_project(share_id)
        if not public_project:
            return None
        
        share = self.collaboration_manager.get_project_share(share_id)
        if not share or not share.allow_cloning:
            return None
        
        # Увеличиваем счетчик клонирований
        public_project['clone_count'] += 1
        
        # Создаем копию проекта для пользователя
        cloned_project = {
            'project_id': str(uuid.uuid4()),
            'original_share_id': share_id,
            'name': f"Copy of {public_project['name']}",
            'cloned_by': user_info.get('name', 'Anonymous'),
            'cloned_at': datetime.now().isoformat()
        }
        
        return cloned_project
    
    def search_public_projects(self, query: str, tags: List[str] = []) -> List[Dict]:
        """Поиск публичных проектов"""
        results = []
        query_lower = query.lower()
        
        for project in self.public_projects.values():
            # Поиск по названию и описанию
            if (query_lower in project['name'].lower() or 
                query_lower in project['description'].lower()):
                results.append(project)
                continue
            
            # Поиск по тегам
            if tags and any(tag in project['tags'] for tag in tags):
                results.append(project)
        
        # Сортируем по релевантности (по количеству просмотров)
        results.sort(key=lambda x: x['view_count'], reverse=True)
        
        return results[:50]  # Максимум 50 результатов

def test_collaboration_system():
    """Тестирование системы совместной работы"""
    
    collab_manager = CollaborationManager()
    sharing_system = ProjectSharingSystem(collab_manager)
    
    # Тестируем создание публичной ссылки
    test_project_data = {
        'name': 'Test E-commerce App',
        'description': 'A full-stack e-commerce application built with Next.js',
        'author': 'Test User',
        'framework': 'nextjs',
        'tags': ['ecommerce', 'nextjs', 'supabase'],
        'files': {'pages/index.js': 'content', 'components/Product.js': 'content'}
    }
    
    share_settings = {
        'visibility': 'public',
        'allow_comments': True,
        'allow_cloning': True
    }
    
    share_id = sharing_system.publish_project('test_123', test_project_data, share_settings)
    
    print("🧪 Тестирование Collaboration System:")
    print(f"   Share ID: {share_id}")
    
    # Тестируем получение публичного проекта
    public_project = sharing_system.get_public_project(share_id)
    if public_project:
        print(f"   ✅ Публичный проект создан: {public_project['name']}")
        print(f"   📊 Файлов: {public_project['files_count']}")
        print(f"   🏷️ Теги: {', '.join(public_project['tags'])}")
    
    # Тестируем клонирование
    cloned = sharing_system.clone_project(share_id, {'name': 'Clone User'})
    if cloned:
        print(f"   ✅ Проект склонирован: {cloned['name']}")
    
    # Тестируем поиск
    search_results = sharing_system.search_public_projects('ecommerce')
    print(f"   🔍 Найдено проектов по запросу 'ecommerce': {len(search_results)}")
    
    print("\n🎉 Collaboration System готова!")

if __name__ == "__main__":
    test_collaboration_system()