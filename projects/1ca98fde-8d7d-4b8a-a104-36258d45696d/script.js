class SnakeGame {
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
});