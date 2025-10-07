#!/usr/bin/env python3
"""
ADVANCED TEMPLATES ENGINE
Система продвинутых шаблонов для создания современных приложений
"""

from typing import Dict, List, Any, Optional
import json

class AdvancedTemplates:
    """Движок продвинутых шаблонов"""
    
    def __init__(self):
        self.templates = self._initialize_templates()
    
    def _initialize_templates(self) -> Dict[str, Any]:
        """Инициализация продвинутых шаблонов"""
        
        return {
            "ai_mentor_3d": {
                "name": "AI Наставник с 3D аватаром",
                "description": "Интерактивный AI наставник с 3D визуализацией и голосовыми возможностями",
                "features": ["3D аватары", "голосовой ввод", "text-to-speech", "психологический анализ", "история разговоров"],
                "technologies": ["Three.js", "Web Speech API", "WebGL", "localStorage"],
                "html_template": self._get_ai_mentor_html(),
                "css_template": self._get_ai_mentor_css(),
                "js_template": self._get_ai_mentor_js(),
                "complexity": "high"
            },
            
            "voice_assistant": {
                "name": "Голосовой ассистент",
                "description": "Голосовой помощник с распознаванием речи и синтезом",
                "features": ["голосовой ввод", "text-to-speech", "команды", "offline режим"],
                "technologies": ["Web Speech API", "Service Worker"],
                "html_template": self._get_voice_assistant_html(),
                "css_template": self._get_voice_assistant_css(),
                "js_template": self._get_voice_assistant_js(),
                "complexity": "medium"
            },
            
            "3d_showcase": {
                "name": "3D Витрина",
                "description": "Интерактивная 3D витрина товаров с WebGL",
                "features": ["3D модели", "интерактивность", "освещение", "анимации"],
                "technologies": ["Three.js", "WebGL", "GLTF"],
                "html_template": self._get_3d_showcase_html(),
                "css_template": self._get_3d_showcase_css(),
                "js_template": self._get_3d_showcase_js(),
                "complexity": "high"
            },
            
            "mobile_first": {
                "name": "Mobile-First PWA",
                "description": "Прогрессивное веб-приложение с мобильным дизайном",
                "features": ["PWA", "offline", "push уведомления", "установка"],
                "technologies": ["Service Worker", "Web App Manifest", "PWA"],
                "html_template": self._get_mobile_first_html(),
                "css_template": self._get_mobile_first_css(),
                "js_template": self._get_mobile_first_js(),
                "complexity": "medium"
            }
        }
    
    def get_template(self, template_type: str) -> Optional[Dict[str, Any]]:
        """Получить шаблон по типу"""
        return self.templates.get(template_type)
    
    def get_best_template(self, features: List[str], project_type: str) -> str:
        """Выбрать лучший шаблон на основе функций"""
        
        # Анализ функций
        has_3d = any("3d" in f.lower() for f in features)
        has_voice = any("голос" in f.lower() or "voice" in f.lower() for f in features)
        has_ai = any("ai" in f.lower() or "ии" in f.lower() for f in features)
        has_mobile = any("мобил" in f.lower() or "mobile" in f.lower() for f in features)
        
        # AI наставник - высший приоритет
        if (has_ai or "наставник" in project_type.lower() or "mentor" in project_type.lower()) and (has_3d or has_voice):
            return "ai_mentor_3d"
        
        # Голосовой ассистент
        elif has_voice and has_ai:
            return "voice_assistant"
            
        # 3D приложения
        elif has_3d:
            return "3d_showcase"
            
        # Мобильные приложения
        elif has_mobile:
            return "mobile_first"
            
        # По умолчанию - AI наставник
        else:
            return "ai_mentor_3d"
    
    def _get_ai_mentor_html(self) -> str:
        """HTML шаблон для AI наставника"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Наставник 3D</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <header class="header">
            <h1>🤖 AI Наставник 3D</h1>
            <div class="mentor-selector">
                <label>Выберите наставника:</label>
                <select id="mentorSelect">
                    <option value="elon">🚀 Илон Маск</option>
                    <option value="jobs">💻 Стив Джобс</option>
                    <option value="gates">🌍 Билл Гейтс</option>
                    <option value="bezos">📦 Джефф Безос</option>
                    <option value="buffett">💰 Уоррен Баффет</option>
                </select>
            </div>
        </header>
        
        <div class="main-content">
            <div class="mentor-avatar">
                <div id="avatar3d" class="avatar-container">
                    <div class="avatar-placeholder">
                        <div class="loading">Загрузка 3D модели...</div>
                    </div>
                </div>
                <div class="mentor-info">
                    <h3 id="mentorName">Илон Маск</h3>
                    <p id="mentorDescription">Визионер и предприниматель, основатель Tesla, SpaceX и Neuralink</p>
                </div>
            </div>
            
            <div class="chat-interface">
                <div class="chat-messages" id="chatMessages">
                    <div class="message ai-message">
                        <div class="message-avatar">🤖</div>
                        <div class="message-content">
                            <strong>AI Наставник:</strong> Привет! Я готов поделиться опытом и знаниями. О чем хотите поговорить?
                        </div>
                    </div>
                </div>
                
                <div class="chat-input-container">
                    <textarea id="userInput" placeholder="Задайте вопрос своему наставнику..."></textarea>
                    <button id="sendBtn">Отправить</button>
                </div>
            </div>
        </div>
        
        <div class="features-panel">
            <h4>Возможности:</h4>
            <ul>
                <li>💬 Реалистичные диалоги</li>
                <li>🎯 Персональные советы</li>
                <li>📊 Анализ ситуаций</li>
                <li>🚀 Стратегии развития</li>
                <li>💡 Инновационные идеи</li>
                <li>🎤 Голосовой ввод</li>
                <li>🔊 Озвучивание ответов</li>
                <li>🎭 3D аватары</li>
            </ul>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_ai_mentor_css(self) -> str:
        """CSS шаблон для AI наставника"""
        return '''/* Современный дизайн AI наставника */
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ff6b35;
    --mentor-color: #ff6b35;
    --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --text-color: #ffffff;
    --text-secondary: #e0e0e0;
    --bg-dark: #1a1a2e;
    --bg-card: rgba(255, 255, 255, 0.1);
    --border-radius: 12px;
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg-gradient);
    color: var(--text-color);
    min-height: 100vh;
    overflow-x: hidden;
}

.app-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    max-width: 1400px;
    margin: 0 auto;
    padding: 20px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 30px;
}

.header h1 {
    font-size: 2rem;
    font-weight: 700;
    background: linear-gradient(45deg, #ff6b35, #ffbe0b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.mentor-selector {
    display: flex;
    align-items: center;
    gap: 12px;
}

.mentor-selector select {
    background: var(--bg-card);
    color: var(--text-color);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    padding: 10px 16px;
    font-size: 1rem;
    cursor: pointer;
    transition: var(--transition);
    backdrop-filter: blur(10px);
}

.main-content {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    flex: 1;
    align-items: start;
}

.mentor-avatar {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;
}

.avatar-container {
    width: 400px;
    height: 400px;
    background: radial-gradient(circle at center, rgba(255, 255, 255, 0.1) 0%, rgba(0, 0, 0, 0.3) 100%);
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow);
    backdrop-filter: blur(20px);
}

.avatar-container canvas {
    width: 100% !important;
    height: 100% !important;
    border-radius: 50%;
}

.avatar-placeholder {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    opacity: 0.7;
}

.avatar-placeholder .loading {
    font-size: 0.9rem;
    color: var(--text-secondary);
    animation: fadeInOut 1.5s infinite;
}

.mentor-info {
    text-align: center;
    max-width: 400px;
}

.mentor-info h3 {
    font-size: 1.8rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: var(--mentor-color);
}

.chat-interface {
    display: flex;
    flex-direction: column;
    height: 600px;
    background: var(--bg-card);
    border-radius: var(--border-radius);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    box-shadow: var(--shadow);
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    scroll-behavior: smooth;
}

.message {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
    animation: slideInUp 0.3s ease-out;
}

.message.user-message {
    flex-direction: row-reverse;
}

.message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    background: var(--mentor-color);
    flex-shrink: 0;
}

.message-content {
    flex: 1;
    background: rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    padding: 12px 16px;
    backdrop-filter: blur(10px);
    max-width: 80%;
}

.chat-input-container {
    display: flex;
    gap: 12px;
    padding: 20px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
}

#userInput {
    flex: 1;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    padding: 12px 16px;
    color: var(--text-color);
    font-size: 1rem;
    resize: none;
    min-height: 44px;
    transition: var(--transition);
    backdrop-filter: blur(10px);
}

#sendBtn {
    background: var(--mentor-color);
    color: white;
    border: none;
    border-radius: var(--border-radius);
    padding: 12px 24px;
    font-size: 1rem;
    cursor: pointer;
    transition: var(--transition);
}

#sendBtn:hover {
    background: linear-gradient(45deg, #ff6b35, #ff8c42);
    transform: translateY(-1px);
}

.voice-btn {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius);
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 1.2rem;
}

.voice-btn.listening {
    background: var(--mentor-color);
    animation: pulse 1s infinite;
}

.features-panel {
    background: var(--bg-card);
    border-radius: var(--border-radius);
    padding: 24px;
    margin-top: 30px;
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.features-panel ul {
    list-style: none;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
}

/* Анимации */
@keyframes pulse {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.05); }
    100% { opacity: 1; transform: scale(1); }
}

@keyframes fadeInOut {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Адаптивный дизайн */
@media (max-width: 1024px) {
    .main-content {
        grid-template-columns: 1fr;
        gap: 30px;
    }
    
    .avatar-container {
        width: 300px;
        height: 300px;
    }
}

@media (max-width: 768px) {
    .header {
        flex-direction: column;
        gap: 20px;
    }
    
    .avatar-container {
        width: 250px;
        height: 250px;
    }
    
    .chat-interface {
        height: 400px;
    }
}'''
    
    def _get_ai_mentor_js(self) -> str:
        """JavaScript шаблон для AI наставника"""
        return '''// AI Наставник 3D - Продвинутый JavaScript
let scene, camera, renderer, currentAvatar;
let voices = [];
let recognition = null;
let isListening = false;
let currentMentor = 'elon';
let conversationHistory = [];

// Данные наставников
const mentors = {
    elon: {
        name: 'Илон Маск',
        description: 'Визионер и предприниматель, основатель Tesla, SpaceX и Neuralink',
        color: '#ff6b35',
        personality: 'дерзкий, инновационный, амбициозный'
    },
    jobs: {
        name: 'Стив Джобс',
        description: 'Легендарный основатель Apple, революционер технологий',
        color: '#007aff',
        personality: 'перфекционист, креативный, требовательный'
    },
    gates: {
        name: 'Билл Гейтс',
        description: 'Основатель Microsoft, филантроп и визионер',
        color: '#00a1f1',
        personality: 'аналитичный, стратегический, гуманный'
    },
    bezos: {
        name: 'Джефф Безос',
        description: 'Основатель Amazon, пионер электронной коммерции',
        color: '#ff9900',
        personality: 'целеустремленный, клиентоориентированный'
    },
    buffett: {
        name: 'Уоррен Баффет',
        description: 'Легендарный инвестор, оракул из Омахи',
        color: '#2e8b57',
        personality: 'мудрый, терпеливый, ценностно-ориентированный'
    }
};

// Инициализация
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupVoiceSupport();
    setupEventListeners();
    createAvatar();
});

function initializeApp() {
    console.log('🚀 Инициализация AI Наставника 3D...');
    
    if (!isWebGLSupported()) {
        showError('WebGL не поддерживается');
        return;
    }
    
    init3DScene();
    loadConversationHistory();
}

function isWebGLSupported() {
    try {
        const canvas = document.createElement('canvas');
        return !!(window.WebGLRenderingContext && canvas.getContext('webgl'));
    } catch (e) {
        return false;
    }
}

function init3DScene() {
    const container = document.getElementById('avatar3d');
    
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 5;
    
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    
    // Освещение
    const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    scene.add(directionalLight);
    
    animate();
}

function createAvatar() {
    const mentor = mentors[currentMentor];
    
    if (currentAvatar) {
        scene.remove(currentAvatar);
    }
    
    currentAvatar = new THREE.Group();
    
    // Голова
    const headGeometry = new THREE.SphereGeometry(1, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({ 
        color: mentor.color,
        shininess: 100,
        transparent: true,
        opacity: 0.9
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 1.5;
    currentAvatar.add(head);
    
    // Тело
    const bodyGeometry = new THREE.CylinderGeometry(0.6, 0.8, 2, 8);
    const bodyMaterial = new THREE.MeshPhongMaterial({ 
        color: new THREE.Color(mentor.color).multiplyScalar(0.7)
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    currentAvatar.add(body);
    
    // Глаза
    const eyeGeometry = new THREE.SphereGeometry(0.1, 8, 8);
    const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
    
    const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    leftEye.position.set(-0.3, 1.7, 0.8);
    currentAvatar.add(leftEye);
    
    const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
    rightEye.position.set(0.3, 1.7, 0.8);
    currentAvatar.add(rightEye);
    
    scene.add(currentAvatar);
    
    // Анимация появления
    currentAvatar.scale.set(0, 0, 0);
    animateAvatarAppearance();
    updateMentorInfo();
}

function animateAvatarAppearance() {
    const startTime = Date.now();
    const duration = 1000;
    
    function animate() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        
        currentAvatar.scale.set(eased, eased, eased);
        currentAvatar.rotation.y = (1 - eased) * Math.PI * 2;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    
    if (currentAvatar) {
        const time = Date.now() * 0.001;
        currentAvatar.rotation.y += 0.005;
        currentAvatar.position.y = Math.sin(time * 2) * 0.1;
    }
    
    renderer.render(scene, camera);
}

function setupVoiceSupport() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        
        recognition.lang = 'ru-RU';
        recognition.continuous = false;
        recognition.interimResults = false;
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('userInput').value = transcript;
            sendMessage();
        };
        
        recognition.onerror = function(event) {
            console.error('Speech error:', event.error);
            isListening = false;
            updateVoiceButton();
        };
        
        recognition.onend = function() {
            isListening = false;
            updateVoiceButton();
        };
    }
    
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = function() {
            voices = speechSynthesis.getVoices();
        };
        voices = speechSynthesis.getVoices();
    }
}

function setupEventListeners() {
    document.getElementById('mentorSelect').addEventListener('change', function(e) {
        currentMentor = e.target.value;
        createAvatar();
    });
    
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    addVoiceButton();
    window.addEventListener('resize', onWindowResize);
}

function addVoiceButton() {
    const inputContainer = document.querySelector('.chat-input-container');
    
    const voiceBtn = document.createElement('button');
    voiceBtn.id = 'voiceBtn';
    voiceBtn.className = 'voice-btn';
    voiceBtn.innerHTML = '🎤';
    voiceBtn.addEventListener('click', toggleVoiceInput);
    
    inputContainer.appendChild(voiceBtn);
}

function toggleVoiceInput() {
    if (!recognition) {
        showNotification('Голосовой ввод не поддерживается');
        return;
    }
    
    if (isListening) {
        recognition.stop();
        isListening = false;
    } else {
        recognition.start();
        isListening = true;
        showNotification('Говорите...');
    }
    
    updateVoiceButton();
}

function updateVoiceButton() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.innerHTML = isListening ? '⏹️' : '🎤';
        voiceBtn.classList.toggle('listening', isListening);
    }
}

async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addMessage(message, 'user');
    input.value = '';
    
    showTypingIndicator();
    
    try {
        // Имитация AI ответа (заменить на реальный API)
        const response = await simulateAIResponse(message);
        
        removeTypingIndicator();
        addMessage(response, 'ai');
        speakText(response);
        
    } catch (error) {
        console.error('Ошибка:', error);
        removeTypingIndicator();
        addMessage('Извините, произошла ошибка.', 'ai');
    }
}

async function simulateAIResponse(message) {
    // Симуляция задержки
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const mentor = mentors[currentMentor];
    const responses = {
        elon: [
            "Думайте от первых принципов! Разложите проблему на основные элементы.",
            "Не бойтесь провала - это путь к инновациям. SpaceX взрывалась много раз, прежде чем полетела.",
            "Масштабируйте решения для всего человечества. Как это поможет миллиардам людей?"
        ],
        jobs: [
            "Простота - высшая форма изящества. Уберите всё лишнее.",
            "Фокусируйтесь на том, что действительно важно. Совершенство в деталях создает магию.",
            "Think Different. Инновация отличает лидера от последователя."
        ],
        gates: [
            "Анализируйте данные перед принятием решений. Что говорят цифры?",
            "Инвестируйте в образование и знания. Это лучшая инвестиция в будущее.",
            "Решайте проблемы системно. Как это вписывается в большую картину?"
        ],
        bezos: [
            "Начинайте с клиента и идите назад. Что нужно вашим клиентам?",
            "Мыслите долгосрочно. День 1 всё ещё продолжается.",
            "Изобретайте и будьте готовы к непониманию. Неудача и изобретательство неразлучны."
        ],
        buffett: [
            "Инвестируйте в то, что понимаете. Круг компетенций - ваша сила.",
            "Время - друг замечательного бизнеса и враг посредственного.",
            "Будьте жадными, когда другие боятся, и осторожными, когда другие жадные."
        ]
    };
    
    const mentorResponses = responses[currentMentor] || responses.elon;
    return mentorResponses[Math.floor(Math.random() * mentorResponses.length)];
}

function addMessage(text, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <strong>${mentors[currentMentor].name}:</strong>
                <p>${text}</p>
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${text}</p>
                <div style="font-size: 0.75rem; opacity: 0.7; margin-top: 4px;">
                    ${new Date().toLocaleTimeString()}
                </div>
            </div>
            <div class="message-avatar">👤</div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    conversationHistory.push({ sender, text, timestamp: new Date().toISOString() });
    saveConversationHistory();
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div style="display: flex; gap: 4px; padding: 8px 0;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #ff6b35; animation: pulse 1.4s infinite;"></span>
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #ff6b35; animation: pulse 1.4s infinite 0.2s;"></span>
                <span style="width: 6px; height: 6px; border-radius: 50%; background: #ff6b35; animation: pulse 1.4s infinite 0.4s;"></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    const voice = voices.find(v => v.lang.includes('ru')) || voices[0];
    if (voice) utterance.voice = voice;
    
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    speechSynthesis.speak(utterance);
}

function updateMentorInfo() {
    const mentor = mentors[currentMentor];
    document.getElementById('mentorName').textContent = mentor.name;
    document.getElementById('mentorDescription').textContent = mentor.description;
    document.documentElement.style.setProperty('--mentor-color', mentor.color);
}

function saveConversationHistory() {
    try {
        localStorage.setItem('ai_mentor_history', JSON.stringify(conversationHistory));
    } catch (error) {
        console.error('Ошибка сохранения:', error);
    }
}

function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('ai_mentor_history');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            const recentMessages = conversationHistory.slice(-5);
            
            if (recentMessages.length > 0) {
                const messagesContainer = document.getElementById('chatMessages');
                messagesContainer.innerHTML = '';
                recentMessages.forEach(msg => addMessage(msg.text, msg.sender));
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки:', error);
    }
}

function onWindowResize() {
    const container = document.getElementById('avatar3d');
    if (container && camera && renderer) {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
}

function showNotification(message) {
    // Простая реализация уведомлений
    console.log('Уведомление:', message);
}

function showError(message) {
    const container = document.getElementById('avatar3d');
    container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ff4757;">
            <h3>❌ Ошибка</h3>
            <p>${message}</p>
            <button onclick="location.reload()" style="margin-top: 20px; padding: 10px 20px; background: #ff6b35; color: white; border: none; border-radius: 8px; cursor: pointer;">
                Перезагрузить
            </button>
        </div>
    `;
}'''
    
    def _get_voice_assistant_html(self) -> str:
        """HTML для голосового ассистента"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Голосовой Ассистент</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="app-container">
        <div class="voice-interface">
            <div class="voice-circle" id="voiceCircle">
                <div class="pulse-ring"></div>
                <div class="voice-icon">🎤</div>
            </div>
            <h2 id="status">Нажмите для активации</h2>
            <div class="transcript" id="transcript"></div>
        </div>
        
        <div class="response-area" id="responseArea">
            <!-- Ответы ассистента -->
        </div>
        
        <div class="controls">
            <button id="toggleBtn" class="control-btn">Активировать</button>
            <button id="settingsBtn" class="control-btn">Настройки</button>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_voice_assistant_css(self) -> str:
        """CSS для голосового ассистента"""
        return '''body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.app-container {
    text-align: center;
    max-width: 600px;
    padding: 40px;
}

.voice-interface {
    margin-bottom: 40px;
}

.voice-circle {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    cursor: pointer;
    transition: all 0.3s ease;
}

.voice-circle:hover {
    transform: scale(1.05);
}

.voice-circle.listening {
    background: rgba(255, 107, 53, 0.2);
    animation: pulse 2s infinite;
}

.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid rgba(255, 255, 255, 0.3);
    border-radius: 50%;
    animation: pulse-ring 1.5s infinite;
}

.voice-icon {
    font-size: 3rem;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

@keyframes pulse-ring {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.3); opacity: 0; }
}

.transcript {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
}

.response-area {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    min-height: 100px;
}

.controls {
    display: flex;
    gap: 20px;
    justify-content: center;
}

.control-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    border-radius: 25px;
    padding: 12px 24px;
    color: white;
    cursor: pointer;
    transition: all 0.3s ease;
}

.control-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}'''
    
    def _get_voice_assistant_js(self) -> str:
        """JavaScript для голосового ассистента"""
        return '''let recognition;
let isListening = false;
let voices = [];

document.addEventListener('DOMContentLoaded', function() {
    initVoiceAssistant();
    setupEventListeners();
});

function initVoiceAssistant() {
    if ('webkitSpeechRecognition' in window) {
        recognition = new webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'ru-RU';
        
        recognition.onstart = function() {
            isListening = true;
            updateUI();
        };
        
        recognition.onresult = function(event) {
            const transcript = event.results[0][0].transcript;
            document.getElementById('transcript').textContent = transcript;
            
            if (event.results[0].isFinal) {
                processCommand(transcript);
            }
        };
        
        recognition.onend = function() {
            isListening = false;
            updateUI();
        };
    }
    
    if ('speechSynthesis' in window) {
        voices = speechSynthesis.getVoices();
        speechSynthesis.onvoiceschanged = function() {
            voices = speechSynthesis.getVoices();
        };
    }
}

function setupEventListeners() {
    document.getElementById('voiceCircle').addEventListener('click', toggleListening);
    document.getElementById('toggleBtn').addEventListener('click', toggleListening);
}

function toggleListening() {
    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
}

function updateUI() {
    const circle = document.getElementById('voiceCircle');
    const status = document.getElementById('status');
    const btn = document.getElementById('toggleBtn');
    
    if (isListening) {
        circle.classList.add('listening');
        status.textContent = 'Слушаю...';
        btn.textContent = 'Остановить';
    } else {
        circle.classList.remove('listening');
        status.textContent = 'Нажмите для активации';
        btn.textContent = 'Активировать';
    }
}

function processCommand(command) {
    const response = generateResponse(command);
    displayResponse(response);
    speakResponse(response);
}

function generateResponse(command) {
    const lowerCommand = command.toLowerCase();
    
    if (lowerCommand.includes('время')) {
        return `Сейчас ${new Date().toLocaleTimeString()}`;
    }
    
    if (lowerCommand.includes('дата')) {
        return `Сегодня ${new Date().toLocaleDateString()}`;
    }
    
    if (lowerCommand.includes('погода')) {
        return 'Извините, я не могу получить данные о погоде. Проверьте прогноз в вашем приложении.';
    }
    
    if (lowerCommand.includes('привет') || lowerCommand.includes('здравствуй')) {
        return 'Привет! Как дела? Чем могу помочь?';
    }
    
    return 'Интересный вопрос! Я ещё учусь понимать такие запросы.';
}

function displayResponse(response) {
    const responseArea = document.getElementById('responseArea');
    responseArea.innerHTML = `<p>${response}</p>`;
}

function speakResponse(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        const russianVoice = voices.find(voice => voice.lang.includes('ru'));
        if (russianVoice) {
            utterance.voice = russianVoice;
        }
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }
}'''
    
    def _get_3d_showcase_html(self) -> str:
        """HTML для 3D витрины"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>3D Витрина</title>
    <link rel="stylesheet" href="styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <h1>3D Витрина</h1>
            <div class="controls">
                <button id="resetView">Сброс вида</button>
                <button id="autoRotate">Автовращение</button>
            </div>
        </header>
        
        <div class="showcase">
            <div id="canvas-container"></div>
            <div class="info-panel">
                <h3 id="itemName">Выберите объект</h3>
                <p id="itemDescription">Кликните на объект для просмотра информации</p>
            </div>
        </div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_3d_showcase_css(self) -> str:
        """CSS для 3D витрины"""
        return '''body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #2c3e50, #3498db);
    color: white;
    overflow: hidden;
}

.container {
    height: 100vh;
    display: flex;
    flex-direction: column;
}

header {
    padding: 20px;
    background: rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.controls button {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    padding: 10px 20px;
    margin-left: 10px;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    transition: all 0.3s;
}

.controls button:hover {
    background: rgba(255, 255, 255, 0.4);
}

.showcase {
    flex: 1;
    display: flex;
    position: relative;
}

#canvas-container {
    flex: 1;
    position: relative;
}

#canvas-container canvas {
    display: block;
    cursor: grab;
}

#canvas-container canvas:active {
    cursor: grabbing;
}

.info-panel {
    width: 300px;
    background: rgba(0, 0, 0, 0.5);
    padding: 30px;
    backdrop-filter: blur(10px);
}

.info-panel h3 {
    margin-top: 0;
    color: #3498db;
}'''
    
    def _get_3d_showcase_js(self) -> str:
        """JavaScript для 3D витрины"""
        return '''let scene, camera, renderer;
let objects = [];
let selectedObject = null;
let autoRotateEnabled = false;
let mouse = new THREE.Vector2();
let raycaster = new THREE.Raycaster();

init();
animate();

function init() {
    // Сцена
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x2c3e50);
    
    // Камера
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Рендерер
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth - 300, window.innerHeight - 80);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    
    document.getElementById('canvas-container').appendChild(renderer.domElement);
    
    // Освещение
    const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    
    // Создание объектов
    createObjects();
    
    // События
    setupEventListeners();
}

function createObjects() {
    // Куб
    const cubeGeometry = new THREE.BoxGeometry();
    const cubeMaterial = new THREE.MeshPhongMaterial({ color: 0x3498db });
    const cube = new THREE.Mesh(cubeGeometry, cubeMaterial);
    cube.position.x = -2;
    cube.userData = { name: 'Куб', description: 'Базовый геометрический объект' };
    scene.add(cube);
    objects.push(cube);
    
    // Сфера
    const sphereGeometry = new THREE.SphereGeometry(0.7, 32, 32);
    const sphereMaterial = new THREE.MeshPhongMaterial({ color: 0xe74c3c });
    const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
    sphere.position.x = 0;
    sphere.userData = { name: 'Сфера', description: 'Идеально круглый объект' };
    scene.add(sphere);
    objects.push(sphere);
    
    // Тор
    const torusGeometry = new THREE.TorusGeometry(0.7, 0.3, 16, 100);
    const torusMaterial = new THREE.MeshPhongMaterial({ color: 0x2ecc71 });
    const torus = new THREE.Mesh(torusGeometry, torusMaterial);
    torus.position.x = 2;
    torus.userData = { name: 'Тор', description: 'Объект в форме бублика' };
    scene.add(torus);
    objects.push(torus);
}

function setupEventListeners() {
    // Клик по объектам
    renderer.domElement.addEventListener('click', onMouseClick);
    
    // Управление камерой
    renderer.domElement.addEventListener('mousedown', onMouseDown);
    renderer.domElement.addEventListener('mousemove', onMouseMove);
    
    // Кнопки управления
    document.getElementById('resetView').addEventListener('click', resetView);
    document.getElementById('autoRotate').addEventListener('click', toggleAutoRotate);
    
    // Изменение размера
    window.addEventListener('resize', onWindowResize);
}

function onMouseClick(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(objects);
    
    if (intersects.length > 0) {
        selectObject(intersects[0].object);
    }
}

function selectObject(object) {
    // Сброс предыдущего выделения
    if (selectedObject) {
        selectedObject.material.emissive.setHex(0x000000);
    }
    
    // Выделение нового объекта
    selectedObject = object;
    object.material.emissive.setHex(0x444444);
    
    // Обновление информации
    document.getElementById('itemName').textContent = object.userData.name;
    document.getElementById('itemDescription').textContent = object.userData.description;
}

let isMouseDown = false;
let mouseX = 0;
let mouseY = 0;

function onMouseDown(event) {
    isMouseDown = true;
    mouseX = event.clientX;
    mouseY = event.clientY;
}

function onMouseMove(event) {
    if (!isMouseDown) return;
    
    const deltaX = event.clientX - mouseX;
    const deltaY = event.clientY - mouseY;
    
    camera.position.x += deltaX * 0.01;
    camera.position.y -= deltaY * 0.01;
    
    mouseX = event.clientX;
    mouseY = event.clientY;
}

document.addEventListener('mouseup', function() {
    isMouseDown = false;
});

function resetView() {
    camera.position.set(0, 0, 5);
    camera.lookAt(0, 0, 0);
}

function toggleAutoRotate() {
    autoRotateEnabled = !autoRotateEnabled;
    const btn = document.getElementById('autoRotate');
    btn.textContent = autoRotateEnabled ? 'Остановить' : 'Автовращение';
}

function animate() {
    requestAnimationFrame(animate);
    
    // Вращение объектов
    objects.forEach((object, index) => {
        object.rotation.x += 0.01;
        object.rotation.y += 0.01;
    });
    
    // Автовращение камеры
    if (autoRotateEnabled) {
        const time = Date.now() * 0.0005;
        camera.position.x = Math.cos(time) * 5;
        camera.position.z = Math.sin(time) * 5;
        camera.lookAt(0, 0, 0);
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = (window.innerWidth - 300) / (window.innerHeight - 80);
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth - 300, window.innerHeight - 80);
}'''
    
    def _get_mobile_first_html(self) -> str:
        """HTML для мобильного PWA"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мобильное PWA</title>
    <meta name="description" content="Прогрессивное веб-приложение">
    <meta name="theme-color" content="#667eea">
    <link rel="manifest" href="manifest.json">
    <link rel="stylesheet" href="styles.css">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📱</text></svg>">
