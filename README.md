# SearchRangers_RAG_system

Проект представляет собой FastAPI API и Streamlit интерфейс для работы с юридическими вопросами, используя Retrieval-Augmented Generation (RAG) на основе модели Llama. Он предназначен для поиска релевантных нормативно-правовых актов и генерации ответов на юридические вопросы с использованием контекста.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/theycallmemax/SearchRangers_RAG_system
    ```

2. Перейдите в директорию проекта:
    

4. Настройте `.env` файл с вашими переменными окружения:

    ```bash
    LLAMA_API_TOKEN=your_llama_api_token
    URI_MILVUS=localhost:19530
    MILVUS_TOKEN=your_milvus_token
    EMBEDDING_MODEL_NAME=multilingual-e5-base
    MAX_TOKENS=500
    TEMPERATURE=0.7

    ```

## Запуск

1. Запустите FastAPI сервер:

    ```bash
    uvicorn backend.main:app --reload --loop asyncio
    ```

2. Запустите Streamlit интерфейс:

    ```bash
    streamlit run frontend/main.py
    ```

3. Перейдите по адресу [http://localhost:8501](http://localhost:8501) для работы с интерфейсом.

## Пример использования

Введите юридический вопрос в интерфейсе, и система автоматически выполнит поиск нормативных актов, сгенерирует контекст и ответ с помощью модели Llama.


## Структура

```bash
    SearchRangers_RAG_system/
│
├── backend/                             # Backend для FastAPI
│   ├── api/                             # Папка с API
│   │   ├── embeddings/                  # Логика эмбеддингов и запросов
│   │   │   ├── llama/                   # Логика взаимодействия с моделью Llama
│   │   │   │   └── llama_model.py       # Модель Llama для генерации ответов
│   │   │   ├── milvus/                  # Логика взаимодействия с Milvus
│   │   │   │   ├── create_collection.py # Создание коллекции в Milvus
│   │   │   │   ├── milvus_config.py     # Конфигурация подключения к Milvus
│   │   │   ├── embeddings_utils.py      # Утилиты для создания эмбеддингов
│   │   │   ├── make_request.py          # Логика обработки запросов
│   │   │   ├── prompts.py               # Промпты для взаимодействия с моделью
│   │   ├── endpoints.py                 # API маршруты для взаимодействия с системой
│   │   ├── __init__.py                  # Инициализация роутеров
│   ├── data/                            # Папка с данными (текстовые файлы НПА)
│   │   └── hmao_npa.txt                 # Пример данных для работы с системой
│   ├── templates/                       # HTML шаблоны для FastAPI (если требуется)
│   │   └── index.html                   # Главная страница
│   ├── main.py                          # Точка входа для FastAPI
│   ├── Dockerfile                       # Dockerfile для запуска backend
│
├── frontend/                            # Папка с фронтендом (Streamlit)
│   ├── main.py                          # Основной файл для Streamlit интерфейса
│   ├── Dockerfile                       # Dockerfile для запуска frontend
│
├── volumes/                             # Папка для томов Docker (если используется)
├── .env                                 # Переменные окружения
├── requirements.txt                     # Зависимости для проекта
├── docker-compose.yml                   # Docker Compose для запуска всей системы
└── README.md                            # Документация проекта

```

## Docker

Если хотите запустить проект в контейнерах, используйте Docker Compose:

```bash
docker-compose up --build
```

## Описание файлов:

backend/api/embeddings/llama/llama_model.py: Модуль для генерации ответов на основе модели Llama.
backend/api/embeddings/milvus/: Модули для взаимодействия с Milvus (хранение и поиск эмбеддингов).
backend/api/embeddings_utils.py: Вспомогательные функции для создания эмбеддингов, суммаризации и преобразования данных.
backend/api/endpoints.py: Основные маршруты API.
frontend/main.py: Логика Streamlit для пользовательского интерфейса.
