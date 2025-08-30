// Lovable AI Platform - Enhanced JavaScript with Backend Integration
console.log('💻 Vibecode AI Platform loaded!');

// Конфигурация для Replit
const API_BASE_URL = window.location.origin;  // Используем текущий домен
const WS_URL = window.location.origin;        // WebSocket на том же домене

// Глобальные переменные
let isTyping = false;
let socket = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    checkBackendHealth();
});

// Проверка работоспособности backend
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('✅ Backend статус:', data);
        showNotification('🤖 AI система готова к работе!', 'success');
    } catch (error) {
        console.warn('⚠️ Backend недоступен:', error);
        showNotification('⚠️ Режим оффлайн - некоторые функции могут быть ограничены', 'info');
    }
}

// Основная функция инициализации
function initializeApp() {
    setupNavigation();
    setupChatInterface();
    setupAnimations();
    setupScrollEffects();
    setupWebSocket();
}

// Функции для кнопок
// Функция для начала создания (перенаправление в личный кабинет)
window.startCreating = function() {
    console.log('🚀 Перенаправляем в личный кабинет...');

    // Проверяем, авторизован ли пользователь
    checkAuthAndRedirect();
};

async function checkAuthAndRedirect() {
    try {
        const response = await fetch('/api/user/profile');
        if (response.ok) {
            // Пользователь авторизован - перенаправляем в личный кабинет
            window.location.href = '/dashboard';
        } else {
            // Пользователь не авторизован - перенаправляем на страницу входа
            window.location.href = '/auth';
        }
    } catch (error) {
        // В случае ошибки перенаправляем на страницу входа
        window.location.href = '/auth';
    }
}

window.startFreeTrial = function() {
    console.log('🚀 Начинаем бесплатную пробу...');

    // Сначала показываем форму предварительного сбора данных
    showPreRegistrationForm();
};

// Форма предварительного сбора данных как у Lovable
function showPreRegistrationForm() {
    const modal = document.createElement('div');
    modal.className = 'pre-registration-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closePreRegistrationModal()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="modal-header">
                    <h2>🚀 Расскажите о себе</h2>
                    <button class="modal-close" onclick="closePreRegistrationModal()">&times;</button>
                    <p style="color: rgba(255, 255, 255, 0.8); margin: 10px 0 0 0;">Помогите нам создать лучший опыт для вас</p>
                </div>
                <div class="modal-body">
                    <form id="preRegistrationForm" class="pre-registration-form">
                        <div class="form-group">
                            <label for="userRole">Кто вы? *</label>
                            <select id="userRole" required>
                                <option value="">Выберите роль</option>
                                <option value="developer">Разработчик</option>
                                <option value="designer">Дизайнер</option>
                                <option value="entrepreneur">Предприниматель</option>
                                <option value="student">Студент</option>
                                <option value="freelancer">Фрилансер</option>
                                <option value="manager">Менеджер продукта</option>
                                <option value="other">Другое</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="experienceLevel">Уровень опыта в разработке? *</label>
                            <select id="experienceLevel" required>
                                <option value="">Выберите уровень</option>
                                <option value="beginner">Новичок (без опыта)</option>
                                <option value="intermediate">Средний (1-3 года)</option>
                                <option value="advanced">Продвинутый (3+ лет)</option>
                                <option value="expert">Эксперт (5+ лет)</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="projectType">Что планируете создавать? *</label>
                            <select id="projectType" required>
                                <option value="">Выберите тип проекта</option>
                                <option value="landing">Лендинги</option>
                                <option value="ecommerce">Интернет-магазины</option>
                                <option value="webapp">Веб-приложения</option>
                                <option value="portfolio">Портфолио</option>
                                <option value="blog">Блоги</option>
                                <option value="business">Корпоративные сайты</option>
                                <option value="startup">Стартап MVP</option>
                                <option value="other">Другое</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="teamSize">Размер команды? *</label>
                            <select id="teamSize" required>
                                <option value="">Выберите размер</option>
                                <option value="solo">Работаю один</option>
                                <option value="small">2-5 человек</option>
                                <option value="medium">6-20 человек</option>
                                <option value="large">20+ человек</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="hearAbout">Как узнали о нас?</label>
                            <select id="hearAbout">
                                <option value="">Выберите источник</option>
                                <option value="search">Поиск Google</option>
                                <option value="social">Социальные сети</option>
                                <option value="youtube">YouTube</option>
                                <option value="friend">Рекомендация друга</option>
                                <option value="blog">Блог/статья</option>
                                <option value="ads">Реклама</option>
                                <option value="other">Другое</option>
                            </select>
                        </div>

                        <button type="submit" class="btn-primary" id="preRegisterBtn">
                            <span>Продолжить регистрацию</span>
                            <div class="btn-glow"></div>
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(modal);

    // Обработчик формы предварительной регистрации
    document.getElementById('preRegistrationForm').addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = {
            userRole: document.getElementById('userRole').value,
            experienceLevel: document.getElementById('experienceLevel').value,
            projectType: document.getElementById('projectType').value,
            teamSize: document.getElementById('teamSize').value,
            hearAbout: document.getElementById('hearAbout').value,
            timestamp: new Date().toISOString()
        };

        // Сохраняем данные для аналитики
        savePreRegistrationData(formData);
        
        // Сразу закрываем предварительную форму и показываем регистрацию
        modal.remove();
        showRegistrationForm();
    });
}

