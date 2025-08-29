import telebot
from telebot import types
import json
import os
import shutil

# Ищу в сообщение числа.
def search_numbers(message:str):
    answer = []
    numbers = ''
    for i, item in enumerate(message):
        if item.isdigit():
            numbers+=item
        elif item == '.' and numbers != '':
            if item not in numbers:
                numbers+=item
            elif numbers != '':
                answer.append(float(numbers))
                numbers = ''
        elif numbers != '':
            answer.append(float(numbers))
            numbers = ''
    if numbers != '':
        answer.append(float(numbers))
    return answer

# Выводим массив в текст, убирая дробную часть у чисел, если она равна 0
def list_in_str(arr:list):
    result = []
    for num in arr:
        if num.is_integer():  # Проверяем, что дробная часть равна 0
            result.append(str(int(num)))  # Добавляем целую часть как int
        else:
            result.append(str(num))  # Добавляем число целиком
    return " ".join(result)



# Создание кнопки под сообщением
def create_buttons_json(json_name: str, json_type: str, bot):
    with open(f'DB/{json_name}.json', 'r', encoding='utf-8') as f:
        SPEECH_PATTERNS = json.load(f)
    arr = SPEECH_PATTERNS[json_type]["keyboard"]

    markup = types.InlineKeyboardMarkup()
    for item in arr:
        button_params = {
            'text': item["name"],
            'callback_data': item["callback_data"]
        }
        if "url" in item:
            button_params['url'] = item["url"].format(bot_username=bot.get_me().username)
        button = types.InlineKeyboardButton(**button_params)
        markup.row(button)
    return markup

# Извлечение JSONа из сообщения
def get_response_json(json_name: str, json_key: str, is_retry: bool = False):
    file_path = f'DB/{json_name}.json'
    backup_path = f'DB/{json_name}_backup.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            SPEECH_PATTERNS = json.load(f)
        return SPEECH_PATTERNS[str(json_key)]

    except (json.JSONDecodeError, IOError, KeyError):

        if not is_retry:
            # Попытка заменить повреждённый файл на резервную копию
            if os.path.exists(backup_path):

                try:
                    shutil.copyfile(backup_path, file_path)

                except IOError:
                    # Не удалось заменить файл — возвращаем None или выбрасываем ошибку
                    return None
                # Рекурсивный вызов с флагом is_retry=True, чтобы избежать бесконечного цикла
                return get_response_json(json_name, json_key, is_retry=True)
        # Если уже была попытка повторного вызова или резервная копия отсутствует,
        # возвращаем None или можно выбросить исключение
        return None

# Сохранение в JSON сообщения
def give_response_json(json_name: str, json_key: str, json_message):
    file_path = f'DB/{json_name}.json'
    backup_path = f'DB/{json_name}_backup.json'

    # Загружаем существующие данные из файла, если он есть
    data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Ошибка: JSON файл повреждён или недоступен для чтения.")
            return

    # Добавляем или обновляем ключ с сообщением
    data[str(json_key)] = json_message

    # Сохраняем обновлённые данные обратно в файл
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError:
        print("Ошибка записи в файл.")
        return

    # Проверяем целостность файла, пытаясь его прочитать
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Ошибка: после записи файл повреждён.")
        return

    # Создаём копию файла
    try:
        shutil.copyfile(file_path, backup_path)
    except IOError:
        print("Ошибка создания резервной копии файла.")
        return

