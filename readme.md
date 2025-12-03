# Это проект на fastapi посвященный бронированию отелей 
## Главная цель проекта - отработка основных технологий backend разработки 
### Перечень использованных технологий:
1. Python 3.12
2. fastapi
3. pydentic
4. postgresql




### Напоминалка для работы с бд
1. Чтобы запустить дбивер нужна команда dbeaver-ce
ссылка на инфу про дбивер https://losst.pro/ustanovka-dbeaver-v-ubuntu-22-04
2. Чтобы проверить статус постгреса нужна команда sudo systemctl status postgresql.service
ссылка на инфу про постгрес https://firstvds.ru/technology/ustanovka-postgresql-na-ubuntu
3. создание миграции
alembic revision --autogenerate -m "add rooms"
4. применение миграции 
alembic upgrade head