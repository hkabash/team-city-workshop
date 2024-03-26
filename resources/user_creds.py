import os
from dotenv import load_dotenv


load_dotenv()


class SuperAdminCreds:
    """
    Креды супер админа. Для авторизации в TeamCity под супер админом оставляется пустым username,
    а пароль - токен из логов контейнера
    """
    USERNAME = ''
    PASSWORD = os.getenv('SUPER_ADMIN_TOKEN')


class AdminClass:
    """
    Креды админа.
    """
    USERNAME = os.getenv('ADMIN_USERNAME')
    PASSWORD = os.getenv('ADMIN_PASSWORD')
