import asyncio
import os
import json
import subprocess
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import re
import ast
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SeverityLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class IssueCategory(Enum):
    CODE_QUALITY = "code_quality"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    BEST_PRACTICES = "best_practices"
    ACCESSIBILITY = "accessibility"

@dataclass
class CodeIssue:
    file_path: str
    line_number: int
    column: int
    severity: SeverityLevel
    category: IssueCategory
    rule_id: str
    message: str
    code_snippet: str
    suggestion: Optional[str] = None
    auto_fixable: bool = False

@dataclass
class QualityMetrics:
    lines_of_code: int
    cyclomatic_complexity: float
    maintainability_index: float
    code_duplication: float
    test_coverage: float
    technical_debt_ratio: float
    security_hotspots: int
    performance_issues: int

@dataclass
class AnalysisResult:
    project_id: str
    analysis_id: str
    timestamp: datetime
    platform: str
    total_files: int
    analyzed_files: int
    issues: List[CodeIssue]
    metrics: QualityMetrics
    summary: Dict[str, Any]
    recommendations: List[str]

class CodeAnalyzer:
    def __init__(self):
        self.analyzers = {
            'swift': SwiftAnalyzer(),
            'kotlin': KotlinAnalyzer(),
            'javascript': JavaScriptAnalyzer(),
            'python': PythonAnalyzer(),
            'dart': DartAnalyzer()
        }
        self.analysis_history: Dict[str, AnalysisResult] = {}
        
    async def analyze_project(self, project_path: str, project_id: str, 
                            platform: str = 'auto') -> AnalysisResult:
        """Анализирует качество кода проекта"""
        analysis_id = f"{project_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Starting code analysis for project {project_id}")
        
        try:
            # Определяем платформу автоматически если не указана
            if platform == 'auto':
                platform = self._detect_platform(project_path)
                
            # Собираем файлы для анализа
            files_to_analyze = self._collect_files(project_path, platform)
            
            # Выполняем анализ
            all_issues = []
            metrics_data = {
                'lines_of_code': 0,
                'cyclomatic_complexity': 0,
                'files_analyzed': 0
            }
            
            for file_path in files_to_analyze:
                try:
                    file_issues, file_metrics = await self._analyze_file(file_path, platform)
                    all_issues.extend(file_issues)
                    
                    # Собираем метрики
                    metrics_data['lines_of_code'] += file_metrics.get('loc', 0)
                    metrics_data['cyclomatic_complexity'] += file_metrics.get('complexity', 0)
                    metrics_data['files_analyzed'] += 1
                    
                except Exception as e:
                    logger.warning(f"Failed to analyze file {file_path}: {str(e)}")
                    
            # Вычисляем общие метрики
            metrics = self._calculate_metrics(metrics_data, all_issues)
            
            # Генерируем рекомендации
            recommendations = self._generate_recommendations(all_issues, metrics)
            
            # Создаем результат анализа
            result = AnalysisResult(
                project_id=project_id,
                analysis_id=analysis_id,
                timestamp=datetime.now(),
                platform=platform,
                total_files=len(files_to_analyze),
                analyzed_files=metrics_data['files_analyzed'],
                issues=all_issues,
                metrics=metrics,
                summary=self._create_summary(all_issues, metrics),
                recommendations=recommendations
            )
            
            self.analysis_history[analysis_id] = result
            logger.info(f"Code analysis completed: {len(all_issues)} issues found")
            
            return result
            
        except Exception as e:
            logger.error(f"Code analysis failed: {str(e)}")
            raise
            
    def _detect_platform(self, project_path: str) -> str:
        """Определяет платформу проекта"""
        if any(f.endswith('.xcodeproj') for f in os.listdir(project_path)):
            return 'ios'
        elif os.path.exists(os.path.join(project_path, 'build.gradle')):
            return 'android'
        elif os.path.exists(os.path.join(project_path, 'package.json')):
            return 'web'
        elif os.path.exists(os.path.join(project_path, 'pubspec.yaml')):
            return 'flutter'
        else:
            return 'generic'
            
    def _collect_files(self, project_path: str, platform: str) -> List[str]:
        """Собирает файлы для анализа"""
        extensions_map = {
            'ios': ['.swift', '.m', '.h'],
            'android': ['.kt', '.java'],
            'web': ['.js', '.ts', '.jsx', '.tsx'],
            'flutter': ['.dart'],
            'generic': ['.py', '.js', '.ts', '.swift', '.kt', '.dart']
        }
        
        extensions = extensions_map.get(platform, ['.py', '.js', '.ts'])
        files = []
        
        for root, dirs, filenames in os.walk(project_path):
            # Исключаем служебные директории
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'build', 'dist']]
            
            for filename in filenames:
                if any(filename.endswith(ext) for ext in extensions):
                    files.append(os.path.join(root, filename))
                    
        return files
        
    async def _analyze_file(self, file_path: str, platform: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        """Анализирует отдельный файл"""
        file_extension = Path(file_path).suffix.lower()
        
        # Определяем анализатор
        analyzer = None
        if file_extension in ['.swift']:
            analyzer = self.analyzers.get('swift')
        elif file_extension in ['.kt', '.java']:
            analyzer = self.analyzers.get('kotlin')
        elif file_extension in ['.js', '.ts', '.jsx', '.tsx']:
            analyzer = self.analyzers.get('javascript')
        elif file_extension in ['.py']:
            analyzer = self.analyzers.get('python')
        elif file_extension in ['.dart']:
            analyzer = self.analyzers.get('dart')
            
        if analyzer:
            return await analyzer.analyze(file_path)
        else:
            return await self._generic_analysis(file_path)
            
    async def _generic_analysis(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        """Базовый анализ для любых файлов"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {
                'loc': len([line for line in lines if line.strip()]),
                'complexity': 1,  # Базовая сложность
                'comments': len([line for line in lines if line.strip().startswith(('//', '#', '/*'))])
            }
            
            # Проверяем базовые проблемы
            for i, line in enumerate(lines, 1):
                # Длинные строки
                if len(line) > 120:
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=120,
                        severity=SeverityLevel.WARNING,
                        category=IssueCategory.CODE_QUALITY,
                        rule_id="long_line",
                        message="Line too long (>120 characters)",
                        code_snippet=line[:100] + "..." if len(line) > 100 else line,
                        suggestion="Consider breaking this line into multiple lines"
                    ))
                    
                # TODO комментарии
                if 'TODO' in line or 'FIXME' in line:
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=line.find('TODO') if 'TODO' in line else line.find('FIXME'),
                        severity=SeverityLevel.INFO,
                        category=IssueCategory.MAINTAINABILITY,
                        rule_id="todo_comment",
                        message="TODO/FIXME comment found",
                        code_snippet=line.strip(),
                        suggestion="Consider creating a proper issue tracker item"
                    ))
                    
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"Generic analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}
            
    def _calculate_metrics(self, metrics_data: Dict[str, Any], issues: List[CodeIssue]) -> QualityMetrics:
        """Вычисляет общие метрики качества"""
        total_loc = metrics_data.get('lines_of_code', 0)
        files_count = metrics_data.get('files_analyzed', 1)
        
        # Подсчет проблем по категориям
        security_issues = len([i for i in issues if i.category == IssueCategory.SECURITY])
        performance_issues = len([i for i in issues if i.category == IssueCategory.PERFORMANCE])
        critical_issues = len([i for i in issues if i.severity == SeverityLevel.CRITICAL])
        
        # Вычисляем метрики
        avg_complexity = metrics_data.get('cyclomatic_complexity', 0) / max(files_count, 1)
        
        # Индекс поддерживаемости (упрощенная формула)
        maintainability = max(0, min(100, 
            100 - (len(issues) / max(total_loc / 100, 1)) * 10
        ))
        
        # Технический долг (процент проблемных строк)
        tech_debt = min(100, (len(issues) / max(total_loc, 1)) * 100)
        
        # Дублирование кода (мок значение)
        code_duplication = min(20, len(issues) * 0.1)
        
        # Покрытие тестами (мок значение)
        test_coverage = max(0, 80 - len(issues) * 0.5)
        
        return QualityMetrics(
            lines_of_code=total_loc,
            cyclomatic_complexity=avg_complexity,
            maintainability_index=maintainability,
            code_duplication=code_duplication,
            test_coverage=test_coverage,
            technical_debt_ratio=tech_debt,
            security_hotspots=security_issues,
            performance_issues=performance_issues
        )
        
    def _generate_recommendations(self, issues: List[CodeIssue], metrics: QualityMetrics) -> List[str]:
        """Генерирует рекомендации по улучшению кода"""
        recommendations = []
        
        # Анализ по метрикам
        if metrics.maintainability_index < 70:
            recommendations.append("Индекс поддерживаемости низкий. Рекомендуется рефакторинг кода")
            
        if metrics.cyclomatic_complexity > 10:
            recommendations.append("Высокая цикломатическая сложность. Разбейте сложные функции на более простые")
            
        if metrics.code_duplication > 10:
            recommendations.append("Обнаружено дублирование кода. Выделите общую логику в отдельные функции")
            
        if metrics.test_coverage < 70:
            recommendations.append("Низкое покрытие тестами. Добавьте больше unit-тестов")
            
        # Анализ по проблемам
        critical_issues = [i for i in issues if i.severity == SeverityLevel.CRITICAL]
        if critical_issues:
            recommendations.append(f"Найдено {len(critical_issues)} критических проблем. Исправьте их в первую очередь")
            
        security_issues = [i for i in issues if i.category == IssueCategory.SECURITY]
        if security_issues:
            recommendations.append(f"Обнаружено {len(security_issues)} проблем безопасности. Требуется немедленное исправление")
            
        performance_issues = [i for i in issues if i.category == IssueCategory.PERFORMANCE]
        if performance_issues:
            recommendations.append(f"Найдено {len(performance_issues)} проблем производительности. Оптимизируйте код")
            
        # Общие рекомендации
        if len(issues) > 100:
            recommendations.append("Большое количество проблем. Рассмотрите возможность постепенного рефакторинга")
            
        if not recommendations:
            recommendations.append("Качество кода хорошее! Продолжайте следовать лучшим практикам")
            
        return recommendations
        
    def _create_summary(self, issues: List[CodeIssue], metrics: QualityMetrics) -> Dict[str, Any]:
        """Создает сводку анализа"""
        issues_by_severity = {}
        issues_by_category = {}
        
        for issue in issues:
            # По уровню серьезности
            severity = issue.severity.value
            issues_by_severity[severity] = issues_by_severity.get(severity, 0) + 1
            
            # По категориям
            category = issue.category.value
            issues_by_category[category] = issues_by_category.get(category, 0) + 1
            
        # Определяем общую оценку
        if metrics.maintainability_index >= 80:
            quality_grade = "A"
        elif metrics.maintainability_index >= 70:
            quality_grade = "B"
        elif metrics.maintainability_index >= 60:
            quality_grade = "C"
        elif metrics.maintainability_index >= 50:
            quality_grade = "D"
        else:
            quality_grade = "F"
            
        return {
            "total_issues": len(issues),
            "issues_by_severity": issues_by_severity,
            "issues_by_category": issues_by_category,
            "quality_grade": quality_grade,
            "metrics_summary": {
                "maintainability": f"{metrics.maintainability_index:.1f}%",
                "complexity": f"{metrics.cyclomatic_complexity:.1f}",
                "test_coverage": f"{metrics.test_coverage:.1f}%",
                "technical_debt": f"{metrics.technical_debt_ratio:.1f}%"
            }
        }
        
    async def get_analysis_result(self, analysis_id: str) -> Optional[AnalysisResult]:
        """Возвращает результат анализа"""
        return self.analysis_history.get(analysis_id)
        
    async def get_project_history(self, project_id: str) -> List[AnalysisResult]:
        """Возвращает историю анализов проекта"""
        return [result for result in self.analysis_history.values() 
                if result.project_id == project_id]
                
    async def compare_analyses(self, analysis_id1: str, analysis_id2: str) -> Dict[str, Any]:
        """Сравнивает два анализа"""
        result1 = self.analysis_history.get(analysis_id1)
        result2 = self.analysis_history.get(analysis_id2)
        
        if not result1 or not result2:
            return {"error": "Analysis not found"}
            
        return {
            "comparison": {
                "issues_change": len(result2.issues) - len(result1.issues),
                "maintainability_change": result2.metrics.maintainability_index - result1.metrics.maintainability_index,
                "complexity_change": result2.metrics.cyclomatic_complexity - result1.metrics.cyclomatic_complexity,
                "coverage_change": result2.metrics.test_coverage - result1.metrics.test_coverage
            },
            "trend": "improving" if len(result2.issues) < len(result1.issues) else "declining"
        }

class BaseAnalyzer:
    """Базовый класс для анализаторов"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        """Анализирует файл"""
        raise NotImplementedError

class SwiftAnalyzer(BaseAnalyzer):
    """Анализатор для Swift кода"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {'loc': len([line for line in lines if line.strip()]), 'complexity': 1}
            
            # Анализ специфичный для Swift
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Принудительное разворачивание опционалов
                if '!' in line and not line_stripped.startswith('//'):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=line.find('!'),
                        severity=SeverityLevel.WARNING,
                        category=IssueCategory.BEST_PRACTICES,
                        rule_id="force_unwrap",
                        message="Forced unwrapping of optional value",
                        code_snippet=line.strip(),
                        suggestion="Consider using optional binding or nil-coalescing operator"
                    ))
                    
                # Слишком длинные функции
                if line_stripped.startswith('func ') or line_stripped.startswith('private func '):
                    # Подсчитываем строки до закрывающей скобки
                    brace_count = 0
                    func_lines = 0
                    for j in range(i, len(lines)):
                        if '{' in lines[j-1]:
                            brace_count += lines[j-1].count('{')
                        if '}' in lines[j-1]:
                            brace_count -= lines[j-1].count('}')
                        func_lines += 1
                        if brace_count == 0:
                            break
                            
                    if func_lines > 50:
                        issues.append(CodeIssue(
                            file_path=file_path,
                            line_number=i,
                            column=0,
                            severity=SeverityLevel.WARNING,
                            category=IssueCategory.MAINTAINABILITY,
                            rule_id="long_function",
                            message=f"Function too long ({func_lines} lines)",
                            code_snippet=line.strip(),
                            suggestion="Consider breaking this function into smaller functions"
                        ))
                        
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"Swift analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}

