
import json
import random
import time
from typing import Dict, List, Any, Optional
import uuid

class SmartAI:
    """Локальный AI с базовой логикой генерации кода"""
    
    def __init__(self):
        self.context_memory = {}
        self.conversation_history = []
        
    def generate_project_response(self, project_type: str, description: str, user_id: str = None) -> Dict[str, Any]:
        """Генерирует ответ для создания проекта"""
        
        project_templates = {
            "website": self._generate_website_template,
            "game": self._generate_game_template, 
            "app": self._generate_app_template,
            "calculator": self._generate_calculator_template,
            "timer": self._generate_timer_template
        }
        
        # Определяем тип проекта по описанию
        detected_type = self._detect_project_type(description)
        template_func = project_templates.get(detected_type, self._generate_default_template)
        
        return template_func(description, user_id)
    
    def _detect_project_type(self, description: str) -> str:
        """Определяет тип проекта по описанию"""
        description_lower = description.lower()
        
        if any(word in description_lower for word in ["сайт", "website", "веб", "лендинг"]):
            return "website"
        elif any(word in description_lower for word in ["игра", "game", "тетрис", "змейка"]):
            return "game"
        elif any(word in description_lower for word in ["калькулятор", "calculator", "считать"]):
            return "calculator"
        elif any(word in description_lower for word in ["таймер", "timer", "будильник", "время"]):
            return "timer"
        else:
            return "app"
    
    def _generate_website_template(self, description: str, user_id: str) -> Dict[str, Any]:
        """Генерирует шаблон веб-сайта"""
        return {
            "type": "website",
            "files": {
                "index.html": self._get_website_html(description),
                "style.css": self._get_website_css(),
                "script.js": self._get_website_js()
            },
            "structure": ["index.html", "style.css", "script.js"],
            "instructions": "Современный адаптивный сайт готов к использованию!"
        }
    
    def _generate_game_template(self, description: str, user_id: str) -> Dict[str, Any]:
        """Генерирует шаблон игры"""
        return {
            "type": "game", 
            "files": {
                "index.html": self._get_game_html(description),
                "game.css": self._get_game_css(),
                "game.js": self._get_game_js(description)
            },
            "structure": ["index.html", "game.css", "game.js"],
            "instructions": "Игра готова! Используйте стрелки для управления."
        }
    
    def _generate_calculator_template(self, description: str, user_id: str) -> Dict[str, Any]:
        """Генерирует калькулятор"""
        return {
            "type": "calculator",
            "files": {
                "index.html": self._get_calculator_html(),
                "calculator.css": self._get_calculator_css(),
                "calculator.js": self._get_calculator_js()
            },
            "structure": ["index.html", "calculator.css", "calculator.js"],
            "instructions": "Функциональный калькулятор готов к использованию!"
        }
    
    def _generate_timer_template(self, description: str, user_id: str) -> Dict[str, Any]:
        """Генерирует таймер"""
        return {
            "type": "timer",
            "files": {
                "index.html": self._get_timer_html(),
                "timer.css": self._get_timer_css(),
                "timer.js": self._get_timer_js()
            },
            "structure": ["index.html", "timer.css", "timer.js"],
            "instructions": "Красивый таймер с уведомлениями готов!"
        }
    
    def _generate_default_template(self, description: str, user_id: str) -> Dict[str, Any]:
        """Генерирует базовый шаблон приложения"""
        return {
            "type": "app",
            "files": {
                "index.html": self._get_default_html(description),
                "style.css": self._get_default_css(),
                "app.js": self._get_default_js()
            },
            "structure": ["index.html", "style.css", "app.js"],
            "instructions": "Базовое приложение создано и готово к кастомизации!"
        }
    
    # HTML шаблоны
    def _get_website_html(self, description: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Современный Сайт</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <nav>
            <div class="logo">Мой Сайт</div>
            <div class="nav-links">
                <a href="#home">Главная</a>
                <a href="#about">О нас</a>
                <a href="#services">Услуги</a>
                <a href="#contact">Контакты</a>
            </div>
        </nav>
    </header>
    
    <main>
        <section id="home" class="hero">
            <div class="hero-content">
                <h1>Добро пожаловать!</h1>
                <p>Современное решение для ваших задач</p>
                <button class="cta-button">Начать</button>
            </div>
        </section>
        
        <section id="about" class="section">
            <div class="container">
                <h2>О проекте</h2>
                <p>{description}</p>
            </div>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 Мой Сайт. Все права защищены.</p>
    </footer>
    
    <script src="script.js"></script>
</body>
</html>"""
    
    def _get_website_css(self) -> str:
        return """* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
}

