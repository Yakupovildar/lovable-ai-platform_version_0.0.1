from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import json
import zipfile
import tempfile
import shutil
from datetime import datetime
import uuid
from pathlib import Path
import subprocess
import threading
import queue
import time
import random
# Placeholder imports for missing modules
class SuperSmartAI:
    def generate_response(self, message):
        return {"type": "ai_response", "message": f"AI получил: {message}"}

class SmartNLP:
    def correct_and_normalize(self, text):
        return text.lower().strip()

class ProjectVersionControl:
    def get_next_version(self, project_type):
        return "1.0"
    def save_project_version(self, project_id, version, files, message):
        pass
    def get_project_versions(self, project_id):
        return []

class UserInteractionLogger:
    def log_event(self, event, data, session_id=None):
        print(f"LOG: {event} - {data}")
    def log_interaction(self, session_id, message, processed, msg_type):
        print(f"INTERACTION: {session_id} - {message}")
    def log_incoming_message(self, session_id, message):
        print(f"INCOMING: {session_id} - {message}")
    def log_ai_response(self, session_id, response):
        print(f"AI_RESPONSE: {session_id}")
    def log_error(self, event, data):
        print(f"ERROR: {event} - {data}")

class AdvancedProjectGenerator:
    def generate_project(self, project_type, description, project_name, user_preferences=None):
        return generator.generate_project(project_type, description, project_name)
    def add_feature(self, project_id, feature):
        return True

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def serve_frontend():
    """Serve main frontend page"""
    return send_file('../index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Backend is running"})

# Конфигурация
PROJECTS_DIR = "projects"
TEMP_DIR = "temp"
LOGS_DIR = "logs"
USER_DATA_DIR = "user_data"
MAX_PROJECTS_PER_USER = 10

# Создаём директории если их нет
os.makedirs(PROJECTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(USER_DATA_DIR, exist_ok=True)

# Очередь для обработки генерации проектов
project_queue = queue.Queue()

# Инициализация новых компонентов
ai_agent = SuperSmartAI()
nlp_processor = SmartNLP()
version_control = ProjectVersionControl()
interaction_logger = UserInteractionLogger()
advanced_generator = AdvancedProjectGenerator()

class ProjectGenerator:
    def __init__(self):
        self.templates = {
            "snake_game": {
                "files": {
                    "index.html": self.get_snake_html,
                    "styles.css": self.get_snake_css,
                    "script.js": self.get_snake_js,
                    "README.md": self.get_snake_readme
                }
            },
            "tetris_game": {
                "files": {
                    "index.html": self.get_tetris_html,
                    "styles.css": self.get_tetris_css,
                    "script.js": self.get_tetris_js,
                    "README.md": self.get_tetris_readme
                }
            },
            "todo_app": {
                "files": {
                    "index.html": self.get_todo_html,
                    "styles.css": self.get_todo_css,
                    "script.js": self.get_todo_js,
                    "README.md": self.get_todo_readme
                }
            },
            "weather_app": {
                "files": {
                    "index.html": self.get_weather_html,
                    "styles.css": self.get_weather_css,
                    "script.js": self.get_weather_js,
                    "README.md": self.get_weather_readme
                }
            }
        }

    def generate_project(self, project_type, description, project_name, style="modern"):
        """Генерирует проект на основе описания"""
        try:
            project_id = str(uuid.uuid4())
            project_path = os.path.join(PROJECTS_DIR, project_id)
            os.makedirs(project_path, exist_ok=True)

            template = self.templates.get(project_type, self.templates["snake_game"])

            for file_path, generator_func in template["files"].items():
                full_path = os.path.join(project_path, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                content = generator_func(project_name, description, style)
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Логирование создания проекта
            interaction_logger.log_event("project_creation", {
                "project_id": project_id,
                "project_type": project_type,
                "project_name": project_name,
                "description": description,
                "style": style
            })

            return {
                "success": True,
                "project_id": project_id,
                "project_name": project_name,
                "project_type": project_type,
                "files": list(template["files"].keys())
            }
        except Exception as e:
            interaction_logger.log_error("project_creation_failed", {"error": str(e)})
            return {
                "success": False,
                "error": str(e)
            }

    def get_snake_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="game-container">
        <div class="game-header">
            <h1>{project_name}</h1>
            <div class="game-info">
                <div class="score">Счёт: <span id="score">0</span></div>
                <div class="high-score">Рекорд: <span id="highScore">0</span></div>
            </div>
        </div>

        <div class="game-area">
            <canvas id="gameCanvas" width="400" height="400"></canvas>
            <div class="game-overlay" id="gameOverlay">
                <div class="start-screen">
                    <h2>🐍 Змейка</h2>
                    <p>Управление: стрелки или WASD</p>
                    <button id="startBtn" class="game-btn">Начать игру</button>
                </div>
            </div>
        </div>

        <div class="game-controls">
            <div class="mobile-controls">
                <button class="control-btn" data-direction="up">↑</button>
                <div class="control-row">
                    <button class="control-btn" data-direction="left">←</button>
                    <button class="control-btn" data-direction="down">↓</button>
                    <button class="control-btn" data-direction="right">→</button>
                </div>
            </div>
        </div>

        <div class="game-footer">
            <p>{description}</p>
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_snake_css(self, project_name, description, style):
        themes = {
            "modern": """
                --primary-color: #667eea;
                --secondary-color: #764ba2;
                --accent-color: #f093fb;
                --bg-color: #0f0f23;
                --text-color: #ffffff;
                --snake-color: #00ff88;
                --food-color: #ff6b6b;
            """,
            "retro": """
                --primary-color: #ff6b35;
                --secondary-color: #f7931e;
                --accent-color: #ffd23f;
                --bg-color: #1a1a1a;
                --text-color: #00ff00;
                --snake-color: #00ff00;
                --food-color: #ff0040;
            """,
            "neon": """
                --primary-color: #ff0080;
                --secondary-color: #8000ff;
                --accent-color: #00ff80;
                --bg-color: #000015;
                --text-color: #ffffff;
                --snake-color: #00ffff;
                --food-color: #ff0080;
            """
        }

        theme = themes.get(style, themes["modern"])

        return f"""* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    {theme}
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.game-container {{
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 500px;
    width: 100%;
}}

.game-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.game-info {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    font-size: 1.2rem;
    font-weight: 600;
}}

.game-area {{
    position: relative;
    margin: 2rem 0;
}}

#gameCanvas {{
    border: 3px solid var(--accent-color);
    border-radius: 15px;
    background: var(--bg-color);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}}

.game-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
}}

.start-screen {{
    text-align: center;
    color: white;
}}

.start-screen h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.game-btn {{
    background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
    border: none;
    color: white;
    padding: 1rem 2rem;
    border-radius: 25px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}}

.game-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}}

.mobile-controls {{
    margin-top: 2rem;
}}

.control-btn {{
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    font-size: 1.5rem;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.control-btn:hover {{
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}}

.control-row {{
    display: flex;
    justify-content: center;
    align-items: center;
}}

.game-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.8;
}}

.hidden {{
    display: none !important;
}}

@media (max-width: 600px) {{
    .game-container {{
        padding: 1rem;
        margin: 1rem;
    }}

    #gameCanvas {{
        width: 100%;
        height: auto;
        max-width: 350px;
    }}

    .game-header h1 {{
        font-size: 2rem;
    }}

    .game-info {{
        font-size: 1rem;
    }}
}}"""

    def get_snake_js(self, project_name, description, style):
        return """class SnakeGame {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.scoreElement = document.getElementById('score');
        this.highScoreElement = document.getElementById('highScore');
        this.overlay = document.getElementById('gameOverlay');
        this.startBtn = document.getElementById('startBtn');

        this.gridSize = 20;
        this.tileCount = this.canvas.width / this.gridSize;

        this.reset();
        this.setupControls();
        this.loadHighScore();
    }

    reset() {
        this.snake = [
            {x: 10, y: 10}
        ];
        this.food = this.generateFood();
        this.dx = 0;
        this.dy = 0;
        this.score = 0;
        this.gameRunning = false;
        this.updateScore();
    }

    generateFood() {
        return {
            x: Math.floor(Math.random() * this.tileCount),
            y: Math.floor(Math.random() * this.tileCount)
        };
    }

    setupControls() {
        this.startBtn.addEventListener('click', () => this.startGame());

        document.addEventListener('keydown', (e) => {
            if (!this.gameRunning) return;

            switch(e.key) {
                case 'ArrowUp':
                case 'w':
                case 'W':
                    if (this.dy !== 1) {
                        this.dx = 0;
                        this.dy = -1;
                    }
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    if (this.dy !== -1) {
                        this.dx = 0;
                        this.dy = 1;
                    }
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    if (this.dx !== 1) {
                        this.dx = -1;
                        this.dy = 0;
                    }
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    if (this.dx !== -1) {
                        this.dx = 1;
                        this.dy = 0;
                    }
                    break;
            }
        });

        document.querySelectorAll('.control-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                if (!this.gameRunning) return;

                const direction = btn.dataset.direction;
                switch(direction) {
                    case 'up':
                        if (this.dy !== 1) {
                            this.dx = 0;
                            this.dy = -1;
                        }
                        break;
                    case 'down':
                        if (this.dy !== -1) {
                            this.dx = 0;
                            this.dy = 1;
                        }
                        break;
                    case 'left':
                        if (this.dx !== 1) {
                            this.dx = -1;
                            this.dy = 0;
                        }
                        break;
                    case 'right':
                        if (this.dx !== -1) {
                            this.dx = 1;
                            this.dy = 0;
                        }
                        break;
                }
            });
        });
    }

    startGame() {
        this.reset();
        this.gameRunning = true;
        this.overlay.classList.add('hidden');
        this.dx = 1;
        this.dy = 0;
        this.gameLoop();
    }

    gameLoop() {
        if (!this.gameRunning) return;

        setTimeout(() => {
            this.clearCanvas();
            this.moveSnake();
            this.drawFood();
            this.drawSnake();

            if (this.checkGameOver()) {
                this.endGame();
                return;
            }

            this.gameLoop();
        }, 150);
    }

    clearCanvas() {
        this.ctx.fillStyle = 'rgba(15, 15, 35, 0.9)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }

    moveSnake() {
        const head = {x: this.snake[0].x + this.dx, y: this.snake[0].y + this.dy};

        if (head.x === this.food.x && head.y === this.food.y) {
            this.score += 10;
            this.updateScore();
            this.food = this.generateFood();
        } else {
            this.snake.pop();
        }

        this.snake.unshift(head);
    }

    drawSnake() {
        this.ctx.fillStyle = '#00ff88';
        this.ctx.shadowColor = '#00ff88';
        this.ctx.shadowBlur = 10;

        this.snake.forEach((segment, index) => {
            if (index === 0) {
                this.ctx.fillStyle = '#00ffaa';
            } else {
                this.ctx.fillStyle = '#00ff88';
            }

            this.ctx.fillRect(
                segment.x * this.gridSize + 2,
                segment.y * this.gridSize + 2,
                this.gridSize - 4,
                this.gridSize - 4
            );
        });

        this.ctx.shadowBlur = 0;
    }

    drawFood() {
        this.ctx.fillStyle = '#ff6b6b';
        this.ctx.shadowColor = '#ff6b6b';
        this.ctx.shadowBlur = 15;

        this.ctx.beginPath();
        this.ctx.arc(
            this.food.x * this.gridSize + this.gridSize / 2,
            this.food.y * this.gridSize + this.gridSize / 2,
            this.gridSize / 2 - 2,
            0,
            2 * Math.PI
        );
        this.ctx.fill();

        this.ctx.shadowBlur = 0;
    }

    checkGameOver() {
        const head = this.snake[0];

        if (head.x < 0 || head.x >= this.tileCount || head.y < 0 || head.y >= this.tileCount) {
            return true;
        }

        for (let i = 1; i < this.snake.length; i++) {
            if (head.x === this.snake[i].x && head.y === this.snake[i].y) {
                return true;
            }
        }

        return false;
    }

    endGame() {
        this.gameRunning = false;
        this.updateHighScore();

        this.overlay.innerHTML = `
            <div class="start-screen">
                <h2>🎮 Игра окончена!</h2>
                <p>Ваш счёт: ${this.score}</p>
                <p>Рекорд: ${this.getHighScore()}</p>
                <button id="restartBtn" class="game-btn">Играть снова</button>
            </div>
        `;

        this.overlay.classList.remove('hidden');

        document.getElementById('restartBtn').addEventListener('click', () => {
            this.startGame();
        });
    }

    updateScore() {
        this.scoreElement.textContent = this.score;
    }

    loadHighScore() {
        const highScore = localStorage.getItem('snakeHighScore') || 0;
        this.highScoreElement.textContent = highScore;
    }

    getHighScore() {
        return localStorage.getItem('snakeHighScore') || 0;
    }

    updateHighScore() {
        const currentHigh = parseInt(this.getHighScore());
        if (this.score > currentHigh) {
            localStorage.setItem('snakeHighScore', this.score);
            this.highScoreElement.textContent = this.score;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new SnakeGame();
});"""

    def get_snake_readme(self, project_name, description, style):
        return f"""# {project_name}

{description}

## 🎮 Игра "Змейка"

Классическая игра змейка с современным дизайном и адаптивным интерфейсом.

### Особенности:
- 🎨 Красивый современный дизайн
- 📱 Адаптивность для мобильных устройств
- 🎯 Система очков и рекордов
- ⌨️ Управление клавишами и сенсорными кнопками
- 💾 Сохранение лучшего результата

### Управление:
- **Клавиши:** Стрелки или WASD
- **Мобильные:** Сенсорные кнопки

### Технологии:
- HTML5 Canvas
- CSS3 с градиентами и анимациями
- Vanilla JavaScript ES6+

Создано с помощью Lovable AI"""

    def get_tetris_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="game-container">
        <div class="game-header">
            <h1>{project_name}</h1>
            <div class="game-info">
                <div class="score">Счёт: <span id="score">0</span></div>
                <div class="level">Уровень: <span id="level">1</span></div>
                <div class="lines">Линии: <span id="lines">0</span></div>
            </div>
        </div>

        <div class="game-area">
            <div class="next-piece">
                <h3>Следующая фигура</h3>
                <canvas id="nextCanvas" width="120" height="120"></canvas>
            </div>
            <canvas id="gameCanvas" width="300" height="600"></canvas>
            <div class="game-overlay" id="gameOverlay">
                <div class="start-screen">
                    <h2>🧩 Тетрис</h2>
                    <p>Управление: стрелки, пробел для поворота</p>
                    <button id="startBtn" class="game-btn">Начать игру</button>
                </div>
            </div>
        </div>

        <div class="game-controls">
            <div class="mobile-controls">
                <button class="control-btn" data-action="rotate">↻</button>
                <div class="control-row">
                    <button class="control-btn" data-action="left">←</button>
                    <button class="control-btn" data-action="down">↓</button>
                    <button class="control-btn" data-action="right">→</button>
                </div>
            </div>
        </div>

        <div class="game-footer">
            <p>{description}</p>
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_tetris_css(self, project_name, description, style):
        return f"""/* CSS для Тетриса */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

:root {{
    --primary-color: #4a148c; /* Purple */
    --secondary-color: #00bcd4; /* Cyan */
    --accent-color: #ffeb3b; /* Yellow */
    --bg-color: #121212; /* Dark background */
    --text-color: #ffffff;
    --block-colors: #FF0D72, #0DC2FF, #0DFF72, #F538FF, #FFFB0D, #FF8E0D, #AD1457; /* Random colors for blocks */
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.game-container {{
    background: rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    text-align: center;
    max-width: 600px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.game-header h1 {{
    font-size: 2.5rem;
    margin-bottom: 1rem;
    background: linear-gradient(45deg, var(--accent-color), var(--primary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

.game-info {{
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-bottom: 2rem;
    font-size: 1.1rem;
    font-weight: 600;
}}

.game-area {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 2rem;
}}

#gameCanvas {{
    border: 3px solid var(--accent-color);
    border-radius: 15px;
    background: var(--bg-color);
    box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.5);
}}

.next-piece {{
    text-align: center;
}}

#nextCanvas {{
    border: 2px solid var(--accent-color);
    background: var(--bg-color);
    border-radius: 10px;
    margin-top: 10px;
}}

.game-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 15px;
}}

.start-screen {{
    text-align: center;
    color: white;
}}

.start-screen h2 {{
    font-size: 2rem;
    margin-bottom: 1rem;
}}

.game-btn {{
    background: linear-gradient(45deg, var(--primary-color), var(--accent-color));
    border: none;
    color: white;
    padding: 1rem 2rem;
    border-radius: 25px;
    font-size: 1.1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}}

.game-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4);
}}

.mobile-controls {{
    margin-top: 2rem;
}}

.control-btn {{
    background: rgba(255, 255, 255, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 10px;
    font-size: 1.5rem;
    margin: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.control-btn:hover {{
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}}

.control-row {{
    display: flex;
    justify-content: center;
    align-items: center;
}}

.game-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.8;
}}

.hidden {{
    display: none !important;
}}

@media (max-width: 600px) {{
    .game-container {{
        padding: 1rem;
        margin: 1rem;
    }}

    .game-area {{
        flex-direction: column;
        gap: 10px;
    }}

    #gameCanvas {{
        width: 100%;
        max-width: 350px;
        height: auto;
    }}

    .game-header h1 {{
        font-size: 2rem;
    }}

    .game-info {{
        font-size: 1rem;
        flex-wrap: wrap;
        justify-content: center;
    }}
}}"""

    def get_tetris_js(self, project_name, description, style):
        return """
let board = [];
let score = 0;
let level = 1;
let lines = 0;
let currentPiece = null;
let nextPiece = null;
let animationId = null;
let isGameOver = false;
let gameInterval = 1000; // ms

const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30; // px

const canvas = document.getElementById('gameCanvas');
const context = canvas.getContext('2d');
const nextCanvas = document.getElementById('nextCanvas');
const nextContext = nextCanvas.getContext('2d');
const scoreElement = document.getElementById('score');
const levelElement = document.getElementById('level');
const linesElement = document.getElementById('lines');
const overlay = document.getElementById('gameOverlay');
const startBtn = document.getElementById('startBtn');

// Тема и цвета блоков
const themes = {
    "modern": {
        "--primary-color": "#4a148c", "--secondary-color": "#00bcd4", "--accent-color": "#ffeb3b", "--bg-color": "#121212", "--text-color": "#ffffff",
        "--block-colors": ["#FF0D72", "#0DC2FF", "#0DFF72", "#F538FF", "#FFFB0D", "#FF8E0D", "#AD1457"]
    },
    "retro": {
        "--primary-color": "#ff6b35", "--secondary-color": "#f7931e", "--accent-color": "#ffd23f", "--bg-color": "#1a1a1a", "--text-color": "#00ff00",
        "--block-colors": ["#00FF00", "#FFFF00", "#FFA500", "#FF4500", "#8A2BE2", "#FF1493", "#00CED1"]
    },
    "neon": {
        "--primary-color": "#ff0080", "--secondary-color": "#8000ff", "--accent-color": "#00ff80", "--bg-color": "#000015", "--text-color": "#ffffff",
        "--block-colors": ["#00FFFF", "#FFFF00", "#FF00FF", "#00FF00", "#FFFFFF", "#FF0000", "#0000FF"]
    }
};

// Применяем тему (если передана)
const themeName = document.body.className.replace('-theme', '') || 'modern';
const selectedTheme = themes[themeName] || themes['modern'];
Object.keys(selectedTheme).forEach(key => {
    document.documentElement.style.setProperty(key, selectedTheme[key]);
});
const BLOCK_COLORS = selectedTheme['--block-colors'];

// Формы фигур (tetrominoes)
const TETROMINOES = [
    { shape: [[1, 1, 1, 1]], color: BLOCK_COLORS[0] }, // I
    { shape: [[1, 1], [1, 1]], color: BLOCK_COLORS[1] }, // O
    { shape: [[1, 1, 0], [0, 1, 1]], color: BLOCK_COLORS[2] }, // S
    { shape: [[0, 1, 1], [1, 1, 0]], color: BLOCK_COLORS[3] }, // Z
    { shape: [[1, 1, 1], [0, 1, 0]], color: BLOCK_COLORS[4] }, // T
    { shape: [[1, 1, 1], [1, 0, 0]], color: BLOCK_COLORS[5] }, // L
    { shape: [[1, 1, 1], [0, 0, 1]], color: BLOCK_COLORS[6] }  // J
];

// Функции для инициализации и управления игрой
function createPiece() {
    const rand = Math.floor(Math.random() * TETROMINOES.length);
    const piece = TETROMINOES[rand];
    return {
        x: Math.floor(COLS / 2) - Math.floor(piece.shape[0].length / 2),
        y: 0,
        shape: piece.shape,
        color: piece.color
    };
}

function isValidMove(piece, board) {
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x]) {
                const boardX = piece.x + x;
                const boardY = piece.y + y;

                // Проверка выхода за границы поля
                if (boardY < 0 || boardY >= ROWS || boardX < 0 || boardX >= COLS) {
                    return false;
                }
                // Проверка столкновения с уже занятыми ячейками
                if (board[boardY] && board[boardY][boardX]) {
                    return false;
                }
            }
        }
    }
    return true;
}

function drawBlock(x, y, color, context) {
    context.fillStyle = color;
    context.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1);
    context.fillStyle = 'rgba(255, 255, 255, 0.3)';
    context.fillRect(x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4);
}

function drawPiece(piece, context) {
    context.fillStyle = piece.color;
    for (let y = 0; y < piece.shape.length; y++) {
        for (let x = 0; x < piece.shape[y].length; x++) {
            if (piece.shape[y][x]) {
                drawBlock(piece.x + x, piece.y + y, piece.color, context);
            }
        }
    }
}

function drawBoard() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (board[y] && board[y][x]) {
                drawBlock(x, y, board[y][x], context);
            }
        }
    }
}

function drawNextPiece() {
    nextContext.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    if (nextPiece) {
        drawPiece(nextPiece, nextContext);
    }
}

function clearLines() {
    let linesCleared = 0;
    for (let y = ROWS - 1; y >= 0; ) {
        if (board[y].every(cell => cell)) {
            for (let i = y; i > 0; i--) {
                board[i] = board[i - 1];
            }
            board[0] = Array(COLS).fill(null);
            linesCleared++;
        } else {
            y--;
        }
    }

    if (linesCleared > 0) {
        lines += linesCleared;
        score += calculateScore(linesCleared, level);
        updateScoreboard();
        updateLevelAndInterval();
    }
}

function calculateScore(linesCleared, level) {
    const points = [0, 40, 100, 300, 1200]; // Очки за 1, 2, 3, 4 линии
    return points[linesCleared] * level;
}

function updateLevelAndInterval() {
    const newLevel = Math.floor(lines / 10) + 1;
    if (newLevel > level) {
        level = newLevel;
        gameInterval = Math.max(100, 1000 - (level - 1) * 50); // Уменьшаем интервал
    }
}

function updateScoreboard() {
    scoreElement.textContent = score;
    levelElement.textContent = level;
    linesElement.textContent = lines;
}

function freezePiece() {
    for (let y = 0; y < currentPiece.shape.length; y++) {
        for (let x = 0; x < currentPiece.shape[y].length; x++) {
            if (currentPiece.shape[y][x]) {
                const boardX = currentPiece.x + x;
                const boardY = currentPiece.y + y;
                if (boardY >= 0) { // Только если часть фигуры на поле
                    if (!board[boardY]) board[boardY] = Array(COLS).fill(null);
                    board[boardY][boardX] = currentPiece.color;
                }
            }
        }
    }
    clearLines();
    currentPiece = nextPiece;
    nextPiece = createPiece();
    if (!isValidMove(currentPiece, board)) {
        gameOver();
        return;
    }
    drawNextPiece();
}

function move(deltaX) {
    currentPiece.x += deltaX;
    if (!isValidMove(currentPiece, board)) {
        currentPiece.x -= deltaX; // Откатываем ход
    }
}

function rotate() {
    const rotatedShape = currentPiece.shape[0].map((_, index) => currentPiece.shape.map(row => row[index])).reverse();
    const rotatedPiece = { ...currentPiece, shape: [rotatedShape] }; // Оборачиваем в массив для совместимости
    if (isValidMove(rotatedPiece, board)) {
        currentPiece = rotatedPiece;
    } else {
        // Попытка "подпрыгнуть" фигуру, если она упирается в стену
        const wallkickOffset = currentPiece.x < COLS / 2 ? 1 : -1;
        const kickedPiece = { ...currentPiece, x: currentPiece.x + wallkickOffset };
        if (isValidMove(kickedPiece, board)) {
            currentPiece = kickedPiece;
        }
    }
}


function drop() {
    currentPiece.y++;
    if (!isValidMove(currentPiece, board)) {
        currentPiece.y--; // Возвращаем на прежнюю позицию
        freezePiece();
        return true; // Фигура упала
    }
    return false;
}

function gameLoop() {
    if (isGameOver) return;

    const didDrop = drop();
    if (!didDrop) {
        drawBoard();
        drawPiece(currentPiece, context);
    }
    animationId = setTimeout(gameLoop, gameInterval);
}

function gameOver() {
    isGameOver = true;
    cancelAnimationFrame(animationId);
    overlay.innerHTML = `
        <div class="start-screen">
            <h2>🎮 Игра окончена!</h2>
            <p>Ваш счёт: ${score}</p>
            <p>Рекорд: ${localStorage.getItem('tetrisHighScore') || 0}</p>
            <button id="restartBtn" class="game-btn">Играть снова</button>
        </div>
    `;
    overlay.classList.remove('hidden');
    document.getElementById('restartBtn').addEventListener('click', startGame);
}

function startGame() {
    isGameOver = false;
    score = 0;
    level = 1;
    lines = 0;
    gameInterval = 1000;
    board = Array(ROWS).fill(null).map(() => Array(COLS).fill(null));
    currentPiece = createPiece();
    nextPiece = createPiece();
    updateScoreboard();
    drawBoard();
    drawNextPiece();
    if (animationId) clearTimeout(animationId);
    animationId = setTimeout(gameLoop, gameInterval);
    overlay.classList.add('hidden');

    // Сохранение рекорда
    const highScore = localStorage.getItem('tetrisHighScore') || 0;
    if (score > highScore) {
        localStorage.setItem('tetrisHighScore', score);
    }
}

// Обработка ввода
document.addEventListener('keydown', (e) => {
    if (isGameOver || !currentPiece) return;

    switch (e.key) {
        case 'ArrowLeft':
        case 'a':
        case 'A':
            move(-1);
            break;
        case 'ArrowRight':
        case 'd':
        case 'D':
            move(1);
            break;
        case 'ArrowDown':
        case 's':
        case 'S':
            drop(); // Быстрое падение
            break;
        case ' ': // Пробел для поворота
            rotate();
            break;
    }
    drawBoard();
    drawPiece(currentPiece, context);
});

// Обработка мобильных кнопок
document.querySelectorAll('.control-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (isGameOver || !currentPiece) return;

        const action = btn.dataset.action;
        switch (action) {
            case 'left':
                move(-1);
                break;
            case 'right':
                move(1);
                break;
            case 'down':
                drop();
                break;
            case 'rotate':
                rotate();
                break;
        }
        drawBoard();
        drawPiece(currentPiece, context);
    });
});

startBtn.addEventListener('click', startGame);

// Начальная загрузка
document.addEventListener('DOMContentLoaded', () => {
    canvas.width = COLS * BLOCK_SIZE;
    canvas.height = ROWS * BLOCK_SIZE;
    nextCanvas.width = 4 * BLOCK_SIZE;
    nextCanvas.height = 4 * BLOCK_SIZE;
    context.scale(BLOCK_SIZE, BLOCK_SIZE);
    nextContext.scale(BLOCK_SIZE, BLOCK_SIZE);
});
"""

    def get_tetris_readme(self, project_name, description, style):
        return f"""# {project_name} - Тетрис

{description}

Классическая головоломка Тетрис с современным интерфейсом."""

    def get_todo_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="app-container">
        <div class="app-header">
            <h1>{project_name}</h1>
            <p class="app-description">{description}</p>
        </div>

        <div class="todo-input-section">
            <div class="input-group">
                <input type="text" id="todoInput" placeholder="Добавить новую задачу..." maxlength="100">
                <button id="addBtn" class="add-btn">+</button>
            </div>
        </div>

        <div class="todo-filters">
            <button class="filter-btn active" data-filter="all">Все</button>
            <button class="filter-btn" data-filter="active">Активные</button>
            <button class="filter-btn" data-filter="completed">Выполненные</button>
        </div>

        <div class="todo-list" id="todoList">
            <!-- Задачи будут добавлены динамически -->
        </div>

        <div class="todo-stats">
            <span id="totalTasks">0 задач</span>
            <button id="clearCompleted" class="clear-btn">Очистить выполненные</button>
        </div>

        <div class="app-footer">
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_todo_css(self, project_name, description, style):
        return f"""/* CSS для TODO приложения */
:root {{
    --primary-color: #3f51b5; /* Indigo */
    --secondary-color: #009688; /* Teal */
    --accent-color: #ff5722; /* Deep Orange */
    --bg-color: #f5f5f5; /* Light Gray */
    --text-color: #333333; /* Dark Gray */
    --input-bg: #ffffff;
    --border-color: #e0e0e0;
    --completed-color: #bdbdbd; /* Light Gray for completed */
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.app-container {{
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 500px;
    width: 100%;
    backdrop-filter: blur(5px);
}}

.app-header {{
    margin-bottom: 2rem;
}}

.app-header h1 {{
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.app-description {{
    font-size: 1.1rem;
    color: #616161;
}}

.todo-input-section {{
    margin-bottom: 1.5rem;
}}

.input-group {{
    display: flex;
    gap: 10px;
}}

#todoInput {{
    flex-grow: 1;
    padding: 1rem;
    border: 1px solid var(--border-color);
    border-radius: 25px;
    font-size: 1rem;
    background-color: var(--input-bg);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}}

#todoInput:focus {{
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(255, 87, 34, 0.2);
}}

.add-btn {{
    background: var(--accent-color);
    border: none;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    font-size: 1.8rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(255, 87, 34, 0.3);
}}

.add-btn:hover {{
    transform: scale(1.1);
}}

.todo-filters {{
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: center;
    gap: 15px;
}}

.filter-btn {{
    background: none;
    border: none;
    color: var(--primary-color);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    transition: all 0.3s ease;
}}

.filter-btn.active {{
    background: var(--primary-color);
    color: white;
    box-shadow: 0 4px 10px rgba(63, 81, 181, 0.3);
}}

.filter-btn:hover {{
    background: rgba(63, 81, 181, 0.1);
}}

.todo-list {{
    max-height: 300px;
    overflow-y: auto;
    text-align: left;
    margin-bottom: 1.5rem;
    padding-right: 10px; /* Для скроллбара */
}}

.todo-item {{
    background: var(--input-bg);
    padding: 1rem;
    margin-bottom: 10px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: background 0.3s ease;
}}

.todo-item.completed {{
    background: var(--completed-color);
    opacity: 0.7;
}}

.todo-item.completed .todo-text {{
    text-decoration: line-through;
    color: #757575;
}}

.todo-content {{
    display: flex;
    align-items: center;
    gap: 15px;
    flex-grow: 1;
    overflow: hidden; /* Предотвращает вылезание текста */
}}

.checkbox {{
    width: 20px;
    height: 20px;
    border: 2px solid var(--primary-color);
    border-radius: 5px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.3s ease;
}}

.checkbox.checked {{
    background: var(--primary-color);
    border-color: var(--primary-color);
}}

.checkbox.checked::after {{
    content: '✔';
    color: white;
    font-size: 14px;
}}

.todo-text {{
    font-size: 1rem;
    word-break: break-word; /* Перенос длинных слов */
}}

.todo-actions {{
    display: flex;
    gap: 5px;
}}

.action-btn {{
    background: none;
    border: none;
    font-size: 1.2rem;
    cursor: pointer;
    color: #9e9e9e;
    transition: color 0.3s ease;
}}

.action-btn.edit:hover {{
    color: var(--accent-color);
}}

.action-btn.delete:hover {{
    color: #f44336;
}}

.todo-stats {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    font-size: 0.9rem;
    color: #757575;
}}

.clear-btn {{
    background: none;
    border: 1px solid var(--border-color);
    color: var(--secondary-color);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s ease;
}}

.clear-btn:hover {{
    background: var(--secondary-color);
    color: white;
    border-color: var(--secondary-color);
}}

.app-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.7;
    color: #616161;
}}

/* Стили для мобильных устройств */
@media (max-width: 500px) {{
    .app-container {{
        padding: 1.5rem;
    }}
    .app-header h1 {{
        font-size: 2rem;
    }}
    .input-group {{
        flex-direction: column;
    }}
    #todoInput {{
        margin-bottom: 10px;
    }}
}}
"""

    def get_todo_js(self, project_name, description, style):
        return """
const todoInput = document.getElementById('todoInput');
const addBtn = document.getElementById('addBtn');
const todoList = document.getElementById('todoList');
const totalTasksElement = document.getElementById('totalTasks');
const clearCompletedBtn = document.getElementById('clearCompleted');
const filterButtons = document.querySelectorAll('.filter-btn');

let todos = []; // Массив для хранения задач
let currentFilter = 'all'; // Текущий фильтр

// --- Функции для работы с задачами ---

// Добавление новой задачи
function addTodo() {
    const taskText = todoInput.value.trim();
    if (!taskText) return;

    const newTodo = {
        id: Date.now(), // Уникальный ID
        text: taskText,
        completed: false
    };

    todos.push(newTodo);
    todoInput.value = ''; // Очищаем поле ввода
    renderTodos();
    updateStats();
    saveTodos(); // Сохраняем в localStorage
}

// Удаление задачи
function deleteTodo(id) {
    todos = todos.filter(todo => todo.id !== id);
    renderTodos();
    updateStats();
    saveTodos();
}

// Переключение статуса задачи (выполнена/активна)
function toggleTodoComplete(id) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, completed: !todo.completed } : todo
    );
    renderTodos();
    updateStats();
    saveTodos();
}

// Редактирование задачи (простой вариант - обновление текста)
function editTodo(id, newText) {
    todos = todos.map(todo =>
        todo.id === id ? { ...todo, text: newText } : todo
    );
    renderTodos();
    saveTodos();
}

// Очистка выполненных задач
function clearCompletedTodos() {
    todos = todos.filter(todo => !todo.completed);
    renderTodos();
    updateStats();
    saveTodos();
}

// --- Функции для рендеринга ---

// Создание HTML элемента для задачи
function createTodoElement(todo) {
    const listItem = document.createElement('div');
    listItem.className = `todo-item ${todo.completed ? 'completed' : ''}`;
    listItem.dataset.id = todo.id;

    listItem.innerHTML = `
        <div class="todo-content">
            <div class="checkbox ${todo.completed ? 'checked' : ''}" data-action="complete"></div>
            <span class="todo-text">${todo.text}</span>
        </div>
        <div class="todo-actions">
            <button class="action-btn edit" data-action="edit">✏️</button>
            <button class="action-btn delete" data-action="delete">🗑️</button>
        </div>
    `;

    // Обработчики событий для элементов задачи
    const checkbox = listItem.querySelector('.checkbox');
    const deleteBtn = listItem.querySelector('.delete');
    const editBtn = listItem.querySelector('.edit');
    const todoTextSpan = listItem.querySelector('.todo-text');

    checkbox.addEventListener('click', () => toggleTodoComplete(todo.id));
    deleteBtn.addEventListener('click', () => deleteTodo(todo.id));
    editBtn.addEventListener('click', () => {
        const newText = prompt('Редактировать задачу:', todo.text);
        if (newText !== null && newText.trim()) {
            editTodo(todo.id, newText.trim());
        }
    });

    return listItem;
}

// Отображение задач на основе фильтра
function renderTodos() {
    todoList.innerHTML = ''; // Очищаем список перед рендерингом

    const filteredTodos = todos.filter(todo => {
        switch (currentFilter) {
            case 'active':
                return !todo.completed;
            case 'completed':
                return todo.completed;
            default: // 'all'
                return true;
        }
    });

    if (filteredTodos.length === 0) {
        todoList.innerHTML = '<p style="text-align: center; margin-top: 20px; color: #9e9e9e;">Список задач пуст!</p>';
    } else {
        filteredTodos.forEach(todo => {
            todoList.appendChild(createTodoElement(todo));
        });
    }
}

// Обновление статистики (общее количество задач)
function updateStats() {
    const activeCount = todos.filter(todo => !todo.completed).length;
    totalTasksElement.textContent = `${activeCount} активных задач`; // Изменил для отображения активных
    clearCompletedBtn.disabled = todos.every(todo => !todo.completed); // Делаем кнопку неактивной, если нет выполненных
}

// --- Функции для сохранения и загрузки ---

function saveTodos() {
    localStorage.setItem('todos', JSON.stringify(todos));
}

function loadTodos() {
    const savedTodos = localStorage.getItem('todos');
    if (savedTodos) {
        todos = JSON.parse(savedTodos);
    }
    renderTodos();
    updateStats();
}

// --- Обработчики событий ---

// Добавление задачи по клику или Enter
addBtn.addEventListener('click', addTodo);
todoInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTodo();
    }
});

// Обработка фильтров
filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        currentFilter = button.dataset.filter;
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        renderTodos();
    });
});

// Очистка выполненных
clearCompletedBtn.addEventListener('click', clearCompletedTodos);

// --- Инициализация ---
document.addEventListener('DOMContentLoaded', loadTodos);
"""

    def get_todo_readme(self, project_name, description, style):
        return f"""# {project_name} - TODO Приложение

{description}

Простое и стильное приложение для управления списком дел.

## Возможности:
- Добавление, удаление, редактирование задач
- Отметка задач как выполненных
- Фильтрация задач (все, активные, выполненные)
- Очистка выполненных задач
- Сохранение списка в localStorage
- Адаптивный дизайн
"""

    def get_weather_html(self, project_name, description, style):
        return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body class="{style}-theme">
    <div class="weather-app">
        <div class="app-header">
            <h1>{project_name}</h1>
            <p>{description}</p>
        </div>

        <div class="search-section">
            <div class="search-group">
                <input type="text" id="cityInput" placeholder="Введите название города..." />
                <button id="searchBtn" class="search-btn">🔍</button>
            </div>
        </div>

        <div class="weather-display" id="weatherDisplay">
            <div class="weather-card">
                <div class="current-weather">
                    <div class="weather-icon">☀️</div>
                    <div class="temperature">--°C</div>
                    <div class="city-name">--</div>
                    <div class="weather-description">--</div>
                </div>

                <div class="weather-details">
                    <div class="detail-item">
                        <span class="detail-label">Ощущается как</span>
                        <span class="detail-value">--°C</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Влажность</span>
                        <span class="detail-value">--%</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Ветер</span>
                        <span class="detail-value">-- км/ч</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-label">Давление</span>
                        <span class="detail-value">-- гПа</span>
                    </div>
                </div>

                <div class="forecast">
                    <h3>Прогноз на 5 дней</h3>
                    <div class="forecast-list" id="forecastList">
                        <p>Загрузка прогноза...</p>
                    </div>
                </div>
            </div>
        </div>

        <div class="app-footer">
            <p>Создано с помощью Lovable AI</p>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>"""

    def get_weather_css(self, project_name, description, style):
        return f"""/* CSS для Weather приложения */
:root {{
    --primary-color: #0077b6; /* Blue */
    --secondary-color: #90e0ef; /* Light Blue */
    --accent-color: #ffb703; /* Orange */
    --bg-color: #e0f2f7; /* Very Light Blue */
    --text-color: #1a1a1a; /* Dark Gray */
    --card-bg: #ffffff;
    --detail-bg: #f8f9fa;
    --forecast-bg: #f1f3f4;
}}

body {{
    font-family: 'Arial', sans-serif;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--text-color);
}}

.weather-app {{
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    text-align: center;
    max-width: 550px;
    width: 100%;
    backdrop-filter: blur(5px);
}}

.app-header {{
    margin-bottom: 2rem;
}}

.app-header h1 {{
    font-size: 2.5rem;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}}

.app-description {{
    font-size: 1rem;
    color: #616161;
}}

.search-section {{
    margin-bottom: 2rem;
}}

.search-group {{
    display: flex;
    gap: 10px;
}}

#cityInput {{
    flex-grow: 1;
    padding: 1rem;
    border: 1px solid var(--primary-color);
    border-radius: 25px;
    font-size: 1rem;
    background-color: var(--card-bg);
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.05);
}}

