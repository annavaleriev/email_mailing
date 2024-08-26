from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from pytz import timezone

from config import settings

DATABASE = settings.DATABASES["default"]  # Получение настроек базы данных

job_stores = {  # Создание хранилища задач
    "default": SQLAlchemyJobStore(  # Использование SQLAlchemyJobStore
        url=f'postgresql://{DATABASE["USER"]}:{DATABASE["PASSWORD"]}'  # Подключение к базе данных
            f'@{DATABASE["HOST"]}:{DATABASE["PORT"]}/{DATABASE["NAME"]}'  # Подключение к базе данных
    )
}

scheduler = BackgroundScheduler(jobstores=job_stores, timezone=timezone(settings.TIME_ZONE))
# Создание планировщика
scheduler.start()  # Запуск планировщика
