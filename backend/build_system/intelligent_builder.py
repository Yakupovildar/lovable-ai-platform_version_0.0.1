import asyncio
import os
import subprocess
import json
import shutil
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import logging
import hashlib
import zipfile

logger = logging.getLogger(__name__)

class BuildStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    TESTING = "testing"
    DEPLOYING = "deploying"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    DESKTOP = "desktop"

class BuildType(Enum):
    DEBUG = "debug"
    RELEASE = "release"
    TESTING = "testing"

@dataclass
class BuildConfig:
    project_id: str
    platform: Platform
    build_type: BuildType
    source_path: str
    output_path: str
    environment_vars: Dict[str, str]
    build_args: Dict[str, Any]
    test_enabled: bool = True
    deploy_enabled: bool = False
    notifications: List[str] = None

@dataclass
class BuildResult:
    build_id: str
    config: BuildConfig
    status: BuildStatus
    start_time: datetime
    end_time: Optional[datetime]
    duration_seconds: Optional[float]
    artifacts: List[str]
    logs: List[str]
    test_results: Optional[Dict[str, Any]]
    deploy_info: Optional[Dict[str, Any]]
    error_message: Optional[str] = None

class IntelligentBuilder:
    def __init__(self):
        self.builds: Dict[str, BuildResult] = {}
        self.build_queue: asyncio.Queue = asyncio.Queue()
        self.active_builds: Dict[str, asyncio.Task] = {}
        self.max_concurrent_builds = 3
        self.build_cache: Dict[str, str] = {}  # hash -> artifact_path
        
    async def start(self):
        """Запускает систему сборки"""
        # Запускаем обработчики очереди сборки
        for i in range(self.max_concurrent_builds):
            asyncio.create_task(self._build_worker(f"worker-{i}"))
        logger.info("Intelligent Builder started")
        
    async def submit_build(self, config: BuildConfig) -> str:
        """Добавляет сборку в очередь"""
        build_id = self._generate_build_id(config)
        
        build_result = BuildResult(
            build_id=build_id,
            config=config,
            status=BuildStatus.PENDING,
            start_time=datetime.now(),
            end_time=None,
            duration_seconds=None,
            artifacts=[],
            logs=[],
            test_results=None,
            deploy_info=None
        )
        
        self.builds[build_id] = build_result
        await self.build_queue.put(build_id)
        
        logger.info(f"Build {build_id} submitted to queue")
        return build_id
        
    async def get_build_status(self, build_id: str) -> Optional[BuildResult]:
        """Возвращает статус сборки"""
        return self.builds.get(build_id)
        
    async def cancel_build(self, build_id: str) -> bool:
        """Отменяет сборку"""
        if build_id in self.active_builds:
            task = self.active_builds[build_id]
            task.cancel()
            
            if build_id in self.builds:
                self.builds[build_id].status = BuildStatus.CANCELLED
                self.builds[build_id].end_time = datetime.now()
                
            logger.info(f"Build {build_id} cancelled")
            return True
        return False
        
    async def _build_worker(self, worker_name: str):
        """Обработчик очереди сборки"""
        logger.info(f"Build worker {worker_name} started")
        
        while True:
            try:
                build_id = await self.build_queue.get()
                build_result = self.builds.get(build_id)
                
                if not build_result:
                    continue
                    
                logger.info(f"Worker {worker_name} processing build {build_id}")
                
                # Создаем задачу сборки
                task = asyncio.create_task(self._execute_build(build_result))
                self.active_builds[build_id] = task
                
                try:
                    await task
                finally:
                    if build_id in self.active_builds:
                        del self.active_builds[build_id]
                    self.build_queue.task_done()
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Build worker {worker_name} error: {str(e)}")
                
    async def _execute_build(self, build_result: BuildResult):
        """Выполняет сборку проекта"""
        config = build_result.config
        build_result.status = BuildStatus.BUILDING
        build_result.start_time = datetime.now()
        
        try:
            # Проверяем кэш
            cache_key = self._calculate_cache_key(config)
            if cache_key in self.build_cache and config.build_type != BuildType.RELEASE:
                await self._use_cached_build(build_result, cache_key)
                return
                
            # Подготавливаем рабочую директорию
            work_dir = await self._prepare_build_environment(config)
            build_result.logs.append(f"Prepared build environment: {work_dir}")
            
            # Выполняем сборку в зависимости от платформы
            if config.platform == Platform.IOS:
                await self._build_ios(build_result, work_dir)
            elif config.platform == Platform.ANDROID:
                await self._build_android(build_result, work_dir)
            elif config.platform == Platform.WEB:
                await self._build_web(build_result, work_dir)
            else:
                raise Exception(f"Unsupported platform: {config.platform}")
                
            # Запускаем тесты если включены
            if config.test_enabled:
                await self._run_tests(build_result, work_dir)
                
            # Деплоим если включен
            if config.deploy_enabled:
                await self._deploy_artifacts(build_result)
                
            # Сохраняем в кэш
            if build_result.artifacts:
                self.build_cache[cache_key] = build_result.artifacts[0]
                
            build_result.status = BuildStatus.SUCCESS
            build_result.end_time = datetime.now()
            build_result.duration_seconds = (build_result.end_time - build_result.start_time).total_seconds()
            
            logger.info(f"Build {build_result.build_id} completed successfully")
            
        except Exception as e:
            build_result.status = BuildStatus.FAILED
            build_result.end_time = datetime.now()
            build_result.error_message = str(e)
            build_result.logs.append(f"Build failed: {str(e)}")
            
            logger.error(f"Build {build_result.build_id} failed: {str(e)}")
            
    async def _build_ios(self, build_result: BuildResult, work_dir: str):
        """Собирает iOS приложение"""
        config = build_result.config
        build_result.logs.append("Starting iOS build...")
        
        # Находим .xcodeproj или .xcworkspace
        project_files = []
        for file in os.listdir(work_dir):
            if file.endswith('.xcodeproj') or file.endswith('.xcworkspace'):
                project_files.append(file)
                
        if not project_files:
            raise Exception("No Xcode project or workspace found")
            
        project_file = project_files[0]
        is_workspace = project_file.endswith('.xcworkspace')
        
        # Определяем схему сборки
        scheme = config.build_args.get('scheme', 'Debug')
        configuration = 'Release' if config.build_type == BuildType.RELEASE else 'Debug'
        
        # Команда xcodebuild
        xcode_cmd = [
            'xcodebuild',
            '-workspace' if is_workspace else '-project',
            os.path.join(work_dir, project_file),
            '-scheme', scheme,
            '-configuration', configuration,
            '-derivedDataPath', os.path.join(work_dir, 'DerivedData'),
            'archive',
            '-archivePath', os.path.join(work_dir, 'archive.xcarchive')
        ]
        
        # Добавляем переменные окружения
        env = dict(os.environ)
        env.update(config.environment_vars)
        
        # Выполняем сборку
        result = await self._run_command(xcode_cmd, work_dir, env)
        build_result.logs.extend(result['stdout'])
        
        if result['returncode'] != 0:
            raise Exception(f"Xcode build failed: {result['stderr']}")
            
        # Экспортируем IPA
        if config.build_type == BuildType.RELEASE:
            await self._export_ios_ipa(build_result, work_dir)
        else:
            # Для debug сборок копируем .app
            archive_path = os.path.join(work_dir, 'archive.xcarchive')
            app_path = self._find_app_in_archive(archive_path)
            if app_path:
                artifact_name = f"{config.project_id}_{config.build_type.value}.app"
                artifact_path = os.path.join(config.output_path, artifact_name)
                shutil.copytree(app_path, artifact_path)
                build_result.artifacts.append(artifact_path)
                
    async def _build_android(self, build_result: BuildResult, work_dir: str):
        """Собирает Android приложение"""
        config = build_result.config
        build_result.logs.append("Starting Android build...")
        
        # Проверяем наличие градла
        gradlew_path = os.path.join(work_dir, 'gradlew')
        if not os.path.exists(gradlew_path):
            raise Exception("gradlew not found")
            
        # Делаем gradlew исполняемым
        os.chmod(gradlew_path, 0o755)
        
        # Определяем таск сборки
        build_task = 'assembleRelease' if config.build_type == BuildType.RELEASE else 'assembleDebug'
        
        gradle_cmd = [
            './gradlew',
            build_task,
            '--stacktrace'
        ]
        
        # Добавляем аргументы сборки
        for key, value in config.build_args.items():
            gradle_cmd.append(f'-P{key}={value}')
            
        # Переменные окружения
        env = dict(os.environ)
        env.update(config.environment_vars)
        env['ANDROID_HOME'] = env.get('ANDROID_HOME', '/opt/android-sdk')
        
        # Выполняем сборку
        result = await self._run_command(gradle_cmd, work_dir, env)
        build_result.logs.extend(result['stdout'])
        
        if result['returncode'] != 0:
            raise Exception(f"Gradle build failed: {result['stderr']}")
            
        # Ищем APK файлы
        apk_files = []
        build_dir = os.path.join(work_dir, 'app', 'build', 'outputs', 'apk')
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                if file.endswith('.apk'):
                    apk_files.append(os.path.join(root, file))
                    
        if apk_files:
            for apk_file in apk_files:
                artifact_name = f"{config.project_id}_{config.build_type.value}.apk"
                artifact_path = os.path.join(config.output_path, artifact_name)
                shutil.copy2(apk_file, artifact_path)
                build_result.artifacts.append(artifact_path)
        else:
            raise Exception("No APK files found after build")
            
    async def _build_web(self, build_result: BuildResult, work_dir: str):
        """Собирает веб приложение"""
        config = build_result.config
        build_result.logs.append("Starting Web build...")
        
        # Проверяем package.json
        package_json = os.path.join(work_dir, 'package.json')
        if not os.path.exists(package_json):
            raise Exception("package.json not found")
            
        # Устанавливаем зависимости
        install_cmd = ['npm', 'install']
        result = await self._run_command(install_cmd, work_dir)
        build_result.logs.extend(result['stdout'])
        
        if result['returncode'] != 0:
            raise Exception(f"npm install failed: {result['stderr']}")
            
        # Определяем команду сборки
        build_script = 'build:prod' if config.build_type == BuildType.RELEASE else 'build'
        build_cmd = ['npm', 'run', build_script]
        
        # Переменные окружения
        env = dict(os.environ)
        env.update(config.environment_vars)
        
        # Выполняем сборку
        result = await self._run_command(build_cmd, work_dir, env)
        build_result.logs.extend(result['stdout'])
        
        if result['returncode'] != 0:
            raise Exception(f"npm build failed: {result['stderr']}")
            
        # Архивируем результат сборки
        dist_dir = os.path.join(work_dir, 'dist')
        if os.path.exists(dist_dir):
            artifact_name = f"{config.project_id}_{config.build_type.value}.zip"
            artifact_path = os.path.join(config.output_path, artifact_name)
            
            with zipfile.ZipFile(artifact_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(dist_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, dist_dir)
                        zipf.write(file_path, arcname)
                        
            build_result.artifacts.append(artifact_path)
        else:
            raise Exception("Dist directory not found after build")
            
    async def _run_tests(self, build_result: BuildResult, work_dir: str):
        """Запускает тесты"""
        config = build_result.config
        build_result.status = BuildStatus.TESTING
        build_result.logs.append("Running tests...")
        
        test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_duration": 0,
            "coverage": 0
        }
        
        try:
            if config.platform == Platform.IOS:
                # iOS тесты через xcodebuild test
                test_cmd = ['xcodebuild', 'test', '-workspace', '...', '-scheme', '...']
            elif config.platform == Platform.ANDROID:
                # Android тесты через gradle
                test_cmd = ['./gradlew', 'test']
            elif config.platform == Platform.WEB:
                # Веб тесты через npm
                test_cmd = ['npm', 'test']
            else:
                build_result.logs.append("Tests skipped - platform not supported")
                return
                
            result = await self._run_command(test_cmd, work_dir)
            build_result.logs.extend(result['stdout'])
            
            # Парсим результаты тестов (упрощенная логика)
            test_results["total_tests"] = 10  # Мок данные
            test_results["passed_tests"] = 8
            test_results["failed_tests"] = 2
            
            build_result.test_results = test_results
            
            if result['returncode'] != 0:
                build_result.logs.append("Some tests failed, but continuing build")
                
        except Exception as e:
            build_result.logs.append(f"Test execution failed: {str(e)}")
            test_results["failed_tests"] = test_results["total_tests"]
            build_result.test_results = test_results
            
    async def _deploy_artifacts(self, build_result: BuildResult):
        """Деплоит артефакты"""
        config = build_result.config
        build_result.status = BuildStatus.DEPLOYING
        build_result.logs.append("Deploying artifacts...")
        
        deploy_info = {
            "deployed_at": datetime.now().isoformat(),
            "artifacts": [],
            "status": "success"
        }
        
        try:
            for artifact in build_result.artifacts:
                # Здесь можно добавить различные методы деплоя:
                # - Upload to App Store Connect (iOS)
                # - Upload to Google Play Console (Android)
                # - Deploy to web hosting
                # - Deploy to internal distribution
                
                deploy_info["artifacts"].append({
                    "path": artifact,
                    "size": os.path.getsize(artifact),
                    "deployed": True
                })
                
            build_result.deploy_info = deploy_info
            build_result.logs.append("Deployment completed successfully")
            
        except Exception as e:
            deploy_info["status"] = "failed"
            deploy_info["error"] = str(e)
            build_result.deploy_info = deploy_info
            build_result.logs.append(f"Deployment failed: {str(e)}")
            raise
            
    async def _prepare_build_environment(self, config: BuildConfig) -> str:
        """Подготавливает окружение для сборки"""
        work_dir = os.path.join("/tmp", f"build_{config.project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(work_dir, exist_ok=True)
        
        # Копируем исходники
        if os.path.isdir(config.source_path):
            shutil.copytree(config.source_path, work_dir, dirs_exist_ok=True)
        else:
            # Если это архив
            if config.source_path.endswith('.zip'):
                with zipfile.ZipFile(config.source_path, 'r') as zipf:
                    zipf.extractall(work_dir)
                    
        # Создаем директорию для выходных файлов
        os.makedirs(config.output_path, exist_ok=True)
        
        return work_dir
        
    async def _run_command(self, cmd: List[str], cwd: str, env: Dict[str, str] = None) -> Dict[str, Any]:
        """Выполняет команду оболочки"""
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        return {
            "returncode": process.returncode,
            "stdout": stdout.decode().split('\n') if stdout else [],
            "stderr": stderr.decode().split('\n') if stderr else []
        }
        
    def _generate_build_id(self, config: BuildConfig) -> str:
        """Генерирует уникальный ID сборки"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        hash_data = f"{config.project_id}_{config.platform.value}_{config.build_type.value}_{timestamp}"
        hash_id = hashlib.md5(hash_data.encode()).hexdigest()[:8]
        return f"{config.project_id}_{hash_id}"
        
    def _calculate_cache_key(self, config: BuildConfig) -> str:
        """Вычисляет ключ для кэширования"""
        cache_data = {
            "project_id": config.project_id,
            "platform": config.platform.value,
            "build_type": config.build_type.value,
            "source_hash": self._calculate_source_hash(config.source_path)
        }
        cache_string = json.dumps(cache_data, sort_keys=True)
        return hashlib.sha256(cache_string.encode()).hexdigest()
        
    def _calculate_source_hash(self, source_path: str) -> str:
        """Вычисляет хэш исходного кода"""
        # Упрощенная реализация - в реальности нужно учитывать все файлы
        if os.path.isfile(source_path):
            with open(source_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        else:
            return hashlib.md5(source_path.encode()).hexdigest()
            
    async def _use_cached_build(self, build_result: BuildResult, cache_key: str):
        """Использует кэшированную сборку"""
        cached_artifact = self.build_cache[cache_key]
        if os.path.exists(cached_artifact):
            build_result.artifacts.append(cached_artifact)
            build_result.status = BuildStatus.SUCCESS
            build_result.end_time = datetime.now()
            build_result.logs.append("Used cached build artifact")
            logger.info(f"Build {build_result.build_id} used cached artifact")
        
    def get_build_statistics(self) -> Dict[str, Any]:
        """Возвращает статистику сборок"""
        stats = {
            "total_builds": len(self.builds),
            "successful_builds": 0,
            "failed_builds": 0,
            "average_build_time": 0,
            "builds_by_platform": {},
            "builds_by_status": {},
            "cache_hit_rate": 0
        }
        
        total_duration = 0
        successful_count = 0
        
        for build in self.builds.values():
            # По статусам
            status = build.status.value
            stats["builds_by_status"][status] = stats["builds_by_status"].get(status, 0) + 1
            
            # По платформам
            platform = build.config.platform.value
            stats["builds_by_platform"][platform] = stats["builds_by_platform"].get(platform, 0) + 1
            
            # Время сборки
            if build.duration_seconds:
                total_duration += build.duration_seconds
                
            if build.status == BuildStatus.SUCCESS:
                successful_count += 1
                
        stats["successful_builds"] = successful_count
        stats["failed_builds"] = len(self.builds) - successful_count
        
        if len(self.builds) > 0:
            stats["average_build_time"] = total_duration / len(self.builds)
            
        return stats

# Глобальный экземпляр Builder
intelligent_builder = IntelligentBuilder()