#cityInput:focus {{
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(255, 183, 3, 0.2);
}}

.search-btn {{
    background: var(--accent-color);
    border: none;
    color: var(--text-color);
    width: 50px;
    height: 50px;
    border-radius: 25px;
    font-size: 1.4rem;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 10px rgba(255, 183, 3, 0.3);
}}

.search-btn:hover {{
    transform: scale(1.1);
}}

.weather-card {{
    background: var(--card-bg);
    border-radius: 15px;
    padding: 1.5rem;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
}}

.current-weather {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--forecast-bg);
    padding-bottom: 1.5rem;
}}

.weather-icon {{
    font-size: 4rem;
    margin-bottom: 0.5rem;
}}

.temperature {{
    font-size: 3rem;
    font-weight: 700;
    color: var(--primary-color);
}}

.city-name {{
    font-size: 1.5rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}}

.weather-description {{
    font-size: 1.2rem;
    color: #757575;
}}

.weather-details {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}}

.detail-item {{
    background: var(--detail-bg);
    padding: 0.8rem;
    border-radius: 10px;
    text-align: center;
}}

.detail-label {{
    display: block;
    font-size: 0.9rem;
    color: #757575;
    margin-bottom: 0.3rem;
}}

.detail-value {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.forecast h3 {{
    margin-bottom: 1rem;
    color: var(--primary-color);
}}

.forecast-list {{
    display: flex;
    overflow-x: auto;
    gap: 10px;
    padding-bottom: 10px; /* Отступ для скроллбара */
}}

.forecast-item {{
    background: var(--forecast-bg);
    padding: 1rem;
    border-radius: 10px;
    min-width: 100px;
    text-align: center;
    flex-shrink: 0;
}}

.forecast-item .date {{
    font-size: 0.9rem;
    color: #757575;
    margin-bottom: 0.5rem;
}}

.forecast-item .icon {{
    font-size: 2rem;
    margin-bottom: 0.5rem;
}}

.forecast-item .temp {{
    font-size: 1.1rem;
    font-weight: 600;
}}

.app-footer {{
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0.7;
    color: #616161;
}}

/* Стили для мобильных устройств */
@media (max-width: 550px) {{
    .weather-app {{
        padding: 1.5rem;
    }}
    .app-header h1 {{
        font-size: 2rem;
    }}
    .search-group {{
        flex-direction: column;
    }}
    #cityInput {{
        margin-bottom: 10px;
    }}
    .weather-details {{
        grid-template-columns: 1fr;
    }}
}}
"""

    def get_weather_js(self, project_name, description, style):
        return """
