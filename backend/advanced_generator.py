
import uuid
import os
from datetime import datetime
from typing import Dict, List, Any

class AdvancedProjectGenerator:
    def __init__(self):
        self.templates = {
            # Сложные приложения
            "crm_system": {
                "name": "CRM Система",
                "description": "Полноценная CRM с аналитикой",
                "complexity": "enterprise",
                "technologies": ["React", "Node.js", "PostgreSQL", "Redis"],
                "features": ["Управление клиентами", "Аналитика", "Отчеты", "API"]
            },
            "ecommerce_platform": {
                "name": "E-commerce Платформа", 
                "description": "Интернет-магазин с админкой",
                "complexity": "high",
                "technologies": ["Vue.js", "Express", "MongoDB", "Stripe"],
                "features": ["Каталог", "Корзина", "Платежи", "Админка"]
            },
            "social_network": {
                "name": "Социальная Сеть",
                "description": "Мини соцсеть с чатами",
                "complexity": "high", 
                "technologies": ["React", "Socket.io", "MongoDB", "JWT"],
                "features": ["Профили", "Посты", "Чаты", "Лайки"]
            },
            "ai_dashboard": {
                "name": "AI Дашборд",
                "description": "Панель с AI аналитикой",
                "complexity": "high",
                "technologies": ["React", "Python", "TensorFlow", "Chart.js"],
                "features": ["ML модели", "Визуализация", "Предсказания", "API"]
            },
            # Сайты и лендинги
            "business_landing": {
                "name": "Бизнес Лендинг",
                "description": "Корпоративный сайт с CRM интеграцией",
                "complexity": "medium",
                "technologies": ["HTML5", "CSS3", "JavaScript", "PHP"],
                "features": ["Адаптивность", "Формы", "SEO", "Аналитика"]
            },
            "portfolio_site": {
                "name": "Портфолио Сайт",
                "description": "Персональное портфолио с галереей",
                "complexity": "medium", 
                "technologies": ["Next.js", "Tailwind", "Framer Motion"],
                "features": ["Галерея", "Блог", "Контакты", "Анимации"]
            }
        }

    def generate_complex_project(self, project_type: str, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Генерирует сложный проект"""
        if project_type not in self.templates:
            project_type = "crm_system"  # По умолчанию
        
        template = self.templates[project_type]
        project_id = str(uuid.uuid4())
        
        # Генерируем структуру проекта
        project_structure = self._generate_project_structure(template, requirements)
        
        # Создаем файлы
        files = self._generate_project_files(template, project_structure, requirements)
        
        return {
            "success": True,
            "project_id": project_id,
            "template": template,
            "structure": project_structure,
            "files": files,
            "setup_instructions": self._generate_setup_instructions(template),
            "deployment_config": self._generate_deployment_config(template)
        }

    def _generate_project_structure(self, template: Dict, requirements: Dict) -> Dict:
        """Генерирует структуру проекта"""
        base_structure = {
            "frontend": {
                "src": ["components", "pages", "hooks", "utils", "styles"],
                "public": ["images", "icons"],
                "config": ["package.json", "vite.config.js"]
            },
            "backend": {
                "src": ["controllers", "models", "routes", "middleware", "utils"],
                "config": ["database.js", "server.js"],
                "tests": ["unit", "integration"]
            },
            "database": {
                "migrations": [],
                "seeds": [],
                "schema": []
            },
            "docs": ["API.md", "SETUP.md", "DEPLOY.md"]
        }
        
        # Адаптируем под сложность
        if template["complexity"] == "enterprise":
            base_structure["microservices"] = {
                "auth-service": ["src", "config", "tests"],
                "user-service": ["src", "config", "tests"],
                "notification-service": ["src", "config", "tests"]
            }
            base_structure["infrastructure"] = {
                "docker": ["Dockerfile", "docker-compose.yml"],
                "kubernetes": ["deployments", "services", "configmaps"],
                "monitoring": ["prometheus", "grafana"]
            }
        
        return base_structure

    def _generate_project_files(self, template: Dict, structure: Dict, requirements: Dict) -> Dict[str, str]:
        """Генерирует файлы проекта"""
        files = {}
        
        # Frontend файлы
        if "React" in template["technologies"]:
            files.update(self._generate_react_files(template, requirements))
        elif "Vue.js" in template["technologies"]:
            files.update(self._generate_vue_files(template, requirements))
        else:
            files.update(self._generate_vanilla_files(template, requirements))
        
        # Backend файлы
        if "Node.js" in template["technologies"]:
            files.update(self._generate_nodejs_files(template, requirements))
        elif "Python" in template["technologies"]:
            files.update(self._generate_python_files(template, requirements))
        
        # Database файлы
        if "PostgreSQL" in template["technologies"]:
            files.update(self._generate_postgres_files(template))
        elif "MongoDB" in template["technologies"]:
            files.update(self._generate_mongo_files(template))
        
        # Конфигурационные файлы
        files.update(self._generate_config_files(template))
        
        return files

    def _generate_react_files(self, template: Dict, requirements: Dict) -> Dict[str, str]:
        """Генерирует React приложение"""
        return {
            "frontend/src/App.jsx": self._get_react_app_template(template, requirements),
            "frontend/src/main.jsx": self._get_react_main_template(),
            "frontend/src/components/Dashboard.jsx": self._get_dashboard_component(template),
            "frontend/src/components/Sidebar.jsx": self._get_sidebar_component(template),
            "frontend/src/hooks/useAuth.js": self._get_auth_hook(),
            "frontend/src/utils/api.js": self._get_api_utils(),
            "frontend/package.json": self._get_react_package_json(template),
            "frontend/vite.config.js": self._get_vite_config(),
            "frontend/index.html": self._get_react_html_template(template)
        }

    def _generate_nodejs_files(self, template: Dict, requirements: Dict) -> Dict[str, str]:
        """Генерирует Node.js backend"""
        return {
            "backend/server.js": self._get_nodejs_server_template(template),
            "backend/src/controllers/authController.js": self._get_auth_controller(),
            "backend/src/controllers/userController.js": self._get_user_controller(),
            "backend/src/models/User.js": self._get_user_model(template),
            "backend/src/routes/auth.js": self._get_auth_routes(),
            "backend/src/routes/users.js": self._get_user_routes(),
            "backend/src/middleware/auth.js": self._get_auth_middleware(),
            "backend/src/utils/database.js": self._get_database_utils(template),
            "backend/package.json": self._get_nodejs_package_json(template),
            "backend/.env.example": self._get_env_example(template)
        }

    def _get_react_app_template(self, template: Dict, requirements: Dict) -> str:
        return f'''import React, {{ useState, useEffect }} from 'react';
import {{ BrowserRouter as Router, Routes, Route, Navigate }} from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Sidebar from './components/Sidebar';
import Login from './components/Login';
import {{ useAuth }} from './hooks/useAuth';
import './App.css';

function App() {{
  const {{ user, login, logout, loading }} = useAuth();
  
  if (loading) {{
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <h2>Загрузка {template['name']}...</h2>
      </div>
    );
  }}

  return (
    <Router>
      <div className="app">
        {{user ? (
          <div className="app-layout">
            <Sidebar user={{user}} onLogout={{logout}} />
            <main className="main-content">
              <Routes>
                <Route path="/" element={{<Dashboard />}} />
                <Route path="/dashboard" element={{<Dashboard />}} />
                <Route path="*" element={{<Navigate to="/dashboard" replace />}} />
              </Routes>
            </main>
          </div>
        ) : (
          <Login onLogin={{login}} />
        )}}
      </div>
    </Router>
  );
}}

export default App;'''

    def _get_nodejs_server_template(self, template: Dict) -> str:
        return f'''const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const mongoose = require('mongoose');
require('dotenv').config();

const authRoutes = require('./src/routes/auth');
const userRoutes = require('./src/routes/users');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(helmet());
app.use(cors({{
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}}));

// Rate limiting
const limiter = rateLimit({{
  windowMs: 15 * 60 * 1000, // 15 минут
  max: 100 // максимум 100 запросов с одного IP
}});
app.use(limiter);

app.use(express.json({{ limit: '10mb' }}));
app.use(express.urlencoded({{ extended: true }}));

// Database connection
mongoose.connect(process.env.MONGODB_URI || 'mongodb://localhost:27017/{template['name'].lower().replace(' ', '_')}', {{
  useNewUrlParser: true,
  useUnifiedTopology: true,
}})
.then(() => console.log('📦 База данных подключена'))
.catch(err => console.error('❌ Ошибка подключения к БД:', err));

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);

// Health check
app.get('/api/health', (req, res) => {{
  res.json({{ 
    status: 'OK', 
    service: '{template['name']}',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  }});
}});

// Error handling middleware
app.use((err, req, res, next) => {{
  console.error('🚨 Ошибка сервера:', err);
  res.status(500).json({{ 
    error: 'Внутренняя ошибка сервера',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Что-то пошло не так'
  }});
}});

// 404 handler
app.use('*', (req, res) => {{
  res.status(404).json({{ error: 'Эндпоинт не найден' }});
}});

app.listen(PORT, '0.0.0.0', () => {{
  console.log(`🚀 {template['name']} запущен на порту ${{PORT}}`);
  console.log(`📍 Сервер доступен по адресу: http://0.0.0.0:${{PORT}}`);
}});

module.exports = app;'''

    def _generate_setup_instructions(self, template: Dict) -> List[str]:
        """Генерирует инструкции по установке"""
        instructions = [
            "🚀 Инструкции по запуску проекта",
            "",
            "1. Установка зависимостей:",
            "   cd frontend && npm install",
            "   cd ../backend && npm install",
            "",
            "2. Настройка окружения:",
            "   cp backend/.env.example backend/.env",
            "   # Заполните переменные окружения",
            "",
            "3. Запуск базы данных:",
        ]
        
        if "PostgreSQL" in template["technologies"]:
            instructions.extend([
                "   # Установите PostgreSQL",
                "   createdb " + template["name"].lower().replace(' ', '_'),
            ])
        elif "MongoDB" in template["technologies"]:
            instructions.extend([
                "   # Установите MongoDB",
                "   mongod --dbpath ./data",
            ])
        
        instructions.extend([
            "",
            "4. Запуск приложения:",
            "   # В первом терминале:",
            "   cd backend && npm run dev",
            "",
            "   # Во втором терминале:",
            "   cd frontend && npm run dev",
            "",
            "5. Откройте http://localhost:3000",
            "",
            "🎯 Готово! Ваше приложение запущено!"
        ])
        
        return instructions

    def _generate_deployment_config(self, template: Dict) -> Dict[str, Any]:
        """Генерирует конфигурацию для деплоя"""
        return {
            "replit": {
                "build_command": "cd frontend && npm run build",
                "run_command": "cd backend && npm start",
                "environment": {
                    "NODE_ENV": "production",
                    "PORT": "5000"
                }
            },
            "docker": {
                "frontend": {
                    "image": "node:18-alpine",
                    "build_context": "./frontend",
                    "port": 3000
                },
                "backend": {
                    "image": "node:18-alpine", 
                    "build_context": "./backend",
                    "port": 5000
                }
            },
            "security": {
                "rate_limiting": True,
                "cors_enabled": True,
                "helmet_protection": True,
                "input_validation": True
            }
        }

    # Placeholder methods для других компонентов
    def _get_react_main_template(self) -> str:
        return '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)'''

    def _get_dashboard_component(self, template: Dict) -> str:
        return f'''import React, {{ useState, useEffect }} from 'react';

const Dashboard = () => {{
  const [stats, setStats] = useState({{
    totalUsers: 0,
    activeProjects: 0,
    revenue: 0
  }});

  useEffect(() => {{
    // Загрузка статистики
    fetchStats();
  }}, []);

  const fetchStats = async () => {{
    try {{
      const response = await fetch('/api/stats');
      const data = await response.json();
      setStats(data);
    }} catch (error) {{
      console.error('Ошибка загрузки статистики:', error);
    }}
  }};

  return (
    <div className="dashboard">
      <h1>Панель управления - {template['name']}</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Пользователи</h3>
          <p className="stat-number">{{stats.totalUsers}}</p>
        </div>
        
        <div className="stat-card">
          <h3>Активные проекты</h3>
          <p className="stat-number">{{stats.activeProjects}}</p>
        </div>
        
        <div className="stat-card">
          <h3>Доход</h3>
          <p className="stat-number">${{stats.revenue}}</p>
        </div>
      </div>
      
      <div className="features-grid">
        [feature for index, feature in enumerate(template['features'])]
          <div key={{index}} className="feature-card">
            <h4>{{feature}}</h4>
            <p>Функция доступна</p>
          </div>
        ))
      </div>
    </div>
  );
}};

export default Dashboard;'''

    # Добавляю остальные методы...
    def _get_sidebar_component(self, template: Dict) -> str:
        return "// Sidebar component placeholder"
    
    def _get_auth_hook(self) -> str:
        return "// Auth hook placeholder"
    
    def _get_api_utils(self) -> str:
        return "// API utils placeholder"
    
    def _get_react_package_json(self, template: Dict) -> str:
        return "// React package.json placeholder"
    
    def _get_vite_config(self) -> str:
        return "// Vite config placeholder"
    
    def _get_react_html_template(self, template: Dict) -> str:
        return "// React HTML template placeholder"
    
    def _get_auth_controller(self) -> str:
        return "// Auth controller placeholder"
    
    def _get_user_controller(self) -> str:
        return "// User controller placeholder"
    
    def _get_user_model(self, template: Dict) -> str:
        return "// User model placeholder"
    
    def _get_auth_routes(self) -> str:
        return "// Auth routes placeholder"
    
    def _get_user_routes(self) -> str:
        return "// User routes placeholder"
    
    def _get_auth_middleware(self) -> str:
        return "// Auth middleware placeholder"
    
    def _get_database_utils(self, template: Dict) -> str:
        return "// Database utils placeholder"
    
    def _get_nodejs_package_json(self, template: Dict) -> str:
        return "// Node.js package.json placeholder"
    
    def _get_env_example(self, template: Dict) -> str:
        return "// .env.example placeholder"
    
    def _generate_vue_files(self, template: Dict, requirements: Dict) -> Dict[str, str]:
        return {}
    
    def _generate_vanilla_files(self, template: Dict, requirements: Dict) -> Dict[str, str]:
        return {}
    
    def _generate_python_files(self, template: Dict, requirements: Dict) -> Dict[str, str]:
        return {}
    
    def _generate_postgres_files(self, template: Dict) -> Dict[str, str]:
        return {}
    
    def _generate_mongo_files(self, template: Dict) -> Dict[str, str]:
        return {}
    
    def _generate_config_files(self, template: Dict) -> Dict[str, str]:
        return {}
