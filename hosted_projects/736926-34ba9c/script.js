const mentors = {
    'elon': { name: 'Илон Маск', avatar: '🚀' },
    'jobs': { name: 'Стив Джобс', avatar: '💻' }
};

function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();
    if (message) {
        addMessage('user', message);
        setTimeout(() => addMessage('ai', 'Интересная мысль! Расскажите больше.'), 1000);
        input.value = '';
    }
}

function addMessage(sender, text) {
    const chat = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.innerHTML = `<strong>${sender === 'user' ? 'Вы' : 'AI'}:</strong> ${text}`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('🤖 AI Mentor загружен');
});