const cityInput = document.getElementById('cityInput');
const searchBtn = document.getElementById('searchBtn');
const weatherDisplay = document.getElementById('weatherDisplay');
const forecastList = document.getElementById('forecastList');

const API_KEY = 'YOUR_OPENWEATHERMAP_API_KEY'; // Замените на ваш API ключ

// Пример данных для отображения (пока нет API)
let currentWeatherData = {
    icon: '☀️',
    temperature: '--',
    city: '--',
    description: '--',
    feels_like: '--',
    humidity: '--',
    wind_speed: '--',
    pressure: '--'
};

let forecastData = [];

const weatherIcons = {
    '01d': '☀️', '01n': '🌙',
    '02d': '☁️', '02n': '☁️',
    '03d': '☁️', '03n': '☁️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌧️', '10n': '🌧️',
    '11d': '⚡', '11n': '⚡',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️'
};

function getWeatherIcon(iconCode) {
    return weatherIcons[iconCode] || '❓';
}

function formatPressure(hpa) {
    return Math.round(hpa); // Давление в гПа
}

function formatWindSpeed(mps) {
    return Math.round(mps * 3.6); // Скорость ветра в км/ч
}

async function fetchWeather(city) {
    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${API_KEY}&units=metric&lang=ru`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при получении данных о погоде:", error);
        displayError("Не удалось загрузить погоду. Проверьте название города.");
        return null;
    }
}

async function fetchForecast(city) {
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${API_KEY}&units=metric&lang=ru`;
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Ошибка при получении данных прогноза:", error);
        return null;
    }
}

