document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

function sendMessage() {
    const userInputElement = document.getElementById('user-input');
    const userInput = userInputElement.value;

    if (userInput.trim() === '') return;

    fetch('/generation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const messagesDiv = document.getElementById('chat-messages');

        // Добавляем сообщение пользователя
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user');
        userMessageDiv.innerHTML = `
            <div class="avatar user-avatar">
                <img src="/static/img/user.png" alt="User avatar">
            </div>
            <p class="text">${userInput}</p>
        `;
        messagesDiv.prepend(userMessageDiv);

        // Добавляем ответ от AI
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.classList.add('message', 'ai');
        aiMessageDiv.innerHTML = `
            <div class="avatar ai-avatar">
                <img src="/static/img/consultant.png" alt="Consultant avatar">
            </div>
            <p class="text">${data.response}</p>
        `;
        messagesDiv.prepend(aiMessageDiv);

        // Очищаем поле ввода
        userInputElement.value = '';

        // Обновляем список актов
        const actsDiv = document.getElementById('sources');
        actsDiv.innerHTML = `<p>${data.acts}</p>`;
    })
    .catch(error => console.error('Ошибка:', error));
}
