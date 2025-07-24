Создаём виртуальное окружение (venv):
    python -m venv myenv

Активируем виртуальное окружение:
    Windiws:
    myenv\Scripts\activate

    Linux/Mac:
    source myenv/bin/activate

Установите библиотеки из requirements.txt:
    pip install -r requirements.txt

Деактивация venv:
    deactivate

Проверка установленных библиотек:
    pip list

Экспортируйте список библиотек в requirements.txt
    pip freeze > requirements.txt