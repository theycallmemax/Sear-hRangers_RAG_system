import os

# from api.embeddings.embeddings import model, tokenizer
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

logger.info('Import HuggingFaceBgeEmbeddings')
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# logger.info("Import HuggingFaceEmbeddings")
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings


# Укажите директорию для кеша
cache_dir = "/root/.cache/hf_models"

# huggingface embedding model
logger.info("Init HuggingFaceEmbeddings(model_name='BAAI/bge-m3')")
model_name = "BAAI/bge-m3"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
cache_folder = cache_dir
embeddings = HuggingFaceBgeEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs, cache_folder=cache_folder
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

acts = txt.split("\n")
acts = [Document(doc) for doc in acts if doc]
logger.info(f"Актов {len(acts)}")


retriever.add_documents(acts)
logger.info("Данные загружены")