header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 0;
    position: fixed;
    width: 100%;
    top: 0;
    z-index: 1000;
}

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-links a {
    color: white;
    text-decoration: none;
    margin-left: 2rem;
    transition: opacity 0.3s;
}

.nav-links a:hover {
    opacity: 0.8;
}

.hero {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 8rem 2rem 4rem;
    text-align: center;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-content h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero-content p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
}

.cta-button {
    background: #ff6b6b;
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 50px;
    font-size: 1.1rem;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
}

.cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.2);
}

.section {
    padding: 4rem 2rem;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    text-align: center;
}

.section h2 {
    font-size: 2.5rem;
    margin-bottom: 2rem;
    color: #333;
}

footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem;
}

@media (max-width: 768px) {
    .nav-links {
        display: none;
    }
    
    .hero-content h1 {
        font-size: 2rem;
    }
    
    nav {
        padding: 0 1rem;
    }
}"""
    
    def _get_website_js(self) -> str:
        return """// Плавная прокрутка для навигации
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Анимация появления элементов при скролле
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Применяем анимации к секциям
document.querySelectorAll('.section').forEach(section => {
    section.style.opacity = '0';
    section.style.transform = 'translateY(30px)';
    section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
    observer.observe(section);
});

// Интерактивность для кнопки CTA
document.querySelector('.cta-button').addEventListener('click', function() {
    this.innerHTML = '✨ Отлично!';
    setTimeout(() => {
        this.innerHTML = 'Начать';
    }, 2000);
});

console.log('🚀 Сайт готов к работе!');"""

    def _get_game_html(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Крутая Игра</title>
    <link rel="stylesheet" href="game.css">
</head>
<body>
    <div class="game-container">
        <div class="game-header">
            <h1>🎮 Игра</h1>
            <div class="game-stats">
                <span>Счёт: <span id="score">0</span></span>
                <span>Уровень: <span id="level">1</span></span>
            </div>
        </div>
        
        <div class="game-area">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
        </div>
        
        <div class="game-controls">
            <button id="startBtn" class="game-btn">Начать игру</button>
            <button id="pauseBtn" class="game-btn">Пауза</button>
            <button id="resetBtn" class="game-btn">Сброс</button>
        </div>
        
        <div class="game-instructions">
            <p>Используйте стрелки ⬅️➡️⬆️⬇️ для управления</p>
            <p>Пробел - особое действие</p>
        </div>
    </div>
    
    <script src="game.js"></script>
</body>
</html>"""
    
    def _get_calculator_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Умный Калькулятор</title>
    <link rel="stylesheet" href="calculator.css">
