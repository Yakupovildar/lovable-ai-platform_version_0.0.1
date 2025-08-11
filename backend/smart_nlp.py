
import re
import difflib
from fuzzywuzzy import fuzz
from textdistance import levenshtein
import spacy
from collections import defaultdict
import json
import time

class SmartNLP:
    def __init__(self):
        self.intent_patterns = {
            'create_game': [
                'игра', 'игру', 'геймс', 'game', 'змейка', 'змеёка', 'змейку', 'снейк', 'snake',
                'тетрис', 'tetris', 'аркада', 'аркаду', 'платформер', 'шутер', 'раннер',
                'головоломка', 'пазл', 'puzzle', 'квест', 'рпг', 'rpg', 'стратегия'
            ],
            'create_app': [
                'приложение', 'приложения', 'app', 'апп', 'мобильное', 'todo', 'тудо', 'туду',
                'планировщик', 'органайзер', 'трекер', 'tracker', 'календарь', 'заметки',
                'чат', 'социальное', 'фитнес', 'здоровье', 'финансы', 'банкинг'
            ],
            'create_website': [
                'сайт', 'сайты', 'website', 'веб', 'web', 'лендинг', 'landing', 'портфолио',
                'блог', 'магазин', 'интернет-магазин', 'ecommerce', 'корпоративный'
            ],
            'create_complex': [
                'сложное', 'enterprise', 'crm', 'erp', 'система', 'платформа', 'dashboard',
                'дашборд', 'админка', 'панель', 'управления', 'аналитика', 'bi'
            ],
            'show_trends': [
                'тренд', 'тренды', 'trends', 'популярно', 'востребовано', 'рынок', 'market',
                'статистика', 'аналитика', 'данные', 'исследование'
            ],
            'monetization': [
                'заработок', 'деньги', 'доход', 'монетизация', 'прибыль', 'бизнес',
                'продажи', 'реклама', 'подписка', 'freemium'
            ]
        }
        
        # Словарь для исправления опечаток
        self.correction_dict = {
            'зиейка': 'змейка',
            'змеёка': 'змейка', 
            'снейк': 'змейка',
            'тетрс': 'тетрис',
            'тетриз': 'тетрис',
            'тудо': 'todo',
            'туду': 'todo',
            'приложени': 'приложение',
            'сайты': 'сайт',
            'вебсайт': 'сайт',
            'трендс': 'тренды',
            'популярн': 'популярно'
        }

    def correct_spelling(self, text):
        """Исправление опечаток в тексте"""
        words = text.lower().split()
        corrected_words = []
        
        for word in words:
            # Убираем знаки препинания
            clean_word = re.sub(r'[^\w]', '', word)
            
            # Проверяем прямые совпадения в словаре
            if clean_word in self.correction_dict:
                corrected_words.append(self.correction_dict[clean_word])
                continue
            
            # Ищем похожие слова
            best_match = None
            best_score = 0
            
            for intent_words in self.intent_patterns.values():
                for correct_word in intent_words:
                    if len(clean_word) > 2 and len(correct_word) > 2:
                        score = fuzz.ratio(clean_word, correct_word)
                        if score > 75 and score > best_score:
                            best_score = score
                            best_match = correct_word
            
            if best_match:
                corrected_words.append(best_match)
            else:
                corrected_words.append(word)
        
        return ' '.join(corrected_words)

    def classify_intent_advanced(self, text):
        """Продвинутая классификация намерений с обработкой опечаток"""
        # Исправляем опечатки
        corrected_text = self.correct_spelling(text)
        
        # Анализируем намерения
        intent_scores = defaultdict(float)
        
        for intent, keywords in self.intent_patterns.items():
            for keyword in keywords:
                # Точное совпадение
                if keyword in corrected_text.lower():
                    intent_scores[intent] += 1.0
                
                # Частичное совпадение
                for word in corrected_text.lower().split():
                    similarity = fuzz.ratio(word, keyword)
                    if similarity > 80:
                        intent_scores[intent] += similarity / 100.0
        
        # Контекстный анализ
        if any(word in corrected_text.lower() for word in ['база данных', 'api', 'backend', 'сложная логика']):
            intent_scores['create_complex'] += 0.5
        
        if any(word in corrected_text.lower() for word in ['landing', 'лендинг', 'промо', 'презентация']):
            intent_scores['create_website'] += 0.5
        
        # Возвращаем наиболее вероятное намерение
        if intent_scores:
            best_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[best_intent]
            return {
                'intent': best_intent,
                'confidence': confidence,
                'corrected_text': corrected_text,
                'suggestions': self.generate_suggestions(best_intent, corrected_text)
            }
        
        return {
            'intent': 'general',
            'confidence': 0.0,
            'corrected_text': corrected_text,
            'suggestions': []
        }

    def generate_suggestions(self, intent, text):
        """Генерация умных предложений на основе намерения"""
        suggestions = {
            'create_game': [
                "🎮 Создать современную змейку с AI-соперником",
                "🧩 Разработать 3D тетрис с мультиплеером", 
                "🏃 Сделать endless runner с процедурной генерацией",
                "🎯 Игра-головоломка с системой достижений"
            ],
            'create_app': [
                "📱 TODO с AI-помощником и командной работой",
                "💪 Фитнес-трекер с персонализированными планами",
                "💰 Финансовый менеджер с аналитикой",
                "📊 CRM-система для малого бизнеса"
            ],
            'create_website': [
                "🌐 Адаптивный лендинг с A/B тестированием",
                "🛒 Интернет-магазин с системой платежей",
                "📝 Корпоративный сайт с CMS",
                "🎨 Портфолио с анимациями и галереей"
            ],
            'create_complex': [
                "⚡ Enterprise CRM с интеграциями",
                "📊 BI-платформа с real-time аналитикой",
                "🔐 Система управления пользователями",
                "🌍 Многопользовательская платформа"
            ],
            'show_trends': [
                "📈 Показать актуальные тренды 2024",
                "💎 ТОП-10 прибыльных ниш",
                "🚀 Быстрорастущие направления",
                "💰 Анализ ROI по сферам"
            ]
        }
        
        return suggestions.get(intent, [
            "💡 Помочь с выбором проекта",
            "🎯 Показать примеры успешных решений",
            "📊 Проанализировать рынок",
            "🚀 Начать с MVP"
        ])
