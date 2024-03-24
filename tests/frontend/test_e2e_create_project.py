import pytest
import allure

from data.project_data import ProjectResponseModel
from pages.create_project_page import CreateProjectPage
from pages.edit_project_page import EditProjectPage
from pages.favorite_projects_page import FavoriteProjectsPage
from utils.data_generator import DataGenerator


class TestCreateProjectE2E:
    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка успешного создания проекта (Manually) через ссылку на создание проекта')
    def test_create_project_manually_via_url(self, project_data, page, super_admin, login):
        project_data = project_data()
        project_id = project_data.id
        project_name = project_data.name
        project_parent = project_data.parentProject["locator"]

        with allure.step("Создание проекта"):
            create_project_page = CreateProjectPage(page)
            create_project_page.go_to_creation_page()
            create_project_page.create_project_manually(project_name, project_id, project_name)

        with allure.step("Проверка редиректа на страницу редактирования и появления текста, что проект успешно создался"):
            edit_project_page = EditProjectPage(page, project_id, project_name)
            edit_project_page.check_edit_project_url()
            edit_project_page.check_project_created_message()

        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_name).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == project_parent, \
                    f"expected parent project = {project_parent}, but '{created_project.parentProjectId}' given"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка перехода на страницу создания проекта при клике на + рядом с лейблом Projects в хедере')
    def test_redirect_to_create_project_page_on_header_button_click(self, page, login):
        home_page = FavoriteProjectsPage(page)
        home_page.header.go_to_create_project_throw_header_button()

        create_project_page = CreateProjectPage(page)
        create_project_page.check_project_creation_page_url()
        create_project_page.check_create_project_manually_page_elements()

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка перехода на страницу создания проекта при клике на Create Project на Home Page, '
                  'если нет проектов')
    def test_redirect_to_create_project_page_on_new_project_click(self, page, login):
        home_page = FavoriteProjectsPage(page)
        home_page.click_create_project_button()

        create_project_page = CreateProjectPage(page)
        create_project_page.check_project_creation_page_url()
        create_project_page.check_create_project_manually_page_elements()

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка перехода на страницу создания под-проекта при клике на New Project '
                  'из существующего проекта на Home Page')
    def test_redirect_to_create_project_page_on_new_project_click_from_existing_project(self, created_project_data,
                                                                                        page, login):
        parent_project_id = created_project_data.id
        parent_project_name = created_project_data.name
        home_page = FavoriteProjectsPage(page)
        home_page.click_new_project_from_dropdown(parent_project_id)

        create_project_page = CreateProjectPage(page)
        create_url = create_project_page.page_url.replace("_Root", parent_project_id)
        create_project_page.check_project_creation_page_url(create_url)
        create_project_page.check_create_project_manually_page_elements()
        create_project_page.parent_project_fragment.check_parent_project(parent_project_name)

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка создания под-проекта при клике на New Project '
                  'из существующего проекта на Home Page')
    def test_create_sub_project(self, created_project_data, project_data, page, super_admin, login):
        parent_project_id = created_project_data.id
        parent_project_name = created_project_data.name
        project_data = project_data()
        project_id = project_data.id
        project_name = project_data.name

        with allure.step("Переход на страницу создания под-проекта"):
            home_page = FavoriteProjectsPage(page)
            home_page.click_new_project_from_dropdown(parent_project_id)

        with allure.step("Создание проекта"):
            create_project_page = CreateProjectPage(page)
            create_project_page.create_project_manually(project_name, project_id, project_name)

        with allure.step("Проверка редиректа на страницу редактирования и появления текста, что проект успешно создался"):
            edit_project_page = EditProjectPage(page, project_id, project_name)
            edit_project_page.check_edit_project_url()
            edit_project_page.check_project_created_message(project_name, parent_project_name)

        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            response = super_admin.api_manager.project_api.get_project_by_locator(project_name).text
            created_project = ProjectResponseModel.model_validate_json(response)
            with pytest.assume:
                assert created_project.id == project_id, \
                    f"expected project id = {project_id}, but '{created_project.id}' given"
            with pytest.assume:
                assert created_project.parentProjectId == parent_project_id, \
                    f"expected parent project = {parent_project_id}, but '{created_project.parentProjectId}' given"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка невозможности создания проекта без имени')
    def test_error_on_project_creation_without_name(self, page, login):

        create_project_page = CreateProjectPage(page)
        create_project_page.go_to_creation_page()
        create_project_page.create_manually_form.click_create_project_button()
        create_project_page.create_manually_form.check_name_error("Project name is empty")

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка невозможности создания проекта c невалидным ID')
    def test_error_on_project_creation_with_invalid_id(self, page, login, project_data):
        project_data = project_data()
        project_data.id = DataGenerator.fake_invalid_id()

        create_project_page = CreateProjectPage(page)
        create_project_page.go_to_creation_page()
        create_project_page.create_project_manually(project_data.name, project_data.id, project_data.name)
        create_project_page.create_manually_form.check_project_id_error(f'''Project ID "{project_data.id}" is 
                                    invalid: starts with non-letter character '{project_data.id[0]}'. 
                                    ID should start with a latin letter and contain only latin letters, 
                                    digits and underscores (at most 225 characters).''')