class KotlinAnalyzer(BaseAnalyzer):
    """Анализатор для Kotlin кода"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {'loc': len([line for line in lines if line.strip()]), 'complexity': 1}
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Использование !! (not-null assertion)
                if '!!' in line and not line_stripped.startswith('//'):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=line.find('!!'),
                        severity=SeverityLevel.WARNING,
                        category=IssueCategory.BEST_PRACTICES,
                        rule_id="not_null_assertion",
                        message="Not-null assertion operator used",
                        code_snippet=line.strip(),
                        suggestion="Consider using safe call operator or proper null checking"
                    ))
                    
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"Kotlin analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}

class JavaScriptAnalyzer(BaseAnalyzer):
    """Анализатор для JavaScript/TypeScript кода"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {'loc': len([line for line in lines if line.strip()]), 'complexity': 1}
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # Использование var вместо let/const
                if line_stripped.startswith('var ') and not line_stripped.startswith('//'):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=0,
                        severity=SeverityLevel.WARNING,
                        category=IssueCategory.BEST_PRACTICES,
                        rule_id="var_usage",
                        message="Use of 'var' instead of 'let' or 'const'",
                        code_snippet=line.strip(),
                        suggestion="Use 'let' for mutable variables or 'const' for constants"
                    ))
                    
                # console.log в production коде
                if 'console.log' in line and not line_stripped.startswith('//'):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=line.find('console.log'),
                        severity=SeverityLevel.INFO,
                        category=IssueCategory.CODE_QUALITY,
                        rule_id="console_log",
                        message="Console.log statement found",
                        code_snippet=line.strip(),
                        suggestion="Remove console.log statements before production"
                    ))
                    
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"JavaScript analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}