</head>
<body>
    <div class="app">
        <header class="header">
            <h1>📱 Мобильное PWA</h1>
            <button id="installBtn" class="install-btn" style="display: none;">Установить</button>
        </header>
        
        <main class="main">
            <section class="hero">
                <h2>Добро пожаловать!</h2>
                <p>Это прогрессивное веб-приложение, оптимизированное для мобильных устройств</p>
            </section>
            
            <section class="features">
                <div class="feature-card">
                    <div class="feature-icon">🚀</div>
                    <h3>Быстрая загрузка</h3>
                    <p>Мгновенная загрузка благодаря Service Worker</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">📱</div>
                    <h3>Мобильный дизайн</h3>
                    <p>Адаптивный интерфейс для всех устройств</p>
                </div>
                
                <div class="feature-card">
                    <div class="feature-icon">🔔</div>
                    <h3>Push уведомления</h3>
                    <p>Получайте важные обновления</p>
                </div>
            </section>
            
            <section class="actions">
                <button class="action-btn primary" id="notifyBtn">Включить уведомления</button>
                <button class="action-btn secondary" id="offlineBtn">Тест офлайн</button>
            </section>
        </main>
        
        <div class="status" id="status">Онлайн</div>
    </div>
    
    <script src="script.js"></script>
</body>
</html>'''
    
    def _get_mobile_first_css(self) -> str:
        """CSS для мобильного PWA"""
        return '''* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    min-height: 100vh;
    overflow-x: hidden;
}

