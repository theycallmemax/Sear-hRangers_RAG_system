import os

class Config:
    """
    Конфигурационный файл для настройки приложения
    """
    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
    LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "/path/to/llama")
