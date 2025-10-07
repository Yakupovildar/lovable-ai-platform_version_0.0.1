
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