function displayWeather(data) {
    if (!data) return;

    currentWeatherData = {
        icon: getWeatherIcon(data.weather[0].icon),
        temperature: Math.round(data.main.temp),
        city: data.name,
        description: data.weather[0].description,
        feels_like: Math.round(data.main.feels_like),
        humidity: data.main.humidity,
        wind_speed: formatWindSpeed(data.wind.speed),
        pressure: formatPressure(data.main.pressure)
    };

    renderCurrentWeather();
}

function renderCurrentWeather() {
    const html = `
        <div class="weather-card">
            <div class="current-weather">
                <div class="weather-icon">${currentWeatherData.icon}</div>
                <div class="temperature">${currentWeatherData.temperature}°C</div>
                <div class="city-name">${currentWeatherData.city}</div>
                <div class="weather-description">${currentWeatherData.description}</div>
            </div>

            <div class="weather-details">
                <div class="detail-item">
                    <span class="detail-label">Ощущается как</span>
                    <span class="detail-value">${currentWeatherData.feels_like}°C</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Влажность</span>
                    <span class="detail-value">${currentWeatherData.humidity}%</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Ветер</span>
                    <span class="detail-value">${currentWeatherData.wind_speed} км/ч</span>
                </div>
                <div class="detail-item">
                    <span class="detail-label">Давление</span>
                    <span class="detail-value">${currentWeatherData.pressure} гПа</span>
                </div>
            </div>

            <div class="forecast">
                <h3>Прогноз на 5 дней</h3>
                <div class="forecast-list" id="forecastList">
                    ${renderForecast(forecastData)}
                </div>
            </div>
        </div>
    `;
    weatherDisplay.innerHTML = html;
}

