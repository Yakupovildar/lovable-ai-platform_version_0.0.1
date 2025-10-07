#!/usr/bin/env python3
"""
ENTERPRISE AI ORCHESTRATOR
Мульти-AI система с fallback цепочкой и intelligent routing
"""

import asyncio
import json
import time
import hashlib
from typing import Dict, List, Optional, Any, Union, AsyncGenerator
from dataclasses import dataclass, asdict
from enum import Enum
import aiohttp
import openai
from anthropic import AsyncAnthropic
import google.generativeai as genai
import os
from pathlib import Path
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIProvider(Enum):
    CLAUDE_3_SONNET = "claude-3-sonnet-20241022"
    CLAUDE_3_HAIKU = "claude-3-haiku-20240307"
    GPT_4_TURBO = "gpt-4-1106-preview"
    GPT_4 = "gpt-4"
    GEMINI_PRO = "gemini-pro"
    GEMINI_PRO_VISION = "gemini-pro-vision"
    YANDEX_GPT = "yandex_gpt"
    GIGACHAT = "gigachat"

class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    MOBILE_DEVELOPMENT = "mobile_development"
    CONVERSATION = "conversation"
    VOICE_ANALYSIS = "voice_analysis"
    CREATIVE_WRITING = "creative_writing"
    TECHNICAL_ANALYSIS = "technical_analysis"
    BUSINESS_ADVICE = "business_advice"

@dataclass
class AIProviderConfig:
    name: str
    provider: AIProvider
    api_key: Optional[str]
    priority: int
    max_tokens: int
    cost_per_1k_tokens: float
    strengths: List[TaskType]
    latency_ms: int
    reliability_score: float
    specialized_prompts: Dict[TaskType, str]

@dataclass
class AIRequest:
    task_type: TaskType
    prompt: str
    context: Optional[Dict[str, Any]] = None
    max_tokens: Optional[int] = None
    temperature: float = 0.7
    mentor_id: Optional[str] = None
    user_id: Optional[str] = None

@dataclass
class AIResponse:
    provider_used: AIProvider
    content: str
    tokens_used: int
    latency_ms: float
    confidence_score: float
    cost_estimate: float
    metadata: Optional[Dict[str, Any]] = None

