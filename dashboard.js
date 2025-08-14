
// JavaScript для личного кабинета
let currentUser = null;
let currentSession = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    checkAuthentication();
    initializeDashboard();
});

// Проверка авторизации
async function checkAuthentication() {
    try {
        const response = await fetch('/api/user/profile');
        if (response.ok) {
            const data = await response.json();
            currentUser = data.user;
            updateUserInterface();
        } else {
            // Не авторизован - перенаправляем на страницу входа
            window.location.href = '/auth';
        }
    } catch (error) {
        console.error('Ошибка проверки авторизации:', error);
        window.location.href = '/auth';
    }
}

// Обновление интерфейса пользователя
function updateUserInterface() {
    if (!currentUser) return;
    
    // Обновляем информацию о пользователе
    document.getElementById('userName').textContent = currentUser.name;
    document.getElementById('userPlan').textContent = getPlanName(currentUser.plan);
    document.getElementById('requestsCount').textContent = currentUser.requests_left;
    
    // Обновляем цвет счетчика запросов
    const requestsElement = document.getElementById('requestsCount');
    if (currentUser.requests_left <= 3) {
        requestsElement.style.color = '#ef4444';
    } else if (currentUser.requests_left <= 7) {
        requestsElement.style.color = '#f59e0b';
    } else {
        requestsElement.style.color = '#22c55e';
    }
    
    // Заполняем форму настроек
    const userNameInput = document.querySelector('#settings-tab #userName');
    const userEmailInput = document.querySelector('#settings-tab #userEmail');
    if (userNameInput) userNameInput.value = currentUser.name;
    if (userEmailInput) userEmailInput.value = currentUser.email;
}

function getPlanName(plan) {
    const plans = {
        'free': 'Бесплатный план',
        'personal': 'Персональный',
        'team': 'Командный'
    };
    return plans[plan] || 'Неизвестный план';
}

// Инициализация функций дашборда
function initializeDashboard() {
    setupTabs();
    setupChat();
    loadUserProjects();
    loadChatHistory();
}

// Настройка вкладок
function setupTabs() {
    const menuItems = document.querySelectorAll('.menu-item');
    const tabContents = document.querySelectorAll('.tab-content');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            showTab(tabName);
        });
    });
}

function showTab(tabName) {
    // Обновляем активную вкладку в меню
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Показываем нужную вкладку
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Загружаем данные для вкладки если нужно
    if (tabName === 'projects') {
        loadUserProjects();
    } else if (tabName === 'history') {
        loadChatHistory();
    }
}

// Настройка чата
function setupChat() {
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

// Отправка сообщения в чат
async function sendMessage() {
    const chatInput = document.getElementById('chatInput');
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Проверяем лимиты
    if (currentUser && currentUser.requests_left <= 0 && currentUser.plan === 'free') {
        showLimitModal();
        return;
    }
    
    // Добавляем сообщение пользователя
    addMessage(message, 'user');
    chatInput.value = '';
    
    // Показываем индикатор печати
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                session_id: currentSession
            })
        });
        
        hideTypingIndicator();
        
        if (response.status === 429) {
            // Лимит исчерпан
            const data = await response.json();
            showLimitModal();
            return;
        }
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Обновляем счетчик запросов
        if (data.requests_left !== undefined) {
            currentUser.requests_left = data.requests_left;
            updateUserInterface();
        }
        
        // Добавляем ответ AI с красивым форматированием
        addMessage(data.message, 'ai', data);
        
        // Показываем предложения если есть
        if (data.suggestions && data.suggestions.length > 0) {
            showSuggestions(data.suggestions);
        }
        
    } catch (error) {
        console.error('Ошибка отправки сообщения:', error);
        hideTypingIndicator();
        addMessage('🤖 Извините, произошла ошибка. Попробуйте еще раз.', 'ai');
    }
}

