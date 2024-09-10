from pymilvus import MilvusClient
import os
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    # Инициализация клиента Milvus с параметрами из переменных окружения
    logger.info("Попытка подключения к Milvus...")
    client = MilvusClient(uri=os.getenv('URI_MILVUS'), token=os.getenv('MILVUS_TOKEN'))
    logger.info(f"Успешное подключение к Milvus по адресу {os.getenv('URI_MILVUS')}")
except Exception as e:
    # Логируем ошибку при подключении
    logger.error(f"Ошибка при подключении к Milvus: {str(e)}")
    raise e