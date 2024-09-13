import requests
import streamlit as st
import time  # Добавляем импорт модуля time
from get_act_name import extract_title


# Настройка CSS для белого фона и изменения размера элементов
st.markdown(
    """
    <style>
        
        .block-container {
            padding: 1rem 2rem;  /* Добавляем отступы для большего пространства */
        }
        .stButton button {
            width: 100%;  /* Кнопки на всю ширину блока */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Заголовок приложения
st.title("AI консультант по НПА")

# Ввод вопроса от пользователя
question = st.text_area("Введите ваш вопрос:")

# Кнопка отправки запроса
if st.button("Отправить", key="send_button"):
    if question:
        # Пустое место для ответа
        response_placeholder = st.empty()

        # Показываем, что модель "пишет"
        with st.spinner("Ассистент пишет ответ..."):
            # Имитация запроса на бэкэнд
            response = requests.post(
                "http://backend:8000/generation", json={"question": question}
            )

            if response.status_code == 200:
                answer = response.json().get("response")
                acts = response.json().get("context")

                    # Выводим на экран список НПА
                for i in range(len(acts)):
                    with st.expander(f"{extract_title(acts[i])}"):
                        st.write(f"{acts[i]}")
                # Симуляция того, как LLM пишет ответ по частям
                typed_text = ""
                for char in answer:
                    typed_text += char
                    response_placeholder.text(
                        typed_text
                    )  # Постепенное обновление текста
                    time.sleep(0.01)  # Задержка между символами для эффекта "печати"
            else:
                st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Пожалуйста, введите вопрос.")


# Разделитель
st.markdown("---")

# Секция загрузки файлов снизу
st.subheader("Загрузите файл НПА в базу ассистента")
uploaded_file = st.file_uploader("Загрузите файл НПА", type=["txt", "pdf", "docx"])

# Кнопка для загрузки документа
if st.button("Добавить документ", key="upload_button"):
    if uploaded_file:
        try:
            with st.spinner("Загрузка документа..."):
                file_content = uploaded_file.read()
                # Попробуем декодировать содержимое файла
                try:
                    file_content = file_content.decode('utf-8')
                except UnicodeDecodeError:
                    st.error("Ошибка декодирования файла. Попробуйте другой файл.")
                    file_content = file_content.decode('cp1251', errors='ignore')

                # Отправляем файл на бэкэнд для добавления в базу
                add_doc_response = requests.post(
                    "http://backend:8000/documents/add_document",
                    json={"file_content": file_content}
                )

                if add_doc_response.status_code == 200:
                    st.success("Документ успешно добавлен в базу.")
                else:
                    st.error(f"Ошибка при добавлении документа: {add_doc_response.status_code}")
                    st.error(add_doc_response.json())  # Вывести сообщение об ошибке от сервера
        except Exception as e:
            st.error(f"Ошибка при добавлении документа: {e}")
    else:
        st.warning("Пожалуйста, загрузите файл.")
