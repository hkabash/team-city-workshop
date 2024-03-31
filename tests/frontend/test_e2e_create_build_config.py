import pytest
import allure

from data.build_config_data import BuildConfigResponseModel
from pages.create_build_config_page import CreateBuildConfigPage
from pages.create_project_from_url_page import CreateProjectFromUrlPage
from pages.create_project_page import CreateProjectPage
from pages.create_vcs_root_page import CreateVcsRootPage
from enums.vcs_root import TEST_REPO_URL
from pages.discover_runners_page import DiscoverRunnersPage
from utils.data_generator import DataGenerator


class TestCreateBuildConfigE2E:
    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка успешного создания билд-конфигурации')
    def test_create_build_config(self, created_project_data, build_config_data, page, super_admin, login):
        project_id = created_project_data.id
        build_config_name = build_config_data.name
        build_config_id = build_config_data.id

        with allure.step("Создание билд-конфигурации"):
            create_build_config_page = CreateBuildConfigPage(page, project_id)
            create_build_config_page.go_to_creation_page()
            create_build_config_page.create_build_config_manually(build_config_name, build_config_id, build_config_name)

        with allure.step("Проверка редиректа на страницу Version Control Settings и появления текста, "
                         "что билд-конфигурация успешно создалась"):
            add_vcs_root_page = CreateVcsRootPage(page)
            add_vcs_root_page.check_vcs_root_creation_page_url()
            add_vcs_root_page.check_build_config_created_message()

        with allure.step("Отправка запроса на получение информации о созданной билд-конфигурации"):
            get_build_config_response = super_admin.api_manager.build_config_api.get_build_config_by_locator(build_config_id).text

        with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
            created_build_config = BuildConfigResponseModel.model_validate_json(get_build_config_response)
        with pytest.assume:
            assert created_build_config.id == build_config_id, \
                f"expected build config id is {build_config_id}, but '{created_build_config.id}' given"
        with pytest.assume:
            assert created_build_config.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{created_build_config.project.id}' given"

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка успешного создания билд-конфигурации и проекта из repository URL')
    @pytest.mark.project_data_name_only(True)
    def test_create_build_config_with_project_from_repo_url(self, page, super_admin, login, project_data):
        project_data = project_data()
        project_name = project_data.name
        project_id = project_name.capitalize()
        build_config_name = DataGenerator.fake_name()
        build_config_id = f"{project_name.capitalize()}_{build_config_name.capitalize()}"

        with allure.step("Создание проекта из Repo URL и билд-конфигурации"):
            create_project_page = CreateProjectPage(page)
            create_project_page.go_to_creation_page()
            create_project_page.create_project_from_url(TEST_REPO_URL)

            create_project_from_url_page = CreateProjectFromUrlPage(page)
            create_project_from_url_page.input_project_name(project_name)
            create_project_from_url_page.input_build_config_name(build_config_name)
            create_project_from_url_page.click_proceed_button()

        with allure.step("Проверка редиректа на страницу Discover Runners и появления текста, "
                         "что проект, билд-конфигурация успешно создались"):
            discover_runners_page = DiscoverRunnersPage(page)
            discover_runners_page.check_discover_runners_page_url()
            discover_runners_page.check_project_and_build_config_created_message(project_name, build_config_name,
                                                                                 TEST_REPO_URL)

        with allure.step("Отправка запроса на получение информации о созданной билд-конфигурации"):
            get_build_config_response = super_admin.api_manager.build_config_api.get_build_config_by_locator(build_config_id).text

        with allure.step("Проверка соответствия параметров созданной билд конфигурации"):
            created_build_config = BuildConfigResponseModel.model_validate_json(get_build_config_response)
        with pytest.assume:
            assert created_build_config.id == build_config_id, \
                f"expected build config id is {build_config_id}, but '{created_build_config.id}' given"
        with pytest.assume:
            assert created_build_config.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{created_build_config.project.id}' given"

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка невозможности создания билд-конфигурации без имени')
    def test_error_on_build_config_creation_without_name(self, page, login, created_project_data):
        project_id = created_project_data.id

        create_build_config_page = CreateBuildConfigPage(page, project_id)
        create_build_config_page.go_to_creation_page()
        create_build_config_page.menu_list_create.click_create_manually()
        create_build_config_page.create_manually_form.click_create_build_config_button()
        with pytest.assume:
            create_build_config_page.create_manually_form.check_name_error("Name must not be empty")
        with pytest.assume:
            create_build_config_page.create_manually_form.check_build_config_id_error("The ID field must not be empty.")

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('Проверка невозможности создания билд-конфигурации c невалидным ID')
    def test_error_on_build_config_creation_with_invalid_id(self, page, login, created_project_data, build_config_data):
        project_id = created_project_data.id
        build_config_data.id = DataGenerator.fake_invalid_id()

        create_build_config_page = CreateBuildConfigPage(page, project_id)
        create_build_config_page.go_to_creation_page()
        create_build_config_page.create_build_config_manually(build_config_data.name, build_config_data.id,
                                                              build_config_data.name)

        create_build_config_page.create_manually_form.check_build_config_id_error(f'''Build configuration or template ID 
                                    "{build_config_data.id}" is 
                                    invalid: starts with non-letter character '{build_config_data.id[0]}'. 
                                    ID should start with a latin letter and contain only latin letters, 
                                    digits and underscores (at most 225 characters).''')
