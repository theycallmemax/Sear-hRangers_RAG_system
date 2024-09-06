from llamaapi import LlamaAPI
from llama.config import get_llama_api_token  # Импорт функции для получения токена
import logging

# Логгер для отслеживания действий
logger = logging.getLogger(__name__)

# Инициализация LlamaAPI с использованием токена
llama_api_token = get_llama_api_token()
if not llama_api_token:
    raise ValueError("LLAMA_API_TOKEN not found. Ensure it's set in your .env file.")

llama = LlamaAPI(llama_api_token)

def generate_with_llama(prompt: str) -> str:
    """
    Генерация текста с использованием LlamaAPI.
    Аргументы:
        prompt (str): Вопрос пользователя или другой ввод.
    
    Возвращает:
        str: Сгенерированный текст ответа.
    """
    logger.info("Отправка запроса к LlamaAPI...")
    
    api_request_json = {
        "model": "llama3.1-8b",
        "messages": [
            {"role": "system", "content": "Отвечай на русском языке."},
            {"role": "user", "content": prompt},
        ]
    }

    try:
        # Выполнение запроса к LlamaAPI
        response = llama.run(api_request_json)
        response_data = response.json()
        
        if 'error' in response_data:
            logger.error(f"Ошибка в ответе LlamaAPI: {response_data['error']}")
            return f"Ошибка: {response_data['error']}"
        
        # Возвращаем сгенерированный текст
        logger.info("Ответ успешно сгенерирован.")
        return response_data['choices'][0]['message']['content']
    
    except Exception as e:
        logger.error(f"Ошибка при генерации текста: {str(e)}")
        return "Ошибка при генерации текста"