// Сохранение данных предварительной регистрации
async function savePreRegistrationData(data) {
    try {
        await fetch('/api/pre-registration', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        console.log('📊 Данные предварительной регистрации сохранены:', data);
    } catch (error) {
        console.error('Ошибка сохранения данных:', error);
    }
}

// Показать основную форму регистрации
function showRegistrationForm() {
    // Создаем модальное окно для регистрации с российской спецификой
    const modal = document.createElement('div');
    modal.className = 'signup-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>🇷🇺 Регистрация в Vibecode</h2>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <!-- Преимущества регистрации -->
                    <div class="registration-benefits">
                        <div class="benefit-highlight">
                            ✅ Первый проект бесплатно<br>
                            ✅ Российские серверы<br>
                            ✅ Поддержка на русском языке
                        </div>
                    </div>

                    <form id="signupForm" class="signup-form">
                        <div class="form-group">
                            <label for="email">📧 Email или телефон</label>
                            <input type="text" id="email" required placeholder="example@mail.ru или +7 (999) 123-45-67">
                            <div class="field-help">Мы поддерживаем российские почтовые сервисы</div>
                        </div>
                        <div class="form-group">
                            <label for="password">🔒 Пароль</label>
                            <input type="password" id="password" required placeholder="Минимум 8 символов">
                            <div class="password-strength" id="passwordStrength"></div>
                        </div>
                        <div class="form-group">
                            <label for="name">👤 Как к вам обращаться?</label>
                            <input type="text" id="name" required placeholder="Имя или название компании">
                        </div>
                        <div class="form-group">
                            <label for="businessType">🏢 Тип деятельности</label>
                            <select id="businessType" required>
                                <option value="">Выберите направление</option>
                                <option value="startup">Стартап / MVP</option>
                                <option value="freelance">Фриланс / Веб-студия</option>
                                <option value="corporate">Корпоративный клиент</option>
                                <option value="education">Образование</option>
                                <option value="personal">Личные проекты</option>
                            </select>
                        </div>

                        <!-- Согласие на обработку данных -->
                        <div class="form-group checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="dataProcessing" required>
                                <span class="checkmark"></span>
                                Согласен на <a href="#" onclick="showPrivacyPolicy()">обработку персональных данных</a> согласно 152-ФЗ
                            </label>
                        </div>

                        <div class="form-group checkbox-group">
                            <label class="checkbox-label">
                                <input type="checkbox" id="marketing">
                                <span class="checkmark"></span>
                                Хочу получать полезные материалы о разработке (не чаще 1 раза в неделю)
                            </label>
                        </div>

                        <button type="submit" class="btn-primary" id="submitBtn">
                            <span>🚀 Начать бесплатно</span>
                            <div class="btn-glow"></div>
                        </button>

                        <!-- Индикаторы доверия -->
                        <div class="trust-indicators">
                            <div class="trust-item">🔒 SSL шифрование</div>
                            <div class="trust-item">🇷🇺 Российские серверы</div>
                            <div class="trust-item">⚡ Мгновенная активация</div>
                        </div>
                    </form>

                    <div class="modal-footer">
                        <p>Уже есть аккаунт? <a href="#" onclick="showLogin()">Войти в систему</a></p>
                        <div class="payment-methods">
                            <small>Принимаем: Мир, Visa, Mastercard, СБП</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Добавляем стили для модального окна
    const style = document.createElement('style');
    style.textContent = `
                 .signup-modal {
             position: fixed;
             top: 0;
             left: 0;
             width: 100%;
             height: 100%;
             z-index: 10000;
             display: flex;
             align-items: center;
             justify-content: center;
             background: rgba(0, 0, 0, 0.8);
             backdrop-filter: blur(10px);
         }
        .modal-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
        }
        .modal-content {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            padding: 30px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
            position: relative;
            z-index: 10001;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .modal-header h2 {
            color: white;
            margin: 0;
            font-size: 24px;
        }
        .modal-close {
            background: none;
            border: none;
            color: white;
            font-size: 24px;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            transition: background 0.3s;
        }
        .modal-close:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        .signup-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .form-group label {
            color: white;
            font-weight: 500;
            font-size: 14px;
        }
        .form-group input {
            padding: 12px 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.05);
            color: white;
            font-size: 16px;
            transition: all 0.3s;
        }
        .form-group input:focus {
            outline: none;
            border-color: #6366f1;
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        .form-group input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        .modal-footer {
            margin-top: 20px;
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
        }
        .modal-footer a {
            color: #6366f1;
            text-decoration: none;
            font-weight: 500;
        }
        .modal-footer a:hover {
            text-decoration: underline;
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(modal);

    // Валидация пароля в реальном времени
    const passwordInput = document.getElementById('password');
    const strengthIndicator = document.getElementById('passwordStrength');

    passwordInput.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        let feedback = [];

        if (password.length >= 8) strength++;
        else feedback.push('минимум 8 символов');

        if (/[A-Z]/.test(password)) strength++;
        else feedback.push('заглавная буква');

        if (/[0-9]/.test(password)) strength++;
        else feedback.push('цифра');

        if (/[^A-Za-z0-9]/.test(password)) strength++;
        else feedback.push('специальный символ');

        const colors = ['#ef4444', '#f59e0b', '#eab308', '#22c55e'];
        const texts = ['Слабый', 'Средний', 'Хороший', 'Отличный'];

        strengthIndicator.style.color = colors[strength - 1] || '#ef4444';
        strengthIndicator.textContent = strength > 0 ? `${texts[strength - 1]} пароль` : '';

        if (feedback.length > 0 && password.length > 0) {
            strengthIndicator.textContent += ` (нужно: ${feedback.join(', ')})`;
        }
    });

    // Обработчик формы с валидацией
    document.getElementById('signupForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const submitBtn = document.getElementById('submitBtn');
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const name = document.getElementById('name').value;
        const businessType = document.getElementById('businessType').value;
        const dataProcessing = document.getElementById('dataProcessing').checked;

        // Валидация
        if (!validateEmail(email) && !validatePhone(email)) {
            showNotification('❌ Введите корректный email или телефон', 'error');
            return;
        }

        if (password.length < 8) {
            showNotification('❌ Пароль должен содержать минимум 8 символов', 'error');
            return;
        }

        if (!businessType) {
            showNotification('❌ Выберите тип деятельности', 'error');
            return;
        }

        if (!dataProcessing) {
            showNotification('❌ Необходимо согласие на обработку данных', 'error');
            return;
        }

        // Анимация загрузки
        submitBtn.innerHTML = `
            <span>Создаем аккаунт...</span>
            <div class="loading-spinner"></div>
        `;
        submitBtn.disabled = true;

        console.log('📝 Регистрация:', { email, name, businessType });

        // Симуляция запроса к серверу
        setTimeout(() => {
            showNotification('✅ Добро пожаловать в Vibecode! Проверьте почту для подтверждения', 'success');

            // Аналитика для определения аудитории
            trackUserRegistration(businessType, email);

            // Показываем онбординг БЕЗ автозакрытия модального окна
            showOnboarding(businessType);
        }, 2000);
    });

    // Функции валидации
    function validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function validatePhone(phone) {
        const phoneRegex = /^\+?7[\s\-]?\(?9\d{2}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }

    function trackUserRegistration(businessType, contact) {
        // Отправляем данные для анализа аудитории
        console.log('📊 Аналитика пользователя:', {
            segment: businessType,
            contact_type: validateEmail(contact) ? 'email' : 'phone',
            timestamp: new Date().toISOString()
        });
    }
};

window.showDemo = function() {
    console.log('🎬 Показываем демо...');
    // Прокручиваем к демо разделу
    const demoSection = document.getElementById('demo');
    if (demoSection) {
        demoSection.scrollIntoView({ behavior: 'smooth' });

        // Запускаем демо анимацию через небольшую задержку
        setTimeout(() => {
            startDemoAnimation();
        }, 1000);
    }
};

window.closeModal = function() {
    const signupModal = document.querySelector('.signup-modal');
    const loginModal = document.querySelector('.login-modal');
    const preRegModal = document.querySelector('.pre-registration-modal');

    if (signupModal) {
        signupModal.remove();
    }
    if (loginModal) {
        loginModal.remove();
    }
    if (preRegModal) {
        preRegModal.remove();
    }
};

window.closePreRegistrationModal = function() {
    const preRegModal = document.querySelector('.pre-registration-modal');
    if (preRegModal) {
        preRegModal.remove();
    }
};

window.showLogin = function() {
    console.log('🔐 Показываем форму входа...');

    // Создаем модальное окно для входа
    const modal = document.createElement('div');
    modal.className = 'login-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Вход</h2>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <form id="loginForm" class="login-form">
                        <div class="form-group">
                            <label for="loginEmail">Email</label>
                            <input type="email" id="loginEmail" required placeholder="your@email.com">
                        </div>
                        <div class="form-group">
                            <label for="loginPassword">Пароль</label>
                            <input type="password" id="loginPassword" required placeholder="Введите пароль">
                        </div>
                        <button type="submit" class="btn-primary">
                            <span>Войти</span>
                            <div class="btn-glow"></div>
                        </button>
                    </form>
                    <div class="modal-footer">
                        <p>Нет аккаунта? <a href="#" onclick="showSignup()">Регистрация</a></p>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Добавляем стили для модального окна входа
    const style = document.createElement('style');
    style.textContent = `
        .login-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(10px);
        }
        .login-form {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
    `;

    document.head.appendChild(style);
    document.body.appendChild(modal);

    // Обработчик формы входа
    document.getElementById('loginForm').addEventListener('submit', function(e) {
        e.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        console.log('🔐 Вход:', { email });

        // Здесь можно добавить реальную логику входа
        showNotification('✅ Вход выполнен успешно!', 'success');

        setTimeout(() => {
            closeModal();
            // Перенаправляем на главную страницу или дашборд
            window.location.href = '#chat';
        }, 2000);
    });
};

window.showSignup = function() {
    // Закрываем текущее модальное окно и показываем регистрацию
    closeModal();
    setTimeout(() => {
        startFreeTrial();
    }, 300);
};

// Показать политику конфиденциальности
window.showPrivacyPolicy = function() {
    const modal = document.createElement('div');
    modal.className = 'privacy-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content" style="max-width: 600px; max-height: 80vh; overflow-y: auto;">
                <div class="modal-header">
                    <h2>🔒 Политика конфиденциальности</h2>
                    <button class="modal-close" onclick="closeModal()">&times;</button>
                </div>
                <div class="modal-body">
                    <div class="privacy-content">
                        <h3>Обработка персональных данных</h3>
                        <p>ООО "Vibecode" (далее - Компания) обязуется обеспечить конфиденциальность персональных данных в соответствии с 152-ФЗ "О персональных данных".</p>

                        <h4>Какие данные мы собираем:</h4>
                        <ul>
                            <li>Контактная информация (email, телефон)</li>
                            <li>Имя и тип деятельности</li>
                            <li>Техническая информация о использовании сервиса</li>
                        </ul>

                        <h4>Как мы используем данные:</h4>
                        <ul>
                            <li>Предоставление услуг платформы</li>
                            <li>Техническая поддержка</li>
                            <li>Улучшение сервиса</li>
                            <li>Информирование о новых возможностях (с вашего согласия)</li>
                        </ul>

                        <h4>Безопасность:</h4>
                        <p>Данные хранятся на серверах в России с применением современных методов шифрования. Доступ к данным имеют только уполномоченные сотрудники.</p>

                        <h4>Ваши права:</h4>
                        <ul>
                            <li>Получение информации об обработке ваших данных</li>
                            <li>Внесение изменений в данные</li>
                            <li>Удаление данных (право на забвение)</li>
                            <li>Ограничение обработки</li>
                        </ul>

                        <p><strong>Контакты:</strong> privacy@vibecode.ru, +7 (495) 123-45-67</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
};

// Онбординг для разных типов пользователей
window.showOnboarding = function(businessType) {
    const onboardingData = {
        'startup': {
            title: '🚀 Добро пожаловать, стартапер!',
            description: 'Создадим ваш MVP за 15 минут',
            suggestions: [
                'Создать лендинг для стартапа',
                'Интернет-магазин с оплатой',
                'Приложение для сбора заявок',
                'CRM для управления клиентами'
            ]
        },
        'freelance': {
            title: '💼 Приветствуем фрилансера!',
            description: 'Ускорьте работу с клиентами в 10 раз',
            suggestions: [
                'Портфолио веб-дизайнера',
                'Сайт для digital-агентства',
                'Система управления проектами',
                'Калькулятор стоимости услуг'
            ]
        },
        'corporate': {
            title: '🏢 Добро пожаловать в Vibecode Business!',
            description: 'Создавайте корпоративные решения быстро и безопасно',
            suggestions: [
                'Корпоративный сайт',
                'Внутренний портал сотрудников',
                'Система отчетности',
                'Презентационные лендинги'
            ]
        }
    };

    const data = onboardingData[businessType] || onboardingData['startup'];

    const modal = document.createElement('div');
    modal.className = 'onboarding-modal';
    modal.innerHTML = `
        <div class="modal-overlay">
            <div class="modal-content" style="max-width: 700px;">
                <div class="modal-header">
                    <h2>${data.title}</h2>
                </div>
                <div class="modal-body">
                    <p style="font-size: 1.2rem; text-align: center; margin-bottom: 2rem;">${data.description}</p>

                    <h3>Популярные проекты в вашей сфере:</h3>
                    <div class="suggestions-grid">
                        ${data.suggestions.map(suggestion => `
                            <div class="suggestion-card" onclick="startProjectCreation('${suggestion}')">
                                <h4>${suggestion}</h4>
                                <p>Создать за 5-10 минут</p>
                                <div class="card-action">Начать →</div>
                            </div>
                        `).join('')}
                    </div>

                    <div style="text-align: center; margin-top: 2rem;">
                        <button class="btn-secondary" onclick="closeModal()">
                            Спасибо, разберусь сам
                        </button>
                        <button class="btn-primary" onclick="goToChat()" style="margin-left: 1rem;">
                            Хочу создать что-то свое
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
};

// Начать создание проекта
window.startProjectCreation = function(projectType) {
    closeModal();
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.value = `Создай ${projectType.toLowerCase()}`;
        document.getElementById('chat').scrollIntoView({ behavior: 'smooth' });
        setTimeout(() => {
            sendMessage();
        }, 1000);
    }
};

