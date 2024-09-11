document.getElementById('question-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    const question = document.getElementById('question').value;

    // Отправляем запрос для генерации ответа
    const responseGeneration = await fetch('/generation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question: question }),
    });

    // Parse the response as JSON
    const dataGeneration = await responseGeneration.json();

    // Проверяем наличие ответа и актов, и обновляем страницу
    if (dataGeneration.response) {
        document.getElementById('answer').textContent = dataGeneration.response;
    } else {
        document.getElementById('answer').textContent = 'Ошибка: не удалось получить ответ.';
    }

    if (dataGeneration.acts) {
        document.getElementById('acts').textContent = dataGeneration.acts;
    } else {
        document.getElementById('acts').textContent = 'Ошибка: не удалось получить акты.';
    }
});
