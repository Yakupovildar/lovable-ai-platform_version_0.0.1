import re
import string
from typing import List, Dict, Any

class SmartNLP:
    def __init__(self):
        self.stopwords = {
            'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между'
        }

    def correct_and_normalize(self, text: str) -> str:
        """Исправляет опечатки и нормализует текст"""
        if not text:
            return ""

        # Приводим к нижнему регистру
        text = text.lower().strip()

        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', text)

        # Простые исправления частых опечаток
        corrections = {
            'создай': ['создай', 'создать', 'сделай', 'сделать'],
            'игра': ['игра', 'игру', 'игры'],
            'приложение': ['приложение', 'прилож', 'приложения'],
            'сайт': ['сайт', 'сайты', 'website'],
            'мобильное': ['мобильное', 'мобильн', 'mobile'],
        }

        # Применяем исправления
        for correct, variants in corrections.items():
            for variant in variants:
                if variant in text and variant != correct:
                    text = text.replace(variant, correct)

        return text

    def extract_keywords(self, text: str) -> List[str]:
        """Извлекает ключевые слова из текста"""
        if not text:
            return []

        # Убираем пунктуацию
        text = text.translate(str.maketrans('', '', string.punctuation))

        # Разбиваем на слова
        words = text.lower().split()

        # Фильтруем стоп-слова
        keywords = [word for word in words if word not in self.stopwords and len(word) > 2]

        return keywords

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Простой анализ тональности"""
        positive_words = ['хочу', 'нужно', 'создай', 'сделай', 'отлично', 'супер', 'класс', 'круто', 'прекрасно']
        negative_words = ['не', 'нет', 'плохо', 'ужасно', 'отвратительно']

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return {
            'sentiment': sentiment,
            'confidence': abs(positive_count - negative_count) / max(len(text.split()), 1),
            'positive_score': positive_count,
            'negative_score': negative_count
        }

    def classify_intent(self, text: str) -> str:
        """Классифицирует намерение пользователя"""
        text_lower = text.lower()

        # Создание приложения
        if any(word in text_lower for word in ['создай', 'сделай', 'разработай', 'хочу создать']):
            return 'create_app'

        # Вопросы
        elif any(word in text_lower for word in ['как', 'что', 'где', 'когда', 'почему']):
            return 'question'

        # Приветствие
        elif any(word in text_lower for word in ['привет', 'здравствуй', 'добрый']):
            return 'greeting'

        # Подтверждение
        elif any(word in text_lower for word in ['да', 'согласен', 'ок', 'хорошо']):
            return 'confirmation'

        # Отрицание
        elif any(word in text_lower for word in ['нет', 'не согласен', 'отмена']):
            return 'rejection'

        return 'general'