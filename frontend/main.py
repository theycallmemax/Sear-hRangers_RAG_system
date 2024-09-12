import requests
import streamlit as st

st.title("AI консультант по НПА")

# Ввод вопроса от пользователя
question = st.text_area("Введите ваш вопрос:")

# Кнопка отправки запроса
if st.button("Отправить"):
    if question:
        # Отправляем запрос на FastAPI эндпоинт
        response = requests.post(
            "http://backend:8000/generation", json={"question": question}
        )

        if response.status_code == 200:
            # Отображаем ответ на вопрос
            answer = response.json().get("response")
            st.write(f"Ответ: {answer}")

            # Отображаем ответ на вопрос
            acts = response.json().get("acts")
            st.write(f"Ответ: {acts}")
        else:
            st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Пожалуйста, введите вопрос.")
