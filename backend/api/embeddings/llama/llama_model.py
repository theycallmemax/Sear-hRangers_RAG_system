from llamaapi import LlamaAPI
import logging
import os


# Логгер для отслеживания действий
logger = logging.getLogger(__name__)

# Инициализация LlamaAPI с использованием токена
llama_api_token = os.getenv('LLAMA_API_TOKEN')
if not llama_api_token:
    raise ValueError("LLAMA_API_TOKEN not found. Ensure it's set in your .env file.")

llama = LlamaAPI(llama_api_token)

def generate_with_llama(context, system_prompt, question, max_tokens=4096, temperature=0.1, quary='') -> str:
    """
    Генерация текста с использованием LlamaAPI на основе предоставленного контекста, системного сообщения и вопроса.
    
    Аргументы:
        context (str): Контекст, который должен быть использован для ответа.
        system_prompt (str): Системное сообщение для Llama API.
        question (str): Вопрос пользователя, на который нужно ответить.
        max_tokens (int): Максимальное количество токенов (по умолчанию 4096).
        temperature (float): Параметр температуры для контроля случайности (по умолчанию 0.1).
        quary (str): Дополнительный запрос для форматирования (по умолчанию '').

    Возвращает:
        str: Сгенерированный текст ответа.
    """
    logger.info("Отправка запроса к LlamaAPI...")

    # Формируем запрос к Llama API
    api_request_json = {
        'model': 'llama3.1-8b',
        'max_tokens': max_tokens,
        'temperature': temperature,
        "messages": [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': question.format(context=context, quary=quary)}
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