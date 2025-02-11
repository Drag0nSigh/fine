USER = 'user'
API = 'api'
ADMIN = 'admin'
USER_ROLE_CHOICES = [
    (USER, 'user'),
    (API, 'api'),
    (ADMIN, 'admin'),
]
MAX_LENGTH_USERNAME = 64
MAX_LENGTH_EMAIL = 64
MAX_LENGTH_ID_TG = 15
MAX_LENGTH_ROLE = 10
API_URL_CARS_LIST = '/partner_auto/'
API_BASE_URL = 'https://api.onlinegibdd.ru/v3'
API_URL_FINES_LIST_PER_PAGE = '/partner_fines/get_per_page/'