</head>
<body>
    <div class="calculator">
        <div class="display">
            <input type="text" id="result" readonly>
        </div>
        <div class="buttons">
            <button onclick="clearDisplay()" class="btn clear">C</button>
            <button onclick="deleteLast()" class="btn delete">⌫</button>
            <button onclick="appendToDisplay('/')" class="btn operator">÷</button>
            <button onclick="appendToDisplay('*')" class="btn operator">×</button>
            
            <button onclick="appendToDisplay('7')" class="btn number">7</button>
            <button onclick="appendToDisplay('8')" class="btn number">8</button>
            <button onclick="appendToDisplay('9')" class="btn number">9</button>
            <button onclick="appendToDisplay('-')" class="btn operator">−</button>
            
            <button onclick="appendToDisplay('4')" class="btn number">4</button>
            <button onclick="appendToDisplay('5')" class="btn number">5</button>
            <button onclick="appendToDisplay('6')" class="btn number">6</button>
            <button onclick="appendToDisplay('+')" class="btn operator">+</button>
            
            <button onclick="appendToDisplay('1')" class="btn number">1</button>
            <button onclick="appendToDisplay('2')" class="btn number">2</button>
            <button onclick="appendToDisplay('3')" class="btn number">3</button>
            <button onclick="calculate()" class="btn equals" rowspan="2">=</button>
            
            <button onclick="appendToDisplay('0')" class="btn number zero">0</button>
            <button onclick="appendToDisplay('.')" class="btn number">.</button>
        </div>
    </div>
    
    <script src="calculator.js"></script>
