#!/usr/bin/env python3
"""
Новые API endpoints для конкуренции с Lovable.dev
- AI Chat система
- GitHub интеграция 
- Mobile preview
- Iterative development
"""

from flask import request, jsonify, session
from datetime import datetime
import json
import uuid
from collaborative_features import CollaborationManager, ProjectSharingSystem

def register_competitive_routes(app, ai_chat_bot, github_integration, version_control, mobile_generator, device_preview, collaboration_manager=None, sharing_system=None):
    """Регистрирует новые конкурентные API routes"""
    
    # Инициализируем collaboration систему если не передана
    if not collaboration_manager:
        collaboration_manager = CollaborationManager()
    if not sharing_system:
        sharing_system = ProjectSharingSystem(collaboration_manager)
    
    # =============================================================================
    # AI CHAT СИСТЕМА
    # =============================================================================
    
    @app.route('/api/ai-chat/create-session', methods=['POST'])
    def create_chat_session():
        """Создает новую AI chat сессию для проекта"""
        try:
            data = request.json
            project_id = data.get('project_id')
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
                
            # Получаем контекст проекта из хранилища
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            
            # Создаем контекст для AI
            from ai_chat_system import ProjectContext
            project_context = ProjectContext(
                project_id=project_id,
                name=project.get('name', 'Unnamed Project'),
                description=project.get('description', ''),
                project_type=project.get('project_type', 'general'),
                framework=project.get('framework', 'nextjs'),
                files=project.get('files', {}),
                database_schema=project.get('database_schema', {}),
                deployment_info=project.get('deployment_info', {}),
                history=[]
            )
            
            # Создаем сессию
            session_id = ai_chat_bot.create_chat_session(project_context)
            
            return jsonify({
                'success': True,
                'session_id': session_id,
                'project_name': project_context.name
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/ai-chat/send-message', methods=['POST'])
    def send_chat_message():
        """Отправляет сообщение в AI chat"""
        try:
            data = request.json
            session_id = data.get('session_id')
            message = data.get('message')
            
            if not session_id or not message:
                return jsonify({'error': 'session_id and message required'}), 400
                
            # Отправляем сообщение
            response = ai_chat_bot.send_message(session_id, message)
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/ai-chat/history/<session_id>', methods=['GET'])
    def get_ai_chat_session_history(session_id):
        """Получает историю чата"""
        try:
            history = ai_chat_bot.get_chat_history(session_id)
            return jsonify({
                'success': True,
                'messages': history
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================================================
    # GITHUB ИНТЕГРАЦИЯ
    # =============================================================================
    
    @app.route('/api/github/authenticate', methods=['POST'])
    def github_authenticate():
        """Аутентификация пользователя через GitHub"""
        try:
            data = request.json
            access_token = data.get('access_token')
            
            if not access_token:
                return jsonify({'error': 'access_token required'}), 400
                
            user_data = github_integration.authenticate_user(access_token)
            
            if user_data:
                # Сохраняем в сессию
                session['github_token'] = access_token
                session['github_user'] = user_data
                
                return jsonify({
                    'success': True,
                    'user': user_data
                })
            else:
                return jsonify({'error': 'Invalid access token'}), 401
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/github/repositories', methods=['GET'])
    def get_user_repositories():
        """Получает список репозиториев пользователя"""
        try:
            github_token = session.get('github_token')
            repositories = github_integration.get_user_repositories(github_token)
            
            repos_data = [
                {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'html_url': repo.html_url,
                    'clone_url': repo.clone_url,
                    'private': repo.private,
                    'created_at': repo.created_at
                }
                for repo in repositories
            ]
            
            return jsonify({
                'success': True,
                'repositories': repos_data
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/github/sync-project', methods=['POST'])
    def sync_project_to_github():
        """Синхронизирует проект с GitHub"""
        try:
            data = request.json
            project_id = data.get('project_id')
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
                
            github_token = session.get('github_token')
            if not github_token:
                return jsonify({'error': 'GitHub authentication required'}), 401
                
            # Получаем проект
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            
            # Синхронизируем с GitHub
            result = version_control.sync_project_to_github(
                project_id=project_id,
                project_name=project.get('name', 'Vibecode Project'),
                project_files=project.get('files', {}),
                user_github_token=github_token
            )
            
            if result['success']:
                # Обновляем проект с GitHub информацией
                project['github_info'] = result['repository']
                
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/github/update-project', methods=['POST'])
    def update_github_project():
        """Обновляет проект на GitHub"""
        try:
            data = request.json
            project_id = data.get('project_id')
            commit_message = data.get('commit_message', 'Update via Vibecode AI')
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
                
            github_token = session.get('github_token')
            if not github_token:
                return jsonify({'error': 'GitHub authentication required'}), 401
                
            # Получаем обновленные файлы проекта
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            
            # Обновляем на GitHub
            result = version_control.update_github_project(
                project_id=project_id,
                updated_files=project.get('files', {}),
                user_github_token=github_token,
                commit_message=commit_message
            )
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================================================
    # MOBILE PREVIEW & RESPONSIVE
    # =============================================================================
    
    @app.route('/api/mobile/generate-responsive', methods=['POST'])
    def generate_responsive_component():
        """Генерирует responsive React компонент"""
        try:
            data = request.json
            component_name = data.get('component_name', 'ResponsiveComponent')
            component_type = data.get('component_type', 'general')
            
            # Генерируем компонент
            component_code = mobile_generator.generate_responsive_component(
                component_name, component_type
            )
            
            # Генерируем viewport конфигурацию
            viewport_config = mobile_generator.generate_viewport_config()
            
            return jsonify({
                'success': True,
                'component_code': component_code,
                'viewport_config': viewport_config,
                'component_name': component_name,
                'component_type': component_type
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/mobile/device-preview', methods=['GET'])
    def get_device_preview_interface():
        """Получает интерфейс для preview разных устройств"""
        try:
            preview_html = device_preview.generate_preview_interface()
            
            return jsonify({
                'success': True,
                'preview_html': preview_html,
                'devices': list(device_preview.devices.keys())
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/mobile/optimize-project', methods=['POST'])
    def optimize_project_for_mobile():
        """Оптимизирует существующий проект для мобильных устройств"""
        try:
            data = request.json
            project_id = data.get('project_id')
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
                
            # Получаем проект
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            
            # Оптимизируем файлы для мобильных устройств
            optimized_files = {}
            original_files = project.get('files', {})
            
            for file_path, content in original_files.items():
                if file_path.endswith('.js') or file_path.endswith('.jsx'):
                    # Добавляем responsive классы в JSX компоненты
                    optimized_content = _add_responsive_classes(content)
                    optimized_files[file_path] = optimized_content
                elif file_path == 'tailwind.config.js':
                    # Обновляем Tailwind конфигурацию
                    optimized_files[file_path] = mobile_generator.generate_viewport_config()['tailwind_config']
                elif file_path == 'next.config.js':
                    # Обновляем Next.js конфигурацию
                    optimized_files[file_path] = mobile_generator.generate_viewport_config()['next_config']
                else:
                    optimized_files[file_path] = content
            
            # Добавляем mobile стили
            optimized_files['styles/mobile.css'] = mobile_generator.generate_mobile_styles()
            
            # Обновляем проект
            project['files'] = optimized_files
            project['mobile_optimized'] = True
            project['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'Проект оптимизирован для мобильных устройств',
                'optimized_files': len(optimized_files),
                'mobile_optimized': True
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================================================
    # ITERATIVE DEVELOPMENT
    # =============================================================================
    
    @app.route('/api/project/iterate', methods=['POST'])
    def iterate_project():
        """Итеративная доработка проекта через AI"""
        try:
            data = request.json
            project_id = data.get('project_id')
            instruction = data.get('instruction')
            session_id = data.get('session_id')
            
            if not all([project_id, instruction]):
                return jsonify({'error': 'project_id and instruction required'}), 400
                
            # Получаем проект
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            
            # Если есть активная AI сессия, используем её
            if session_id:
                ai_response = ai_chat_bot.send_message(session_id, instruction)
                if not ai_response['success']:
                    return jsonify(ai_response), 500
            
            # Применяем изменения (здесь будет логика модификации файлов)
            iteration_result = _apply_project_iteration(project, instruction)
            
            # Обновляем историю
            if 'history' not in project:
                project['history'] = []
                
            project['history'].append({
                'timestamp': datetime.now().isoformat(),
                'instruction': instruction,
                'changes': iteration_result.get('changes', []),
                'session_id': session_id
            })
            
            project['updated_at'] = datetime.now().isoformat()
            
            return jsonify({
                'success': True,
                'message': 'Проект успешно доработан',
                'changes': iteration_result.get('changes', []),
                'ai_response': ai_response if session_id else None
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/project/history/<project_id>', methods=['GET'])
    def get_project_history(project_id):
        """Получает историю изменений проекта"""
        try:
            # Получаем проект
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
                
            project = fullstack_projects[project_id]
            history = project.get('history', [])
            
            return jsonify({
                'success': True,
                'project_id': project_id,
                'history': history,
                'total_iterations': len(history)
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    # =============================================================================
    # COLLABORATION & SHARING
    # =============================================================================
    
    @app.route('/api/collaboration/join-project', methods=['POST'])
    def join_project_collaboration():
        """Присоединяется к совместной работе над проектом"""
        try:
            data = request.json
            project_id = data.get('project_id')
            user_info = data.get('user_info', {})
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
            
            # Получаем активных участников
            collaborators = collaboration_manager.get_active_collaborators(project_id)
            
            return jsonify({
                'success': True,
                'project_id': project_id,
                'active_collaborators': collaborators,
                'socket_url': '/socket.io'  # Для подключения к Socket.IO
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/collaboration/comments/<project_id>', methods=['GET'])
    def get_project_comments(project_id):
        """Получает комментарии проекта"""
        try:
            comments = collaboration_manager.get_project_comments(project_id)
            return jsonify({
                'success': True,
                'comments': comments
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/sharing/publish', methods=['POST'])
    def publish_project():
        """Публикует проект для общего доступа"""
        try:
            data = request.json
            project_id = data.get('project_id')
            settings = data.get('settings', {})
            
            if not project_id:
                return jsonify({'error': 'project_id required'}), 400
            
            # Получаем данные проекта
            from app import fullstack_projects
            if project_id not in fullstack_projects:
                return jsonify({'error': 'Project not found'}), 404
            
            project_data = fullstack_projects[project_id]
            project_data['author'] = session.get('username', 'Anonymous')
            
            # Публикуем проект
            share_id = sharing_system.publish_project(project_id, project_data, settings)
            
            return jsonify({
                'success': True,
                'share_id': share_id,
                'share_url': f"{request.host_url}share/{share_id}",
                'settings': settings
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/sharing/public-projects', methods=['GET'])
    def get_public_projects():
        """Получает список публичных проектов"""
        try:
            limit = int(request.args.get('limit', 20))
            offset = int(request.args.get('offset', 0))
            
            projects = sharing_system.get_public_projects_list(limit, offset)
            
            return jsonify({
                'success': True,
                'projects': projects,
                'has_more': len(projects) == limit
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def _add_responsive_classes(jsx_content: str) -> str:
    """Добавляет responsive классы в JSX контент"""
    import re
    
    # Простая логика добавления responsive классов
    # В реальности здесь будет более сложный парсинг
    
    # Добавляем responsive классы к div элементам
    jsx_content = re.sub(
        r'className="([^"]*)"',
        lambda m: f'className="{m.group(1)} sm:px-6 md:px-8 lg:px-12"' if 'px-' in m.group(1) else m.group(0),
        jsx_content
    )
    
    # Добавляем responsive текст
    jsx_content = re.sub(
        r'className="([^"]*text-[^"]*)"',
        lambda m: f'className="{m.group(1)} sm:text-lg md:text-xl"',
        jsx_content
    )
    
    return jsx_content

def _apply_project_iteration(project: dict, instruction: str) -> dict:
    """Применяет итеративные изменения к проекту"""
    
    changes = []
    instruction_lower = instruction.lower()
    
    # Простая логика обработки инструкций
    if 'цвет' in instruction_lower or 'color' in instruction_lower:
        changes.append('Updated color scheme')
    elif 'кнопка' in instruction_lower or 'button' in instruction_lower:
        changes.append('Modified button styles')
    elif 'текст' in instruction_lower or 'text' in instruction_lower:
        changes.append('Updated text content')
    elif 'компонент' in instruction_lower or 'component' in instruction_lower:
        changes.append('Added/modified components')
    else:
        changes.append('General improvements')
    
    return {
        'changes': changes,
        'applied_at': datetime.now().isoformat()
    }