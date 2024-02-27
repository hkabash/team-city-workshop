from http import HTTPStatus
import pytest
import allure
from data.build_config_data import BuildConfigResponseModel


class TestBuildConfig:

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка успешного создания билд-конфигурации')
    @allure.description('Тест проверяет успешное создание новой билд-конфигурации')
    def test_build_config_create(self, super_admin, created_project_data, build_config_data):
        project_id = created_project_data.id
        build_config_id = build_config_data.id
        with allure.step('Отправка запроса на создание билд-конфигурации'):
            response = super_admin.api_manager.build_config_api.create_build_config(build_config_data.model_dump()).text
            build_config_response = BuildConfigResponseModel.model_validate_json(response)

        with pytest.assume:
            assert build_config_response.id == build_config_id, \
                f"expected build config id is {build_config_id}, but '{build_config_response.id}' given"

        with pytest.assume:
            assert build_config_response.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{build_config_response.project.id}' given"

        with allure.step("Отправка запроса на получение информации о созданной билд-конфигурации"):
            get_build_config_response = super_admin.api_manager.build_config_api.get_build_config_by_locator(build_config_id).text

        with allure.step("проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
            created_build_config = BuildConfigResponseModel.model_validate_json(get_build_config_response)
        with pytest.assume:
            assert created_build_config.id == build_config_id, \
                f"expected build config id is {build_config_id}, but '{created_build_config.id}' given"
        with pytest.assume:
            assert created_build_config.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{created_build_config.project.id}' given"

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка создания билд-конфигурации только с обязательными параметрами (имя и id проекта)')
    @allure.description('Тест проверяет создание новой билд-конфигурации только с именем и id проекта с теле запроса')
    @pytest.mark.project_id_and_name_only(True)
    def test_build_config_create_with_name_and_project_only(self, super_admin, created_project_data, build_config_data):
        project_id = created_project_data.id
        build_config_name = build_config_data.name
        expected_build_config_id = f"{project_id}_{build_config_name.capitalize()}"

        with allure.step('Отправка запроса на создание билд-конфигурации'):
            response = super_admin.api_manager.build_config_api.create_build_config(build_config_data.model_dump()).text
            build_config_response = BuildConfigResponseModel.model_validate_json(response)

        with pytest.assume:
            assert build_config_response.name == build_config_name, \
                f"expected build config name id is {build_config_name}, but '{build_config_response.name}' given"
        with pytest.assume:
            assert build_config_response.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{build_config_response.project.id}' given"
        with pytest.assume:
            assert build_config_response.id == expected_build_config_id, \
                f"expected build config id is {expected_build_config_id}, but '{build_config_response.id}' given"

        with allure.step("Отправка запроса на получение информации о созданной билд-конфигурации"):
            get_build_config_response = super_admin.api_manager.build_config_api.get_build_config_by_locator(expected_build_config_id).text

        with allure.step("Проверка соответствия параметров созданной билд конфигурации с отправленными данными"):
            created_build_config = BuildConfigResponseModel.model_validate_json(get_build_config_response)
        with pytest.assume:
            assert created_build_config.name == build_config_name, \
                f"expected build config name id is {build_config_name}, but '{created_build_config.name}' given"
        with pytest.assume:
            assert created_build_config.project.id == project_id, \
                f"expected build config project id is {project_id}, but '{created_build_config.project.id}' given"
        with pytest.assume:
            assert created_build_config.id == expected_build_config_id, \
                f"expected build config id is {expected_build_config_id}, but '{created_build_config.id}' given"

    @allure.feature('Управление билд-конфигурациями')
    @allure.story('Создание билд-конфигурации')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания билд-конфигурации без обязательны полей (id проекта или имени)')
    @allure.description('Тест проверяет, что билд-конфигурация не создана без id проекта или имени')
    @pytest.mark.parametrize("missing_parameter", ["project",
                                                   "name"])
    def test_build_config_not_created_without_required_parameters(self, super_admin, build_config_data, missing_parameter):
        build_config_id = build_config_data.id
        build_config_data_dict = build_config_data.model_dump()
        build_config_data_dict.pop(missing_parameter)

        with allure.step('Отправка запроса на создание билд-конфигурации'):
            response = super_admin.api_manager.build_config_api.create_build_config(build_config_data_dict,
                                                                                    expected_status=HTTPStatus.BAD_REQUEST).text
        error_text = None
        if missing_parameter == "project":
            error_text = " Build type creation request should contain project node."
        elif missing_parameter == "name":
            error_text = "When creating a build type, non empty name should be provided."

        with allure.step('Проверка ошибки в теле ответа'):
            with pytest.assume:
                if missing_parameter == "project":
                    assert error_text in response
                elif missing_parameter == "name":
                    assert error_text in response

        with allure.step('Отправка запроса на получение информации о всех билд конфигурациях'):
            get_build_configs_response = super_admin.api_manager.build_config_api.get_build_configs().json()
            build_config_ids = [build_config.get('id', "") for build_config in
                                get_build_configs_response.get('buildType', [])]
        with pytest.assume:
            assert build_config_id not in build_config_ids, \
                f"Build with id '{build_config_id}' is present in build configs"