// Переход к чату
window.goToChat = function() {
    closeModal();
    document.getElementById('chat').scrollIntoView({ behavior: 'smooth' });
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
        chatInput.focus();
        chatInput.placeholder = "Опишите ваш проект подробно: какой сайт нужен, для чего, какие функции...";
    }
};

// Глобальная функция для инициализации WebSocket
window.initializeWebSocket = function() {
    try {
        console.log('🔄 Подключаюсь к WebSocket...', window.location.origin);

        // Проверяем, что Socket.IO загружен
        if (typeof io === 'undefined') {
            console.log('⚠️ Socket.IO не загружен, пропускаем WebSocket');
            return;
        }

        // Подключаемся к WebSocket серверу
        socket = io(API_BASE_URL, {
            transports: ['polling', 'websocket'],
            timeout: 5000,
            forceNew: true
        });

        socket.on('connect', function() {
            console.log('🔌 WebSocket подключен!');
        });

        socket.on('disconnect', function() {
            console.log('❌ WebSocket отключен!');
        });

        socket.on('connect_error', function(error) {
            console.error('❌ Ошибка подключения WebSocket:', error);
            showConnectionStatus('Ошибка подключения', 'error');
            socket = null;
        });

        socket.on('project_status', function(data) {
            console.log('📦 Получен статус проекта:', data);
            handleProjectStatus(data);
        });

    } catch (error) {
        console.error('Ошибка подключения к WebSocket:', error);
        showConnectionStatus('Ошибка подключения', 'error');
        socket = null;
    }
};

