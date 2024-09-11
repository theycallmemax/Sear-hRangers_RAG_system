import os

from api.embeddings.embeddings_utils import make_embedding
from api.embeddings.llama.llama_model import generate_with_llama
from logger import logger
from transformers import AutoModel, AutoTokenizer

# Инициализация модели и токенизатора
logger.info(
    f"Инициализация модели и токенизатора с моделью: {os.getenv('EMBEDDING_MODEL_NAME')}"
)


tokenizer = AutoTokenizer.from_pretrained(os.getenv("EMBEDDING_MODEL_NAME"))
model = AutoModel.from_pretrained(os.getenv("EMBEDDING_MODEL_NAME"))


def generate_embeddings(query):
    """
    Функция для генерации эмбеддингов с использованием Llama API.
    """
    # Используем функцию для генерации ответа через Llama API
    response = generate_with_llama(query)

    # Генерация эмбеддингов из ответа с помощью вспомогательной функции
    embeddings = make_embedding(response)

    return embeddings
