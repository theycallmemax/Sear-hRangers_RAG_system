import streamlit as st
import requests

from get_act_name import extract_title

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
            # Получаем ответ и список НПА
            answer = response.json().get("response")
            acts = response.json().get("acts")

            # Выводим на экран ответ
            st.write(f"Тип ответаacts: {type(acts)}\nОтвет:{answer}")

            # Выводим на экран список НПА
            for i in range(len(acts)):
                with st.expander(f"{extract_title(acts[i])}"):
                    st.write(f"{acts[i]}")

        else:
            st.error(f"Ошибка: {response.status_code}")
    else:
        st.warning("Пожалуйста, введите вопрос.")