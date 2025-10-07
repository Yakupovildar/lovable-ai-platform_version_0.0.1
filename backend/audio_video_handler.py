#!/usr/bin/env python3
"""
AUDIO & VIDEO INTEGRATION MODULE
Продвинутая система интеграции голоса и видео для AI наставника
"""

import asyncio
import json
import base64
import tempfile
import os
from typing import Dict, List, Optional, Any, AsyncGenerator
from dataclasses import dataclass
from enum import Enum
import aiohttp
import aiofiles
from pathlib import Path

class VoiceProvider(Enum):
    OPENAI_WHISPER = "openai_whisper"
    ELEVENLABS = "elevenlabs"
    AZURE_SPEECH = "azure_speech"
    GOOGLE_CLOUD = "google_cloud"
    YANDEX_SPEECHKIT = "yandex_speechkit"

class TTSProvider(Enum):
    ELEVENLABS = "elevenlabs"
    OPENAI_TTS = "openai_tts"
    AZURE_TTS = "azure_tts" 
    YANDEX_TTS = "yandex_tts"
    COQUI_TTS = "coqui_tts"

@dataclass
class VoiceProfile:
    """Профиль голоса наставника"""
    mentor_id: str
    voice_id: str
    provider: TTSProvider
    language: str
    pitch: float
    speed: float
    volume: float
    emotion_range: Dict[str, Any]

@dataclass
class AudioProcessingResult:
    """Результат обработки аудио"""
    text: str
    confidence: float
    language: str
    duration: float
    emotion: Optional[str] = None
    sentiment: Optional[str] = None

