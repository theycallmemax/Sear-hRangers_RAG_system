from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from pymilvus import connections
import logging

logger = logging.getLogger(__name__)

# Подключение к Milvus
def init_milvus():
    connections.connect(host="127.0.0.1", port="19530")  # Убедись, что порт соответствует порту Milvus

    # Проверка подключения
    logger.info("Подключение к Milvus установлено")

# Инициализация модели эмбеддингов
def get_vector_store():
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    vector_store = Milvus.from_existing_index(embedding=embeddings, index_name="npa_index")
    return vector_store

def create_milvus_index(embeddings_data):
    """
    Создает индекс и загружает данные эмбеддингов в Milvus.
    """
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-large-en-v1.5")
    vector_store = Milvus(embedding=embeddings, collection_name="npa_index")

    logger.info("Добавляем эмбеддинги в Milvus...")
    vector_store.add_texts(embeddings_data)
    logger.info("Эмбеддинги успешно добавлены!")