.app {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.header {
    padding: 20px;
    background: rgba(0, 0, 0, 0.2);
    display: flex;
    justify-content: space-between;
    align-items: center;
    backdrop-filter: blur(10px);
}

.header h1 {
    font-size: 1.5rem;
}

.install-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    padding: 10px 16px;
    border-radius: 20px;
    color: white;
    cursor: pointer;
    font-size: 0.9rem;
}

.main {
    flex: 1;
    padding: 20px;
}

.hero {
    text-align: center;
    margin-bottom: 40px;
}

.hero h2 {
    font-size: 2rem;
    margin-bottom: 10px;
}

.hero p {
    opacity: 0.9;
    font-size: 1.1rem;
}

.features {
    display: grid;
    grid-template-columns: 1fr;
    gap: 20px;
    margin-bottom: 40px;
}

@media (min-width: 768px) {
    .features {
        grid-template-columns: repeat(3, 1fr);
    }
}

.feature-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.feature-card h3 {
    margin-bottom: 12px;
    font-size: 1.2rem;
}

.feature-card p {
    opacity: 0.8;
    font-size: 0.9rem;
    line-height: 1.5;
}

.actions {
    display: flex;
    flex-direction: column;
    gap: 16px;
    align-items: center;
}

@media (min-width: 768px) {
    .actions {
        flex-direction: row;
        justify-content: center;
    }
}

