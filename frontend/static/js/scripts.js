// Обработка нажатия клавиши Enter
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();  // Предотвращаем стандартное поведение (новая строка)
        sendMessage();  // Отправляем сообщение
    }
});

// Функция отправки сообщения
function sendMessage() {
    const userInputElement = document.getElementById('user-input');
    const userInput = userInputElement.value;

    console.log('Отправка сообщения:', userInput);  // Отслеживаем ввод пользователя

    if (userInput.trim() === '') return;  // Не отправляем пустые сообщения

    fetch('/submit_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Ответ с сервера:', data);  // Отслеживаем ответ от сервера
        const messagesDiv = document.getElementById('chat-messages');

        // Добавляем сообщение пользователя
        const userMessageDiv = document.createElement('div');
        userMessageDiv.classList.add('message', 'user');
        userMessageDiv.innerHTML = `
            <div class="avatar user-avatar">
                <img src="/static/img/user.png" alt="User avatar">
            </div>
            <p class="text">${data.user_message}</p>
        `;
        messagesDiv.prepend(userMessageDiv);

        // Добавляем сообщение консультанта
        const aiMessageDiv = document.createElement('div');
        aiMessageDiv.classList.add('message', 'ai');
        aiMessageDiv.innerHTML = `
            <div class="avatar ai-avatar">
                <img src="/static/img/consultant.png" alt="Consultant avatar">
            </div>
            <p class="text">${data.response_message}</p>
        `;
        messagesDiv.prepend(aiMessageDiv);

        // Очищаем поле ввода
        userInputElement.value = '';
    })
    .catch(error => console.error('Ошибка:', error));
}