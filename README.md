# 💻 Lovable AI Platform

ИИ платформа для генерации кода с использованием российских AI сервисов.

## 🚀 Быстрый запуск

### Автоматический запуск (рекомендуется)
```bash
python3 start_project.py
```

Этот скрипт автоматически:
- ✅ Проверит версию Python
- 📦 Создаст виртуальное окружение
- 🔧 Установит все зависимости
- 🚀 Запустит backend и frontend
- 🌐 Откроет браузер

### Ручной запуск

1. **Настройка backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # На macOS/Linux
# или
venv\Scripts\activate     # На Windows
pip install -r requirements.txt
python app.py
```

2. **Запуск frontend:**
```bash
# В новом терминале
python3 -m http.server 8000
```

3. **Открыть в браузере:**
```
http://localhost:8000
```

## 📋 Что работает

### ✅ AI агент
- 🤖 **SmartAI** - локальный AI с памятью и обучением
- 🔄 **GigaChat** - российский AI от Сбера (требует API ключи)
- 📝 **Yandex GPT** - AI от Яндекса (требует API ключи)
- 🏠 **LocalAI** - локальные модели (опционально)

### ✅ Создание проектов
- ⏰ **Будильники и таймеры** с красивым дизайном
- 🧮 **Калькуляторы** с современным интерфейсом
- 🎮 **Игры** (на реакцию, головоломки, аркадные)
- 📱 **Веб-приложения** (React, Vue, HTML)
- 🎨 **Портфолио и сайты**
- 🛒 **E-commerce** проекты
- 📝 **Блоги и новостные сайты**

### ✅ Функции
- 🔄 **Real-time чат** с AI
- 📦 **Автоматическая генерация** проектов
- 🎨 **Дизайнерские системы** (modern-dark, light, colorful)
- 📱 **Адаптивный дизайн** для всех устройств
- ⚡ **WebSocket** для мгновенных обновлений
- 📥 **Скачивание** проектов в ZIP архивах
- 🔧 **Улучшение** существующих проектов

## 🛠️ Технологии

### Backend
- **Flask** - веб-фреймворк
- **Flask-SocketIO** - WebSocket поддержка
- **GigaChat** - российский AI API
- **Yandex GPT** - AI от Яндекса
- **SmartAI** - локальный AI с обучением

### Frontend
- **HTML5** - современная разметка
- **CSS3** - градиенты, анимации, адаптивность
- **JavaScript** - интерактивность и WebSocket
- **Responsive Design** - для всех устройств

## 📁 Структура проекта

```
lovable-ai-platform/
├── backend/                 # Backend сервер
│   ├── app.py              # Основное Flask приложение
│   ├── russian_ai.py       # Интеграция с российскими AI
│   ├── ai_config.py        # Конфигурация AI сервисов
│   ├── requirements.txt    # Python зависимости
│   ├── projects/           # Созданные проекты
│   └── temp/               # Временные файлы
├── index.html              # Главная страница
├── styles.css              # Стили
├── script.js               # JavaScript
├── start_project.py        # Скрипт запуска
└── README.md               # Документация
```

## 🔧 Настройка AI сервисов

### GigaChat (Сбер)
1. Получите API ключи на [GigaChat](https://developers.sber.ru/portal/products/gigachat)
2. Создайте файл `.env` в папке `backend`:
```env
GIGACHAT_ENABLED=true
GIGACHAT_CLIENT_ID=ваш_client_id
GIGACHAT_CLIENT_SECRET=ваш_client_secret
```

### Yandex GPT
1. Получите API ключ в [Yandex Cloud](https://cloud.yandex.ru/)
2. Добавьте в `.env`:
```env
YANDEX_GPT_ENABLED=true
YANDEX_API_KEY=ваш_api_key
YANDEX_FOLDER_ID=ваш_folder_id
```

## 🎯 Примеры использования

### Создание будильника
```bash
curl -X POST http://localhost:5002/api/generate-project \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Красивый будильник с таймером",
    "project_name": "Мой будильник",
    "project_type": "html"
  }'
```

### Чат с AI
```bash
curl -X POST http://localhost:5002/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Создай калькулятор"}'
```

## 🌐 API Endpoints

- `GET /api/ai/status` - статус AI сервисов
- `POST /api/chat` - чат с AI
- `POST /api/generate-project` - создание проекта
- `POST /api/generate-project-with-design` - создание с дизайном
- `POST /api/improve-project` - улучшение проекта
- `GET /api/projects` - список проектов
- `GET /api/download/<project_id>` - скачивание проекта

## 🐛 Устранение неполадок

### Ошибка "python: command not found"
На macOS используйте `python3` вместо `python`

### Ошибка "ModuleNotFoundError: No module named 'flask'"
Активируйте виртуальное окружение:
```bash
cd backend
source venv/bin/activate
```

### Ошибка "externally-managed-environment"
Используйте виртуальное окружение или добавьте флаг:
```bash
pip install --break-system-packages -r requirements.txt
```

### Backend не запускается
Проверьте:
1. Виртуальное окружение активировано
2. Все зависимости установлены
3. Порт 5002 свободен

## 📞 Поддержка

Если у вас возникли проблемы:
1. Проверьте логи в терминале
2. Убедитесь, что все зависимости установлены
3. Проверьте, что порты 5002 и 8000 свободны

## 🎉 Готово!

Теперь у вас есть полнофункциональная AI платформа для генерации кода! 

- 🌐 Откройте http://localhost:8000
- 💬 Пообщайтесь с AI
- 🚀 Создавайте проекты
- 📦 Скачивайте готовые решения

**Приятного использования!** 🎊 