.action-btn {
    border: none;
    padding: 16px 32px;
    border-radius: 25px;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    min-width: 200px;
}

.action-btn.primary {
    background: rgba(255, 255, 255, 0.9);
    color: #333;
}

.action-btn.primary:hover {
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
}

.action-btn.secondary {
    background: transparent;
    color: white;
    border: 2px solid rgba(255, 255, 255, 0.5);
}

.action-btn.secondary:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: white;
}

.status {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: rgba(0, 0, 0, 0.8);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    backdrop-filter: blur(10px);
}

.status.offline {
    background: rgba(231, 76, 60, 0.8);
}

/* Touch improvements */
@media (hover: none) and (pointer: coarse) {
    .action-btn {
        padding: 20px 32px;
        font-size: 1.1rem;
    }
}'''
    
    def _get_mobile_first_js(self) -> str:
        """JavaScript для мобильного PWA"""
        return '''// PWA функциональность
let deferredPrompt;
let isOnline = navigator.onLine;

// Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('sw.js')
            .then(function(registration) {
                console.log('SW зарегистрирован:', registration.scope);
            })
            .catch(function(error) {
                console.log('SW ошибка:', error);
            });
    });
}

// Установка PWA
window.addEventListener('beforeinstallprompt', function(e) {
    e.preventDefault();
    deferredPrompt = e;
    document.getElementById('installBtn').style.display = 'block';
});

