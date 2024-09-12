import os

from api.embeddings.llama.llama_model import generate_with_llama
from api.embeddings.milvus.create_collection import retriever
from api.embeddings.prompts import question_2, question_3, system_prompt
from logger import logger


def make_request(query):
    try:
        # Переформулирование запроса на юридический язык
        logger.info(f"Переформулирование запроса: {query}")
        query = generate_with_llama(
            context=query,
            system_prompt=system_prompt,
            question=question_3,
            max_tokens=os.getenv("MAX_TOKENS"),
            temperature=os.getenv("TEMPERATURE"),
        )
        logger.info(f"Запрос переформулирован: {query}")

        # Создание эмбеддинга для запроса
        logger.info(f"Создание эмбеддинга для запроса: {query}")

        # embedding_query = make_embedding(query, model, tokenizer)  # TODO замена
        # logger.info(
        #     f"Эмбеддинг для запроса создан. Размерность: {len(embedding_query[0])}"
        # )

        # Поиск наиболее подходящих актов

        # logger.info(f"Поиск в коллекции '{os.getenv('COLLECTION_NAME')}' по запросу")
        logger.info("Поиск в ретривере по запросу: {query}")
        results = retriever.invoke(query)
        logger.info(f"Поиск завершен. Найдено {len(results)} результатов")
        logger.info(f"ВАЖНЕЙШАЯ ХУЙНЯ ИЗ ЛАНГЧЕЙНА {results}")

        acts = [res.page_content for res in results]
        acts_for_llm = "\n\n".join(acts)

        logger.info("Генерация ответа с использованием Llama на основе контекста")
        answer = generate_with_llama(
            context=acts_for_llm,
            system_prompt=system_prompt,
            question=question_2,
            max_tokens=os.getenv("MAX_TOKENS"),
            temperature=os.getenv("TEMPERATURE"),
            quary=query,
        )

        # TODO замена
        # search_res = client.search(
        #     collection_name=os.getenv("COLLECTION_NAME"),
        #     data=embedding_query,
        #     limit=5,
        #     search_params={"metric_type": "COSINE", "params": {}},
        #     output_fields=["summary"],  # Возвращаем текстовое поле
        # )
        # logger.info(f"Поиск завершен. Найдено {len(search_res[0])} результатов")
        # logger.info(f"ВАЖНЕЙШАЯ ХУЙНЯ  {search_res[0]}")
        # Извлечение актов для ответа
        # acts_for_answer = "\n\n".join(
        #     [res["entity"]["summary"] for res in search_res[0]]
        # )
        # logger.info("Акты для ответа сформированы")

        # acts = [res["entity"]["summary"] for res in search_res[0]]

        # Генерация ответа с использованием Llama
        # logger.info("Генерация ответа с использованием Llama на основе контекста")
        # answer = generate_with_llama(
        #     context=acts_for_answer,
        #     system_prompt=system_prompt,
        #     question=question_2,
        #     max_tokens=os.getenv("MAX_TOKENS"),
        #     temperature=os.getenv("TEMPERATURE"),
        #     quary=query,
        # )
        logger.info(f"Ответ успешно сгенерирован: {answer}")
        logger.info(f"АКТЫ ДЛЯ ОТВЕТА: {acts}")
        return answer, acts

    except Exception as e:
        logger.error(f"Ошибка при обработке запроса: {str(e)}")
        raise e