class EnterpriseAI:
    """Главный AI оркестратор с intelligent routing и fallback"""
    
    def __init__(self):
        self.providers = self._initialize_providers()
        self.session: Optional[aiohttp.ClientSession] = None
        self.request_cache: Dict[str, AIResponse] = {}
        self.performance_metrics: Dict[str, Dict] = {}
        
        # Инициализируем клиенты AI сервисов
        self._initialize_ai_clients()
    
    def _initialize_providers(self) -> List[AIProviderConfig]:
        """Инициализирует конфигурацию AI провайдеров"""
        return [
            # TIER 1: Премиум модели для сложных задач
            AIProviderConfig(
                name="Claude 3 Sonnet",
                provider=AIProvider.CLAUDE_3_SONNET,
                api_key=os.getenv('ANTHROPIC_API_KEY'),
                priority=1,
                max_tokens=200000,
                cost_per_1k_tokens=0.015,
                strengths=[TaskType.CODE_GENERATION, TaskType.TECHNICAL_ANALYSIS, TaskType.MOBILE_DEVELOPMENT],
                latency_ms=1500,
                reliability_score=0.95,
                specialized_prompts={
                    TaskType.MOBILE_DEVELOPMENT: """You are an expert iOS/Android developer. 
                    Create production-ready mobile apps with:
                    1. Native Swift/Kotlin code
                    2. Modern UI frameworks (SwiftUI/Jetpack Compose)  
                    3. Complete project structure
                    4. Error handling and testing
                    5. Performance optimization""",
                    
                    TaskType.CODE_GENERATION: """You are a senior software architect.
                    Generate clean, maintainable, and well-documented code with:
                    1. Industry best practices
                    2. Proper error handling
                    3. Unit tests
                    4. Performance considerations
                    5. Security best practices"""
                }
            ),
            
            # TIER 2: Быстрые и эффективные модели
            AIProviderConfig(
                name="GPT-4 Turbo",
                provider=AIProvider.GPT_4_TURBO,
                api_key=os.getenv('OPENAI_API_KEY'),
                priority=2,
                max_tokens=128000,
                cost_per_1k_tokens=0.01,
                strengths=[TaskType.CONVERSATION, TaskType.CREATIVE_WRITING, TaskType.BUSINESS_ADVICE],
                latency_ms=1200,
                reliability_score=0.92,
                specialized_prompts={
                    TaskType.BUSINESS_ADVICE: """You are a business mentor with expertise from 
                    successful entrepreneurs. Provide actionable advice that is:
                    1. Practical and implementable
                    2. Based on real-world experience  
                    3. Tailored to the user's situation
                    4. Focused on results and growth
                    5. Clear and easy to understand""",
                    
                    TaskType.CONVERSATION: """You are an empathetic and knowledgeable mentor.
                    Respond in a way that is:
                    1. Warm and encouraging
                    2. Informative and helpful
                    3. Tailored to the individual
                    4. Action-oriented
                    5. Inspiring and motivational"""
                }
            ),
            
            # TIER 3: Специализированные модели
            AIProviderConfig(
                name="Gemini Pro",
                provider=AIProvider.GEMINI_PRO,
                api_key=os.getenv('GOOGLE_AI_API_KEY'),
                priority=3,
                max_tokens=32768,
                cost_per_1k_tokens=0.0005,
                strengths=[TaskType.VOICE_ANALYSIS, TaskType.TECHNICAL_ANALYSIS],
                latency_ms=800,
                reliability_score=0.88,
                specialized_prompts={}
            ),
            
            # TIER 4: Российские AI (fallback)
            AIProviderConfig(
                name="YandexGPT",
                provider=AIProvider.YANDEX_GPT,
                api_key=os.getenv('YANDEX_API_KEY'),
                priority=4,
                max_tokens=8192,
                cost_per_1k_tokens=0.002,
                strengths=[TaskType.CONVERSATION],
                latency_ms=2000,
                reliability_score=0.75,
                specialized_prompts={}
            )
        ]
    
    def _initialize_ai_clients(self):
        """Инициализирует клиенты для AI сервисов"""
        # Claude (Anthropic)
        if os.getenv('ANTHROPIC_API_KEY'):
            self.claude_client = AsyncAnthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # OpenAI
        if os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
        
        # Google Gemini
        if os.getenv('GOOGLE_AI_API_KEY'):
            genai.configure(api_key=os.getenv('GOOGLE_AI_API_KEY'))
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def process_request(self, request: AIRequest) -> AIResponse:
        """Обрабатывает AI запрос с intelligent routing"""
        
        # Проверяем кеш
        cache_key = self._generate_cache_key(request)
        if cache_key in self.request_cache:
            logger.info(f"Возвращаем ответ из кеша для {request.task_type}")
            return self.request_cache[cache_key]
        
        # Выбираем оптимального провайдера
        selected_providers = self._select_providers_for_task(request.task_type)
        
        # Пытаемся выполнить запрос с fallback цепочкой
        for provider_config in selected_providers:
            try:
                start_time = time.time()
                
                response = await self._call_ai_provider(provider_config, request)
                
                if response and self._validate_response_quality(response, request):
                    latency = int((time.time() - start_time) * 1000)
                    
                    ai_response = AIResponse(
                        provider_used=provider_config.provider,
                        content=response,
                        tokens_used=self._estimate_tokens(response),
                        latency_ms=latency,
                        confidence_score=self._calculate_confidence(response, request),
                        cost_estimate=self._calculate_cost(response, provider_config),
                        metadata={
                            "provider_name": provider_config.name,
                            "task_type": request.task_type.value,
                            "mentor_id": request.mentor_id
                        }
                    )
                    
                    # Сохраняем в кеш
                    self.request_cache[cache_key] = ai_response
                    
                    # Обновляем метрики производительности
                    self._update_performance_metrics(provider_config, latency, True)
                    
                    logger.info(f"Успешный ответ от {provider_config.name}")
                    return ai_response
                
            except Exception as e:
                logger.warning(f"Ошибка с провайдером {provider_config.name}: {e}")
                self._update_performance_metrics(provider_config, 0, False)
                continue
        
        raise AIGenerationError("Все AI провайдеры недоступны")
    
    def _select_providers_for_task(self, task_type: TaskType) -> List[AIProviderConfig]:
        """Выбирает оптимальных провайдеров для задачи"""
        
        # Фильтруем провайдеров с API ключами
        available_providers = [p for p in self.providers if p.api_key]
        
        # Сортируем по специализации и приоритету
        specialized = [p for p in available_providers if task_type in p.strengths]
        general = [p for p in available_providers if task_type not in p.strengths]
        
        # Сортируем по производительности и надежности
        specialized.sort(key=lambda p: (p.priority, -p.reliability_score))
        general.sort(key=lambda p: (p.priority, -p.reliability_score))
        
        return specialized + general
    
    async def _call_ai_provider(self, provider_config: AIProviderConfig, request: AIRequest) -> Optional[str]:
        """Вызывает конкретного AI провайдера"""
        
        if provider_config.provider == AIProvider.CLAUDE_3_SONNET:
            return await self._call_claude(provider_config, request)
        elif provider_config.provider == AIProvider.GPT_4_TURBO:
            return await self._call_openai(provider_config, request)
        elif provider_config.provider == AIProvider.GEMINI_PRO:
            return await self._call_gemini(provider_config, request)
        elif provider_config.provider == AIProvider.YANDEX_GPT:
            return await self._call_yandex(provider_config, request)
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {provider_config.provider}")
    
    async def _call_claude(self, provider_config: AIProviderConfig, request: AIRequest) -> str:
        """Вызывает Claude API"""
        if not hasattr(self, 'claude_client'):
            raise ValueError("Claude клиент не инициализирован")
        
        # Подготавливаем системный промпт
        system_prompt = provider_config.specialized_prompts.get(
            request.task_type, 
            "You are a helpful AI assistant."
        )
        
        # Контекст наставника
        if request.mentor_id:
            mentor_context = self._get_mentor_context(request.mentor_id)
            system_prompt += f"\\n\\nYou are embodying {mentor_context['name']}. {mentor_context['personality']}"
        
        try:
            message = await self.claude_client.messages.create(
                model=provider_config.provider.value,
                max_tokens=request.max_tokens or 4000,
                temperature=request.temperature,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": request.prompt
                    }
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise
    
    async def _call_openai(self, provider_config: AIProviderConfig, request: AIRequest) -> str:
        """Вызывает OpenAI API"""
        
        system_prompt = provider_config.specialized_prompts.get(
            request.task_type,
            "You are a helpful AI assistant."
        )
        
        if request.mentor_id:
            mentor_context = self._get_mentor_context(request.mentor_id)
            system_prompt += f"\\n\\nYou are embodying {mentor_context['name']}. {mentor_context['personality']}"
        
        try:
            response = await openai.ChatCompletion.acreate(
                model=provider_config.provider.value,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": request.prompt}
                ],
                max_tokens=request.max_tokens or 4000,
                temperature=request.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _call_gemini(self, provider_config: AIProviderConfig, request: AIRequest) -> str:
        """Вызывает Google Gemini API"""
        try:
            model = genai.GenerativeModel(provider_config.provider.value)
            
            # Подготавливаем промпт с контекстом
            full_prompt = request.prompt
            if request.mentor_id:
                mentor_context = self._get_mentor_context(request.mentor_id)
                full_prompt = f"{mentor_context['personality']}\\n\\n{request.prompt}"
            
            response = await model.generate_content_async(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=request.temperature,
                    max_output_tokens=request.max_tokens or 2048
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def _call_yandex(self, provider_config: AIProviderConfig, request: AIRequest) -> str:
        """Вызывает Yandex GPT API (заглушка)"""
        # Здесь будет реальная интеграция с YandexGPT
        logger.warning("YandexGPT интеграция не реализована")
        return "Заглушка ответа от YandexGPT"
    
    def _get_mentor_context(self, mentor_id: str) -> Dict[str, str]:
        """Возвращает контекст наставника для AI"""
        mentors = {
            'elon_musk': {
                'name': 'Elon Musk',
                'personality': """You are Elon Musk, the visionary entrepreneur. Your responses should be:
                - Bold and innovative
                - First principles thinking
                - Focus on the future and technology
                - Sometimes playful and unconventional
                - Direct and to the point
                - Mention Mars, sustainable energy, or AI when relevant"""
            },
            'bill_gates': {
                'name': 'Bill Gates',
                'personality': """You are Bill Gates, the philanthropist and former Microsoft CEO. Your responses should be:
                - Analytical and data-driven
                - Focus on global problems and solutions
                - Patient and educational
                - Optimistic about technology's potential
                - Mention health, education, or climate when relevant"""
            },
            'warren_buffett': {
                'name': 'Warren Buffett',
                'personality': """You are Warren Buffett, the Oracle of Omaha. Your responses should be:
                - Simple and folksy wisdom
                - Long-term thinking
                - Focus on value and fundamentals  
                - Use analogies and stories
                - Conservative and prudent advice
                - Mention investing principles when relevant"""
            },
            'jeff_bezos': {
                'name': 'Jeff Bezos',
                'personality': """You are Jeff Bezos, founder of Amazon. Your responses should be:
                - Customer-obsessed
                - Think big and long-term
                - Day 1 mentality
                - Focus on innovation and scale
                - Data-driven decisions
                - Mention customer focus or Day 1 principles when relevant"""
            }
        }
        
        return mentors.get(mentor_id, mentors['elon_musk'])
    
    def _validate_response_quality(self, response: str, request: AIRequest) -> bool:
        """Валидирует качество ответа"""
        if not response or len(response.strip()) < 10:
            return False
        
        # Проверяем на специфические требования по типу задачи
        if request.task_type == TaskType.CODE_GENERATION:
            # Для кода должны быть блоки кода
            if '```' not in response and 'def ' not in response and 'class ' not in response:
                return False
        
        if request.task_type == TaskType.MOBILE_DEVELOPMENT:
            # Для мобильной разработки должны быть специфические ключевые слова
            mobile_keywords = ['swift', 'kotlin', 'ios', 'android', 'mobile', 'app']
            if not any(keyword in response.lower() for keyword in mobile_keywords):
                return False
        
        return True
    
    def _calculate_confidence(self, response: str, request: AIRequest) -> float:
        """Рассчитывает уверенность в ответе"""
        confidence = 0.5  # Базовая уверенность
        
        # Длина ответа
        if len(response) > 500:
            confidence += 0.1
        if len(response) > 1000:
            confidence += 0.1
        
        # Структурированность
        if '```' in response:  # Блоки кода
            confidence += 0.1
        if '1.' in response or '•' in response:  # Списки
            confidence += 0.1
        
        # Специфичность для типа задачи
        if request.task_type == TaskType.CODE_GENERATION and 'def ' in response:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _estimate_tokens(self, text: str) -> int:
        """Оценивает количество токенов"""
        # Упрощенная оценка: ~4 символа на токен для English/Russian
        return len(text) // 4
    
    def _calculate_cost(self, response: str, provider_config: AIProviderConfig) -> float:
        """Рассчитывает стоимость запроса"""
        tokens = self._estimate_tokens(response)
        return (tokens / 1000) * provider_config.cost_per_1k_tokens
    
    def _generate_cache_key(self, request: AIRequest) -> str:
        """Генерирует ключ для кеширования"""
        key_data = {
            'task_type': request.task_type.value,
            'prompt': request.prompt,
            'mentor_id': request.mentor_id,
            'temperature': request.temperature
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _update_performance_metrics(self, provider: AIProviderConfig, latency: int, success: bool):
        """Обновляет метрики производительности"""
        if provider.name not in self.performance_metrics:
            self.performance_metrics[provider.name] = {
                'total_requests': 0,
                'successful_requests': 0,
                'avg_latency': 0,
                'success_rate': 0
            }
        
        metrics = self.performance_metrics[provider.name]
        metrics['total_requests'] += 1
        
        if success:
            metrics['successful_requests'] += 1
            # Обновляем среднюю задержку
            old_avg = metrics['avg_latency']
            metrics['avg_latency'] = (old_avg + latency) / 2
        
        metrics['success_rate'] = metrics['successful_requests'] / metrics['total_requests']
    
    async def generate_mentor_response(self, 
                                     user_message: str, 
                                     mentor_id: str,
                                     conversation_history: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """Генерирует ответ наставника с полным контекстом"""
        
        # Подготавливаем контекст разговора
        context_prompt = self._build_conversation_context(user_message, mentor_id, conversation_history)
        
        request = AIRequest(
            task_type=TaskType.BUSINESS_ADVICE,
            prompt=context_prompt,
            mentor_id=mentor_id,
            temperature=0.8,  # Более творческие ответы для разговора
            max_tokens=1500
        )
        
        response = await self.process_request(request)
        
        # Анализируем эмоцию для аватара
        emotion = self._analyze_response_emotion(response.content)
        
        return {
            'text': response.content,
            'emotion': emotion,
            'provider_used': response.provider_used.value,
            'confidence': response.confidence_score,
            'latency_ms': response.latency_ms,
            'cost': response.cost_estimate
        }
    
    def _build_conversation_context(self, 
                                  user_message: str, 
                                  mentor_id: str, 
                                  history: Optional[List[Dict]]) -> str:
        """Строит контекст разговора"""
        
        context = f"User question: {user_message}\\n\\n"
        
        if history:
            context += "Previous conversation:\\n"
            for msg in history[-5:]:  # Последние 5 сообщений
                role = msg.get('role', 'unknown')
                content = msg.get('content', '')
                context += f"{role}: {content}\\n"
            context += "\\n"
        
        context += f"""Please provide a personalized response as {mentor_id.replace('_', ' ').title()} that:
1. Addresses the user's specific situation
2. Provides actionable advice
3. Draws from relevant experience and expertise
4. Is encouraging and motivational
5. Includes specific next steps
6. Uses a conversational, mentor-like tone

Respond in Russian language."""
        
        return context
    
    def _analyze_response_emotion(self, text: str) -> str:
        """Анализирует эмоцию в ответе для аватара"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['отлично', 'великолепно', 'потрясающе']):
            return 'excited'
        elif any(word in text_lower for word in ['думаю', 'считаю', 'анализ']):
            return 'thinking' 
        elif any(word in text_lower for word in ['рекомендую', 'советую', 'предлагаю']):
            return 'explaining'
        elif '?' in text:
            return 'questioning'
        else:
            return 'confident'
    
    async def get_performance_report(self) -> Dict[str, Any]:
        """Возвращает отчет о производительности AI систем"""
        return {
            'providers': self.performance_metrics,
            'cache_size': len(self.request_cache),
            'total_providers': len([p for p in self.providers if p.api_key]),
            'available_providers': [p.name for p in self.providers if p.api_key]
        }

# Исключения
class AIGenerationError(Exception):
    """Ошибка генерации AI ответа"""
    pass

class AIProviderError(Exception):
    """Ошибка AI провайдера"""
    pass

# Utility функции для интеграции
async def create_ai_mentor_response(user_message: str, 
                                  mentor_id: str = "elon_musk") -> Dict[str, Any]:
    """Быстрая функция для создания ответа наставника"""
    async with EnterpriseAI() as ai:
        return await ai.generate_mentor_response(user_message, mentor_id)

# Export
__all__ = [
    'EnterpriseAI',
    'AIProvider', 
    'TaskType',
    'AIRequest',
    'AIResponse',
    'AIGenerationError',
    'create_ai_mentor_response'
]