// Функция showConnectionStatus удалена - уведомления о подключении больше не показываются

// Обработка статуса проекта
function handleProjectStatus(data) {
    const { status, message, project_id, download_url } = data;

    if (status === 'completed') {
        showNotification('✅ Проект создан успешно!', 'success');
        showDownloadButton(download_url, project_id);
    } else if (status === 'error') {
        showNotification('❌ Ошибка создания проекта', 'error');
    } else if (status === 'generating') {
        showNotification('🔄 Создаю проект...', 'info');
    }
}

// Показать кнопку скачивания
function showDownloadButton(downloadUrl, projectId) {
    const downloadDiv = document.createElement('div');
    downloadDiv.className = 'download-notification';
    downloadDiv.innerHTML = `
        <div style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(45deg, #8b5cf6, #06b6d4);
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
            z-index: 10000;
            animation: slideInUp 0.3s ease;
        ">
            <h4 style="margin: 0 0 0.5rem 0;">🎉 Проект готов!</h4>
            <p style="margin: 0 0 1rem 0; opacity: 0.9;">Ваш проект создан успешно</p>
            <button onclick="downloadProject('${downloadUrl}')" style="
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 8px;
                cursor: pointer;
                font-weight: 600;
                transition: all 0.3s ease;
            ">📥 Скачать</button>
        </div>
    `;

    document.body.appendChild(downloadDiv);

    // Убираем автозакрытие - пользователь сам решит когда закрыть
}

