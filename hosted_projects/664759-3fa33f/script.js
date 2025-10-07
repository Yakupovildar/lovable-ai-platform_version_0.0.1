// Глобальные переменры
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
        personality: 'дерзкий, инновационный, прямолинейный, амбициозный',
        voice: 'ru-RU',
        color: '#ff6b35'
    },
    jobs: {
        name: 'Стив Джобс',
        description: 'Легендарный основатель Apple, революционер технологий',
        personality: 'перфекционист, креативный, требовательный, харизматичный',
        voice: 'en-US',
        color: '#007aff'
    },
    gates: {
        name: 'Билл Гейтс',
        description: 'Основатель Microsoft, филантроп и визионер',
        personality: 'аналитичный, стратегический, гуманный, дальновидный',
        voice: 'en-US',
        color: '#00a1f1'
    },
    bezos: {
        name: 'Джефф Безос',
        description: 'Основатель Amazon, пионер электронной коммерции',
        personality: 'целеустремленный, клиентоориентированный, долгосрочный',
        voice: 'en-US',
        color: '#ff9900'
    },
    buffett: {
        name: 'Уоррен Баффет',
        description: 'Легендарный инвестор, оракул из Омахи',
        personality: 'мудрый, терпеливый, простой, ценностно-ориентированный',
        voice: 'en-US',
        color: '#2e8b57'
    }
};

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupVoiceSupport();
    setupEventListeners();
    createAvatar();
});

// Основная инициализация
function initializeApp() {
    console.log('🚀 Инициализация AI Наставника 3D...');
    
    // Проверка поддержки WebGL
    if (!isWebGLSupported()) {
        showError('WebGL не поддерживается в вашем браузере');
        return;
    }
    
    // Инициализация 3D сцены
    init3DScene();
    
    // Загрузка истории разговоров
    loadConversationHistory();
    
    console.log('✅ Приложение инициализировано');
}

// Проверка поддержки WebGL
function isWebGLSupported() {
    try {
        const canvas = document.createElement('canvas');
        return !!(window.WebGLRenderingContext && canvas.getContext('webgl'));
    } catch (e) {
        return false;
    }
}

// Инициализация 3D сцены
function init3DScene() {
    const container = document.getElementById('avatar3d');
    
    // Создание сцены
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x1a1a2e);
    
    // Настройка камеры
    camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.z = 5;
    
    // Создание рендерера
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    
    // Очищение контейнера и добавление рендерера
    container.innerHTML = '';
    container.appendChild(renderer.domElement);
    
    // Добавление освещения
    const ambientLight = new THREE.AmbientLight(0x404040, 0.4);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(10, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    
    // Запуск анимации
    animate();
}

// Создание 3D аватара
function createAvatar() {
    const mentor = mentors[currentMentor];
    
    // Удаление предыдущего аватара
    if (currentAvatar) {
        scene.remove(currentAvatar);
    }
    
    // Создание группы для аватара
    currentAvatar = new THREE.Group();
    
    // Голова (сфера)
    const headGeometry = new THREE.SphereGeometry(1, 32, 32);
    const headMaterial = new THREE.MeshPhongMaterial({ 
        color: mentor.color,
        shininess: 100,
        transparent: true,
        opacity: 0.9
    });
    const head = new THREE.Mesh(headGeometry, headMaterial);
    head.position.y = 1.5;
    head.castShadow = true;
    currentAvatar.add(head);
    
    // Тело (цилиндр)
    const bodyGeometry = new THREE.CylinderGeometry(0.6, 0.8, 2, 8);
    const bodyMaterial = new THREE.MeshPhongMaterial({ 
        color: new THREE.Color(mentor.color).multiplyScalar(0.7)
    });
    const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
    body.castShadow = true;
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
    
    // Зрачки
    const pupilGeometry = new THREE.SphereGeometry(0.05, 8, 8);
    const pupilMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
    
    const leftPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    leftPupil.position.set(-0.3, 1.7, 0.85);
    currentAvatar.add(leftPupil);
    
    const rightPupil = new THREE.Mesh(pupilGeometry, pupilMaterial);
    rightPupil.position.set(0.3, 1.7, 0.85);
    currentAvatar.add(rightPupil);
    
    // Добавление аватара в сцену
    scene.add(currentAvatar);
    
    // Анимация появления
    currentAvatar.scale.set(0, 0, 0);
    animateAvatarAppearance();
    
    // Обновление информации о наставнике
    updateMentorInfo();
}

