import logging
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_embeddings_model():
    logger.info("Инициализация модели эмбеддингов HuggingFaceBgeEmbeddings")
    model_name = "BAAI/bge-large-en-v1.5"
    model_kwargs = {'device': 'cpu'}  # Используйте 'cuda', если доступен GPU
    encode_kwargs = {'normalize_embeddings': True}
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    
    logger.info("Модель эмбеддингов инициализирована")
    return embeddings