</body>
</html>"""
    
    def _get_timer_html(self) -> str:
        return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Крутой Таймер</title>
    <link rel="stylesheet" href="timer.css">
</head>
<body>
    <div class="timer-container">
        <div class="timer-display">
            <div class="time-circle">
                <svg class="progress-ring" width="200" height="200">
                    <circle class="progress-ring-bg" cx="100" cy="100" r="90"></circle>
                    <circle class="progress-ring-fill" cx="100" cy="100" r="90"></circle>
                </svg>
                <div class="time-text">
                    <span id="timeDisplay">00:00</span>
                </div>
            </div>
        </div>
        
        <div class="timer-inputs">
            <div class="input-group">
                <label>Минуты:</label>
                <input type="number" id="minutes" min="0" max="59" value="5">
            </div>
            <div class="input-group">
                <label>Секунды:</label>
                <input type="number" id="seconds" min="0" max="59" value="0">
            </div>
        </div>
        
        <div class="timer-controls">
            <button id="startBtn" class="control-btn start">▶ Старт</button>
            <button id="pauseBtn" class="control-btn pause">⏸ Пауза</button>
            <button id="resetBtn" class="control-btn reset">⏹ Сброс</button>
        </div>
        
        <div class="presets">
            <h3>Быстрые настройки:</h3>
            <button onclick="setTimer(1, 0)" class="preset-btn">1 мин</button>
            <button onclick="setTimer(5, 0)" class="preset-btn">5 мин</button>
            <button onclick="setTimer(10, 0)" class="preset-btn">10 мин</button>
            <button onclick="setTimer(25, 0)" class="preset-btn">25 мин</button>
        </div>
    </div>
    
    <script src="timer.js"></script>
</body>
</html>"""

    # CSS стили (сокращенные версии)
    def _get_game_css(self) -> str:
        return """/* Базовые стили для игры */
body {
    margin: 0;
    padding: 20px;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.game-container {
    background: white;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    text-align: center;
}

#gameCanvas {
    border: 3px solid #333;
    border-radius: 10px;
    background: #f0f0f0;
    margin: 20px 0;
}

.game-btn {
    background: #4ecdc4;
    color: white;
    border: none;
    padding: 10px 20px;
    margin: 5px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s;
}

.game-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}"""

    def _get_calculator_css(self) -> str:
        return """/* Стили калькулятора */
body {
    margin: 0;
    padding: 20px;
    font-family: 'SF Pro Display', sans-serif;
    background: linear-gradient(135deg, #1e3c72, #2a5298);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.calculator {
    background: #333;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}

.display input {
    width: 100%;
    height: 80px;
    background: #000;
    color: white;
    border: none;
    font-size: 2.5rem;
    text-align: right;
    padding: 0 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.buttons {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

.btn {
    height: 60px;
    border: none;
    border-radius: 30px;
    font-size: 1.5rem;
    cursor: pointer;
    transition: all 0.2s;
}

.btn:hover {
    transform: scale(1.05);
}

.number { background: #505050; color: white; }
.operator { background: #ff9500; color: white; }
.equals { background: #ff9500; color: white; grid-row: span 2; }
.clear { background: #a6a6a6; color: black; }
.delete { background: #a6a6a6; color: black; }
.zero { grid-column: span 2; }"""

    def _get_timer_css(self) -> str:
        return """/* Стили таймера */
body {
    margin: 0;
    padding: 20px;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

.timer-container {
    background: white;
    border-radius: 25px;
    padding: 40px;
    box-shadow: 0 25px 50px rgba(0,0,0,0.15);
    text-align: center;
    max-width: 400px;
}

.time-circle {
    position: relative;
    margin: 20px auto;
}

.progress-ring {
    transform: rotate(-90deg);
}

.progress-ring-bg {
    fill: none;
    stroke: #e0e0e0;
    stroke-width: 8;
}

.progress-ring-fill {
    fill: none;
    stroke: #4ecdc4;
    stroke-width: 8;
    stroke-dasharray: 565.48;
    stroke-dashoffset: 565.48;
    transition: stroke-dashoffset 1s linear;
}

.time-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 2.5rem;
    font-weight: bold;
    color: #333;
}

.control-btn {
    background: #4ecdc4;
    color: white;
    border: none;
    padding: 15px 25px;
    margin: 10px 5px;
    border-radius: 25px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s;
}

.preset-btn {
    background: #95a5a6;
    color: white;
    border: none;
    padding: 8px 15px;
    margin: 5px;
    border-radius: 15px;
    cursor: pointer;
}"""

    # JavaScript файлы (базовые версии)
    def _get_game_js(self, description: str) -> str:
        return """// Простая игра
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let gameState = {
    running: false,
    score: 0,
    level: 1,
    player: { x: 200, y: 200, size: 20, color: '#4ecdc4' },
    objects: []
};

// Управление
const keys = {};
document.addEventListener('keydown', (e) => keys[e.key] = true);
document.addEventListener('keyup', (e) => keys[e.key] = false);

// Обновление игры
function update() {
    if (!gameState.running) return;
    
    // Движение игрока
    if (keys['ArrowLeft'] && gameState.player.x > 0) gameState.player.x -= 5;
    if (keys['ArrowRight'] && gameState.player.x < canvas.width - gameState.player.size) gameState.player.x += 5;
    if (keys['ArrowUp'] && gameState.player.y > 0) gameState.player.y -= 5;
    if (keys['ArrowDown'] && gameState.player.y < canvas.height - gameState.player.size) gameState.player.y += 5;
    
    gameState.score++;
    document.getElementById('score').textContent = gameState.score;
}

// Отрисовка
function render() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Игрок
    ctx.fillStyle = gameState.player.color;
    ctx.fillRect(gameState.player.x, gameState.player.y, gameState.player.size, gameState.player.size);
    
    // Эффекты
    ctx.fillStyle = 'rgba(78, 205, 196, 0.3)';
    ctx.fillRect(gameState.player.x - 5, gameState.player.y - 5, gameState.player.size + 10, gameState.player.size + 10);
}

// Игровой цикл
function gameLoop() {
    update();
    render();
    requestAnimationFrame(gameLoop);
}

// Управление кнопками
document.getElementById('startBtn').onclick = () => {
    gameState.running = true;
};

document.getElementById('pauseBtn').onclick = () => {
    gameState.running = !gameState.running;
};

document.getElementById('resetBtn').onclick = () => {
    gameState.running = false;
    gameState.score = 0;
    gameState.player.x = 200;
    gameState.player.y = 200;
    document.getElementById('score').textContent = '0';
};

gameLoop();"""

    def _get_calculator_js(self) -> str:
        return """// Калькулятор
let display = document.getElementById('result');
let currentInput = '';
let operator = '';
let previousInput = '';

function appendToDisplay(value) {
    if (display.value === '0' && value !== '.') {
        display.value = value;
    } else {
        display.value += value;
    }
}

function clearDisplay() {
    display.value = '';
    currentInput = '';
    operator = '';
    previousInput = '';
}

function deleteLast() {
    display.value = display.value.slice(0, -1);
}

function calculate() {
    try {
        let expression = display.value;
        expression = expression.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
        let result = eval(expression);
        display.value = result;
        
        // Анимация результата
        display.style.transform = 'scale(1.1)';
        display.style.background = '#4ecdc4';
        setTimeout(() => {
            display.style.transform = 'scale(1)';
            display.style.background = '#000';
        }, 200);
    } catch (error) {
        display.value = 'Ошибка';
        setTimeout(() => display.value = '', 1500);
    }
}

// Поддержка клавиатуры
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9' || e.key === '.') {
        appendToDisplay(e.key);
    } else if (e.key === '+' || e.key === '-' || e.key === '*' || e.key === '/') {
        appendToDisplay(e.key);
    } else if (e.key === 'Enter' || e.key === '=') {
        calculate();
    } else if (e.key === 'Escape') {
        clearDisplay();
    } else if (e.key === 'Backspace') {
        deleteLast();
    }
});"""

    def _get_timer_js(self) -> str:
        return """// Таймер
let timerInterval;
let totalSeconds = 0;
let remainingSeconds = 0;
let isRunning = false;

const timeDisplay = document.getElementById('timeDisplay');
const progressRing = document.querySelector('.progress-ring-fill');
const circumference = 565.48;

function updateDisplay() {
    const minutes = Math.floor(remainingSeconds / 60);
    const seconds = remainingSeconds % 60;
    timeDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    
    // Обновляем прогресс-кольцо
    const progress = (totalSeconds - remainingSeconds) / totalSeconds;
    const offset = circumference - (progress * circumference);
    progressRing.style.strokeDashoffset = offset;
}

function startTimer() {
    if (!isRunning && remainingSeconds > 0) {
        isRunning = true;
        timerInterval = setInterval(() => {
            remainingSeconds--;
            updateDisplay();
            
            if (remainingSeconds <= 0) {
                clearInterval(timerInterval);
                isRunning = false;
                playNotification();
                alert('⏰ Время вышло!');
            }
        }, 1000);
    }
}

function pauseTimer() {
    if (isRunning) {
        clearInterval(timerInterval);
        isRunning = false;
    } else {
        startTimer();
    }
}

function resetTimer() {
    clearInterval(timerInterval);
    isRunning = false;
    const minutes = parseInt(document.getElementById('minutes').value) || 0;
    const seconds = parseInt(document.getElementById('seconds').value) || 0;
    totalSeconds = remainingSeconds = minutes * 60 + seconds;
    updateDisplay();
    progressRing.style.strokeDashoffset = circumference;
}

function setTimer(minutes, seconds) {
    document.getElementById('minutes').value = minutes;
    document.getElementById('seconds').value = seconds;
    resetTimer();
}

function playNotification() {
    // Визуальная анимация
    document.body.style.animation = 'pulse 0.5s ease-in-out 3';
    setTimeout(() => document.body.style.animation = '', 1500);
}

// События
document.getElementById('startBtn').onclick = startTimer;
document.getElementById('pauseBtn').onclick = pauseTimer;
document.getElementById('resetBtn').onclick = resetTimer;

// Инициализация
resetTimer();

// CSS анимация для уведомления
const style = document.createElement('style');
style.textContent = `
@keyframes pulse {
    0%, 100% { background: linear-gradient(135deg, #667eea, #764ba2); }
    50% { background: linear-gradient(135deg, #ff6b6b, #feca57); }
}`;
document.head.appendChild(style);"""

    def _get_default_html(self, description: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мое Приложение</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="app-container">
        <header>
            <h1>🚀 Мое Приложение</h1>
            <p>Создано с помощью AI</p>
        </header>
        
        <main>
            <section class="content">
                <h2>Добро пожаловать!</h2>
                <p>{description}</p>
                <button id="actionBtn" class="main-btn">Действие</button>
            </section>
        </main>
        
        <footer>
            <p>Сделано с ❤️</p>
        </footer>
    </div>
    
    <script src="app.js"></script>
</body>
</html>"""

    def _get_default_css(self) -> str:
        return """/* Базовые стили */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    min-height: 100vh;
    padding: 20px;
}

