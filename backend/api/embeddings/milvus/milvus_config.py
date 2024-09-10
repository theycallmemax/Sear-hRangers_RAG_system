from pymilvus import MilvusClient
from api.embeddings.milvus.create_collection import creating_collection
import os
import logging

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Попытка подключения к Milvus...")
try:
    # Инициализация клиента Milvus с параметрами из переменных окружения
    logger.info("Попытка подключения к Milvus...")
    client = MilvusClient(uri=os.getenv('URI_MILVUS'), token=os.getenv('MILVUS_TOKEN'))
    logger.info(f"Успешное подключение к Milvus по адресу {os.getenv('URI_MILVUS')}")
    creating_collection('data/hmao_npa.txt', 'npa', client)
except Exception as e:
    # Логируем ошибку при подключении
    logger.error(f"Ошибка при подключении к Milvus: {str(e)}")
    raise e