document.getElementById('installBtn').addEventListener('click', function() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(function(choiceResult) {
            console.log('Выбор пользователя:', choiceResult.outcome);
            deferredPrompt = null;
            document.getElementById('installBtn').style.display = 'none';
        });
    }
});

// Push уведомления
document.getElementById('notifyBtn').addEventListener('click', async function() {
    if ('Notification' in window) {
        const permission = await Notification.requestPermission();
        
        if (permission === 'granted') {
            new Notification('PWA уведомление!', {
                body: 'Уведомления успешно включены',
                icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">📱</text></svg>',
                badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">🔔</text></svg>'
            });
            
            this.textContent = '✅ Уведомления включены';
            this.disabled = true;
        }
    }
});

// Тест офлайн режима
document.getElementById('offlineBtn').addEventListener('click', function() {
    if (isOnline) {
        simulateOffline();
    } else {
        location.reload();
    }
});

function simulateOffline() {
    // Симуляция офлайн режима
    isOnline = false;
    updateStatus();
    
    document.getElementById('offlineBtn').textContent = '🔄 Вернуться онлайн';
    
    // Показываем кэшированное сообщение
    alert('Приложение работает в офлайн режиме!\\nБлагодаря Service Worker вы можете продолжать использовать приложение.');
}

// Онлайн/офлайн статус
function updateStatus() {
    const statusEl = document.getElementById('status');
    
    if (isOnline) {
        statusEl.textContent = '🟢 Онлайн';
        statusEl.classList.remove('offline');
    } else {
        statusEl.textContent = '🔴 Офлайн';
        statusEl.classList.add('offline');
    }
}

