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

    if not date:
        return "Дата не найдена"

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
