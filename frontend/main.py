import streamlit as st
import requests

st.title("AI консультант по НПА")

# Ввод вопроса от пользователя
question = st.text_area("Введите ваш вопрос:")

# Кнопка отправки запроса
if st.button("Отправить"):
    if question:
        # Отправляем запрос на FastAPI эндпоинт
        response = requests.post(
            "http://backend:8000/generation",
            json={"question": question}
        )
        
        if response.status_code == 200:
            # Отображаем ответ на вопрос
            answer = response.json().get("answer")
            st.write(f"Ответ: {answer}")
        else:
            st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Пожалуйста, введите вопрос.")
