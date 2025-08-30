// AI Generated JavaScript with Navigation System
document.addEventListener('DOMContentLoaded', function() {
    console.log('App loaded successfully!');
    
    // Initialize navigation system
    initializeNavigation();
    
    // Show main screen by default
    showScreen('main-screen');
});

// Navigation System
function showScreen(screenId) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    
    // Show target screen
    const targetScreen = document.getElementById(screenId);
    if (targetScreen) {
        targetScreen.classList.add('active');
        console.log(`Switched to ${screenId}`);
    }
}

function initializeNavigation() {
    // Add click handlers for navigation buttons
    document.addEventListener('click', function(e) {
        const button = e.target;
        
        // Handle navigation based on button text/data
        if (button.matches('.btn-primary') && button.textContent.includes('Начать')) {
            showScreen('app-screen');
        } else if (button.textContent.includes('Настройки')) {
            showScreen('settings-screen');
        } else if (button.textContent.includes('Назад') || button.textContent.includes('Главная')) {
            showScreen('main-screen');
        }
    });
}

// App functionality - only activates after user clicks "Start"
function startApp() {
    console.log('App started!');
    // Add your main app functionality here
    // This function is called when user reaches app-screen
}

// Settings functionality
function initializeSettings() {
    console.log('Settings initialized');
    // Add settings logic here
}