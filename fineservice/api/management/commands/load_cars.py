import os
import logging

from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from api.clients import GibddCarAPIClient

logger = logging.getLogger('api')  # Используем логгер 'api'

class Command(BaseCommand):
    help = 'Загружает данные об автомобилях из API onlinegibdd.ru'

    def handle(self, *args, **kwargs):
        logger.info("Начало загрузки данных...")

        api_key = os.getenv('TOKEN_ONLINEGIBDD')
        client = GibddCarAPIClient(api_key)
        client.check_token()

        # Получение данных
        raw_data = client.get_cars()
        if not raw_data:
            logger.error("Не удалось получить данные")
            return

        # Парсинг данных
        parsed_data = client.parse_cars(raw_data)
        if not parsed_data:
            logger.error("Не удалось распарсить данные")
            return

        # Сохранение данных в БД
        if client.save_cars_to_db(parsed_data):
            logger.info("Данные успешно загружены")
        else:
            logger.error("Ошибка при сохранении данных")