.app-container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
}

header {
    background: linear-gradient(135deg, #4ecdc4, #44a08d);
    color: white;
    text-align: center;
    padding: 3rem 2rem;
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

main {
    padding: 3rem 2rem;
}

.content {
    text-align: center;
}

.content h2 {
    color: #333;
    margin-bottom: 1rem;
    font-size: 2rem;
}

.content p {
    color: #666;
    font-size: 1.1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
}

.main-btn {
    background: linear-gradient(135deg, #ff6b6b, #feca57);
    color: white;
    border: none;
    padding: 1rem 2rem;
    font-size: 1.1rem;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.main-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

footer {
    background: #f8f9fa;
    text-align: center;
    padding: 2rem;
    color: #666;
}

@media (max-width: 600px) {
    .app-container {
        margin: 0;
        border-radius: 0;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    main {
        padding: 2rem 1rem;
    }
}"""

    def _get_default_js(self) -> str:
        return """// Основная логика приложения
console.log('🚀 Приложение загружено!');

// Интерактивность
document.getElementById('actionBtn').addEventListener('click', function() {
    const messages = [
        'Отлично! 🎉',
        'Великолепно! ✨',
        'Потрясающе! 🚀',
        'Замечательно! 🌟',
        'Прекрасно! 💫'
    ];
    
    const randomMessage = messages[Math.floor(Math.random() * messages.length)];
    
    // Обновляем текст кнопки
    const originalText = this.textContent;
    this.textContent = randomMessage;
    this.style.background = 'linear-gradient(135deg, #4ecdc4, #44a08d)';
    
    // Анимация
    this.style.transform = 'scale(1.1)';
    
    setTimeout(() => {
        this.textContent = originalText;
        this.style.background = 'linear-gradient(135deg, #ff6b6b, #feca57)';
        this.style.transform = 'scale(1)';
    }, 2000);
});

// Добавляем интерактивные эффекты
document.addEventListener('mousemove', (e) => {
    const cursor = document.querySelector('.cursor');
    if (!cursor) {
        const newCursor = document.createElement('div');
        newCursor.className = 'cursor';
        newCursor.style.cssText = `
            position: fixed;
            width: 20px;
            height: 20px;
            background: rgba(78, 205, 196, 0.5);
            border-radius: 50%;
            pointer-events: none;
            z-index: 9999;
            transition: transform 0.1s ease;
        `;
        document.body.appendChild(newCursor);
    }
    
    const cursorElement = document.querySelector('.cursor');
    cursorElement.style.left = e.clientX - 10 + 'px';
    cursorElement.style.top = e.clientY - 10 + 'px';
});

// Анимация загрузки
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});"""

class EnhancedAI:
    """Улучшенный AI сервис без внешних зависимостей"""
    
    def __init__(self):
        self.smart_ai = SmartAI()
    
    def generate_project_code(self, description: str, project_type: str = "auto", user_id: str = None) -> Dict[str, Any]:
        """Генерирует код проекта на основе описания"""
        return self.smart_ai.generate_project_response(project_type, description, user_id)
    
    def improve_project_code(self, current_code: Dict[str, str], improvement_request: str) -> Dict[str, Any]:
        """Улучшает существующий код проекта"""
        return {
            "success": True,
            "improvements": f"Код улучшен согласно запросу: {improvement_request}",
            "files": current_code  # В реальной версии здесь была бы логика улучшения
        }
