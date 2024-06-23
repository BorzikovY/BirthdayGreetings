# BirthdayGreetings
## Инструкции по установке
***- Клонируйте репозиторий:***
```
git clone https://github.com/BorzikovY/BirthdayGreetings
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

### С Docker

***- Запускаем проект:***
```
docker-compose up --build
```

***- Документация доступна по адресу:***
```
http://127.0.0.1:8080/api/v1/swagger/
```
***- Админка доступа по адресу:***
```
http://127.0.0.1:8080/admin/
```

### Без Docker

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

***- Закомментируйте HOST на 126 строке settings.py***
```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config.get("db_name", ),
        "USER": config.get("db_user"),
        "PASSWORD": config.get("db_password"),
        "HOST": config.get("db_host"),
        "PORT": config.get("db_port"),
    }
}
```

***- Примените миграции:***
```
python manage.py makemigrations
python manage.py migrate
```
***- В папке с файлом manage.py выполните команду для локального запуска:***
```
python manage.py runserver
```
***- Документация доступна по адресу:***
```
http://127.0.0.1:8000/api/v1/swagger/
```
***- Админка доступа по адресу:***
```
http://127.0.0.1:8000/admin/
```
### Примечание
1. Для использования админ-панели создайте админа командой:
```
python manage.py createsuperuser
```
2. Аутентификация через JWT токены. [Читайте документацию](https://www.django-rest-framework.org/api-guide/authentication/)

### todo:
1. Написать тесты.