// Скачать проект
function downloadProject(downloadUrl) {
    window.open(downloadUrl, '_blank');
}

// Показать статус AI
function showAIStatus() {
    fetch(`${API_BASE_URL}/api/ai/status`)
        .then(response => response.json())
        .then(data => {
            const status = data.available_services.map(service => 
                `${service.name}: ${service.configured ? '✅' : '❌'}`
            ).join('\n');

            alert(`🤖 Статус AI сервисов:\n\n${status}`);
        })
        .catch(error => {
            console.error('Ошибка получения статуса AI:', error);
            alert('❌ Не удалось получить статус AI сервисов');
        });
}

// Настройка навигации
function setupNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Плавная прокрутка для ссылок
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Настройка чата
function setupChatInterface() {
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendMessage');

    if (chatInput && sendButton) {
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
}

// Отправить сообщение
async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();

    if (!message) return;

    // Добавляем сообщение пользователя
    addMessage(message, 'user');
    chatInput.value = '';

    // Показываем индикатор печати
    showTypingIndicator();

    try {
        // Генерируем или получаем session_id
        let sessionId = localStorage.getItem('ai_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('ai_session_id', sessionId);
        }

        console.log('Отправляю запрос к:', `${API_BASE_URL}/api/chat`);

        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                session_id: sessionId
            })
        });

        console.log('Статус ответа:', response.status);

        if (!response.ok) {
            if (response.status === 401) {
                // Необходима авторизация
                const errorData = await response.json().catch(() => ({}));
                addMessage('🔐 Для использования AI-чата требуется авторизация. Пожалуйста, войдите в систему.', 'ai');
                
                // Показываем кнопку авторизации
                const authButton = document.createElement('button');
                authButton.className = 'auth-redirect-btn';
                authButton.textContent = '🚀 Войти в систему';
                authButton.onclick = () => window.location.href = '/auth.html';
                
                const messagesContainer = document.querySelector('.chat-messages');
                if (messagesContainer) {
                    messagesContainer.appendChild(authButton);
                }
                
                return;
            }
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Получен ответ:', data);

        // Скрываем индикатор печати
        hideTypingIndicator();

        // Добавляем ответ AI
        if (data.message) {
            addMessage(data.message, 'ai', data);
        } else {
            addMessage('🤖 Привет! Отлично, что вы обратились ко мне! Я готов помочь вам создать любое приложение. Что вас интересует?', 'ai');
        }

        // Показываем предложения если есть
        if (data.suggestions && data.suggestions.length > 0) {
            showSuggestions(data.suggestions);
        }

    } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
        hideTypingIndicator();

        // Более дружелюбная обработка ошибок
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            addMessage('🔌 Не удалось подключиться к серверу. Пожалуйста, проверьте подключение.', 'ai');
        } else if (error.message.includes('500')) {
            addMessage('🤖 У меня небольшие технические проблемы. Попробуйте еще раз через минутку!', 'ai');
        } else {
            // Даем осмысленный ответ даже при ошибке
            if (message.toLowerCase().includes('привет') || message.toLowerCase().includes('как дела')) {
                addMessage('🤖 Привет! У меня все отлично! Хотя у меня небольшие проблемы с подключением к основному серверу, но я все равно готов помочь вам. Что хотите создать?', 'ai');
            } else {
                addMessage('🤖 Извините, у меня технические проблемы, но я понял ваш запрос! Могу предложить создать приложение на основе вашей идеи. Что скажете?', 'ai');
            }
        }

        // Показываем предложения по умолчанию
        showSuggestions([
            'Создать игру',
            'Разработать TODO-приложение', 
            'Сделать калькулятор',
            'Помочь с идеей'
        ]);
    }
}

