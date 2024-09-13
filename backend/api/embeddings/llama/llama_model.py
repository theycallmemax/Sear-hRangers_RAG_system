import os

from llamaapi import LlamaAPI
from logger import logger

# Инициализация LlamaAPI с использованием токена
llama_api_token = os.getenv("LLAMA_API_TOKEN")
if not llama_api_token:
    raise ValueError("LLAMA_API_TOKEN not found. Ensure it's set in your .env file.")

llama = LlamaAPI(llama_api_token)


def generate_with_llama(context: str, question: str, system_prompt, quary, max_tokens, temperature) -> str:
    """
    Генерация текста с использованием LlamaAPI на основе предоставленного контекста, системного сообщения и вопроса.


    Аргументы:
        context (str): Контекст, который должен быть использован для ответа.
        question (str): Вопрос пользователя, на который нужно ответить.
        query (str): Дополнительный запрос для форматирования (по умолчанию '').

    Возвращает:
        str: Сгенерированный текст ответа.
    """
    logger.info("Отправка запроса к LlamaAPI...")
    models = ["llama3.1-405b", "llama3.1-70b", "llama3.1-8b"]

    # Обрабатываем каждую модель по очереди
    for model in models:
        # Формируем запрос к Llama API
        api_request_json = {
            "model": model,
            "max_tokens": os.getenv("MAX_TOKENS"),
            "temperature": os.getenv("TEMPERATURE"),
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": question.format(context=context, query=quary),
                },
            ],
        }

        try:
            # Выполнение запроса к LlamaAPI
            response = llama.run(api_request_json)
            response_data = response.json()

            if "error" in response_data:
                logger.error(f"Ошибка в ответе LlamaAPI: {response_data['error']}")
                continue  # Переходим к следующей модели

            # Возвращаем сгенерированный текст
            logger.info("Ответ успешно сгенерирован.")
            return response_data["choices"][0]["message"]["content"]

        except Exception as req_err:
            # Логируем ошибку и пробуем следующую модель
            logger.error(f"Ошибка с моделью {model}: {req_err}")
            continue

    # Если все модели не удались, возвращаем сообщение об ошибке
    return "Не удалось сгенерировать ответ ни одной из моделей."