class PythonAnalyzer(BaseAnalyzer):
    """Анализатор для Python кода"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {'loc': len([line for line in lines if line.strip()]), 'complexity': 1}
            
            # Попытка парсинга AST для более глубокого анализа
            try:
                tree = ast.parse(content)
                
                # Анализ функций
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Слишком много аргументов
                        if len(node.args.args) > 7:
                            issues.append(CodeIssue(
                                file_path=file_path,
                                line_number=node.lineno,
                                column=node.col_offset,
                                severity=SeverityLevel.WARNING,
                                category=IssueCategory.CODE_QUALITY,
                                rule_id="too_many_args",
                                message=f"Function has too many arguments ({len(node.args.args)})",
                                code_snippet=f"def {node.name}(...)",
                                suggestion="Consider using a configuration object or refactoring"
                            ))
                            
            except SyntaxError:
                pass  # Файл может содержать синтаксические ошибки
                
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"Python analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}

class DartAnalyzer(BaseAnalyzer):
    """Анализатор для Dart кода"""
    
    async def analyze(self, file_path: str) -> tuple[List[CodeIssue], Dict[str, Any]]:
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
            metrics = {'loc': len([line for line in lines if line.strip()]), 'complexity': 1}
            
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip()
                
                # print statements в production коде
                if 'print(' in line and not line_stripped.startswith('//'):
                    issues.append(CodeIssue(
                        file_path=file_path,
                        line_number=i,
                        column=line.find('print('),
                        severity=SeverityLevel.INFO,
                        category=IssueCategory.CODE_QUALITY,
                        rule_id="print_statement",
                        message="Print statement found",
                        code_snippet=line.strip(),
                        suggestion="Remove print statements before production or use proper logging"
                    ))
                    
            return issues, metrics
            
        except Exception as e:
            logger.warning(f"Dart analysis failed for {file_path}: {str(e)}")
            return [], {'loc': 0, 'complexity': 0}

# Глобальный экземпляр анализатора
code_analyzer = CodeAnalyzer()