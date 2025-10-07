#!/usr/bin/env python3
"""
WEB RESEARCH ENGINE - Революционная система поиска и анализа
Использует только БЕСПЛАТНЫЕ API с максимальными лимитами!
"""

import os
import json
import time
import asyncio
import aiohttp
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import re
from urllib.parse import quote, urlparse

@dataclass
class ResearchResult:
    """Результат исследования"""
    query: str
    sources: List[Dict[str, Any]]
    analysis: str
    confidence: float
    timestamp: datetime
    total_sources: int

class WebResearchEngine:
    """🚀 Революционный движок веб-исследований"""

    def __init__(self):
        # Бесплатные API с максимальными лимитами
        self.apis = {
            'serpapi': {
                'url': 'https://serpapi.com/search',
                'key': os.getenv('SERPAPI_KEY', ''),
                'limit': 100,  # 100/месяц бесплатно
                'enabled': bool(os.getenv('SERPAPI_KEY'))
            },
            'jina_reader': {
                'url': 'https://r.jina.ai/',
                'limit': 1000,  # 1000/день бесплатно
                'enabled': True  # Не требует API ключа!
            },
            'brave_search': {
                'url': 'https://api.search.brave.com/res/v1/web/search',
                'key': os.getenv('BRAVE_API_KEY', ''),
                'limit': 2000,  # 2000/месяц бесплатно
                'enabled': bool(os.getenv('BRAVE_API_KEY'))
            },
            'webscraping_ai': {
                'url': 'https://api.webscraping.ai/html',
                'key': os.getenv('WEBSCRAPING_AI_KEY', ''),
                'limit': 1000,  # 1000/месяц бесплатно
                'enabled': bool(os.getenv('WEBSCRAPING_AI_KEY'))
            }
        }

        self.usage_stats = {
            'serpapi': 0,
            'jina_reader': 0,
            'brave_search': 0,
            'webscraping_ai': 0
        }

        print("🔍 WebResearchEngine инициализирован:")
        for api, config in self.apis.items():
            status = "✅" if config['enabled'] else "❌"
            print(f"   {api}: {status} (лимит: {config['limit']})")

    async def research_billionaire_interviews(self, query: str, count: int = 20) -> ResearchResult:
        """🎯 Исследует интервью миллиардеров"""

        # Расширяем запрос для поиска интервью
        enhanced_queries = [
            f"{query} interview billionaire rich successful entrepreneur",
            f"{query} интервью миллиардер богатый бизнесмен",
            f"{query} podcast CEO founder startup unicorn",
            f"{query} TED talk business leader motivation"
        ]

        all_sources = []

        for enhanced_query in enhanced_queries:
            print(f"🔍 Ищу: {enhanced_query}")

            # Поиск через доступные API
            sources = await self._multi_search(enhanced_query, count // len(enhanced_queries))
            all_sources.extend(sources)

            # Пауза между запросами
            await asyncio.sleep(1)

        # Удаляем дублирующие источники
        unique_sources = self._deduplicate_sources(all_sources)

        # Анализируем найденные материалы через Groq
        analysis = await self._analyze_interview_content(unique_sources[:count], query)

        return ResearchResult(
            query=query,
            sources=unique_sources[:count],
            analysis=analysis,
            confidence=min(len(unique_sources) / count, 1.0),
            timestamp=datetime.now(),
            total_sources=len(unique_sources)
        )

    async def _multi_search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """🔄 Поиск через несколько API параллельно"""

        search_tasks = []

        # SerpAPI (Google)
        if self.apis['serpapi']['enabled'] and self.usage_stats['serpapi'] < self.apis['serpapi']['limit']:
            search_tasks.append(self._search_serpapi(query, limit))

        # Brave Search
        if self.apis['brave_search']['enabled'] and self.usage_stats['brave_search'] < self.apis['brave_search']['limit']:
            search_tasks.append(self._search_brave(query, limit))

        # Выполняем поиски параллельно
        if search_tasks:
            results = await asyncio.gather(*search_tasks, return_exceptions=True)

            all_results = []
            for result in results:
                if isinstance(result, list):
                    all_results.extend(result)

            return all_results

        return []

    async def _search_serpapi(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """🌐 Поиск через SerpAPI (Google)"""
        try:
            params = {
                'q': query,
                'api_key': self.apis['serpapi']['key'],
                'engine': 'google',
                'num': min(limit, 10),
                'gl': 'us',
                'hl': 'en'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.apis['serpapi']['url'], params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.usage_stats['serpapi'] += 1

                        results = []
                        for item in data.get('organic_results', []):
                            results.append({
                                'title': item.get('title', ''),
                                'url': item.get('link', ''),
                                'snippet': item.get('snippet', ''),
                                'source': 'google',
                                'date': item.get('date', ''),
                                'type': 'web'
                            })

                        return results

        except Exception as e:
            print(f"⚠️ Ошибка SerpAPI: {e}")

        return []

    async def _search_brave(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """🦁 Поиск через Brave Search"""
        try:
            headers = {
                'X-Subscription-Token': self.apis['brave_search']['key']
            }

            params = {
                'q': query,
                'count': min(limit, 20),
                'offset': 0,
                'country': 'us'
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.apis['brave_search']['url'],
                                     params=params, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.usage_stats['brave_search'] += 1

                        results = []
                        for item in data.get('web', {}).get('results', []):
                            results.append({
                                'title': item.get('title', ''),
                                'url': item.get('url', ''),
                                'snippet': item.get('description', ''),
                                'source': 'brave',
                                'date': item.get('published', ''),
                                'type': 'web'
                            })

                        return results

        except Exception as e:
            print(f"⚠️ Ошибка Brave Search: {e}")

        return []

    async def extract_content_from_url(self, url: str) -> str:
        """📄 Извлекает контент из URL через Jina Reader (БЕСПЛАТНО!)"""
        try:
            if self.usage_stats['jina_reader'] >= self.apis['jina_reader']['limit']:
                return "Превышен лимит Jina Reader"

            # Jina Reader - БЕСПЛАТНЫЙ сервис конвертации URL в текст
            reader_url = f"{self.apis['jina_reader']['url']}{url}"

            async with aiohttp.ClientSession() as session:
                async with session.get(reader_url, timeout=30) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.usage_stats['jina_reader'] += 1
                        return content[:5000]  # Ограничиваем размер

        except Exception as e:
            print(f"⚠️ Ошибка извлечения контента: {e}")

        return ""

    def get_youtube_transcript(self, youtube_url: str) -> str:
        """📺 БЕСПЛАТНОЕ получение субтитров YouTube"""
        try:
            from youtube_transcript_api import YouTubeTranscriptApi

            # Извлекаем video_id из URL
            video_id = self._extract_youtube_id(youtube_url)
            if not video_id:
                return ""

            # Получаем субтитры (БЕСПЛАТНО, без лимитов!)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ru'])

            # Объединяем в текст
            full_text = ' '.join([entry['text'] for entry in transcript])
            return full_text[:10000]  # Ограничиваем размер

        except Exception as e:
            print(f"⚠️ Ошибка получения субтитров: {e}")
            return ""

    def _extract_youtube_id(self, url: str) -> Optional[str]:
        """🎬 Извлекает ID видео из YouTube URL"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch.*[&?]v=([a-zA-Z0-9_-]{11})'
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        return None

    async def _analyze_interview_content(self, sources: List[Dict], query: str) -> str:
        """🧠 Анализирует контент интервью через Groq"""

        # Собираем контент из источников
        content_snippets = []
        for source in sources[:10]:  # Анализируем до 10 источников
            snippet = source.get('snippet', '')
            if 'youtube.com' in source.get('url', ''):
                # Для YouTube получаем субтитры
                transcript = self.get_youtube_transcript(source['url'])
                if transcript:
                    snippet = transcript[:1000]

            content_snippets.append({
                'title': source.get('title', ''),
                'content': snippet,
                'url': source.get('url', '')
            })

        # Используем Groq для анализа
        from smart_ai_generator import SmartAIGenerator
        ai_generator = SmartAIGenerator()

        analysis_prompt = f"""
Проанализируй эти интервью и материалы успешных людей по теме: {query}

ИСТОЧНИКИ:
{json.dumps(content_snippets, ensure_ascii=False, indent=2)}

Создай подробный анализ:
1. Ключевые принципы и стратегии
2. Общие паттерны успеха
3. Практические советы
4. Цитаты и инсайты
5. Применимые уроки

Формат ответа: подробный анализ на русском языке.
        """

        try:
            analysis = ai_generator._call_groq_api(analysis_prompt, 'llama-3.1-8b-instant')
            return analysis
        except Exception as e:
            return f"Найдено {len(sources)} релевантных источников по теме '{query}'. Анализ временно недоступен: {e}"

    def _deduplicate_sources(self, sources: List[Dict]) -> List[Dict]:
        """🔄 Удаляет дублирующие источники"""
        seen_urls = set()
        unique_sources = []

        for source in sources:
            url = source.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_sources.append(source)

        return unique_sources

    def get_usage_stats(self) -> Dict[str, Any]:
        """📊 Статистика использования API"""
        return {
            'usage': self.usage_stats,
            'limits': {api: config['limit'] for api, config in self.apis.items()},
            'remaining': {
                api: max(0, config['limit'] - self.usage_stats[api])
                for api, config in self.apis.items()
            }
        }

# Функция для тестирования
async def test_research_engine():
    """🧪 Тестирует движок исследований"""
    engine = WebResearchEngine()

    print("🚀 Тестируем поиск интервью миллиардеров...")

    result = await engine.research_billionaire_interviews(
        "бизнес стратегии успешных предпринимателей",
        count=10
    )

    print(f"✅ Найдено источников: {result.total_sources}")
    print(f"🎯 Уверенность: {result.confidence:.2%}")
    print(f"📝 Анализ: {result.analysis[:200]}...")

    # Статистика использования
    stats = engine.get_usage_stats()
    print(f"📊 Использовано API: {stats['usage']}")

if __name__ == "__main__":
    asyncio.run(test_research_engine())