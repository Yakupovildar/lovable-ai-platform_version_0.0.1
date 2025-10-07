
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
