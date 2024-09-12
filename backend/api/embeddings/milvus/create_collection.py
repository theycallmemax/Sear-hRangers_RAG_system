import os

from api.embeddings.embeddings import model, tokenizer
from api.embeddings.embeddings_utils import (
    converting_data,
    make_embedding,
    make_summary,
)
from api.embeddings.llama.llama_model import llama
from api.embeddings.prompts import question_1, system_prompt
from langchain.retrievers import ParentDocumentRetriever
from langchain.schema.document import Document
from langchain.storage import InMemoryStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_milvus import Milvus
from logger import logger

# logger.info('Import HuggingFaceBgeEmbeddings')
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings

logger.info("Import HuggingFaceEmbeddings")
from langchain_huggingface import HuggingFaceEmbeddings

# huggingface embedding model
logger.info("Init HuggingFaceEmbeddings(model_name='BAAI/bge-m3')")
model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)
logger.info("Embeddings init complete")

URI = os.getenv("URI_MILVUS")
child_chunk_size = 500
parent_chunk_size = 3000
use_parent_splitter = False
k = 3

if use_parent_splitter:
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=parent_chunk_size)
else:
    parent_splitter = None

child_splitter = RecursiveCharacterTextSplitter(chunk_size=child_chunk_size)

# model_name = "BAAI/bge-large-en-v1.5"
# model_kwargs = {"device": "cpu"}
# encode_kwargs = {"normalize_embeddings": True}  # set True to compute cosine similarity
# logger.info('Create HuggingFaceBgeEmbeddings')
# embeddings = HuggingFaceBgeEmbeddings(
#     model_name=model_name,
#     model_kwargs=model_kwargs,
#     encode_kwargs=encode_kwargs,
# )

vectorstore = Milvus(
    embedding_function=embeddings, connection_args={"uri": URI}, auto_id=True
)

store = InMemoryStore()

retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
    search_kwargs={"k": k},
)
data_path = "data/hmao_npa.txt"
with open(data_path, encoding="utf8") as file:
    txt = file.read()

acts = txt.split("\n")[:10]
acts = [Document(doc) for doc in acts if doc]

retriever.add_documents(acts)


def creating_collection(data_path, collection_name, client):
    try:
        # Проверяем наличие коллекции
        if client.has_collection(collection_name):
            logger.info(
                f"Коллекция '{collection_name}' уже существует, создание пропущено."
            )
            return "Коллекция уже существует"

        # Вытаскиваем акты
        logger.info(f"Начало чтения файла: {data_path}")
        with open(data_path, encoding="utf8") as file:
            txt = file.read()

        acts = txt.split("\n")
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
        logger.info(
            f"Эмбеддинги сгенерированы. Размерность эмбеддингов: {embedding_dim}"
        )

        # Преобразование данных для вставки в коллекцию
        logger.info("Преобразование данных для вставки в Milvus")
        insert_data = converting_data(embeddings, summarys, acts)

        # Создание коллекции данных в Milvus
        logger.info(
            f"Создание коллекции '{collection_name}' с размерностью {embedding_dim}"
        )
        client.create_collection(
            collection_name=collection_name,
            dimension=embedding_dim,
            metric_type="COSINE",  # Inner product distance
        )

        # Вставка данных в коллекцию
        logger.info(f"Вставка данных в коллекцию '{collection_name}'")
        client.insert(collection_name=collection_name, data=insert_data)
        logger.info(f"Коллекция '{collection_name}' успешно создана и данные добавлены")

        return "Коллекция создана"

    except Exception as e:
        logger.error(f"Ошибка при создании коллекции: {str(e)}")
        raise e
