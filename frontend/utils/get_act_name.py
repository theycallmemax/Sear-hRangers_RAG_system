def extract_title(document: str) -> str:
    # Возможные ключевые слова для поиска
    keywords = ["Постановление", "Приказ", "Закон", "Распоряжение"]

    # Приводим документ к нижнему регистру для поиска ключевых слов
    lower_doc = document.lower()

    # Поиск ключевого слова
    keyword = None
    for word in keywords:
        if word.lower() in lower_doc:
            keyword = word
            break

    if not keyword:
        return "Заголовок не найден"

    # Поиск первой даты в формате ДД.ММ.ГГГГ
    date = None
    for i in range(len(document) - 9):
        potential_date = document[i:i + 10]
        if (potential_date[2] == '.' and potential_date[5] == '.' and
                potential_date[:2].isdigit() and potential_date[3:5].isdigit() and potential_date[6:].isdigit()):
            date = potential_date
            break

    # Если дата не найдена, вернуть первые три слова и многоточие
    if not date:
        first_three_words = " ".join(document.split()[:3])  # Берём первые три слова
        return f"{first_three_words}..."  # Добавляем многоточие

    # Поиск номера документа после символа "№"
    number_start = document.find("№")
    if number_start == -1:
        return "Номер не найден"

    number = ""
    for char in document[number_start:]:
        if char.isdigit() or char == "№" or char == "-" or char.isalpha() or char.isspace():
            number += char
        else:
            break

    # Формирование заголовка
    title = f"{keyword} от {date} {number.strip()}"

    return title


def truncate_text(text: str, max_length: int) -> str:
    """
    Обрезает текст до заданного количества символов, сохраняя целые слова.
    
    :param text: Исходный текст
    :param max_length: Максимальная длина строки
    :return: Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    
    # Обрезаем текст до заданного лимита, не разрывая слова
    truncated_text = text[:max_length].rsplit(' ', 1)[0]
    
    return truncated_text + "..."  # Добавляем многоточие, если текст был обрезан
