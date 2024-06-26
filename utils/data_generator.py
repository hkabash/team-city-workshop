import string
from faker import Faker

faker_instance = Faker()


class DataGenerator:
    """
    Фейкер для генерации рандомных данных или значений
    """

    @staticmethod
    def fake_project_id():
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = ''.join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        project_id = first_letter + rest_characters + "Project"
        return project_id

    @staticmethod
    def fake_name():
        return faker_instance.word()

    @staticmethod
    def fake_build_id():
        first_letter = faker_instance.random.choice(string.ascii_letters)
        rest_characters = ''.join(faker_instance.random.choices(string.ascii_letters + string.digits, k=10))
        build_id = first_letter + rest_characters + "Build"
        return build_id

    @staticmethod
    def fake_invalid_id():
        invalid_id = ''.join(faker_instance.random.choices(string.digits, k=5))
        return invalid_id
