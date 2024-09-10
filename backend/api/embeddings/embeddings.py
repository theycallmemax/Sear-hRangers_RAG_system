from api.embeddings.llama.llama_model import generate_with_llama
from api.embeddings.embeddings_utils import make_embedding

def generate_embeddings(query):
    """
    Функция для генерации эмбеддингов с использованием Llama API.
    """
    # Используем функцию для генерации ответа через Llama API
    response = generate_with_llama(query)

    # Генерация эмбеддингов из ответа с помощью вспомогательной функции
    embeddings = make_embedding(response)
    
    return embeddings