// Анимация появления аватара
function animateAvatarAppearance() {
    const startTime = Date.now();
    const duration = 1000;
    
    function animate() {
        const elapsed = Date.now() - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing функция
        const eased = 1 - Math.pow(1 - progress, 3);
        
        currentAvatar.scale.set(eased, eased, eased);
        currentAvatar.rotation.y = (1 - eased) * Math.PI * 2;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    animate();
}

// Анимация разговора аватара
function animateSpeaking() {
    if (!currentAvatar) return;
    
    const head = currentAvatar.children[0];
    const originalScale = { x: 1, y: 1, z: 1 };
    
    // Анимация качания головы
    const animation = () => {
        const time = Date.now() * 0.01;
        head.rotation.x = Math.sin(time) * 0.1;
        head.rotation.z = Math.sin(time * 0.7) * 0.05;
        
        // Легкое увеличение при разговоре
        const scale = 1 + Math.sin(time * 2) * 0.02;
        head.scale.set(scale, scale, scale);
    };
    
    return animation;
}

// Цикл анимации
function animate() {
    requestAnimationFrame(animate);
    
    if (currentAvatar) {
        // Постоянное легкое покачивание
        const time = Date.now() * 0.001;
        currentAvatar.rotation.y += 0.005;
        currentAvatar.position.y = Math.sin(time * 2) * 0.1;
    }
    
    renderer.render(scene, camera);
}

// Настройка голосовых возможностей
function setupVoiceSupport() {
    // Инициализация Web Speech API
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
            console.error('Speech recognition error:', event.error);
            showNotification('Ошибка распознавания речи', 'error');
            isListening = false;
            updateVoiceButton();
        };
        
        recognition.onend = function() {
            isListening = false;
            updateVoiceButton();
        };
    }
    
    // Получение доступных голосов
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = function() {
            voices = speechSynthesis.getVoices();
        };
        voices = speechSynthesis.getVoices();
    }
}

// Настройка обработчиков событий
function setupEventListeners() {
    // Смена наставника
    document.getElementById('mentorSelect').addEventListener('change', function(e) {
        currentMentor = e.target.value;
        createAvatar();
    });
    
    // Отправка сообщения
    document.getElementById('sendBtn').addEventListener('click', sendMessage);
    document.getElementById('userInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Добавление кнопки голосового ввода
    addVoiceButton();
    
    // Обработка изменения размера окна
    window.addEventListener('resize', onWindowResize);
}

// Добавление кнопки голосового ввода
function addVoiceButton() {
    const inputContainer = document.querySelector('.chat-input-container');
    
    const voiceBtn = document.createElement('button');
    voiceBtn.id = 'voiceBtn';
    voiceBtn.className = 'voice-btn';
    voiceBtn.innerHTML = '🎤';
    voiceBtn.title = 'Голосовой ввод';
    voiceBtn.addEventListener('click', toggleVoiceInput);
    
    inputContainer.appendChild(voiceBtn);
}

// Переключение голосового ввода
function toggleVoiceInput() {
    if (!recognition) {
        showNotification('Голосовой ввод не поддерживается', 'error');
        return;
    }
    
    if (isListening) {
        recognition.stop();
        isListening = false;
    } else {
        recognition.start();
        isListening = true;
        showNotification('Говорите...', 'info');
    }
    
    updateVoiceButton();
}

// Обновление кнопки голосового ввода
function updateVoiceButton() {
    const voiceBtn = document.getElementById('voiceBtn');
    if (voiceBtn) {
        voiceBtn.innerHTML = isListening ? '⏹️' : '🎤';
        voiceBtn.classList.toggle('listening', isListening);
    }
}

// Отправка сообщения
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Добавление сообщения пользователя
    addMessage(message, 'user');
    input.value = '';
    
    // Показ индикатора загрузки
    showTypingIndicator();
    
    try {
        // Отправка запроса к API наставника  
        const response = await fetch('/api/mentor-chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                mentor: currentMentor,
                personality: mentors[currentMentor].personality,
                history: conversationHistory.slice(-10) // Последние 10 сообщений
            })
        });
        
        const data = await response.json();
        
        if (data.response) {
            // Удаление индикатора загрузки
            removeTypingIndicator();
            
            // Добавление ответа AI
            addMessage(data.response, 'ai');
            
            // Озвучивание ответа
            speakText(data.response);
            
            // Анимация говорящего аватара
            const speakingAnimation = animateSpeaking();
            const speakingInterval = setInterval(speakingAnimation, 50);
            
            setTimeout(() => {
                clearInterval(speakingInterval);
            }, 3000);
            
        } else {
            throw new Error('Нет ответа от сервера');
        }
        
    } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
        removeTypingIndicator();
        addMessage('Извините, произошла ошибка. Попробуйте еще раз.', 'ai');
        showNotification('Ошибка связи с сервером', 'error');
    }
}

