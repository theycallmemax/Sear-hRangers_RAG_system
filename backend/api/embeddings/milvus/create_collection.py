from api.embeddings.prompts import system_prompt, question_1
from api.embeddings.embeddings_utils import *
from api.embeddings.milvus.milvus_config import client
from api.embeddings.llama.llama_model import llama
import logging


# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def creating_collection(data_path, collection_name, token):
    try:
        # Вытаскиваем акты
        logger.info(f"Начало чтения файла: {data_path}")
        with open(data_path, encoding='utf8') as file:
            txt = file.read()

        acts = txt.split('\n')
        acts = [doc for doc in acts if doc]
        logger.info(f"Файл прочитан, количество документов: {len(acts)}")

        # Делаем суммаризацию нормативных актов
        logger.info(f"Начало суммаризации первых {len(acts[:10])} документов")
        summarys = make_summary(acts[:10], llama, system_prompt, question_1)
        logger.info(f"Суммаризация завершена. Количество суммаризаций: {len(summarys)}")

        # Генерация эмбеддингов
        logger.info(f"Начало генерации эмбеддингов для {len(summarys)} суммаризаций")
        embeddings = make_embedding(summarys, model, tokenizer)
        embedding_dim = len(embeddings[0])
        logger.info(f"Эмбеддинги сгенерированы. Размерность эмбеддингов: {embedding_dim}")

        # Преобразование данных для вставки в коллекцию
        logger.info("Преобразование данных для вставки в Milvus")
        insert_data = converting_data(embeddings, summarys, acts)

        # Создание коллекции данных в Milvus
        logger.info(f"Создание коллекции '{collection_name}' с размерностью {embedding_dim}")
        client.create_collection(
            collection_name=collection_name,
            dimension=embedding_dim,
            metric_type="COSINE"  # Inner product distance
        )

        # Вставка данных в коллекцию
        logger.info(f"Вставка данных в коллекцию '{collection_name}'")
        client.insert(collection_name=collection_name, data=insert_data)
        logger.info(f"Коллекция '{collection_name}' успешно создана и данные добавлены")
        
        return 'Коллекция создана'
    except Exception as e:
        logger.error(f"Ошибка при создании коллекции: {str(e)}")
        raise e