function renderForecast(forecastItems) {
    if (!forecastItems || forecastItems.length === 0) {
        return '<p>Нет данных прогноза.</p>';
    }

    let html = '';
    // Отображаем прогноз на 5 дней, беря данные примерно раз в 8 интервалов (24 часа)
    for (let i = 0; i < forecastItems.length; i += 8) {
        const day = forecastItems[i];
        const date = new Date(day.dt * 1000);
        const dayOfWeek = date.toLocaleDateString('ru-RU', { weekday: 'short' });
        const temp = Math.round(day.main.temp);
        const icon = getWeatherIcon(day.weather[0].icon);

        html += `
            <div class="forecast-item">
                <div class="date">${dayOfWeek}</div>
                <div class="icon">${icon}</div>
                <div class="temp">${temp}°C</div>
            </div>
        `;
    }
    return html;
}

function displayError(message) {
    weatherDisplay.innerHTML = `<p class="error-message">${message}</p>`;
}

async function handleSearch() {
    const city = cityInput.value.trim();
    if (!city) {
        displayError("Пожалуйста, введите название города.");
        return;
    }

    // Отображаем индикатор загрузки
    weatherDisplay.innerHTML = '<div class="loading">Загрузка...</div>';

    const weatherData = await fetchWeather(city);
    if (weatherData) {
        const forecastWeatherData = await fetchForecast(city);
        forecastData = forecastWeatherData ? forecastWeatherData.list : [];
        displayWeather(weatherData);
    } else {
        displayError("Город не найден или произошла ошибка.");
    }
}

// --- Обработчики событий ---
searchBtn.addEventListener('click', handleSearch);
cityInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSearch();
    }
});

// --- Инициализация ---
// Можно добавить загрузку погоды по умолчанию при загрузке страницы
// handleSearch(); // Раскомментируйте, если хотите загружать погоду по умолчанию
"""

    def get_weather_readme(self, project_name, description, style):
        return f"""# {project_name} - Погодное приложение

{description}