// Добавление сообщения в чат
function addMessage(text, sender, data = null) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatar = sender === 'ai' ? '🤖' : '👤';
    const avatarClass = sender === 'ai' ? 'ai-avatar' : 'user-avatar';
    
    let messageContent = `<p>${formatMessage(text)}</p>`;
    
    // Если это результат создания проекта, добавляем специальное форматирование
    if (data && data.type === 'project_created' && data.download_url) {
        messageContent += `
            <div class="project-actions" style="margin-top: 1rem;">
                <button class="download-btn" onclick="downloadProject('${data.download_url}', '${data.project_id}')">
                    📦 Скачать проект
                </button>
                <button class="view-btn" onclick="viewProject('${data.project_id}')">
                    👁️ Просмотр файлов
                </button>
            </div>
        `;
    }
    
    // Если AI подводит итоги изменений
    if (data && data.type === 'ai_summary') {
        messageContent = formatAISummary(text, data);
    }
    
    messageDiv.innerHTML = `
        <div class="message-avatar ${avatarClass}">${avatar}</div>
        <div class="message-content">
            ${messageContent}
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Анимация появления
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    setTimeout(() => {
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
        messageDiv.style.transition = 'all 0.3s ease';
    }, 100);
}

// Форматирование сообщений
function formatMessage(text) {
    // Заменяем эмодзи на более крупные
    text = text.replace(/🎉/g, '<span style="font-size: 1.5em;">🎉</span>');
    text = text.replace(/🚀/g, '<span style="font-size: 1.2em;">🚀</span>');
    text = text.replace(/✅/g, '<span style="color: #22c55e;">✅</span>');
    text = text.replace(/💡/g, '<span style="color: #f59e0b;">💡</span>');
    
    // Форматируем заголовки
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong style="color: #8b5cf6;">$1</strong>');
    
    // Форматируем списки
    text = text.replace(/^• (.+)$/gm, '<div style="margin: 0.5rem 0; padding-left: 1rem;">▶ $1</div>');
    
    // Разделяем на абзацы
    text = text.replace(/\n\n/g, '</p><p>');
    
    return text;
}

// Форматирование итогов AI
function formatAISummary(text, data) {
    return `
        <div class="ai-summary">
            <div class="summary-title">
                🎉 ${data.title || 'ГОТОВО! Изменения внесены!'}
            </div>
            <div class="summary-content">
                ${formatMessage(text)}
            </div>
            ${data.changes ? `
                <div class="summary-section">
                    <h4>🔧 Внесенные изменения:</h4>
                    <ul class="summary-list">
                        ${data.changes.map(change => `<li>${change}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
            ${data.next_steps ? `
                <div class="summary-section">
                    <h4>📋 Следующие шаги:</h4>
                    <ul class="summary-list">
                        ${data.next_steps.map(step => `<li>${step}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
}

// Показ индикатора печати
function showTypingIndicator() {
    const chatMessages = document.getElementById('chatMessages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ai-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    
    typingDiv.innerHTML = `
        <div class="message-avatar ai-avatar">🤖</div>
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

function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Показ предложений
function showSuggestions(suggestions) {
    const chatMessages = document.getElementById('chatMessages');
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'suggestions';
    
    const buttons = suggestions.map(suggestion => 
        `<button onclick="sendSuggestion('${suggestion.replace(/'/g, "\\'")}'); removeSuggestions();" class="suggestion-btn">${suggestion}</button>`
    ).join('');
    
    suggestionsDiv.innerHTML = `
        <div class="suggestions-container">
            ${buttons}
        </div>
    `;
    
    chatMessages.appendChild(suggestionsDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendSuggestion(suggestion) {
    const chatInput = document.getElementById('chatInput');
    chatInput.value = suggestion;
    sendMessage();
}

function removeSuggestions() {
    const suggestions = document.querySelector('.suggestions');
    if (suggestions) {
        suggestions.remove();
    }
}

// Загрузка проектов пользователя
async function loadUserProjects() {
    try {
        const response = await fetch('/api/user/projects');
        if (response.ok) {
            const data = await response.json();
            displayProjects(data.projects);
        }
    } catch (error) {
        console.error('Ошибка загрузки проектов:', error);
    }
}

function displayProjects(projects) {
    const projectsGrid = document.getElementById('projectsGrid');
    
    if (projects.length === 0) {
        projectsGrid.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: rgba(255, 255, 255, 0.7);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📁</div>
                <h3>Пока нет проектов</h3>
                <p>Создайте свой первый проект через чат!</p>
            </div>
        `;
        return;
    }
    
    const projectCards = projects.map(project => `
        <div class="project-card" data-project-id="${project.project_id}">
            <div class="project-header">
                <h3>${project.name}</h3>
                <span class="project-type">${project.type}</span>
            </div>
            <div class="project-content">
                <p class="project-description">${project.description || 'Без описания'}</p>
                <div class="project-stats">
                    <span>📄 ${project.files ? project.files.length : 0} файлов</span>
                    <span>🔄 v${project.version || 1}</span>
                    <span class="project-status status-${project.status || 'active'}">${project.status || 'active'}</span>
                </div>
            </div>
            <div class="project-actions">
                <button onclick="openProject('${project.project_id}')" class="btn-primary">
                    <i>📝</i> Редактировать
                </button>
                <button onclick="runProject('${project.project_id}')" class="btn-secondary">
                    <i>▶️</i> Запустить
                </button>
                <button onclick="shareProject('${project.project_id}')" class="btn-outline">
                    <i>🔗</i> Поделиться
                </button>
            </div>
            <div class="project-footer">
                <small>Создан: ${formatDate(project.created_at)}</small>
                <small>Изменен: ${formatDate(project.updated_at)}</small>
            </div>
        </div>
    `).join('');
    
    projectsGrid.innerHTML = projectCards;
}

async function openProject(projectId) {
    try {
        const response = await fetch(`/api/project/${projectId}/files`);
        if (response.ok) {
            const data = await response.json();
            showProjectEditor(projectId, data.files);
        } else {
            showNotification('Ошибка загрузки проекта', 'error');
        }
    } catch (error) {
        console.error('Ошибка открытия проекта:', error);
        showNotification('Ошибка открытия проекта', 'error');
    }
}

async function runProject(projectId) {
    try {
        const response = await fetch(`/api/project/${projectId}/run`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const data = await response.json();
            showNotification('Проект запущен!', 'success');
            // Открыть проект в новой вкладке или iframe
            window.open(data.url, '_blank');
        } else {
            showNotification('Ошибка запуска проекта', 'error');
        }
    } catch (error) {
        console.error('Ошибка запуска проекта:', error);
        showNotification('Ошибка запуска проекта', 'error');
    }
}

function shareProject(projectId) {
    const shareUrl = `${window.location.origin}/project/${projectId}`;
    navigator.clipboard.writeText(shareUrl).then(() => {
        showNotification('Ссылка скопирована в буфер обмена!', 'success');
    });
}

function showProjectEditor(projectId, files) {
    const modal = document.createElement('div');
    modal.className = 'project-editor-modal';
    
    const fileList = files.map(file => `
        <div class="file-item" onclick="selectFile('${file.path}')">
            <span class="file-icon">${getFileIcon(file.type)}</span>
            <span class="file-name">${file.path}</span>
        </div>
    `).join('');
    
    modal.innerHTML = `
        <div class="modal-content project-editor">
            <div class="modal-header">
                <h2>Редактор проекта</h2>
                <button onclick="closeModal()" class="close-btn">×</button>
            </div>
            <div class="editor-body">
                <div class="file-sidebar">
                    <h3>Файлы</h3>
                    <div class="file-list">
                        ${fileList}
                    </div>
                    <button onclick="addNewFile('${projectId}')" class="btn-outline">
                        + Добавить файл
                    </button>
                </div>
                <div class="code-editor">
                    <div class="editor-tabs" id="editorTabs"></div>
                    <textarea id="codeEditor" placeholder="Выберите файл для редактирования"></textarea>
                    <div class="editor-actions">
                        <button onclick="saveCurrentFile()" class="btn-primary">💾 Сохранить</button>
                        <button onclick="formatCode()" class="btn-secondary">🎨 Форматировать</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Инициализируем редактор с первым файлом
    if (files.length > 0) {
        selectFile(files[0].path, files);
    }
    
    // Сохраняем данные для редактора
    window.currentProject = { projectId, files };
}

function selectFile(filePath, files = null) {
    const fileData = files || window.currentProject.files;
    const file = fileData.find(f => f.path === filePath);
    
    if (file) {
        const codeEditor = document.getElementById('codeEditor');
        codeEditor.value = file.content;
        codeEditor.setAttribute('data-file-path', filePath);
        
        // Обновляем активную вкладку
        updateEditorTabs(filePath);
    }
}

async function saveCurrentFile() {
    const codeEditor = document.getElementById('codeEditor');
    const filePath = codeEditor.getAttribute('data-file-path');
    const content = codeEditor.value;
    
    if (!filePath) {
        showNotification('Не выбран файл для сохранения', 'warning');
        return;
    }
    
    try {
        const response = await fetch(`/api/project/${window.currentProject.projectId}/file`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                file_path: filePath,
                file_content: content
            })
        });
        
        if (response.ok) {
            showNotification('Файл сохранен!', 'success');
        } else {
            showNotification('Ошибка сохранения файла', 'error');
        }
    } catch (error) {
        console.error('Ошибка сохранения:', error);
        showNotification('Ошибка сохранения файла', 'error');
    }
}

