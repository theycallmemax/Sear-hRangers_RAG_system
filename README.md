# LegalAI-RAG-FastAPI

Проект представляет собой FastAPI API и Streamlit интерфейс для работы с юридическими вопросами, используя модель Llama.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/your-repo-url.git
    ```

2. Перейдите в директорию проекта:

    ```bash
    cd LegalAI-RAG-FastAPI
    ```

3. Создайте виртуальное окружение и установите зависимости:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
    ```

4. Настройте `.env` файл с вашими переменными окружения:

    ```bash
    LLAMA_API_TOKEN=your_llama_api_token
    ```

## Запуск

1. Запустите FastAPI сервер:

    ```bash
    uvicorn app.main:app --reload
    ```

2. Запустите Streamlit интерфейс:

    ```bash
    streamlit run frontend.py
    ```

3. Перейдите по адресу [http://localhost:8501](http://localhost:8501) для работы с интерфейсом.

## Пример использования

Введите вопрос и получите сгенерированный ответ от модели Llama.

