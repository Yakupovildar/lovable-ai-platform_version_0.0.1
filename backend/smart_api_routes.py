"""
Улучшенные API роуты с интеграцией умных AI сервисов
"""

from flask import Flask, request, jsonify, session, send_file
import json
import uuid
import os
import zipfile
import time
from datetime import datetime
from smart_ai_generator import SmartAIGenerator
from intelligent_chat import IntelligentChat

# Инициализация умных AI сервисов
smart_generator = SmartAIGenerator()
intelligent_chat = IntelligentChat()

def register_smart_routes(app, login_required, monitor_performance, logger, executor, 
                         get_user_by_id, update_user_requests, save_chat_message, 
                         save_user_project, get_cache_key, get_from_cache, set_cache, 
                         clear_user_cache):
    """Регистрирует улучшенные API роуты"""
    
    @app.route('/api/smart-chat', methods=['POST'])
    @login_required
    @monitor_performance
    def smart_chat():
        """Умная обработка сообщений чата с новым AI"""
        data = request.json
        message = data.get('message', '')
        chat_session_id = data.get('session_id', str(uuid.uuid4()))
        
        try:
            user_id = session['user_id']
            
            # Быстрая проверка кэша пользователя
            user_cache_key = get_cache_key("user", user_id)
            user = get_from_cache(user_cache_key)
            if not user:
                user = get_user_by_id(user_id)
                if not user:
                    return jsonify({"error": "Пользователь не найден"}), 404
                set_cache(user_cache_key, user, ttl=60)
            
            # Проверяем лимит запросов
            requests_used = user[5]
            requests_limit = user[6]
            
            if requests_used >= requests_limit and user[4] == 'free':
                return jsonify({
                    "type": "limit_exceeded",
                    "message": "⚡ Лимит бесплатных запросов исчерпан! Оформите подписку для продолжения работы.",
                    "requests_used": requests_used,
                    "requests_limit": requests_limit,
                    "show_subscription": True,
                    "suggestions": intelligent_chat.get_suggestions(f"chat_{user_id}_{chat_session_id}")
                }), 429
            
            print(f"🧠 Обрабатываю умный чат для пользователя {user_id}: {message[:50]}...")
            
            # Используем новый умный чат
            chat_result = intelligent_chat.chat(
                session_id=f"chat_{user_id}_{chat_session_id}",
                user_message=message,
                preferred_ai='auto'  # Автоматически выбираем лучший AI
            )
            
            ai_response = chat_result['response']
            intent_analysis = chat_result['intent_analysis']
            
            print(f"🎯 Намерение: {intent_analysis['intent']}, AI: {chat_result['ai_provider']}")
            
            # Проверяем, нужно ли сгенерировать проект
            project_result = None
            if intent_analysis['intent'] == 'create_project' and any(word in message.lower() for word in ['создай', 'сделай', 'построй']):
                try:
                    print("🚀 Пользователь запросил создание проекта, генерирую...")
                    project_result = smart_generator.generate_project(message, 'auto')
                    
                    if project_result.success:
                        # Сохраняем проект
                        project_id = str(uuid.uuid4())
                        project_path = f"projects/{project_id}"
                        os.makedirs(project_path, exist_ok=True)
                        
                        # Записываем файлы проекта
                        for file_obj in project_result.files:
                            file_path = os.path.join(project_path, file_obj.name)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(file_obj.content)
                        
                        # Создаем ZIP архив
                        zip_path = f"projects/{project_id}.zip"
                        with zipfile.ZipFile(zip_path, 'w') as zipf:
                            for file_obj in project_result.files:
                                zipf.writestr(file_obj.name, file_obj.content)
                        
                        ai_response += f"\n\n🎉 **Проект готов!** Я создал {project_result.project_type} с {len(project_result.files)} файлами.\n\n"
                        ai_response += f"📁 **Структура проекта:** {', '.join(project_result.structure)}\n\n"
                        ai_response += f"📋 **Инструкции:** {project_result.instructions}\n\n"
                        ai_response += f"💾 Проект сохранен с ID: {project_id}"
                        
                        # Сохраняем информацию о проекте в базу
                        save_user_project(user_id, project_id, message, project_result.project_type, json.dumps({
                            'files': [{'name': f.name, 'type': f.type} for f in project_result.files],
                            'structure': project_result.structure,
                            'instructions': project_result.instructions
                        }))
                        
                        print(f"✅ Проект {project_id} успешно создан с {len(project_result.files)} файлами")
                        
                except Exception as e:
                    print(f"❌ Ошибка генерации проекта: {e}")
                    ai_response += "\n\n⚠️ Не удалось создать файлы проекта автоматически, но я готов помочь с кодом!"
            
            # Обновляем счетчики
            if user[4] == 'free':
                executor.submit(update_user_requests, user_id, 1)
                requests_used += 1
            
            # Сохраняем в историю чата
            executor.submit(save_chat_message, user_id, chat_session_id, message, ai_response, 'smart_chat')
            
            # Очищаем кэш пользователя
            clear_user_cache(user_id)
            
            # Формируем ответ
            response_data = {
                "type": "success",
                "message": ai_response,
                "intent": intent_analysis['intent'],
                "project_type": intent_analysis.get('project_type', 'webapp'),
                "ai_provider": chat_result['ai_provider'],
                "suggestions": intelligent_chat.get_suggestions(f"chat_{user_id}_{chat_session_id}"),
                "requests_left": max(0, requests_limit - requests_used),
                "requests_used": requests_used,
                "requests_limit": requests_limit,
                "session_id": chat_session_id,
                "timestamp": chat_result['timestamp']
            }
            
            # Добавляем информацию о проекте если был сгенерирован
            if project_result and project_result.success:
                response_data["project_generated"] = True
                response_data["project_id"] = project_id
                response_data["project_files"] = len(project_result.files)
                response_data["download_url"] = f"/api/download-project/{project_id}"
            
            return jsonify(response_data)
            
        except Exception as e:
            logger.error(f"Ошибка в умном чате: {e}")
            return jsonify({
                "type": "error",
                "message": "🤖 Произошла ошибка. Попробую помочь по-другому!",
                "suggestions": ["Создать простое приложение", "Задать вопрос о коде", "Повторить запрос"],
                "error_details": str(e)
            })

    @app.route('/api/smart-generate-project', methods=['POST'])
    @login_required
    @monitor_performance
    def smart_generate_project():
        """Умная генерация проекта с анализом требований"""
        data = request.json
        description = data.get('description', '')
        project_name = data.get('project_name', 'Мой проект')
        preferred_ai = data.get('ai_provider', 'auto')
        
        try:
            user_id = session['user_id']
            
            # Проверяем пользователя и лимиты
            user = get_user_by_id(user_id)
            if not user:
                return jsonify({"error": "Пользователь не найден"}), 404
            
            requests_used = user[5]
            requests_limit = user[6]
            
            if requests_used >= requests_limit and user[4] == 'free':
                return jsonify({
                    "success": False,
                    "error": "limit_exceeded",
                    "message": "⚡ Лимит бесплатных запросов исчерпан!"
                }), 429
            
            print(f"🚀 Генерирую проект для пользователя {user_id}: {description[:50]}...")
            
            # Генерируем проект с помощью умного генератора
            project_result = smart_generator.generate_project(description, preferred_ai)
            
            if not project_result.success:
                return jsonify({
                    "success": False,
                    "error": "generation_failed",
                    "message": "Не удалось сгенерировать проект. Попробуйте упростить описание."
                })
            
            # Сохраняем проект
            project_id = str(uuid.uuid4())
            project_path = f"projects/{project_id}"
            os.makedirs(project_path, exist_ok=True)
            
            # Записываем файлы
            saved_files = []
            for file_obj in project_result.files:
                file_path = os.path.join(project_path, file_obj.name)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_obj.content)
                saved_files.append({
                    'name': file_obj.name,
                    'type': file_obj.type,
                    'size': len(file_obj.content)
                })
            
            # Создаем ZIP архив
            zip_path = f"projects/{project_id}.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for file_obj in project_result.files:
                    zipf.writestr(file_obj.name, file_obj.content)
            
            # Сохраняем в базу данных
            save_user_project(user_id, project_id, description, project_result.project_type, json.dumps({
                'files': saved_files,
                'structure': project_result.structure,
                'instructions': project_result.instructions
            }))
            
            # Обновляем счетчики
            if user[4] == 'free':
                update_user_requests(user_id, 1)
                requests_used += 1
            
            print(f"✅ Проект {project_id} успешно создан: {len(project_result.files)} файлов")
            
            return jsonify({
                "success": True,
                "project_id": project_id,
                "project_name": project_name,
                "project_type": project_result.project_type,
                "files_count": len(project_result.files),
                "structure": project_result.structure,
                "instructions": project_result.instructions,
                "download_url": f"/api/download-project/{project_id}",
                "files": saved_files,
                "requests_left": max(0, requests_limit - requests_used),
                "message": f"Проект '{project_name}' успешно создан!"
            })
            
        except Exception as e:
            logger.error(f"Ошибка генерации проекта: {e}")
            return jsonify({
                "success": False,
                "error": "generation_error",
                "message": "Произошла ошибка при генерации проекта",
                "error_details": str(e)
            })

    @app.route('/api/download-project/<project_id>')
    @login_required
    def download_smart_project(project_id):
        """Скачивание сгенерированного проекта"""
        try:
            zip_path = f"projects/{project_id}.zip"
            if os.path.exists(zip_path):
                return send_file(
                    zip_path,
                    as_attachment=True,
                    download_name=f"project_{project_id}.zip",
                    mimetype='application/zip'
                )
            else:
                return jsonify({"error": "Проект не найден"}), 404
                
        except Exception as e:
            logger.error(f"Ошибка скачивания проекта {project_id}: {e}")
            return jsonify({"error": "Ошибка скачивания"}), 500

    @app.route('/api/chat-suggestions/<session_id>')
    @login_required
    def get_chat_suggestions(session_id):
        """Получить персонализированные предложения для чата"""
        try:
            user_id = session['user_id']
            chat_session_id = f"chat_{user_id}_{session_id}"
            suggestions = intelligent_chat.get_suggestions(chat_session_id)
            
            return jsonify({
                "success": True,
                "suggestions": suggestions,
                "session_id": session_id
            })
            
        except Exception as e:
            logger.error(f"Ошибка получения предложений: {e}")
            return jsonify({
                "success": False,
                "suggestions": [
                    "Создай современный сайт",
                    "Сделай интерактивную игру", 
                    "Помоги с дизайном",
                    "Объясни технологию"
                ]
            })

    @app.route('/api/analyze-request', methods=['POST'])
    @login_required
    def analyze_user_request():
        """Анализ намерений пользователя без генерации ответа"""
        data = request.json
        message = data.get('message', '')
        
        try:
            analysis = intelligent_chat.analyze_user_intent(message)
            
            return jsonify({
                "success": True,
                "analysis": analysis,
                "estimated_complexity": analysis.get('complexity', 'medium'),
                "suggested_approach": "smart_generation" if analysis['intent'] == 'create_project' else "chat_assistance"
            })
            
        except Exception as e:
            logger.error(f"Ошибка анализа запроса: {e}")
            return jsonify({
                "success": False,
                "error": str(e)
            })

    @app.route('/api/ai-status')
    def get_ai_status():
        """Проверка статуса AI сервисов"""
        try:
            # Используем только бесплатные AI сервисы
            from ai_config import AIConfig
            ai_config = AIConfig()
            
            return jsonify({
                "ai_services": {
                    "gigachat": {
                        "available": ai_config.gigachat_enabled,
                        "model": "GigaChat-Pro" if ai_config.gigachat_enabled else None
                    },
                    "yandex": {
                        "available": ai_config.yandex_enabled,
                        "model": "YandexGPT-Lite" if ai_config.yandex_enabled else None
                    },
                    "localai": {
                        "available": ai_config.localai_enabled,
                        "model": "LocalAI" if ai_config.localai_enabled else None
                    }
                },
                "preferred_ai": ai_config.default_ai,
                "smart_features": {
                    "project_generation": True,
                    "code_analysis": True,
                    "intent_recognition": True,
                    "personalized_suggestions": True
                }
            })
            
        except Exception as e:
            logger.error(f"Ошибка проверки статуса AI: {e}")
            return jsonify({"error": "Не удалось проверить статус AI"})

    print("✅ Умные API роуты зарегистрированы")
    return app