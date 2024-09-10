// Обработка нажатия клавиши Enter
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
});

// Функция отправки сообщения
function sendMessage() {
    const userInputElement = document.getElementById('user-input');
    const userInput = userInputElement.value;

    if (userInput.trim() === '') return;

    fetch('/submit_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput })
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

        // Отображаем список источников
        updateSourceList(data.sources);
    })
    .catch(error => console.error('Ошибка:', error));
}

// Функция обновления списка источников
function updateSourceList(sources) {
    const sourcesDiv = document.getElementById('sources');
    sourcesDiv.innerHTML = ''; // Очищаем предыдущий контент

    sources.forEach((source, index) => {
        const sourceButton = document.createElement('button');
        sourceButton.classList.add('source-button');
        sourceButton.innerText = `${index + 1}. ${source}`;
        sourceButton.onclick = () => loadSourceContent(sourceButton, source);
        sourcesDiv.appendChild(sourceButton);
    });
}

// Функция загрузки контента источника с сервера
function loadSourceContent(button, sourceName) {
    fetch('/get_source_content', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ source_name: sourceName })
    })
    .then(response => response.json())
    .then(data => {
        // Снимаем выделение с предыдущих кнопок
        const buttons = document.querySelectorAll('.source-button');
        buttons.forEach(btn => btn.classList.remove('selected'));

        // Выделяем выбранную кнопку
        button.classList.add('selected');

        // Обновляем контент источника
        const sourceViewer = document.getElementById('source-viewer');
        sourceViewer.innerHTML = `<p>${data.source_content}</p>`;
    })
    .catch(error => console.error('Ошибка при загрузке источника:', error));
}
