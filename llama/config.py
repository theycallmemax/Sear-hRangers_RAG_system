import os
import logging

logger = logging.getLogger(__name__)

def get_llama_api_token() -> str:
    """
    Получает токен LlamaAPI из переменных окружения.
    
    Возвращает:
        str: Токен LlamaAPI.
    """
    llama_api_token = os.getenv('LLAMA_API_TOKEN')
    if not llama_api_token:
        logger.error("LLAMA_API_TOKEN не найден. Убедитесь, что он установлен в файле .env.")
        raise ValueError("LLAMA_API_TOKEN not found. Ensure it's set in your .env file.")
    
    return llama_api_token
