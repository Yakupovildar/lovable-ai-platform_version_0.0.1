
import json
import os
from datetime import datetime
import uuid
import threading
from collections import defaultdict

class UserInteractionLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.session_logs = defaultdict(list)
        self.lock = threading.Lock()

    def log_user_request(self, user_id, session_id, request_data):
        """Логирует запрос пользователя"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "user_request",
            "user_id": user_id,
            "session_id": session_id,
            "request_id": str(uuid.uuid4()),
            "data": request_data
        }
        
        self._write_log(log_entry)
        return log_entry["request_id"]

    def log_ai_response(self, user_id, session_id, request_id, response_data, processing_time):
        """Логирует ответ AI"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "ai_response",
            "user_id": user_id,
            "session_id": session_id,
            "request_id": request_id,
            "processing_time_ms": processing_time,
            "data": response_data
        }
        
        self._write_log(log_entry)

    def log_project_creation(self, user_id, session_id, project_data):
        """Логирует создание проекта"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "project_creation",
            "user_id": user_id,
            "session_id": session_id,
            "project_id": project_data.get("project_id"),
            "project_type": project_data.get("project_type"),
            "data": project_data
        }
        
        self._write_log(log_entry)

    def log_error(self, user_id, session_id, error_data):
        """Логирует ошибки"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": "error",
            "user_id": user_id,
            "session_id": session_id,
            "error_id": str(uuid.uuid4()),
            "data": error_data
        }
        
        self._write_log(log_entry)

    def _write_log(self, log_entry):
        """Записывает лог в файл"""
        with self.lock:
            # Создаем файл по дате
            date_str = datetime.now().strftime("%Y-%m-%d")
            log_file = os.path.join(self.log_dir, f"interactions_{date_str}.jsonl")
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def get_user_analytics(self, user_id, days=30):
        """Получает аналитику по пользователю"""
        analytics = {
            "user_id": user_id,
            "total_requests": 0,
            "total_projects": 0,
            "avg_session_duration": 0,
            "popular_project_types": defaultdict(int),
            "error_count": 0,
            "sessions": []
        }
        
        # Читаем логи за указанный период
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            log_file = os.path.join(self.log_dir, f"interactions_{date_str}.jsonl")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            if entry.get("user_id") == user_id:
                                self._process_analytics_entry(analytics, entry)
                        except json.JSONDecodeError:
                            continue
        
        return analytics

    def _process_analytics_entry(self, analytics, entry):
        """Обрабатывает запись для аналитики"""
        entry_type = entry.get("type")
        
        if entry_type == "user_request":
            analytics["total_requests"] += 1
        elif entry_type == "project_creation":
            analytics["total_projects"] += 1
            project_type = entry.get("project_type", "unknown")
            analytics["popular_project_types"][project_type] += 1
        elif entry_type == "error":
            analytics["error_count"] += 1

    def get_system_analytics(self, days=7):
        """Получает системную аналитику"""
        analytics = {
            "total_users": set(),
            "total_requests": 0,
            "total_projects": 0,
            "total_errors": 0,
            "popular_intents": defaultdict(int),
            "popular_project_types": defaultdict(int),
            "daily_stats": defaultdict(lambda: {
                "requests": 0,
                "projects": 0,
                "users": set()
            })
        }
        
        for i in range(days):
            date = datetime.now() - timedelta(days=i)
            date_str = date.strftime("%Y-%m-%d")
            log_file = os.path.join(self.log_dir, f"interactions_{date_str}.jsonl")
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            self._process_system_analytics_entry(analytics, entry, date_str)
                        except json.JSONDecodeError:
                            continue
        
        # Конвертируем sets в списки для JSON
        analytics["total_users"] = len(analytics["total_users"])
        for day_stats in analytics["daily_stats"].values():
            day_stats["users"] = len(day_stats["users"])
        
        return analytics

    def _process_system_analytics_entry(self, analytics, entry, date_str):
        """Обрабатывает запись для системной аналитики"""
        user_id = entry.get("user_id")
        entry_type = entry.get("type")
        
        if user_id:
            analytics["total_users"].add(user_id)
            analytics["daily_stats"][date_str]["users"].add(user_id)
        
        if entry_type == "user_request":
            analytics["total_requests"] += 1
            analytics["daily_stats"][date_str]["requests"] += 1
            
            # Анализируем намерения
            intent = entry.get("data", {}).get("intent")
            if intent:
                analytics["popular_intents"][intent] += 1
                
        elif entry_type == "project_creation":
            analytics["total_projects"] += 1
            analytics["daily_stats"][date_str]["projects"] += 1
            
            project_type = entry.get("project_type", "unknown")
            analytics["popular_project_types"][project_type] += 1
            
        elif entry_type == "error":
            analytics["total_errors"] += 1

    def export_training_data(self, output_file):
        """Экспортирует данные для обучения AI"""
        training_data = []
        
        # Читаем все логи
        for log_file in os.listdir(self.log_dir):
            if log_file.endswith('.jsonl'):
                file_path = os.path.join(self.log_dir, log_file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line)
                            if entry.get("type") in ["user_request", "ai_response"]:
                                training_data.append(entry)
                        except json.JSONDecodeError:
                            continue
        
        # Группируем запросы и ответы
        paired_data = []
        requests = {}
        
        for entry in training_data:
            if entry.get("type") == "user_request":
                request_id = entry.get("request_id")
                requests[request_id] = entry
            elif entry.get("type") == "ai_response":
                request_id = entry.get("request_id")
                if request_id in requests:
                    paired_data.append({
                        "request": requests[request_id],
                        "response": entry
                    })
        
        # Сохраняем данные для обучения
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(paired_data, f, indent=2, ensure_ascii=False)
        
        return len(paired_data)
