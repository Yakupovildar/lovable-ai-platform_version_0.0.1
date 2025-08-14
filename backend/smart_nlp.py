import re
import string
from typing import List, Dict, Any

class SmartNLP:
    def __init__(self):
        self.stopwords = {
            'а', 'в', 'и', 'с', 'на', 'по', 'для', 'от', 'до', 'из', 'к', 'о', 'у', 'за', 'над', 'под', 'при', 'про'
        }

        # Словарь исправлений опечаток
        self.corrections = {
            'создай': ['создай', 'создать', 'сделай', 'сделать'],
            'приложение': ['приложение', 'прилож', 'app'],
            'игра': ['игра', 'игру', 'game'],
            'сайт': ['сайт', 'сайты', 'website', 'веб'],
            'мобильное': ['мобильное', 'мобильн', 'mobile'],
            'веб': ['веб', 'web', 'интернет']
        }

    def correct_and_normalize(self, text: str) -> str:
        """Исправляет опечатки и нормализует текст"""
        if not text:
            return ""

        # Приводим к нижнему регистру
        text = text.lower().strip()

        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)

        # Удаляем знаки препинания в конце
        text = text.rstrip(string.punctuation)

        return text

    def extract_keywords(self, text: str) -> List[str]:
        """Извлекает ключевые слова из текста"""
        text = self.correct_and_normalize(text)
        words = text.split()

        # Фильтруем стоп-слова
        keywords = [word for word in words if word not in self.stopwords and len(word) > 2]

        return keywords

    def analyze_intent(self, text: str) -> Dict[str, Any]:
        """Анализирует намерение в тексте"""
        text = self.correct_and_normalize(text)
        keywords = self.extract_keywords(text)

        intent_patterns = {
            'create_project': ['создай', 'сделай', 'разработай', 'построй'],
            'modify_project': ['изменить', 'доработать', 'улучшить', 'добавить'],
            'help': ['помощь', 'помоги', 'как', 'что'],
            'greeting': ['привет', 'здравствуй', 'добрый']
        }

        detected_intent = 'general'
        confidence = 0.0

        for intent, patterns in intent_patterns.items():
            matches = sum(1 for pattern in patterns if pattern in text)
            if matches > 0:
                current_confidence = matches / len(patterns)
                if current_confidence > confidence:
                    confidence = current_confidence
                    detected_intent = intent

        return {
            'intent': detected_intent,
            'confidence': confidence,
            'keywords': keywords
        }

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Извлекает именованные сущности"""
        text = self.correct_and_normalize(text)

        entities = {
            'project_types': [],
            'technologies': [],
            'platforms': []
        }

        # Типы проектов
        project_patterns = ['игра', 'приложение', 'сайт', 'бот', 'калькулятор']
        for pattern in project_patterns:
            if pattern in text:
                entities['project_types'].append(pattern)

        # Технологии
        tech_patterns = ['react', 'vue', 'angular', 'python', 'javascript', 'html', 'css']
        for pattern in tech_patterns:
            if pattern in text:
                entities['technologies'].append(pattern)

        # Платформы
        platform_patterns = ['ios', 'android', 'веб', 'мобильное']
        for pattern in platform_patterns:
            if pattern in text:
                entities['platforms'].append(pattern)

        return entities

    def get_similarity(self, text1: str, text2: str) -> float:
        """Вычисляет похожесть двух текстов"""
        keywords1 = set(self.extract_keywords(text1))
        keywords2 = set(self.extract_keywords(text2))

        if not keywords1 or not keywords2:
            return 0.0

        intersection = keywords1.intersection(keywords2)
        union = keywords1.union(keywords2)

        return len(intersection) / len(union) if union else 0.0