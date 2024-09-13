# SearchRangers_RAG_system

Проект представляет собой FastAPI API и Streamlit интерфейс для работы с юридическими вопросами, используя модель Llama.

## Ветви

В проекте существует два основных решения:

- Основное решение находится в ветке `feature/rag`, где реализована логика Retrieval-Augmented Generation (RAG) вручную. (появится в ближайшее время)
- Другое решение находится в ветке `main`, где логика реализована при помощт langchain. (в ближайшее время появится публичный адрес)



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
    MAX_TOKENS=4096
    TEMPERATURE=0.5
    COLLECTION_NAME=npa
    ```

## Запуск

## Docker

Если хотите запустить проект в контейнерах, используйте Docker Compose:

```bash
docker-compose up --build
```

Если хотите запустить проект локально, то измените зависимости и:

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


## API и эндпоинты

### 1. **POST /generation**

- **Описание**: Эндпоинт для генерации ответа на юридический вопрос.
- **Параметры**:
  - `question` (строка) – Вопрос, на который нужно сгенерировать ответ.
- **Функциональность**: Использует модель и функционал для поиска в базе данных нормативных актов. Возвращает ответ и контекст на основе найденных данных.
- **Return**: response, context


### 2. **POST /documents/add_document**
- **Описание**: Эндпоинт для добавления документов (нормативных актов).
- **Параметры**:
file_content (строка) – Содержимое файла с нормативными актами.
- **Функциональность**: Разделяет содержимое файла на строки и добавляет их в базу данных Milvus для последующего поиска.
- **Return**: response, context
## Описание файлов: "message": "Документ успешно добавлен"



backend/api/embeddings/llama/llama_model.py: Модуль для генерации ответов на основе модели Llama.
backend/api/embeddings/milvus/: Модули для взаимодействия с Milvus (хранение и поиск эмбеддингов).
backend/api/embeddings_utils.py: Вспомогательные функции для создания эмбеддингов, суммаризации и преобразования данных.
backend/api/endpoints.py: Основные маршруты API.
frontend/main.py: Логика Streamlit для пользовательского интерфейса.
