
import os
import json
import shutil
import uuid
from datetime import datetime
import zipfile
from pathlib import Path
import hashlib

class ProjectVersionControl:
    def __init__(self, base_dir="projects"):
        self.base_dir = base_dir
        self.versions_dir = os.path.join(base_dir, "versions")
        self.metadata_dir = os.path.join(base_dir, "metadata")
        os.makedirs(self.versions_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)

    def create_project_version(self, project_id, files_dict, version_info):
        """Создает новую версию проекта"""
        timestamp = datetime.now().isoformat()
        version_id = str(uuid.uuid4())
        
        # Создаем структуру версии
        version_path = os.path.join(self.versions_dir, project_id, version_id)
        os.makedirs(version_path, exist_ok=True)
        
        # Сохраняем файлы
        for file_path, content in files_dict.items():
            full_file_path = os.path.join(version_path, file_path)
            os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
            
            with open(full_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        # Создаем метаданные версии
        metadata = {
            "version_id": version_id,
            "project_id": project_id,
            "timestamp": timestamp,
            "version_info": version_info,
            "files": list(files_dict.keys()),
            "file_hashes": {
                path: hashlib.md5(content.encode()).hexdigest() 
                for path, content in files_dict.items()
            }
        }
        
        metadata_path = os.path.join(self.metadata_dir, f"{project_id}_{version_id}.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Обновляем историю проекта
        self.update_project_history(project_id, version_id, version_info)
        
        return version_id

    def update_project_history(self, project_id, version_id, version_info):
        """Обновляет историю версий проекта"""
        history_path = os.path.join(self.metadata_dir, f"{project_id}_history.json")
        
        if os.path.exists(history_path):
            with open(history_path, 'r', encoding='utf-8') as f:
                history = json.load(f)
        else:
            history = {
                "project_id": project_id,
                "created_at": datetime.now().isoformat(),
                "versions": []
            }
        
        version_entry = {
            "version_id": version_id,
            "timestamp": datetime.now().isoformat(),
            "description": version_info.get("description", "Новая версия"),
            "changes": version_info.get("changes", []),
            "author": version_info.get("author", "AI Agent")
        }
        
        history["versions"].append(version_entry)
        
        with open(history_path, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def get_project_versions(self, project_id):
        """Получает список всех версий проекта"""
        history_path = os.path.join(self.metadata_dir, f"{project_id}_history.json")
        
        if os.path.exists(history_path):
            with open(history_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {"project_id": project_id, "versions": []}

    def rollback_to_version(self, project_id, version_id):
        """Откатывает проект к указанной версии"""
        version_path = os.path.join(self.versions_dir, project_id, version_id)
        
        if not os.path.exists(version_path):
            raise ValueError(f"Версия {version_id} не найдена")
        
        # Создаем новую версию как откат
        files_dict = {}
        for root, dirs, files in os.walk(version_path):
            for file in files:
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, version_path)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    files_dict[rel_path] = f.read()
        
        rollback_info = {
            "description": f"Откат к версии {version_id}",
            "changes": ["Восстановлена предыдущая версия"],
            "rollback_from": version_id
        }
        
        new_version_id = self.create_project_version(project_id, files_dict, rollback_info)
        return new_version_id

    def compare_versions(self, project_id, version1_id, version2_id):
        """Сравнивает две версии проекта"""
        metadata1_path = os.path.join(self.metadata_dir, f"{project_id}_{version1_id}.json")
        metadata2_path = os.path.join(self.metadata_dir, f"{project_id}_{version2_id}.json")
        
        if not os.path.exists(metadata1_path) or not os.path.exists(metadata2_path):
            raise ValueError("Одна из версий не найдена")
        
        with open(metadata1_path, 'r', encoding='utf-8') as f:
            metadata1 = json.load(f)
        
        with open(metadata2_path, 'r', encoding='utf-8') as f:
            metadata2 = json.load(f)
        
        comparison = {
            "version1": {
                "id": version1_id,
                "timestamp": metadata1["timestamp"],
                "files": metadata1["files"]
            },
            "version2": {
                "id": version2_id,
                "timestamp": metadata2["timestamp"], 
                "files": metadata2["files"]
            },
            "differences": {
                "added_files": [],
                "removed_files": [],
                "modified_files": []
            }
        }
        
        files1 = set(metadata1["files"])
        files2 = set(metadata2["files"])
        
        comparison["differences"]["added_files"] = list(files2 - files1)
        comparison["differences"]["removed_files"] = list(files1 - files2)
        
        # Проверяем измененные файлы
        common_files = files1 & files2
        for file_path in common_files:
            hash1 = metadata1["file_hashes"].get(file_path)
            hash2 = metadata2["file_hashes"].get(file_path)
            
            if hash1 != hash2:
                comparison["differences"]["modified_files"].append(file_path)
        
        return comparison

    def create_project_backup(self, project_id):
        """Создает полный бэкап проекта"""
        project_versions_path = os.path.join(self.versions_dir, project_id)
        if not os.path.exists(project_versions_path):
            raise ValueError(f"Проект {project_id} не найден")
        
        backup_name = f"backup_{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        backup_path = os.path.join(self.base_dir, "backups")
        os.makedirs(backup_path, exist_ok=True)
        
        backup_file = os.path.join(backup_path, backup_name)
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем все версии
            for root, dirs, files in os.walk(project_versions_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.base_dir)
                    zipf.write(file_path, arcname)
            
            # Добавляем метаданные
            metadata_pattern = f"{project_id}_*.json"
            for metadata_file in Path(self.metadata_dir).glob(metadata_pattern):
                arcname = os.path.join("metadata", metadata_file.name)
                zipf.write(metadata_file, arcname)
        
        return backup_file