// Добавить сообщение в чат
function addMessage(text, sender, data = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = sender === 'ai' ? '🤖' : '👤';
    const avatarClass = sender === 'ai' ? 'ai-avatar' : 'user-avatar';

    let messageContent = `<p>${text}</p>`;

    // Если это проект, добавляем кнопку скачивания
    if (data && data.type === 'project_created' && data.download_url) {
        messageContent += `
            <div class="project-actions">
                <button class="download-btn" onclick="downloadProject('${data.download_url}', '${data.project_id}')">
                    📦 Скачать проект
                </button>
                <button class="view-btn" onclick="viewProject('${data.project_id}')">
                    👁️ Просмотр
                </button>
            </div>
        `;
    }

    messageDiv.innerHTML = `
        <div class="message-avatar ${avatarClass}">${avatar}</div>
        <div class="message-content">
            ${messageContent}
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Показать индикатор печати
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
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

    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Скрыть индикатор печати
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Функции для работы с проектами
window.downloadProject = function(downloadUrl, projectId) {
    console.log('📦 Скачиваем проект:', projectId);

    // Создаем временную ссылку для скачивания
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `project_${projectId}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    showNotification('📦 Проект загружается...', 'info');
};

window.viewProject = function(projectId) {
    console.log('👁️ Просматриваем проект:', projectId);
    showNotification('👁️ Функция просмотра будет добавлена позже', 'info');
};