function getFileIcon(fileType) {
    const icons = {
        'html': '📄',
        'css': '🎨', 
        'javascript': '⚡',
        'python': '🐍',
        'text': '📝'
    };
    return icons[fileType] || '📄';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', { 
        day: '2-digit', 
        month: '2-digit', 
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function closeModal() {
    const modal = document.querySelector('.project-editor-modal');
    if (modal) {
        modal.remove();
    }
                <h3>Пока нет проектов</h3>
                <p>Создайте свой первый проект в чате с AI</p>
                <button class="btn-primary" onclick="showTab('chat')" style="margin-top: 1rem;">
                    💬 Начать в чате
                </button>
            </div>
        `;
        return;
    }
    
    projectsGrid.innerHTML = projects.map(project => `
        <div class="project-card" onclick="openProject('${project.project_id}')">
            <div class="project-title">${project.name}</div>
            <div class="project-date">${formatDate(project.created_at)}</div>
            <div class="project-description">${project.description || 'Без описания'}</div>
            <div class="project-actions" onclick="event.stopPropagation();">
                <button class="project-btn btn-primary" onclick="downloadProject('/api/download/${project.project_id}', '${project.project_id}')">
                    📥 Скачать
                </button>
                <button class="project-btn btn-secondary" onclick="editProject('${project.project_id}')">
                    ✏️ Редактировать
                </button>
            </div>
        </div>
    `).join('');
}

// Загрузка истории чатов
async function loadChatHistory() {
    try {
        const response = await fetch('/api/user/history');
        if (response.ok) {
            const data = await response.json();
            displayChatHistory(data.sessions);
        }
    } catch (error) {
        console.error('Ошибка загрузки истории:', error);
    }
}

function displayChatHistory(sessions) {
    const historyList = document.getElementById('historyList');
    
    if (sessions.length === 0) {
        historyList.innerHTML = `
            <div style="text-align: center; padding: 3rem; color: rgba(255, 255, 255, 0.7);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                <h3>История пуста</h3>
                <p>Начните общение с AI, и здесь появится история ваших разговоров</p>
            </div>
        `;
        return;
    }
    
    historyList.innerHTML = sessions.map(session => {
        const firstMessage = session.messages[0]?.message || 'Без сообщений';
        const title = firstMessage.length > 60 ? firstMessage.substr(0, 60) + '...' : firstMessage;
        
        return `
            <div class="history-item" onclick="loadChatSession('${session.session_id}')">
                <div class="history-title">${title}</div>
                <div class="history-date">${formatDate(session.created_at)} • ${session.messages.length} сообщений</div>
            </div>
        `;
    }).join('');
}

// Функции для работы с проектами
function downloadProject(downloadUrl, projectId) {
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.download = `project_${projectId}.zip`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    showNotification('📦 Проект загружается...', 'success');
}

function viewProject(projectId) {
    showNotification('👁️ Функция просмотра файлов будет добавлена в следующем обновлении', 'info');
}

function editProject(projectId) {
    showTab('chat');
    const chatInput = document.getElementById('chatInput');
    chatInput.value = `Доработай проект с ID: ${projectId}`;
    chatInput.focus();
}

// Модальное окно лимита запросов
function showLimitModal() {
    const modal = document.getElementById('limitModal');
    modal.classList.add('active');
}

function closeLimitModal() {
    const modal = document.getElementById('limitModal');
    modal.classList.remove('active');
}

// Функции подписки
function showComingSoon() {
    showNotification('🚧 Оплата подписок будет доступна в ближайшее время!', 'info');
}

// Сохранение настроек
async function saveSettings() {
    const name = document.querySelector('#settings-tab #userName').value;
    
    try {
        const response = await fetch('/api/user/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name })
        });
        
        if (response.ok) {
            const data = await response.json();
            currentUser.name = name;
            updateUserInterface();
            showNotification('✅ Настройки сохранены', 'success');
        } else {
            const data = await response.json();
            showNotification('❌ ' + data.error, 'error');
        }
    } catch (error) {
        showNotification('❌ Ошибка сохранения настроек', 'error');
    }
}

// Выход из системы
async function logout() {
    try {
        await fetch('/api/logout', { method: 'POST' });
        window.location.href = '/auth';
    } catch (error) {
        console.error('Ошибка выхода:', error);
        window.location.href = '/auth';
    }
}

// Утилитарные функции
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return 'Сегодня';
    } else if (diffDays === 2) {
        return 'Вчера';
    } else if (diffDays <= 7) {
        return `${diffDays} дня назад`;
    } else {
        return date.toLocaleDateString('ru-RU');
    }
}

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

function clearHistory() {
    if (confirm('Вы уверены, что хотите очистить всю историю чатов?')) {
        // TODO: Реализовать API для очистки истории
        showNotification('🧹 Функция очистки истории будет добавлена в следующем обновлении', 'info');
    }
}

// Обновляем главную страницу чтобы убрать чат
function loadChatSession(sessionId) {
    // TODO: Загрузить конкретную сессию чата
    showTab('chat');
    showNotification('📋 Загрузка сессии...', 'info');
}
