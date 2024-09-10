import torch.nn.functional as F
from torch import Tensor
from tqdm import tqdm
from api.embeddings.llama.llama_model import generate_with_llama
from transformers import AutoTokenizer, AutoModel
import os

import torch.nn.functional as F
from torch import Tensor
from tqdm import tqdm
import logging
from api.embeddings.llama.llama_model import generate_with_llama
from transformers import AutoTokenizer, AutoModel
import os

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Инициализация модели и токенизатора
logger.info(f"Инициализация модели и токенизатора с моделью: {os.getenv('EMBEDDING_MODEL_NAME')}")
tokenizer = AutoTokenizer.from_pretrained(os.getenv('EMBEDDING_MODEL_NAME'))
model = AutoModel.from_pretrained(os.getenv('EMBEDDING_MODEL_NAME'))

# For embedding model multilingual-e5-base
def average_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def make_embedding(input_texts, model, tokenizer):
    try:
        logger.info(f"Начало создания эмбеддингов для {len(input_texts)} текстов")
        batch_dict = tokenizer(
            input_texts, max_length=512, 
            padding=True, truncation=True, 
            return_tensors='pt'
        )
        outputs = model(**batch_dict)
        embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=1)
        logger.info("Эмбеддинги успешно созданы")
        return embeddings.tolist()
    except Exception as e:
        logger.error(f"Ошибка при создании эмбеддингов: {str(e)}")
        raise e

# Converting data for insertion
def converting_data(embeds, summaries, original_texts, id_begin=0):
    try:
        logger.info(f"Начало преобразования данных для {len(embeds)} эмбеддингов")
        data = []
        for i, (embed, summary, original_text) in enumerate(zip(embeds, summaries, original_texts)):
            data.append({
                'id': id_begin + i, 
                'vector': embed, 
                'summary': summary, 
                'original_text': original_text,  # TODO: add meta data
            })
        logger.info("Данные успешно преобразованы для вставки")
        return data
    except Exception as e:
        logger.error(f"Ошибка при преобразовании данных: {str(e)}")
        raise e

# Суммаризация
def make_summary(docs, llm, system_prompt, question, get_answer_func=generate_with_llama):
    try:
        logger.info(f"Начало суммаризации для {len(docs)} документов")
        summaries = []
        for doc in tqdm(docs):
            summaries.append(get_answer_func(doc, llm, system_prompt, question))
        logger.info(f"Суммаризация завершена для {len(summaries)} документов")
        return summaries
    except Exception as e:
        logger.error(f"Ошибка при суммаризации документов: {str(e)}")
        raise e