// Показать предложения
function showSuggestions(suggestions) {
    const chatMessages = document.getElementById('chatMessages');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'suggestions';

    const buttons = suggestions.map(suggestion => 
        `<button onclick="sendSuggestion('${suggestion}')" class="suggestion-btn">${suggestion}</button>`
    ).join('');

    suggestionsDiv.innerHTML = `
        <div class="suggestions-container">
            ${buttons}
        </div>
    `;

    chatMessages.appendChild(suggestionsDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Отправить предложение
function sendSuggestion(suggestion) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = suggestion;
    sendMessage();

    // Удаляем предложения
    const suggestions = document.querySelector('.suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

// Показать уведомление
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        ${type === 'success' ? 'background: #10b981;' : 
          type === 'error' ? 'background: #ef4444;' : 
          'background: #3b82f6;'}
    `;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Настройка анимаций
function setupAnimations() {
    // Анимация появления элементов при скролле
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        });
    }, observerOptions);

    // Наблюдаем за карточками функций
    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });
}

// Настройка эффектов скролла
function setupScrollEffects() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = document.querySelector('.hero-background');

        if (parallax) {
            const speed = scrolled * 0.5;
            parallax.style.transform = `translateY(${speed}px)`;
        }
    });
}

// Настройка WebSocket
function setupWebSocket() {
    // WebSocket будет инициализирован асинхронно
    console.log('📡 WebSocket будет инициализирован после загрузки');
}

// CSS анимации
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }

    @keyframes slideInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    @keyframes slideOutDown {
        from { transform: translateY(0); opacity: 1; }
        to { transform: translateY(30px); opacity: 0; }
    }

    @keyframes fadeInUp {
        from { transform: translateY(30px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }

    .typing-dots {
        display: flex;
        gap: 4px;
    }

    .typing-dots span {
        width: 8px;
        height: 8px;
        background: rgba(255, 255, 255, 0.7);
        border-radius: 50%;
        animation: typingDot 1.4s ease-in-out infinite;
    }

    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }

    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }

    @keyframes typingDot {
        0%, 60%, 100% { transform: scale(1); opacity: 0.7; }
        30% { transform: scale(1.2); opacity: 1; }
    }

    .suggestions-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .suggestion-btn {
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #8b5cf6;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
    }

    .suggestion-btn:hover {
        background: rgba(139, 92, 246, 0.3);
        transform: translateY(-1px);
    }

    .user-avatar {
        background: linear-gradient(45deg, #10b981, #06b6d4) !important;
    }
`;

document.head.appendChild(style);

// Демо анимация
let demoAnimationRunning = false;
let demoAnimationTimeout = null;

function startDemoAnimation() {
    if (demoAnimationRunning) return;

    demoAnimationRunning = true;
    console.log('🎬 Запускаю демо анимацию...');

    // Сбрасываем все шаги
    const steps = document.querySelectorAll('.demo-step');
    steps.forEach(step => step.classList.remove('active'));

    // Сбрасываем таймлайн
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach(item => item.classList.remove('active'));

    // Запускаем анимацию по шагам
    setTimeout(() => activateStep(1), 500);
    setTimeout(() => activateStep(2), 3000);
    setTimeout(() => activateStep(3), 6000);
    setTimeout(() => showSuccess(), 9000);
    setTimeout(() => showEmotions(), 10000);
    setTimeout(() => activateTimelineItem(0), 500);
    setTimeout(() => activateTimelineItem(1), 3000);
    setTimeout(() => activateTimelineItem(2), 6000);
    setTimeout(() => activateTimelineItem(3), 9000);
    setTimeout(() => activateTimelineItem(4), 12000);

    // Сбрасываем флаг через 15 секунд
    demoAnimationTimeout = setTimeout(() => {
        demoAnimationRunning = false;
    }, 15000);
}

function activateStep(stepNumber) {
    const step = document.querySelector(`[data-step="${stepNumber}"]`);
    if (step) {
        step.classList.add('active');

        // Специальные эффекты для каждого шага
        if (stepNumber === 1) {
            typeInInput();
        } else if (stepNumber === 2) {
            showThinking();
        } else if (stepNumber === 3) {
            showCodeGeneration();
        }
    }
}

function activateTimelineItem(index) {
    const timelineItems = document.querySelectorAll('.timeline-item');
    timelineItems.forEach(item => item.classList.remove('active'));

    if (timelineItems[index]) {
        timelineItems[index].classList.add('active');
    }
}

function typeInInput() {
    const inputSimulation = document.querySelector('.input-simulation');
    const text = 'Создай интернет-магазин с корзиной';

    if (!inputSimulation) return;

    let i = 0;
    inputSimulation.innerHTML = '<span class="typing-cursor">|</span>';

    const typeInterval = setInterval(() => {
        if (i < text.length) {
            inputSimulation.innerHTML = text.substring(0, i + 1) + '<span class="typing-cursor">|</span>';
            i++;
        } else {
            clearInterval(typeInterval);
        }
    }, 100);
}

function showThinking() {
    const thinkingText = document.querySelector('.ai-thinking p');
    const texts = [
        'Анализирую требования...',
        'Планирую структуру...',
        'Подбираю технологии...',
        'Готовлю шаблоны...'
    ];

    if (!thinkingText) return;

    let currentIndex = 0;
    const thinkingInterval = setInterval(() => {
        if (currentIndex < texts.length) {
            thinkingText.textContent = texts[currentIndex];
            currentIndex++;
        } else {
            clearInterval(thinkingInterval);
        }
    }, 700);
}

function showCodeGeneration() {
    const codeLines = document.querySelectorAll('.code-line');
    codeLines.forEach((line, index) => {
        setTimeout(() => {
            line.style.opacity = '1';
            line.style.transform = 'translateX(0)';
        }, index * 800);
    });
}

function showSuccess() {
    const appContent = document.querySelector('.app-content');
    if (appContent) {
        appContent.innerHTML = `
            <div class="success-animation">
                <div class="check-mark">✓</div>
            </div>
            <p>Готово!</p>
        `;
    }
}

function showEmotions() {
    const emotionFace = document.querySelector('.emotion-face');
    const emotionText = document.querySelector('.emotion-text p');

    if (!emotionFace || !emotionText) return;

    const emotions = [
        { face: '😊', text: '"Вау! Это работает!"' },
        { face: '🤩', text: '"Невероятно быстро!"' },
        { face: '💰', text: '"Уже получил заказы!"' },
        { face: '🎉', text: '"Бизнес процветает!"' }
    ];

    let currentEmotion = 0;
    const emotionInterval = setInterval(() => {
        if (currentEmotion < emotions.length) {
            emotionFace.textContent = emotions[currentEmotion].face;
            emotionText.textContent = emotions[currentEmotion].text;
            currentEmotion++;
        } else {
            clearInterval(emotionInterval);
        }
    }, 2000);
}

// Функция воспроизведения демо видео
window.playDemoVideo = function() {
    console.log('🎥 Воспроизводим демо видео...');

    // Создаем полноэкранное видео демонстрацию
    const videoModal = document.createElement('div');
    videoModal.className = 'video-demo-modal';
    videoModal.innerHTML = `
        <div class="video-modal-overlay" onclick="closeDemoVideo()">
            <div class="modal-content" onclick="event.stopPropagation()">
                <div class="video-modal-header">
                    <h3>🎬 Демонстрация Vibecode AI</h3>
                    <button onclick="closeDemoVideo()" class="modal-close">&times;</button>
                </div>
                <div class="video-demo-container">
                    <div class="demo-progress">
                        <div class="progress-bar" id="demoProgress"></div>
                    </div>
                    <div class="demo-stages">
                        <div class="demo-stage active" id="stage1">
                            <h4>💡 Пользователь вводит идею</h4>
                            <p>"Хочу создать интернет-магазин с возможностью онлайн-оплаты"</p>
                            <div class="stage-visual">
                                <div class="typing-demo">Создай интернет-магазин...</div>
                            </div>
                        </div>
                        <div class="demo-stage" id="stage2">
                            <h4>🤖 ИИ анализирует запрос</h4>
                            <p>Vibecode AI понимает требования и планирует архитектуру</p>
                            <div class="stage-visual">
                                <div class="ai-analysis">
                                    <div class="analysis-item">✓ Определена структура БД</div>
                                    <div class="analysis-item">✓ Выбраны технологии</div>
                                    <div class="analysis-item">✓ Спланирован UI/UX</div>
                                </div>
                            </div>
                        </div>
                        <div class="demo-stage" id="stage3">
                            <h4>⚡ Генерация кода</h4>
                            <p>ИИ создает полнофункциональное приложение</p>
                            <div class="stage-visual">
                                <div class="code-progress">
                                    <div class="progress-item">Frontend (React) - 100%</div>
                                    <div class="progress-item">Backend (Node.js) - 100%</div>
                                    <div class="progress-item">База данных - 100%</div>
                                    <div class="progress-item">Интеграции - 100%</div>
                                </div>
                            </div>
                        </div>
                        <div class="demo-stage" id="stage4">
                            <h4>🎉 Готовый продукт</h4>
                            <p>Полнофункциональный интернет-магазин готов к запуску</p>
                            <div class="stage-visual">
                                <div class="product-showcase">
                                    <div class="feature">✅ Каталог товаров</div>
                                    <div class="feature">✅ Корзина покупок</div>
                                    <div class="feature">✅ Система оплаты</div>
                                    <div class="feature">✅ Админ панель</div>
                                </div>
                            </div>
                        </div>
                        <div class="demo-stage" id="stage5">
                            <h4>💰 Успех в бизнесе</h4>
                            <p>Пользователь получает первые заказы и развивает бизнес</p>
                            <div class="stage-visual">
                                <div class="success-metrics">
                                    <div class="metric">📈 +300% продаж</div>
                                    <div class="metric">👥 1000+ клиентов</div>
                                    <div class="metric">💰 $50K+ доход</div>
                                    <div class="metric">⭐ 4.9/5 рейтинг</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="video-controls">
                        <button onclick="restartDemo()" class="control-btn">🔄 Повторить</button>
                        <button onclick="closeDemoVideo()" class="control-btn primary">✨ Попробовать</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Добавляем стили для видео модального окна
    const videoStyle = document.createElement('style');
    videoStyle.textContent = `
        .video-demo-modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10000;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0, 0, 0, 0.95);
            backdrop-filter: blur(10px);
        }

        .video-modal-content {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            border-radius: 20px;
            padding: 2rem;
            max-width: 900px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .video-modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 1rem;
        }

        .video-modal-header h3 {
            color: white;
            margin: 0;
            font-size: 1.5rem;
        }

        .demo-progress {
            width: 100%;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
            margin-bottom: 2rem;
            overflow: hidden;
        }

        .progress-bar {
            height: 100%;
            background: linear-gradient(45deg, #8b5cf6, #06b6d4);
            width: 0%;
            transition: width 0.5s ease;
            border-radius: 2px;
        }

        .demo-stage {
            display: none;
            text-align: center;
            padding: 2rem;
            animation: stageAppear 0.5s ease;
        }

        .demo-stage.active {
            display: block;
        }

        @keyframes stageAppear {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .demo-stage h4 {
            color: white;
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        .demo-stage p {
            color: rgba(255, 255, 255, 0.8);
            margin-bottom: 2rem;
            font-size: 1.1rem;
        }

        .stage-visual {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 2rem;
            margin: 2rem 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .typing-demo {
            font-family: 'Courier New', monospace;
            font-size: 1.2rem;
            color: #10b981;
            animation: typewriter 2s steps(30) infinite;
        }

        .analysis-item, .progress-item, .feature, .metric {
            background: rgba(139, 92, 246, 0.2);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            color: white;
            animation: itemAppear 0.5s ease;
        }

        @keyframes itemAppear {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        .video-controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-top: 2rem;
        }

        .control-btn {
            padding: 1rem 2rem;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 25px;
            background: rgba(255, 255, 255, 0.05);
            color: white;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .control-btn.primary {
            background: linear-gradient(45deg, #8b5cf6, #06b6d4);
            border-color: transparent;
        }

        .control-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
        }
    `;

    document.head.appendChild(videoStyle);
    document.body.appendChild(videoModal);

    // Запускаем демонстрацию
    startVideoDemo();
};

function startVideoDemo() {
    let currentStage = 1;
    const totalStages = 5;
    const progressBar = document.getElementById('demoProgress');

    const stageInterval = setInterval(() => {
        // Обновляем прогресс
        const progress = (currentStage / totalStages) * 100;
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }

        // Скрываем предыдущий этап
        const prevStage = document.getElementById(`stage${currentStage - 1}`);
        if (prevStage) {
            prevStage.classList.remove('active');
        }

        // Показываем текущий этап
        const currentStageElement = document.getElementById(`stage${currentStage}`);
        if (currentStageElement) {
            currentStageElement.classList.add('active');
        }

        currentStage++;

        if (currentStage > totalStages) {
            clearInterval(stageInterval);
        }
    }, 3000);
}

window.closeDemoVideo = function() {
    const videoModal = document.querySelector('.video-demo-modal');
    if (videoModal) {
        videoModal.remove();
    }
};

window.restartDemo = function() {
    // Сбрасываем все этапы
    document.querySelectorAll('.demo-stage').forEach(stage => {
        stage.classList.remove('active');
    });

    // Показываем первый этап
    const firstStage = document.getElementById('stage1');
    if (firstStage) {
        firstStage.classList.add('active');
    }

    // Перезапускаем демонстрацию
    startVideoDemo();
};

// Автоматический запуск демо анимации при скролле
function setupDemoScrollTrigger() {
    const demoSection = document.getElementById('demo');
    if (!demoSection) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !demoAnimationRunning) {
                setTimeout(() => {
                    startDemoAnimation();
                }, 500);
            }
        });
    }, { threshold: 0.3 });

    observer.observe(demoSection);
}

// Инициализируем демо триггеры при загрузке DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupDemoScrollTrigger);
} else {
    setupDemoScrollTrigger();
}