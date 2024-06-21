# BirthdayGreetings
## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone https://github.com/BorzikovY/BirthdayGreetings
```

***- Установите и активируйте виртуальное окружение:***
- для MacOS
```
python3 -m venv venv
```
- для Windows
```
python -m venv venv
source venv/bin/activate
```
 
***- Установите зависимости из файла requirements.txt:***
```
pip install -r requirements.txt
```

***- Создаем файл .env в корневой директории с содержанием .env-example:***
```
secret_key='django-insecure+kzdnswvayl_7rti8!ig6h$lpztx3-@kt1=5054%496h#&ezs'
debug=1
db_name=birthday-greetings
db_user=admin
db_password=admin
db_host=postgres
db_port=5432
db_url=postgresql://admin:admin@postgres:5432/birthday-greetings
allowed_hosts=*
email_host_user=borzikovu32@gmail.com
```

***- Примените миграции:***
```
python manage.py makemigrations
python manage.py migrate
```
***- Создайте суперпользователя:***
```
python manage.py createsuperuser
```
***- В папке с файлом manage.py выполните команду для локального запуска:***
```
python manage.py runserver
```
***- Локально документация доступна по адресу:***
```
http://127.0.0.1:8000/api/v1/swagger/
```
***- Админка доступа по адресу:***
```
http://127.0.0.1:8000/admin/
```
### Примечание
 Аутентификация через JWT токены.

## todo:
1. Написать тесты.
2. Пофиксить проблемы с docker. 