import requests
import logging

from django.core.exceptions import ValidationError
from typing import Optional, Dict, Any


from core.constants import (
    API_BASE_URL, API_URL_CARS_LIST, API_URL_FINES_LIST_PER_PAGE
)
from fine.models import Car

logger = logging.getLogger('api')


class BaseGibddAPIClient:

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[
        Dict[str, Any]]:
        """
        Универсальный метод для выполнения запросов.

        :param method: HTTP-метод (GET, POST и т.д.)
        :param endpoint: Конечная точка API
        :param kwargs: Дополнительные параметры для requests
        (params, json, data и т.д.)
        :return: JSON-ответ или None в случае ошибки
        """
        url = f"{API_BASE_URL}{endpoint}"
        logger.debug(f"Выполнение запроса: {method} {url}")

        try:
            response = self.session.request(method, url, **kwargs)

            # Проверка статуса HTTP-запроса
            if not response.ok:
                logger.error(
                    f"HTTP Error: {response.status_code} - {response.text}")
                return None

            # Проверка, что ответ — JSON
            try:
                json_data = response.json()
            except ValueError:
                logger.error("Ответ не в виде JSON")
                return None

            # Проверка поля success
            if not json_data.get("success", False):
                logger.error(
                    f"API Error: {json_data.get('message',
                                                'Неизвестная ошибка')}")
                return None

            return json_data.get("data")

        except requests.exceptions.RequestException as e:
            logger.error(f"Запрос вернул ошибку: {str(e)}")
            return None

    def check_token(self) -> bool:
        """
        Проверка работоспособности токена.
        :return: True, если токен рабочий, иначе False
        """
        logger.info("Проверка токена...")
        response = self._make_request(method="GET", endpoint=API_URL_CARS_LIST)

        if response is None:
            logger.error(
                "Токен недействителен или произошла ошибка при проверке")
            return False

        logger.info("Токен действителен")
        return True


class GibddCarsAPIClient(BaseGibddAPIClient):
    """
    Класс для работы с машинами
    """
    def get_cars(self) -> Optional[Dict[str, Any]]:
        """
        Получение списка автомобилей.
        :return: Словарь с данными автомобилей или None в случае ошибки
        """
        return self._make_request(method="GET", endpoint=API_URL_CAR_LIST)

    def parse_cars(self, raw_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Парсинг данных автомобилей.
        :param raw_data: Сырые данные из API
        :return: Обработанные данные или None в случае ошибки
        """
        if not raw_data:
            return None

        parsed_data = {}
        for key, car_data in raw_data.items():
            try:
                parsed_data[key] = {
                    "external_id": car_data.get("id"),
                    'group_id': car_data.get('group_id', 0),
                    'auto_cdi': car_data.get('auto_cdi', ''),
                    'auto_number': car_data.get('auto_number', ''),
                    'auto_region': car_data.get('auto_region', ''),
                    'auto_name': car_data.get('auto_name', ''),
                    'valid_number': car_data.get('valid_number', False),
                    'check_platon': car_data.get('check_platon', False),
                    'owner_inn': car_data.get('owner_inn', ''),
                    'auto_vin': car_data.get('auto_vin', ''),
                    'check_auto': car_data.get('check_auto', False),
                    'check_pass': car_data.get('check_pass', False)
                }
            except KeyError as e:
                logger.error(f"Ошибка данных машины №{key}: {str(e)}")
                continue

        return parsed_data

    def save_cars_to_db(self, parsed_data: Dict[str, Any]) -> bool:
        """
        Сохранение данных автомобилей в базу данных.
        :param parsed_data: Обработанные данные автомобилей
        :return: True, если данные успешно сохранены, иначе False
        """
        if not parsed_data:
            logger.warning("Нет данных для сохранения")
            return False

        success_count = 0
        for key, car_data in parsed_data.items():
            try:
                Car.objects.update_or_create(
                    external_id=car_data["external_id"],
                    defaults=car_data
                )
                success_count += 1
            except ValidationError as e:
                logger.error(f"Ошибка валидации данных для машины №{key}: "
                             f"{str(e)}")
            except Exception as e:
                logger.error(f"Ошибка сохранения машины №{key}: {str(e)}")

        logger.info(f"Успешно сохранено {success_count} автомобилей")
        return success_count > 0


class GibddFinesAPIClient(BaseGibddAPIClient):
    """
    Класс для работы со штрафами.
    """
    def all_fine(self) -> Optional[Dict[str, Any]]:
        """
        Получение списка штрафов.
        :return: Словарь с данными штрафов или None в случае ошибки
        """
        return self._make_request(method="GET",
                                  endpoint=API_URL_FINES_LIST_PER_PAGE)
