import json
import os
import shutil
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
from datetime import datetime
import yaml

logger = logging.getLogger(__name__)

class TemplateType(Enum):
    IOS_MENTOR = "ios_mentor"
    ANDROID_MENTOR = "android_mentor"
    IOS_ECOMMERCE = "ios_ecommerce"
    ANDROID_ECOMMERCE = "android_ecommerce"
    IOS_SOCIAL = "ios_social"
    ANDROID_SOCIAL = "android_social"
    IOS_FITNESS = "ios_fitness"
    ANDROID_FITNESS = "android_fitness"
    IOS_EDUCATION = "ios_education"
    ANDROID_EDUCATION = "android_education"
    REACT_NATIVE_UNIVERSAL = "react_native_universal"
    FLUTTER_UNIVERSAL = "flutter_universal"

class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    CROSS_PLATFORM = "cross_platform"

@dataclass
class TemplateFeature:
    name: str
    description: str
    required: bool
    dependencies: List[str]
    configuration: Dict[str, Any]

@dataclass
class TemplateMetadata:
    template_id: str
    name: str
    description: str
    version: str
    platform: Platform
    template_type: TemplateType
    author: str
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    features: List[TemplateFeature]
    requirements: Dict[str, str]
    examples: List[Dict[str, str]]

class TemplateEngine:
    def __init__(self, templates_directory: str = "templates"):
        self.templates_directory = templates_directory
        self.templates_cache: Dict[str, TemplateMetadata] = {}
        self._ensure_templates_directory()
        self._load_templates()
        
    def _ensure_templates_directory(self):
        """Создает директорию шаблонов если её нет"""
        os.makedirs(self.templates_directory, exist_ok=True)
        
        # Создаем поддиректории для каждой платформы
        for platform in Platform:
            platform_dir = os.path.join(self.templates_directory, platform.value)
            os.makedirs(platform_dir, exist_ok=True)
            
    def _load_templates(self):
        """Загружает все доступные шаблоны"""
        self.templates_cache.clear()
        
        for platform in Platform:
            platform_dir = os.path.join(self.templates_directory, platform.value)
            if os.path.exists(platform_dir):
                for template_dir in os.listdir(platform_dir):
                    template_path = os.path.join(platform_dir, template_dir)
                    if os.path.isdir(template_path):
                        metadata = self._load_template_metadata(template_path)
                        if metadata:
                            self.templates_cache[metadata.template_id] = metadata
                            
        logger.info(f"Loaded {len(self.templates_cache)} templates")
        
    def _load_template_metadata(self, template_path: str) -> Optional[TemplateMetadata]:
        """Загружает метаданные шаблона"""
        metadata_file = os.path.join(template_path, "template.yaml")
        if not os.path.exists(metadata_file):
            return None
            
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            features = []
            for feature_data in data.get('features', []):
                feature = TemplateFeature(
                    name=feature_data['name'],
                    description=feature_data['description'],
                    required=feature_data.get('required', False),
                    dependencies=feature_data.get('dependencies', []),
                    configuration=feature_data.get('configuration', {})
                )
                features.append(feature)
                
            metadata = TemplateMetadata(
                template_id=data['template_id'],
                name=data['name'],
                description=data['description'],
                version=data['version'],
                platform=Platform(data['platform']),
                template_type=TemplateType(data['template_type']),
                author=data.get('author', 'Unknown'),
                created_at=datetime.fromisoformat(data['created_at']),
                updated_at=datetime.fromisoformat(data['updated_at']),
                tags=data.get('tags', []),
                features=features,
                requirements=data.get('requirements', {}),
                examples=data.get('examples', [])
            )
            
            return metadata
            
        except Exception as e:
            logger.error(f"Failed to load template metadata from {template_path}: {str(e)}")
            return None
            
    def get_all_templates(self) -> List[TemplateMetadata]:
        """Возвращает все доступные шаблоны"""
        return list(self.templates_cache.values())
        
    def get_templates_by_platform(self, platform: Platform) -> List[TemplateMetadata]:
        """Возвращает шаблоны для конкретной платформы"""
        return [template for template in self.templates_cache.values() 
                if template.platform == platform]
                
    def get_templates_by_type(self, template_type: TemplateType) -> List[TemplateMetadata]:
        """Возвращает шаблоны конкретного типа"""
        return [template for template in self.templates_cache.values()
                if template.template_type == template_type]
                
    def search_templates(self, query: str) -> List[TemplateMetadata]:
        """Поиск шаблонов по ключевым словам"""
        query = query.lower()
        results = []
        
        for template in self.templates_cache.values():
            if (query in template.name.lower() or 
                query in template.description.lower() or
                any(query in tag.lower() for tag in template.tags)):
                results.append(template)
                
        return results
        
    def get_template(self, template_id: str) -> Optional[TemplateMetadata]:
        """Возвращает конкретный шаблон"""
        return self.templates_cache.get(template_id)
        
    def generate_project_from_template(self, template_id: str, project_name: str, 
                                     output_dir: str, variables: Dict[str, Any] = None) -> Dict[str, Any]:
        """Генерирует проект на основе шаблона"""
        template = self.get_template(template_id)
        if not template:
            return {"success": False, "error": f"Template {template_id} not found"}
            
        try:
            # Путь к шаблону
            template_path = os.path.join(
                self.templates_directory, 
                template.platform.value, 
                template_id
            )
            
            # Путь к выходному проекту
            project_path = os.path.join(output_dir, project_name)
            os.makedirs(project_path, exist_ok=True)
            
            # Копируем файлы шаблона
            template_files_dir = os.path.join(template_path, "files")
            if os.path.exists(template_files_dir):
                self._copy_template_files(template_files_dir, project_path, variables or {})
                
            # Обрабатываем конфигурацию
            config = self._generate_project_config(template, project_name, variables or {})
            config_file = os.path.join(project_path, "project_config.json")
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
            return {
                "success": True,
                "project_path": project_path,
                "template_id": template_id,
                "config": config
            }
            
        except Exception as e:
            logger.error(f"Failed to generate project from template {template_id}: {str(e)}")
            return {"success": False, "error": str(e)}
            
    def _copy_template_files(self, source_dir: str, dest_dir: str, variables: Dict[str, Any]):
        """Копирует и обрабатывает файлы шаблона"""
        for root, dirs, files in os.walk(source_dir):
            # Вычисляем относительный путь
            rel_path = os.path.relpath(root, source_dir)
            if rel_path == '.':
                target_dir = dest_dir
            else:
                target_dir = os.path.join(dest_dir, rel_path)
                os.makedirs(target_dir, exist_ok=True)
                
            for file in files:
                source_file = os.path.join(root, file)
                target_file = os.path.join(target_dir, file)
                
                # Обрабатываем шаблонизацию
                if file.endswith(('.swift', '.kt', '.js', '.ts', '.dart', '.yaml', '.json', '.xml')):
                    self._process_template_file(source_file, target_file, variables)
                else:
                    shutil.copy2(source_file, target_file)
                    
    def _process_template_file(self, source_file: str, target_file: str, variables: Dict[str, Any]):
        """Обрабатывает файл шаблона с заменой переменных"""
        try:
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Простая замена переменных в формате {{variable_name}}
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))
                
            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            logger.error(f"Failed to process template file {source_file}: {str(e)}")
            shutil.copy2(source_file, target_file)
            
    def _generate_project_config(self, template: TemplateMetadata, project_name: str, 
                               variables: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует конфигурацию проекта"""
        return {
            "project_name": project_name,
            "template": {
                "id": template.template_id,
                "name": template.name,
                "version": template.version,
                "platform": template.platform.value,
                "type": template.template_type.value
            },
            "features": [asdict(feature) for feature in template.features],
            "variables": variables,
            "requirements": template.requirements,
            "generated_at": datetime.now().isoformat()
        }
        
    def create_custom_template(self, template_data: Dict[str, Any], 
                             template_files: Dict[str, str]) -> Dict[str, Any]:
        """Создает пользовательский шаблон"""
        try:
            template_id = template_data['template_id']
            platform = Platform(template_data['platform'])
            
            # Создаем директорию для шаблона
            template_path = os.path.join(
                self.templates_directory,
                platform.value,
                template_id
            )
            os.makedirs(template_path, exist_ok=True)
            
            # Сохраняем метаданные
            metadata_file = os.path.join(template_path, "template.yaml")
            with open(metadata_file, 'w', encoding='utf-8') as f:
                yaml.dump(template_data, f, default_flow_style=False, allow_unicode=True)
                
            # Сохраняем файлы шаблона
            files_dir = os.path.join(template_path, "files")
            os.makedirs(files_dir, exist_ok=True)
            
            for file_path, content in template_files.items():
                full_file_path = os.path.join(files_dir, file_path)
                os.makedirs(os.path.dirname(full_file_path), exist_ok=True)
                
                with open(full_file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
            # Перезагружаем шаблоны
            self._load_templates()
            
            return {
                "success": True,
                "template_id": template_id,
                "template_path": template_path
            }
            
        except Exception as e:
            logger.error(f"Failed to create custom template: {str(e)}")
            return {"success": False, "error": str(e)}
            
    def get_template_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику шаблонов"""
        stats = {
            "total_templates": len(self.templates_cache),
            "by_platform": {},
            "by_type": {},
            "by_tags": {},
            "most_featured": None
        }
        
        for template in self.templates_cache.values():
            # По платформам
            platform = template.platform.value
            stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1
            
            # По типам
            template_type = template.template_type.value
            stats["by_type"][template_type] = stats["by_type"].get(template_type, 0) + 1
            
            # По тегам
            for tag in template.tags:
                stats["by_tags"][tag] = stats["by_tags"].get(tag, 0) + 1
                
        # Найти шаблон с наибольшим количеством функций
        if self.templates_cache:
            most_featured = max(self.templates_cache.values(), key=lambda t: len(t.features))
            stats["most_featured"] = {
                "template_id": most_featured.template_id,
                "name": most_featured.name,
                "features_count": len(most_featured.features)
            }
            
        return stats

# Глобальный экземпляр Template Engine
template_engine = TemplateEngine()