class AudioVideoIntegration:
    """Главный класс интеграции голоса и видео"""
    
    def __init__(self):
        self.voice_profiles = self._initialize_mentor_voices()
        self.session: Optional[aiohttp.ClientSession] = None
        self.temp_dir = tempfile.mkdtemp(prefix="ai_mentor_audio_")
        
        # API ключи (должны быть в .env)
        self.apis = {
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY'),
            'openai': os.getenv('OPENAI_API_KEY'), 
            'azure_speech': os.getenv('AZURE_SPEECH_KEY'),
            'yandex_speech': os.getenv('YANDEX_SPEECH_KEY'),
            'google_cloud': os.getenv('GOOGLE_CLOUD_API_KEY')
        }
    
    def _initialize_mentor_voices(self) -> Dict[str, VoiceProfile]:
        """Инициализирует голосовые профили наставников"""
        return {
            'elon_musk': VoiceProfile(
                mentor_id='elon_musk',
                voice_id='pNInz6obpgDQGcFmaJgB',  # Реальный ID от ElevenLabs
                provider=TTSProvider.ELEVENLABS,
                language='ru-RU',
                pitch=1.1,
                speed=1.15,  # Быстрая речь как у Маска
                volume=0.9,
                emotion_range={
                    'excitement': 0.8,
                    'confidence': 0.9,
                    'innovation': 0.95
                }
            ),
            'bill_gates': VoiceProfile(
                mentor_id='bill_gates',
                voice_id='EXAVITQu4vr4xnSDxMaL',
                provider=TTSProvider.ELEVENLABS, 
                language='ru-RU',
                pitch=0.95,
                speed=0.9,  # Медленная, обдуманная речь
                volume=0.85,
                emotion_range={
                    'wisdom': 0.9,
                    'patience': 0.85,
                    'analytical': 0.9
                }
            ),
            'jeff_bezos': VoiceProfile(
                mentor_id='jeff_bezos',
                voice_id='VR6AewLTigWG4xSOukaG',
                provider=TTSProvider.ELEVENLABS,
                language='ru-RU', 
                pitch=0.9,
                speed=1.0,
                volume=0.9,
                emotion_range={
                    'leadership': 0.9,
                    'determination': 0.85,
                    'customer_focus': 0.8
                }
            ),
            'warren_buffett': VoiceProfile(
                mentor_id='warren_buffett',
                voice_id='ZQe5CZNOzWyzPSCn5a3c',
                provider=TTSProvider.ELEVENLABS,
                language='ru-RU',
                pitch=0.85,
                speed=0.8,  # Очень медленная, мудрая речь
                volume=0.8,
                emotion_range={
                    'wisdom': 0.95,
                    'patience': 0.9,
                    'value_investing': 0.85
                }
            )
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
        
        # Очищаем временные файлы
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    async def speech_to_text(self, 
                           audio_data: bytes, 
                           provider: VoiceProvider = VoiceProvider.OPENAI_WHISPER,
                           language: str = "ru") -> AudioProcessingResult:
        """Преобразует речь в текст с продвинутой обработкой"""
        
        if provider == VoiceProvider.OPENAI_WHISPER:
            return await self._whisper_transcribe(audio_data, language)
        elif provider == VoiceProvider.ELEVENLABS:
            return await self._elevenlabs_transcribe(audio_data, language)
        elif provider == VoiceProvider.YANDEX_SPEECHKIT:
            return await self._yandex_transcribe(audio_data, language)
        else:
            raise ValueError(f"Неподдерживаемый провайдер: {provider}")
    
    async def _whisper_transcribe(self, audio_data: bytes, language: str) -> AudioProcessingResult:
        """Транскрибация через OpenAI Whisper"""
        if not self.apis['openai']:
            raise ValueError("OpenAI API ключ не установлен")
        
        # Сохраняем аудио во временный файл
        temp_audio = os.path.join(self.temp_dir, f"audio_{asyncio.get_event_loop().time()}.wav")
        async with aiofiles.open(temp_audio, 'wb') as f:
            await f.write(audio_data)
        
        headers = {
            'Authorization': f'Bearer {self.apis["openai"]}'
        }
        
        data = aiohttp.FormData()
        data.add_field('file', open(temp_audio, 'rb'), filename='audio.wav')
        data.add_field('model', 'whisper-1')
        data.add_field('language', language)
        data.add_field('response_format', 'verbose_json')
        
        async with self.session.post(
            'https://api.openai.com/v1/audio/transcriptions',
            headers=headers,
            data=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                
                # Анализируем эмоции в тексте
                emotion = await self._analyze_emotion(result['text'])
                
                return AudioProcessingResult(
                    text=result['text'],
                    confidence=result.get('confidence', 0.9),
                    language=result.get('language', language),
                    duration=result.get('duration', 0.0),
                    emotion=emotion,
                    sentiment=await self._analyze_sentiment(result['text'])
                )
            else:
                error_text = await response.text()
                raise Exception(f"Whisper API error: {error_text}")
    
    async def text_to_speech(self, 
                           text: str, 
                           mentor_id: str = "elon_musk",
                           emotion: str = "neutral",
                           custom_settings: Optional[Dict] = None) -> bytes:
        """Преобразует текст в речь с голосом наставника"""
        
        voice_profile = self.voice_profiles.get(mentor_id)
        if not voice_profile:
            raise ValueError(f"Голосовой профиль для {mentor_id} не найден")
        
        # Подготавливаем текст с эмоциональными модификациями
        enhanced_text = await self._enhance_text_with_emotion(text, emotion, mentor_id)
        
        if voice_profile.provider == TTSProvider.ELEVENLABS:
            return await self._elevenlabs_tts(enhanced_text, voice_profile, emotion, custom_settings)
        elif voice_profile.provider == TTSProvider.OPENAI_TTS:
            return await self._openai_tts(enhanced_text, voice_profile, emotion)
        else:
            raise ValueError(f"Неподдерживаемый TTS провайдер: {voice_profile.provider}")
    
    async def _elevenlabs_tts(self, 
                            text: str, 
                            voice_profile: VoiceProfile,
                            emotion: str,
                            custom_settings: Optional[Dict] = None) -> bytes:
        """Генерация речи через ElevenLabs с эмоциями"""
        if not self.apis['elevenlabs']:
            raise ValueError("ElevenLabs API ключ не установлен")
        
        # Настраиваем параметры голоса с эмоциями
        voice_settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True
        }
        
        # Модифицируем настройки в зависимости от эмоции
        emotion_modifiers = {
            "excited": {"stability": 0.3, "style": 0.8},
            "calm": {"stability": 0.8, "style": 0.2},
            "confident": {"stability": 0.6, "similarity_boost": 0.9},
            "thoughtful": {"stability": 0.7, "style": 0.1}
        }
        
        if emotion in emotion_modifiers:
            voice_settings.update(emotion_modifiers[emotion])
        
        if custom_settings:
            voice_settings.update(custom_settings)
        
        headers = {
            'Accept': 'audio/mpeg',
            'Content-Type': 'application/json',
            'xi-api-key': self.apis['elevenlabs']
        }
        
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": voice_settings
        }
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_profile.voice_id}"
        
        async with self.session.post(url, headers=headers, json=data) as response:
            if response.status == 200:
                return await response.read()
            else:
                error_text = await response.text()
                raise Exception(f"ElevenLabs API error: {error_text}")
    
    async def _enhance_text_with_emotion(self, text: str, emotion: str, mentor_id: str) -> str:
        """Улучшает текст эмоциональными модификациями для каждого наставника"""
        
        mentor_speech_patterns = {
            'elon_musk': {
                'prefixes': ["Знаете,", "Слушайте,", "Вот что важно:"],
                'emphasis': ["абсолютно", "определенно", "невероятно"],
                'innovation_words': ["будущее", "инновации", "революция", "прорыв"]
            },
            'bill_gates': {
                'prefixes': ["Позвольте объяснить:", "Важно понимать:", "По моему опыту:"],
                'emphasis': ["безусловно", "несомненно", "крайне важно"],
                'analytical_words': ["данные", "исследования", "анализ", "эффективность"]
            },
            'warren_buffett': {
                'prefixes': ["Мой совет такой:", "За годы я понял:", "Простая истина:"],
                'emphasis': ["мудро", "разумно", "долгосрочно"],
                'value_words': ["стоимость", "инвестиции", "терпение", "дисциплина"]
            },
            'jeff_bezos': {
                'prefixes': ["Клиент прежде всего:", "День первый:", "Думайте масштабно:"],
                'emphasis': ["обязательно", "принципиально", "стратегически"],
                'leadership_words': ["лидерство", "инновации", "клиенты", "результат"]
            }
        }
        
        patterns = mentor_speech_patterns.get(mentor_id, mentor_speech_patterns['elon_musk'])
        
        # Добавляем характерные речевые обороты
        enhanced_text = text
        
        if emotion == "confident":
            import random
            prefix = random.choice(patterns['prefixes'])
            enhanced_text = f"{prefix} {enhanced_text}"
        
        # Добавляем эмоциональные акценты
        for emphasis in patterns['emphasis']:
            if emphasis.lower() in enhanced_text.lower():
                enhanced_text = enhanced_text.replace(
                    emphasis.lower(), 
                    f"*{emphasis}*"  # Markdown для эмфазы
                )
        
        return enhanced_text
    
    async def create_3d_avatar_animation(self,
                                       text: str,
                                       emotion: str,
                                       mentor_id: str) -> Dict[str, Any]:
        """Создает данные анимации для 3D аватара"""
        
        # Анализируем текст для определения ключевых моментов анимации
        animation_cues = await self._analyze_text_for_animation(text)
        
        # Определяем базовые эмоции для аватара
        base_emotions = {
            "happy": {"mouth_curve": 0.8, "eye_brightness": 0.9, "eyebrow_raise": 0.3},
            "thinking": {"eye_focus": 0.7, "head_tilt": 0.2, "eyebrow_furrow": 0.5},
            "explaining": {"hand_gesture": 0.8, "eye_contact": 0.9, "mouth_openness": 0.6},
            "confident": {"chest_out": 0.7, "eye_intensity": 0.8, "smile": 0.6},
            "surprised": {"eye_width": 1.0, "eyebrow_raise": 0.9, "mouth_open": 0.8}
        }
        
        animation_data = {
            "mentor_id": mentor_id,
            "emotion": emotion,
            "duration": len(text) * 0.05,  # Примерная продолжительность
            "keyframes": [],
            "facial_expressions": base_emotions.get(emotion, base_emotions["thinking"]),
            "lip_sync": await self._generate_lip_sync_data(text),
            "gesture_cues": animation_cues
        }
        
        return animation_data
    
    async def _generate_lip_sync_data(self, text: str) -> List[Dict[str, float]]:
        """Генерирует данные для синхронизации губ"""
        # Упрощенный алгоритм для демонстрации
        lip_sync = []
        
        vowels = "аеёиоуыэюя"
        consonants = "бвгджзйклмнпрстфхцчшщ"
        
        for i, char in enumerate(text.lower()):
            if char in vowels:
                lip_sync.append({
                    "time": i * 0.1,
                    "mouth_openness": 0.8,
                    "mouth_width": 0.6
                })
            elif char in consonants:
                lip_sync.append({
                    "time": i * 0.1, 
                    "mouth_openness": 0.3,
                    "mouth_width": 0.4
                })
        
        return lip_sync
    
    async def _analyze_text_for_animation(self, text: str) -> List[Dict[str, Any]]:
        """Анализирует текст для определения анимационных подсказок"""
        cues = []
        
        # Поиск ключевых слов для жестикуляции
        gesture_keywords = {
            "большой": {"gesture": "expand_hands", "intensity": 0.8},
            "маленький": {"gesture": "pinch_fingers", "intensity": 0.6},
            "важно": {"gesture": "point_finger", "intensity": 0.9},
            "здесь": {"gesture": "point_location", "intensity": 0.7},
            "вы": {"gesture": "point_person", "intensity": 0.8},
            "я": {"gesture": "point_self", "intensity": 0.6}
        }
        
        words = text.lower().split()
        for i, word in enumerate(words):
            if word in gesture_keywords:
                cues.append({
                    "time": i * 0.5,  # Примерное время произношения
                    "type": "gesture",
                    "data": gesture_keywords[word]
                })
        
        # Поиск вопросов для изменения интонации
        if "?" in text:
            cues.append({
                "time": len(words) * 0.4,
                "type": "intonation",
                "data": {"eyebrow_raise": 0.7, "head_tilt": 0.3}
            })
        
        return cues
    
    async def _analyze_emotion(self, text: str) -> str:
        """Анализирует эмоцию в тексте"""
        # Упрощенный анализ эмоций
        emotion_keywords = {
            "happy": ["рад", "отлично", "замечательно", "великолепно", "счастлив"],
            "excited": ["невероятно", "потрясающе", "фантастика", "вау"],
            "thinking": ["думаю", "размышляю", "анализирую", "рассматриваю"],
            "confident": ["уверен", "определенно", "точно", "безусловно"],
            "concerned": ["беспокоюсь", "тревожно", "проблема", "сложно"]
        }
        
        text_lower = text.lower()
        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return emotion
        
        return "neutral"
    
    async def _analyze_sentiment(self, text: str) -> str:
        """Анализирует тональность текста"""
        positive_words = ["хорошо", "отлично", "замечательно", "успех", "прогресс"]
        negative_words = ["плохо", "ужасно", "проблема", "неудача", "провал"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    async def process_real_time_conversation(self,
                                           audio_stream: AsyncGenerator[bytes, None],
                                           mentor_id: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Обрабатывает разговор в реальном времени"""
        
        voice_profile = self.voice_profiles[mentor_id]
        conversation_buffer = []
        
        async for audio_chunk in audio_stream:
            try:
                # Транскрибируем аудио
                transcription = await self.speech_to_text(
                    audio_chunk, 
                    VoiceProvider.OPENAI_WHISPER
                )
                
                if transcription.text.strip():
                    conversation_buffer.append({
                        "type": "user_input",
                        "text": transcription.text,
                        "emotion": transcription.emotion,
                        "confidence": transcription.confidence,
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
                    # Генерируем ответ ИИ (здесь будет вызов AI сервиса)
                    ai_response = await self._generate_ai_response(
                        transcription.text, 
                        mentor_id, 
                        conversation_buffer
                    )
                    
                    # Создаем аудио ответ
                    response_audio = await self.text_to_speech(
                        ai_response["text"], 
                        mentor_id,
                        ai_response["emotion"]
                    )
                    
                    # Создаем анимацию аватара
                    avatar_animation = await self.create_3d_avatar_animation(
                        ai_response["text"],
                        ai_response["emotion"],
                        mentor_id
                    )
                    
                    yield {
                        "user_input": transcription.text,
                        "ai_response": ai_response["text"], 
                        "audio_data": base64.b64encode(response_audio).decode(),
                        "animation_data": avatar_animation,
                        "emotion": ai_response["emotion"],
                        "confidence": transcription.confidence
                    }
            
            except Exception as e:
                yield {
                    "error": str(e),
                    "timestamp": asyncio.get_event_loop().time()
                }
    
    async def _generate_ai_response(self, 
                                  user_text: str, 
                                  mentor_id: str, 
                                  conversation_history: List[Dict]) -> Dict[str, Any]:
        """Генерирует ответ ИИ (заглушка для интеграции с AI сервисом)"""
        
        # Здесь будет интеграция с продвинутым AI сервисом
        # Пока возвращаем базовую заглушку
        
        mentor_responses = {
            'elon_musk': {
                "default": "Это интересная задача! Я думаю, нам нужно подходить к этому как к инженерной проблеме первых принципов.",
                "emotion": "confident"
            },
            'bill_gates': {
                "default": "По моему опыту, здесь важно сначала проанализировать данные и понять корень проблемы.",
                "emotion": "analytical"
            },
            'warren_buffett': {
                "default": "Мой совет: всегда думайте долгосрочно и инвестируйте в то, что понимаете.",
                "emotion": "wise"
            },
            'jeff_bezos': {
                "default": "Начните с клиента и работайте в обратном направлении. Всегда день первый!",
                "emotion": "determined"
            }
        }
        
        return mentor_responses.get(mentor_id, mentor_responses['elon_musk'])

# Utility функции для интеграции с фронтендом
class AudioVideoAPI:
    """API класс для фронтенда"""
    
    def __init__(self):
        self.integration = AudioVideoIntegration()
    
    async def process_voice_message(self, 
                                  audio_data: bytes, 
                                  mentor_id: str) -> Dict[str, Any]:
        """Обрабатывает голосовое сообщение от пользователя"""
        async with self.integration:
            try:
                # Транскрибируем речь
                transcription = await self.integration.speech_to_text(audio_data)
                
                # Генерируем ответ
                ai_response = await self.integration._generate_ai_response(
                    transcription.text,
                    mentor_id,
                    []
                )
                
                # Создаем аудио ответ
                response_audio = await self.integration.text_to_speech(
                    ai_response["text"],
                    mentor_id,
                    ai_response["emotion"]
                )
                
                # Создаем анимацию
                animation = await self.integration.create_3d_avatar_animation(
                    ai_response["text"],
                    ai_response["emotion"], 
                    mentor_id
                )
                
                return {
                    "success": True,
                    "user_text": transcription.text,
                    "ai_response": ai_response["text"],
                    "audio_response": base64.b64encode(response_audio).decode(),
                    "animation_data": animation,
                    "emotion": ai_response["emotion"],
                    "confidence": transcription.confidence
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }

# Export главных классов
__all__ = [
    'AudioVideoIntegration',
    'AudioVideoAPI', 
    'VoiceProvider',
    'TTSProvider',
    'VoiceProfile',
    'AudioProcessingResult'
]