// Добавление сообщения в чат
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
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-content">
                <p>${text}</p>
                <div class="message-time">${new Date().toLocaleTimeString()}</div>
            </div>
            <div class="message-avatar">👤</div>
        `;
    }
    
    messagesContainer.appendChild(messageDiv);
    
    // Сохранение в историю
    conversationHistory.push({ sender, text, timestamp: new Date().toISOString() });
    saveConversationHistory();
    
    // Прокрутка вниз
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Анимация появления
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    
    requestAnimationFrame(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    });
}

// Показ индикатора печати
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">🤖</div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    messagesContainer.appendChild(typingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Удаление индикатора печати
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Озвучивание текста
function speakText(text) {
    if (!('speechSynthesis' in window)) return;
    
    // Остановка предыдущего озвучивания
    speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Настройка голоса
    const mentor = mentors[currentMentor];
    const voice = voices.find(v => v.lang.includes(mentor.voice)) || voices[0];
    if (voice) {
        utterance.voice = voice;
    }
    
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 0.8;
    
    // Анимация во время озвучивания
    utterance.onstart = function() {
        if (currentAvatar) {
            currentAvatar.userData.speaking = true;
        }
    };
    
    utterance.onend = function() {
        if (currentAvatar) {
            currentAvatar.userData.speaking = false;
        }
    };
    
    speechSynthesis.speak(utterance);
}

// Обновление информации о наставнике
function updateMentorInfo() {
    const mentor = mentors[currentMentor];
    
    document.getElementById('mentorName').textContent = mentor.name;
    document.getElementById('mentorDescription').textContent = mentor.description;
    
    // Обновление цветовой схемы
    document.documentElement.style.setProperty('--mentor-color', mentor.color);
}

// Сохранение истории разговоров
function saveConversationHistory() {
    try {
        localStorage.setItem('ai_mentor_history', JSON.stringify(conversationHistory));
    } catch (error) {
        console.error('Ошибка сохранения истории:', error);
    }
}

// Загрузка истории разговоров
function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('ai_mentor_history');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            
            // Восстановление последних 5 сообщений
            const recentMessages = conversationHistory.slice(-5);
            const messagesContainer = document.getElementById('chatMessages');
            
            // Очистка начального сообщения
            messagesContainer.innerHTML = '';
            
            recentMessages.forEach(msg => {
                addMessage(msg.text, msg.sender);
            });
            
            if (recentMessages.length === 0) {
                // Добавление приветственного сообщения
                addMessage('Привет! Я готов поделиться опытом и знаниями. О чем хотите поговорить?', 'ai');
            }
        }
    } catch (error) {
        console.error('Ошибка загрузки истории:', error);
    }
}

// Обработка изменения размера окна
function onWindowResize() {
    const container = document.getElementById('avatar3d');
    if (container && camera && renderer) {
        camera.aspect = container.clientWidth / container.clientHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(container.clientWidth, container.clientHeight);
    }
}

// Показ уведомлений
function showNotification(message, type = 'info') {
    // Создание контейнера для уведомлений, если не существует
    let notificationContainer = document.getElementById('notifications');
    if (!notificationContainer) {
        notificationContainer = document.createElement('div');
        notificationContainer.id = 'notifications';
        notificationContainer.className = 'notifications-container';
        document.body.appendChild(notificationContainer);
    }
    
    // Создание уведомления
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notificationContainer.appendChild(notification);
    
    // Анимация появления
    requestAnimationFrame(() => {
        notification.classList.add('show');
    });
    
    // Автоматическое удаление
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Показ ошибки
function showError(message) {
    const container = document.getElementById('avatar3d');
    container.innerHTML = `
        <div class="error-message">
            <h3>❌ Ошибка</h3>
            <p>${message}</p>
            <button onclick="location.reload()">Перезагрузить</button>
        </div>
    `;
}

// Экспорт функций для глобального использования
window.sendMessage = sendMessage;
window.toggleVoiceInput = toggleVoiceInput;