Простое погодное приложение, показывающее текущую погоду и прогноз.
Требуется API ключ OpenWeatherMap.
"""

# Инициализируем генератор проектов
generator = ProjectGenerator()

# Улучшенный AI-агент с диалоговым процессом
class SmartAI:
    def __init__(self):
        self.conversation_history = {} # Храним историю по session_id
        self.user_preferences = {}
        self.project_context = {}
        self.user_session = {} # Состояние сессии пользователя

        # Тренды и аналитика
        self.market_trends = {
            "mobile_games": {
                "popularity": 95,
                "description": "Мобильные игры - самый популярный сегмент. Особенно востребованы казуальные игры.",
                "examples": ["Змейка", "Тетрис", "Головоломки", "Аркады"]
            },
            "productivity_apps": {
                "popularity": 85,
                "description": "Приложения продуктивности очень востребованы после пандемии.",
                "examples": ["TODO списки", "Планировщики", "Трекеры привычек", "Заметки"]
            },
            "health_fitness": {
                "popularity": 80,
                "description": "Здоровье и фитнес - растущий тренд с высокой монетизацией.",
                "examples": ["Счетчики калорий", "Трекеры тренировок", "Медитация", "Сон"]
            },
            "social_apps": {
                "popularity": 75,
                "description": "Социальные приложения имеют высокий потенциал вирусности.",
                "examples": ["Чаты", "Фото-обмен", "Знакомства", "Сообщества"]
            },
            "utility_apps": {
                "popularity": 70,
                "description": "Утилиты решают конкретные проблемы пользователей.",
                "examples": ["Погода", "Калькуляторы", "QR-сканеры", "Конвертеры"]
            }
        }

    def generate_personalized_response(self, message, session_id="default"):
        """Генерирует умный ответ с учетом контекста и сессии"""
        if session_id not in self.user_session:
            self.user_session[session_id] = {
                "stage": "initial",
                "project_type": None,
                "preferences": {},
                "questions_asked": [],
                "conversation": [],
                "current_project_id": None,
                "project_creation_in_progress": False
            }

        session = self.user_session[session_id]
        session["conversation"].append({"user": message, "timestamp": time.time()})
        
        # Обработка сообщений с опечатками и синонимами
        processed_message = nlp_processor.correct_and_normalize(message)
        message_type = self.analyze_message(processed_message)

        # Логирование взаимодействия
        interaction_logger.log_interaction(session_id, message, processed_message, message_type)

        # Управление состоянием диалога
        if session["stage"] == "initial":
            return self.handle_initial_stage(processed_message, message_type, session_id)
        elif session["stage"] == "clarifying":
            return self.handle_clarifying_stage(processed_message, session_id)
        elif session["stage"] == "creating":
            return self.handle_creating_stage(processed_message, session_id)
        elif session["stage"] == "editing":
            return self.handle_editing_stage(processed_message, session_id)
        else: # Общий случай или если этап не определен
            return self.handle_general_stage(processed_message, session_id)

    def analyze_message(self, message):
        """Анализирует сообщение пользователя"""
        message_lower = message.lower()

        # Игры
        if any(word in message_lower for word in ["игра", "игру", "game", "змейка", "тетрис", "аркад", "головоломка", "стрелялка", "раннер"]):
            return "game_request"

        # Приложения продуктивности
        if any(word in message_lower for word in ["todo", "планировщик", "заметки", "органайзер", "продуктивность", "список дел", "календарь", "трекер"]):
            return "productivity_request"

        # Утилиты
        if any(word in message_lower for word in ["калькулятор", "погода", "конвертер", "утилита", "инструмент", "помощник"]):
            return "utility_request"
        
        # Рыночный анализ
        if any(word in message_lower for word in ["тренд", "рынок", "популярно", "востребовано", "статистика"]):
            return "market_analysis"

        # Приветствия
        if any(word in message_lower for word in ["привет", "здравствуй", "добрый", "hi", "hello", "доброе утро", "добрый день"]):
            return "greeting"

        # Подтверждения
        if any(word in message_lower for word in ["да", "yes", "согласен", "подходит", "создавай", "давай", "ок", "хорошо", "ура", "отлично"]):
            return "confirmation"

        # Отрицания / Отклонения
        if any(word in message_lower for word in ["нет", "no", "не подходит", "другое", "иначе", "отмена", "плохо"]):
            return "rejection"
            
        # Запрос на скачивание
        if any(word in message_lower for word in ["скачать", "скачай", "архив", "zip", "загрузить"]):
            return "download_request"
            
        # Запрос на редактирование / доработку
        if any(word in message_lower for word in ["доработать", "улучшить", "изменить", "добавить", "редактировать", "фича", "функция"]):
            return "edit_request"

        return "general"

    def handle_initial_stage(self, message, message_type, session_id):
        """Обработка начальной стадии диалога"""
        session = self.user_session[session_id]

        if message_type == "greeting":
            return {
                "type": "ai_response",
                "message": "Привет! 👋 Я ваш персональный AI-консультант по созданию no-code приложений!\n\n🚀 **Что мы можем создать:**\n• 🎮 Игры (аркады, головоломки)\n• 📱 Приложения продуктивности (TODO, планировщики)\n• 🛠 Полезные утилиты (погода, калькулятор)\n• 🌐 Лендинги для ваших приложений\n\n💡 Расскажите, какое приложение вы хотели бы создать? Я помогу выбрать лучший вариант и сгенерировать базовую версию!",
                "suggestions": [
                    "Хочу создать игру",
                    "Нужно приложение для работы",
                    "Покажи популярные тренды",
                    "Помоги с идеей"
                ]
            }

        elif message_type == "game_request":
            session["stage"] = "clarifying"
            session["project_type"] = "game"
            return self.ask_clarification("game", session_id)

        elif message_type == "productivity_request":
            session["stage"] = "clarifying"
            session["project_type"] = "productivity"
            return self.ask_clarification("productivity", session_id)

        elif message_type == "utility_request":
            session["stage"] = "clarifying"
            session["project_type"] = "utility"
            return self.ask_clarification("utility", session_id)
            
        elif message_type == "market_analysis":
            return self.show_market_analysis()
            
        elif message_type == "edit_request":
             return {
                "type": "ai_response",
                "message": "💡 Отличная идея! Доработка и улучшение - это ключ к успеху. Что именно вы хотите изменить или добавить в ваше приложение?",
                "suggestions": [
                    "Добавить новые функции",
                    "Изменить дизайн",
                    "Улучшить производительность",
                    "Покажи примеры доработок"
                ]
            }

        else:
            return {
                "type": "ai_response",
                "message": "📊 **Популярные направления:**\n• 🎮 **Игры** - всегда в тренде!\n• 📱 **Продуктивность** - решают реальные задачи.\n\nРасскажите подробнее о вашей идее, и я помогу воплотить её в жизнь!",
                "suggestions": [
                    "Создать игру",
                    "Приложение для бизнеса",
                    "Показать тренды подробнее",
                    "Помоги выбрать идею"
                ]
            }

    def ask_clarification(self, project_type, session_id):
        """Задает уточняющие вопросы по типу проекта"""
        session = self.user_session[session_id]
        questions = []
        
        if project_type == "game":
            questions = [
                "Какой жанр игры вас больше интересует? (аркада, головоломка, стратегия, раннер)",
                "Какую целевую аудиторию вы видите? (дети, подростки, взрослые)",
                "Какой стиль дизайна предпочитаете? (минималистичный, яркий, ретро, неоновый)",
                "Нужна ли система очков, рекордов или достижений?",
                "Планируете ли в будущем многопользовательский режим?"
            ]
            intro_message = "Отлично! 🎮 Игры - самое популярное направление. Что насчет стиля? Например, современный, ретро или неоновый?"
        elif project_type == "productivity":
            questions = [
                "Какую основную проблему должно решать приложение? (организация задач, учет времени, управление проектами)",
                "Кто ваша целевая аудитория? (студенты, офисные работники, фрилансеры)",
                "Нужна ли синхронизация между устройствами или облачное хранение?",
                "Какие функции считаете наиболее важными? (напоминания, интеграции, статистика)",
                "Предпочитаете простой интерфейс или многофункциональный?"
            ]
            intro_message = "Превосходно! 📱 Приложения продуктивности очень востребованы. Для начала, какое основное назначение приложения?"
        elif project_type == "utility":
            questions = [
                "Какую конкретную задачу должно решать приложение? (расчеты, информация, преобразование)",
                "Кто будет основным пользователем?",
                "Нужны ли какие-то особые функции (например, интеграция с другими сервисами)?",
                "Предпочтительный дизайн (простой, интерактивный, с визуализациями)?"
            ]
            intro_message = "Отличный выбор! 🛠 Утилиты решают конкретные проблемы. Начнем с определения основной функции: калькулятор, погодное приложение или что-то другое?"
        else: # Общий случай
            questions = [
                "Расскажите подробнее о вашей идее",
                "Кто будет использовать это приложение?",
                "Какую главную проблему оно должно решать?",
                "Есть ли примеры похожих приложений, которые вам нравятся?",
                "Какой бюджет и сроки вы рассматриваете?"
            ]
            intro_message = "Интересно! Чтобы я мог лучше понять вашу идею, расскажите подробнее, что вы хотите создать?"

        session["questions_asked"] = questions
        session["stage"] = "clarifying"
        
        return {
            "type": "ai_response",
            "message": f"{intro_message}\n\n{questions[0]}",
            "suggestions": self.get_suggestions_for_question(questions[0])
        }

    def get_suggestions_for_question(self, question):
        """Генерирует примерные ответы для уточняющих вопросов"""
        if "жанр игры" in question:
            return ["Аркада", "Головоломка", "Раннер", "Стратегия", "Другое"]
        elif "целевую аудиторию" in question:
            return ["Дети", "Подростки", "Взрослые", "Все"]
        elif "стиль дизайна" in question:
            return ["Современный", "Ретро", "Неоновый", "Минималистичный"]
        elif "основную проблему" in question:
            return ["Организация задач", "Учет времени", "Быстрые расчеты", "Информация о погоде"]
        elif "основное назначение" in question:
            return ["TODO список", "Планировщик", "Трекер привычек", "Заметки"]
        elif "конкретную задачу" in question:
            return ["Умный калькулятор", "Погодное приложение", "Конвертер валют", "QR-сканер"]
        else:
            return ["Да", "Нет", "Уточните"]

    def handle_clarifying_stage(self, message, session_id):
        """Обработка стадии уточнений"""
        session = self.user_session[session_id]
        
        # Сохраняем ответ пользователя
        if session["questions_asked"]:
            current_question = session["questions_asked"][0]
            session["preferences"][current_question] = message
            session["questions_asked"].pop(0) # Удаляем заданный вопрос

        if not session["questions_asked"]: # Если вопросы закончились
            session["stage"] = "confirming"
            project_type = session["project_type"]
            project_name = f"{project_type.replace('_', ' ').title()} от AI"
            description = f"Базовая версия {project_type.replace('_', ' ')}."
            
            # Попытка определить название и описание на основе предпочтений
            if project_type == "game":
                game_type = session["preferences"].get("Какой жанр игры вас больше интересует?", "игра")
                style = session["preferences"].get("Какой стиль дизайна предпочитаете?", "современный")
                project_name = f"{style.capitalize()} {game_type.capitalize()} Игра"
                description = f"Увлекательная {game_type} игра в {style} стиле."
            elif project_type == "productivity":
                app_purpose = session["preferences"].get("Какую основную проблему должно решать приложение?", "приложение")
                project_name = f"Удобный {app_purpose}"
                description = f"Приложение для {app_purpose}."
            elif project_type == "utility":
                utility_type = session["preferences"].get("Какую конкретную задачу должно решать приложение?", "утилита")
                project_name = f"Умный {utility_type}"
                description = f"Функциональная {utility_type}."

            session["project_details"] = {
                "type": project_type,
                "name": project_name,
                "description": description
            }

            return {
                "type": "ai_response",
                "message": f"✅ Отлично! Мы собрали достаточно информации. Хотите создать '{project_name}'?\n\n*Описание:* {description}\n\nЯ могу сгенерировать базовую версию приложения.",
                "suggestions": ["Да, создавай!", "Нет, давай изменим", "Покажи другие варианты", "Добавить больше деталей"],
                "project_details": session["project_details"] # Передаем детали для подтверждения
            }
        else:
            next_question = session["questions_asked"][0]
            return {
                "type": "ai_response",
                "message": next_question,
                "suggestions": self.get_suggestions_for_question(next_question)
            }

    def handle_confirming_stage(self, message, session_id):
        """Обработка подтверждения создания проекта"""
        session = self.user_session[session_id]
        
        if self.analyze_message(message) == "confirmation":
            if session.get("project_details"):
                details = session["project_details"]
                
                # Обновляем версию проекта перед созданием
                project_version = version_control.get_next_version(details["type"])
                log_message = f"Создание проекта: {details['name']} (v{project_version})"
                interaction_logger.log_event("project_creation_start", {**details, "version": project_version})

                # Используем расширенный генератор
                result = advanced_generator.generate_project(
                    project_type=details["type"],
                    description=details["description"],
                    project_name=details["name"],
                    user_preferences=session["preferences"] # Передаем предпочтения
                )

                if result['success']:
                    project_id = result['project_id']
                    session["current_project_id"] = project_id
                    session["stage"] = "created" # Переходим в состояние "создано"
                    
                    # Сохраняем информацию о версии
                    version_control.save_project_version(project_id, project_version, result.get("files", []), log_message)
                    
                    # Логирование успешного создания
                    interaction_logger.log_event("project_creation_success", {
                        "project_id": project_id,
                        "project_name": details["name"],
                        "version": project_version
                    })

                    archive_url = f"/api/download/{project_id}"
                    return {
                        "type": "project_created",
                        "message": f"🎉 **Ваше приложение '{details['name']}' готово!**\n\n✨ Успешно сгенерирована версия {project_version}.\n\n🚀 **Что дальше?**\n1. Скачайте архив для просмотра.\n2. Используйте его как основу для дальнейшей разработки.\n\n💰 **Потенциал:** Такие приложения могут приносить доход от $500 до $2000/месяц!\n\n🔧 Хотите добавить новые функции или создать что-то еще?",
                        "project_id": project_id,
                        "download_url": archive_url,
                        "version": project_version,
                        "suggestions": [
                            "📥 Скачать проект",
                            "🔧 Добавить новые функции",
                            "🔄 Создать новую версию",
                            "✨ Создать другое приложение",
                            "📊 Показать аналитику"
                        ]
                    }
                else:
                    session["stage"] = "initial" # Возвращаемся к началу
                    interaction_logger.log_error("project_creation_failed", {
                        "project_name": details["name"],
                        "error": result.get('error', 'Неизвестная ошибка')
                    })
                    return {
                        "type": "error",
                        "message": f"❌ Произошла ошибка при создании проекта: {result.get('error', 'Неизвестная ошибка')}. Попробуем еще раз?",
                        "suggestions": ["Попробовать снова", "Создать другой тип", "Отмена"]
                    }
            else:
                return self.handle_general_stage(message, session_id) # Неожиданный сценарий
        
        elif self.analyze_message(message) == "rejection":
             session["stage"] = "clarifying" # Возвращаемся к уточнениям
             return self.ask_clarification(session["project_type"], session_id)
        
        else: # Если пользователь ответил что-то другое
             return {
                "type": "ai_response",
                "message": f"🤔 Пожалуйста, подтвердите создание приложения '{session['project_details']['name']}' (да/нет) или скажите, если хотите что-то изменить.",
                "suggestions": ["Да, создавай!", "Изменить настройки", "Отмена"]
            }

    def handle_creating_stage(self, message, session_id):
        """Обработка стадии создания проекта (когда проект уже создан)"""
        session = self.user_session[session_id]
        
        if self.analyze_message(message) == "download_request":
            if session.get("current_project_id"):
                return {
                    "type": "ai_response",
                    "message": "📥 Отлично! Вы можете скачать ваш проект по ссылке ниже. После изучения, я готов помочь с доработками!",
                    "download_url": f"/api/download/{session['current_project_id']}",
                    "suggestions": [
                        "🔧 Добавить новые функции",
                        "🔄 Создать новую версию",
                        "✨ Создать другое приложение",
                        "📊 Показать историю версий"
                    ]
                }
            else:
                return {
                    "type": "ai_response",
                    "message": "🙁 Похоже, у вас пока нет созданных проектов. Давайте начнем с создания!",
                    "suggestions": ["Создать игру", "Разработать приложение", "Помоги с идеей"]
                }
        
        elif self.analyze_message(message) == "edit_request":
            session["stage"] = "editing"
            return {
                "type": "ai_response",
                "message": "🔧 Отлично! Что именно вы хотели бы добавить или изменить в вашем приложении?",
                "suggestions": [
                    "Добавить звуковые эффекты",
                    "Создать систему достижений",
                    "Разработать PWA-версию",
                    "Интегрировать аналитику",
                    "Изменить дизайн"
                ]
            }

        elif "верси" in message.lower(): # Запрос на версионность
             if session.get("current_project_id"):
                 project_id = session["current_project_id"]
                 versions = version_control.get_project_versions(project_id)
                 if versions:
                     version_history = "\n".join([f"- v{v['version']}: {v['description']} ({v['timestamp']})" for v in versions])
                     return {
                         "type": "ai_response",
                         "message": f"📜 **История версий вашего проекта '{session['project_details']['name']}':**\n{version_history}\n\nКакую версию вы хотели бы посмотреть или доработать?",
                         "project_id": project_id,
                         "versions": versions,
                         "suggestions": ["Показать код версии X", "Вернуться к последней", "Создать новую версию"]
                     }
                 else:
                     return {
                         "type": "ai_response",
                         "message": "У этого проекта пока нет истории версий.",
                         "suggestions": ["Создать новую версию", "Добавить функции"]
                     }
             else:
                 return {
                     "type": "ai_response",
                     "message": "Сначала нужно создать проект, чтобы вести его версионность.",
                     "suggestions": ["Создать приложение"]
                 }

        else:
            # Возвращаем стандартный ответ, если запрос не распознан
            return self.handle_general_stage(message, session_id)

    def handle_editing_stage(self, message, session_id):
        """Обработка стадии редактирования/добавления функций"""
        session = self.user_session[session_id]
        
        if session.get("current_project_id"):
            project_id = session["current_project_id"]
            
            # Обработка запроса на добавление фичи
            if self.analyze_message(message) == "edit_request":
                # Здесь будет логика вызова advanced_generator.add_feature()
                # Для примера, просто ответим, что функция добавлена
                feature_description = f"Новая функция: '{message}'" # Условное описание
                
                # Логируем запрос на фичу
                interaction_logger.log_event("feature_request", {
                    "project_id": project_id,
                    "feature": message,
                    "user_request": message
                })

                # Попытка добавить фичу (имитация)
                success = advanced_generator.add_feature(project_id, message) # Реальная реализация будет здесь

                if success:
                    # Создание новой версии
                    new_version = version_control.get_next_version(session["project_details"]["type"])
                    version_control.save_project_version(project_id, new_version, [], f"Добавлена функция: {message}")
                    
                    session["stage"] = "created" # Возвращаемся в состояние "создано"
                    
                    return {
                        "type": "ai_response",
                        "message": f"✨ Функция '{message}' успешно добавлена! Создана новая версия {new_version}.\n\nХотите скачать обновленный проект или добавить что-то еще?",
                        "project_id": project_id,
                        "version": new_version,
                        "download_url": f"/api/download/{project_id}",
                        "suggestions": ["📥 Скачать проект", "🔧 Добавить еще", "✨ Создать новое приложение"]
                    }
                else:
                    return {
                        "type": "error",
                        "message": f"❌ Не удалось добавить функцию '{message}'. Попробуйте другую или уточните запрос.",
                        "suggestions": ["Попробовать другую функцию", "Изменить запрос", "Отмена"]
                    }
            else:
                # Если пользователь просто общается, переходим к общему ответу
                return self.handle_general_stage(message, session_id)

        else:
            # Если нет текущего проекта, возвращаемся к началу
            return self.handle_initial_stage(message, "general", session_id)

    def handle_general_stage(self, message, session_id):
        """Обработка общих вопросов и нераспознанных сообщений"""
        session = self.user_session[session_id]

        # Попытка получить ответ от основного AI ассистента
        try:
            ai_response = ai_agent.generate_response(message) # Используем базовый AI
            if ai_response and ai_response.get("type") == "ai_response":
                 # Добавляем стандартные предложения, если они не противоречат ответу AI
                default_suggestions = [
                    "Создать приложение",
                    "Показать тренды",
                    "Помочь с идеей",
                    "Показать мои проекты"
                ]
                
                if "suggestions" not in ai_response or not ai_response["suggestions"]:
                    ai_response["suggestions"] = default_suggestions
                else:
                    # Добавляем, если не дублируются
                    for sug in default_suggestions:
                        if sug not in ai_response["suggestions"]:
                            ai_response["suggestions"].append(sug)
                            
                return ai_response
        except Exception as e:
            print(f"Ошибка при обращении к базовому AI: {e}")

        # Если базовый AI не дал ответа или произошла ошибка
        return {
            "type": "ai_response",
            "message": "🤔 Я здесь, чтобы помочь вам создать отличное приложение! Расскажите, что вас интересует?",
            "suggestions": [
                "Создать игру",
                "Разработать приложение",
                "Показать тренды",
                "Помочь с идеей",
                "Показать мои проекты"
            ]
        }
        
    def show_market_analysis(self):
        """Показывает анализ рынка и трендов"""
        trends_text = "📊 **Анализ рынка мобильных приложений 2024:**\n\n"
        sorted_trends = sorted(self.market_trends.items(), key=lambda item: item[1]['popularity'], reverse=True)
        
        for i, (key, trend) in enumerate(sorted_trends):
            trends_text += f"{i+1}. 📈 **{trend['description']}**\n"
            if trend['examples']:
                trends_text += f"   • Примеры: {', '.join(trend['examples'])}\n"
        
        trends_text += "\n**💡 Совет:** Начните с игры или приложения продуктивности - они имеют высокий потенциал и спрос!"
        
        return {
            "type": "ai_response",
            "message": trends_text,
            "suggestions": [
                "Создать популярную игру",
                "Разработать TODO-приложение", 
                "Показать примеры успешных проектов",
                "Помоги выбрать под мой бюджет"
            ]
        }

# --- API Routes ---

@app.route('/api/chat', methods=['POST'])
def chat():
    """Обработка сообщений чата"""
    data = request.json
    message = data.get('message', '')
    session_id = data.get('session_id', str(uuid.uuid4())) # Генерируем session_id, если не предоставлен

    try:
        # Логируем запрос перед обработкой AI
        interaction_logger.log_incoming_message(session_id, message)
        
        ai_response = ai_agent.generate_personalized_response(message, session_id)
        
        # Логируем ответ AI
        interaction_logger.log_ai_response(session_id, ai_response)
        
        return jsonify(ai_response)
        
    except Exception as e:
        print(f"Ошибка в API /api/chat: {e}")
        interaction_logger.log_error("api_chat_exception", {"session_id": session_id, "error": str(e)})
        
        # Fallback на базовый ответ
        return jsonify({
            "type": "error",
            "message": "🤖 Извините, произошла непредвиденная ошибка. Попробуйте переформулировать ваш запрос.",
            "suggestions": ["Создать приложение", "Получить совет", "Изучить рынок", "Повторить запрос"]
        })

@app.route('/api/generate-project', methods=['POST'])
def generate_project():
    """Генерация проекта (из UI)"""
    data = request.json
    description = data.get('description', '')
    project_name = data.get('project_name', 'Мой проект')
    project_type = data.get('project_type', 'snake_game')
    style = data.get('style', 'modern')
    user_preferences = data.get('preferences', {}) # Получаем предпочтения из UI

    # Создаем запись пользователя, если ее нет
    user_id = data.get('user_id', 'anonymous') # Предполагаем, что есть user_id
    if user_id not in ai_agent.user_session:
         ai_agent.user_session[user_id] = {
             "stage": "created", # Сразу переводим в состояние "создано"
             "current_project_id": None,
             "project_details": {},
             "preferences": user_preferences # Сохраняем предпочтения
         }
    else:
        ai_agent.user_session[user_id]["preferences"].update(user_preferences)

    # Обновляем детали проекта на основе предпочтений
    project_details = {
        "type": project_type,
        "name": project_name,
        "description": description
    }
    if project_type == "game":
        project_details["name"] = f"{style.capitalize()} {project_type.replace('_', ' ').title()} Игра"
        project_details["description"] = f"Увлекательная {project_type.replace('_', ' ')} игра в {style} стиле."
    elif project_type == "productivity":
        project_details["name"] = f"Удобный {project_type.replace('_', ' ').title()}"
        project_details["description"] = f"Приложение для повышения продуктивности."
    elif project_type == "utility":
        project_details["name"] = f"Умный {project_type.replace('_', ' ').title()}"
        project_details["description"] = f"Функциональная утилита."
    
    ai_agent.user_session[user_id]["project_details"] = project_details

    # Логируем старт генерации
    project_version = version_control.get_next_version(project_type)
    log_message = f"Генерация проекта (UI): {project_details['name']} (v{project_version})"
    interaction_logger.log_event("project_creation_start", {**project_details, "version": project_version, "user_id": user_id})

    # Генерируем проект
    result = advanced_generator.generate_project(
        project_type=project_type,
        description=project_details["description"],
        project_name=project_details["name"],
        user_preferences=user_preferences
    )

    if result['success']:
        project_id = result['project_id']
        ai_agent.user_session[user_id]["current_project_id"] = project_id
        
        # Сохраняем версию
        version_control.save_project_version(project_id, project_version, result.get("files", []), log_message)
        interaction_logger.log_event("project_creation_success", {
            "project_id": project_id,
            "project_name": project_details["name"],
            "version": project_version,
            "user_id": user_id
        })
        
        archive_url = f"/api/download/{project_id}"
        result['download_url'] = archive_url
        result['project_id'] = project_id
        result['version'] = project_version
        result['message'] = f"Проект '{project_details['name']}' (v{project_version}) успешно создан!"
    else:
        interaction_logger.log_error("api_generate_project_failed", {"error": result.get('error'), "user_id": user_id})
        result['message'] = f"Ошибка генерации проекта: {result.get('error', 'Неизвестная ошибка')}"

    return jsonify(result)

@app.route('/api/download/<project_id>')
def download_project(project_id):
    """Скачивание проекта"""
    project_path = os.path.join(PROJECTS_DIR, project_id)
    archive_path = os.path.join(TEMP_DIR, f"{project_id}.zip")

    if not os.path.exists(project_path):
        interaction_logger.log_error("download_project_not_found", {"project_id": project_id})
        return jsonify({"error": "Проект не найден"}), 404

    # Создаём архив если его нет
    if not os.path.exists(archive_path):
        try:
            create_project_archive(project_id)
            interaction_logger.log_event("archive_created_on_demand", {"project_id": project_id})
        except Exception as e:
            interaction_logger.log_error("archive_creation_failed_on_demand", {"project_id": project_id, "error": str(e)})
            return jsonify({"error": "Не удалось создать архив"}), 500

    interaction_logger.log_event("project_downloaded", {"project_id": project_id})
    return send_file(archive_path, as_attachment=True, download_name=f"project_{project_id}.zip")

@app.route('/api/projects')
def list_projects():
    """Список проектов пользователя"""
    user_id = request.args.get('user_id', 'anonymous')
    projects = []
    
    user_projects_dir = os.path.join(USER_DATA_DIR, user_id, PROJECTS_DIR)
    os.makedirs(user_projects_dir, exist_ok=True)

    for project_id in os.listdir(user_projects_dir):
        project_path = os.path.join(user_projects_dir, project_id)
        if os.path.isdir(project_path):
            try:
                project_info_path = os.path.join(project_path, "project_info.json")
                if os.path.exists(project_info_path):
                    with open(project_info_path, 'r') as f:
                        info = json.load(f)
                        projects.append({
                            "id": project_id,
                            "name": info.get("name", f"Проект {project_id[:8]}"),
                            "type": info.get("type", "unknown"),
                            "created_at": info.get("created_at", datetime.fromtimestamp(os.path.getctime(project_path)).isoformat())
                        })
                else: # Fallback, если info нет
                    projects.append({
                        "id": project_id,
                        "name": f"Проект {project_id[:8]}",
                        "type": "unknown",
                        "created_at": datetime.fromtimestamp(os.path.getctime(project_path)).isoformat()
                    })
            except Exception as e:
                print(f"Ошибка чтения информации о проекте {project_id}: {e}")
                interaction_logger.log_error("api_list_projects_read_error", {"project_id": project_id, "error": str(e)})

    interaction_logger.log_event("api_projects_list_requested", {"user_id": user_id, "count": len(projects)})
    return jsonify({"projects": projects})
    
@app.route('/api/project/versions/<project_id>')
def get_project_versions(project_id):
    """Получить историю версий проекта"""
    versions = version_control.get_project_versions(project_id)
    if versions is None:
        interaction_logger.log_error("api_get_versions_not_found", {"project_id": project_id})
        return jsonify({"error": "Проект или его версии не найдены"}), 404
    
    interaction_logger.log_event("api_get_project_versions", {"project_id": project_id, "count": len(versions)})
    return jsonify({"versions": versions})

@app.route('/api/project/revert/<project_id>', methods=['POST'])
def revert_project_version(project_id):
    """Откатить проект к предыдущей версии"""
    data = request.json
    target_version = data.get('version') # Номер версии для отката

    if not target_version:
        return jsonify({"error": "Не указана версия для отката"}), 400

    # Логика отката через version_control
    success = version_control.revert_project(project_id, target_version)

    if success:
        interaction_logger.log_event("project_reverted", {"project_id": project_id, "version": target_version})
        return jsonify({"success": True, "message": f"Проект успешно откачен до версии {target_version}"})
    else:
        interaction_logger.log_error("api_revert_project_failed", {"project_id": project_id, "version": target_version})
        return jsonify({"success": False, "error": "Не удалось откатить проект"}), 500

@app.route('/api/ai/status')
def get_ai_status():
    """Получить статус AI сервисов"""
    return jsonify({
        "available_services": [
            {
                "name": "SuperSmartAI",
                "enabled": True,
                "configured": True
            },
            {
                "name": "SmartNLP",
                "enabled": True,
                "configured": True
            },
            {
                "name": "ProjectVersionControl",
                "enabled": True,
                "configured": True
            },
            {
                "name": "UserInteractionLogger",
                "enabled": True,
                "configured": True
            },
            {
                "name": "AdvancedProjectGenerator",
                "enabled": True,
                "configured": True
            }
        ],
        "current_ai": "SuperSmartAI",
        "configured": True
    })
    
@app.route('/api/logs/interaction', methods=['POST'])
def log_interaction_api():
    """API для логирования пользовательских взаимодействий"""
    data = request.json
    session_id = data.get('session_id')
    event_type = data.get('event_type')
    payload = data.get('payload')
    
    if not session_id or not event_type:
        return jsonify({"error": "Отсутствуют обязательные поля: session_id, event_type"}), 400
        
    interaction_logger.log_event(event_type, payload, session_id)
    return jsonify({"success": True, "message": "Событие залогировано"})

# --- WebSocket ---
@socketio.on('connect')
def handle_connect():
    print('Клиент подключился')

@socketio.on('disconnect')
def handle_disconnect():
    print('Клиент отключился')

@socketio.on('generate_project_ws')
def handle_project_generation_ws(data):
    """Обработка генерации проекта через WebSocket"""
    session_id = data.get('session_id', str(uuid.uuid4()))
    project_type = data.get('project_type', 'snake_game')
    description = data.get('description', '')
    project_name = data.get('project_name', 'Мой проект')
    preferences = data.get('preferences', {})

    # Используем AI для получения деталей проекта, если они не предоставлены
    if not description or not project_name:
        # Здесь можно было бы вызвать AI для генерации деталей, но для примера используем стандартные
        project_name = f"{project_type.capitalize()} от AI"
        description = f"Базовая версия {project_type.replace('_', ' ')}."

    # Создаем проект через AI ассистента, имитируя запрос
    ai_response = ai_agent.generate_personalized_response(f"Создай {project_type}", session_id)
    
    if ai_response.get("type") == "project_created":
        emit('project_status', {
            'status': 'completed',
            'project_id': ai_response['project_id'],
            'download_url': ai_response['download_url'],
            'message': ai_response['message'],
            'version': ai_response.get('version', 1)
        }, room=request.sid) # Отправляем ответ обратно клиенту
    else:
        emit('project_status', {
            'status': 'error',
            'message': ai_response.get('message', 'Не удалось создать проект')
        }, room=request.sid)

# --- Вспомогательные функции ---
def create_project_archive(project_id):
    """Создаёт zip-архив проекта"""
    project_path = os.path.join(PROJECTS_DIR, project_id)
    archive_path = os.path.join(TEMP_DIR, f"{project_id}.zip")

    if not os.path.exists(project_path):
        raise FileNotFoundError(f"Директория проекта не найдена: {project_path}")

    try:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_path)
                    zipf.write(file_path, arcname)
        return archive_path
    except Exception as e:
        interaction_logger.log_error("create_project_archive_failed", {"project_id": project_id, "error": str(e)})
        raise

if __name__ == '__main__':
    print("🚀 Запускаю Lovable AI Platform...")
    print("📍 Backend: http://0.0.0.0:5000")
    print("🔌 WebSocket: ws://0.0.0.0:5000")
    print("💡 Для остановки нажмите Ctrl+C")
    print("=" * 50)

    socketio.run(app, host='0.0.0.0', port=5000, debug=True)