// События онлайн/офлайн
window.addEventListener('online', function() {
    isOnline = true;
    updateStatus();
});

window.addEventListener('offline', function() {
    isOnline = false;
    updateStatus();
});

// Инициализация
updateStatus();

// Touch события для улучшенного мобильного опыта
let touchStartY = 0;
let touchEndY = 0;

document.addEventListener('touchstart', function(e) {
    touchStartY = e.changedTouches[0].screenY;
});

document.addEventListener('touchend', function(e) {
    touchEndY = e.changedTouches[0].screenY;
    handleSwipe();
});

function handleSwipe() {
    const swipeDistance = touchEndY - touchStartY;
    
    if (Math.abs(swipeDistance) > 50) {
        if (swipeDistance > 0) {
            // Свайп вниз - можно добавить функциональность
            console.log('Свайп вниз');
        } else {
            // Свайп вверх - можно добавить функциональность
            console.log('Свайп вверх');
        }
    }
}

// Создание манифеста
const manifestContent = {
    "name": "Мобильное PWA",
    "short_name": "PWA",
    "description": "Прогрессивное веб-приложение",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#667eea",
    "theme_color": "#667eea",
    "icons": [
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📱</text></svg>",
            "sizes": "192x192",
            "type": "image/svg+xml"
        },
        {
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📱</text></svg>",
            "sizes": "512x512",
            "type": "image/svg+xml"
        }
    ]
};

// Service Worker содержимое
const swContent = `
const CACHE_NAME = 'pwa-cache-v1';
const urlsToCache = [
    '/',
    '/styles.css',
    '/script.js'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            }
        )
    );
});
`;

// Динамическое создание файлов
if ('serviceWorker' in navigator) {
    // Создаем service worker
    const swBlob = new Blob([swContent], { type: 'application/javascript' });
    const swUrl = URL.createObjectURL(swBlob);
    
    // Создаем манифест
    const manifestBlob = new Blob([JSON.stringify(manifestContent, null, 2)], { type: 'application/json' });
    const manifestUrl = URL.createObjectURL(manifestBlob);
    
    // Добавляем ссылку на манифест в head
    const link = document.createElement('link');
    link.rel = 'manifest';
    link.href = manifestUrl;
    document.head.appendChild(link);
}'''
    
    def get_templates_list(self) -> List[str]:
        """Получить список доступных шаблонов"""
        return list(self.templates.keys())
    
    def get_template_by_features(self, features: List[str]) -> Dict[str, Any]:
        """Получить шаблон на основе функций"""
        template_type = self.get_best_template(features, "")
        return self.get_template(template_type)