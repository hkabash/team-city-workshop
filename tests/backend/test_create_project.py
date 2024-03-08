from http import HTTPStatus

import pytest
import allure
from enums.roles import Roles
from data.project_data import ProjectResponseModel


class TestCreateProject:
    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка успешного создания проекта разными ролями')
    @allure.description('Тест проверяет успешное создание нового проекта доступными ролями')
    @pytest.mark.parametrize("user_role", [Roles.PROJECT_ADMIN.value,
                                           Roles.SYSTEM_ADMIN.value,
                                           Roles.AGENT_MANAGER.value])
    def test_project_create_with_role(self, project_data, user_create, user_role):
        project_data = project_data()
        project_user = user_create(role=user_role)
        project_user.api_manager.auth_api.auth_and_get_csrf_token(project_user.creds)
        with allure.step('Отправка запроса на создание проекта'):
            response = project_user.api_manager.project_api.create_project(project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert project_response.id == project_data.id, \
                f"expected project id is {project_data.id}, but '{project_response.id}' given"
        with pytest.assume:
            assert project_response.parentProjectId == project_data.parentProject["locator"], \
                (f"expected parent project id is {project_data.parentProject['locator']}, "
                 f"but '{project_response.parentProjectId}' given")

        with allure.step("Отправка запроса на получение информации о созданном проекте"):
            get_project_response = project_user.api_manager.project_api.get_project_by_locator(project_data.id).text

        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            created_project = ProjectResponseModel.model_validate_json(get_project_response)
        with pytest.assume:
            assert created_project.id == project_data.id, \
                f"expected project id is {project_data.id}, but '{created_project.id}' given"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания проекта невалидными ролями')
    @allure.description('Тест проверяет, что проект не создан невалидными ролями и что его нет в общем списке проектов.')
    @pytest.mark.parametrize("user_role",
                             [Roles.PROJECT_DEVELOPER.value,
                              Roles.PROJECT_VIEWER.value])
    def test_project_not_created_with_unavailable_role(self, project_data, user_create, user_role):
        project_data = project_data()
        project_user = user_create(role=user_role)
        project_user.api_manager.auth_api.auth_and_get_csrf_token(project_user.creds)
        with allure.step('Отправка запроса на создание проекта'):
            response = project_user.api_manager.project_api.create_project(project_data.model_dump(),
                                                                           expected_status=HTTPStatus.FORBIDDEN).text
        with pytest.assume:
            assert "Access denied. Check the user has enough permissions to perform the operation." in response

        with allure.step('Отправка запроса на получение информации о всех проектах'):
            get_projects_response = project_user.api_manager.project_api.get_projects().json()
            project_ids = [project.get('id', "") for project in get_projects_response.get('project', [])]
        with pytest.assume:
            assert project_data.id not in project_ids, \
                f"Project with id '{project_data.id}' is present in projects"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка создания проекта только с именем')
    @allure.description('Тест проверяет создание нового проекта, если передать только имя')
    @pytest.mark.project_data_name_only(True)
    def test_project_created_with_name_only(self, super_admin, project_data):
        project_data = project_data()
        project_name = project_data.name
        expected_project_id = project_name.capitalize()
        expected_parent_project_id = "_Root"

        with allure.step('Отправка запроса на создание проекта'):
            response = super_admin.api_manager.project_api.create_project(project_data.model_dump()).text
            project_response = ProjectResponseModel.model_validate_json(response)
        with pytest.assume:
            assert project_response.name == project_name, \
                f"expected project name is {project_name}, but '{project_response.name}' given"

        with allure.step('Отправка запроса на получение информации о созданном проекте'):
            get_project_response = super_admin.api_manager.project_api.get_project_by_locator(project_name).text

        with allure.step("Проверка соответствия параметров созданного проекта с отправленными данными"):
            created_project = ProjectResponseModel.model_validate_json(get_project_response)

            with pytest.assume:
                assert created_project.name == project_name, \
                    f"expected project name is '{project_name}', but '{created_project.name}' given"

            with pytest.assume:
                assert created_project.id == expected_project_id, \
                    f"expected project id is '{expected_project_id}', but '{created_project.id}' given"

            with pytest.assume:
                assert created_project.parentProject.id == expected_parent_project_id, \
                    f"expected parent project is '{expected_parent_project_id}', but '{created_project.parentProject.id}' given"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания проекта без имени')
    @allure.description('Тест проверяет, что проект не создан и что его нет в общем списке проектов.')
    def test_project_not_created_without_name(self, super_admin, project_data):
        project_data = project_data()
        project_data_dict = project_data.model_dump()
        project_data_dict.pop("name")

        with allure.step('Отправка запроса на создание проекта'):
            response = super_admin.api_manager.project_api.create_project(project_data_dict,
                                                                          expected_status=HTTPStatus.BAD_REQUEST).text
        with allure.step('Проверка текста в ответе'):
            with pytest.assume:
                assert f"Project name cannot be empty." in response

        with allure.step('Отправка запроса на получение информации о всех проектах'):
            get_projects_response = super_admin.api_manager.project_api.get_projects().json()
            project_ids = [project.get('id', "") for project in get_projects_response.get('project', [])]
        with pytest.assume:
            assert project_data.id not in project_ids, \
                f"Project with '{project_data.id}' is present in projects"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания проекта с существующим именем')
    @allure.description('Тест проверяет, что проект не может быть создан с уже существующим именем')
    def test_project_not_created_with_duplicated_name(self, super_admin, project_data):
        project_data_1 = project_data()
        project_name_1 = project_data_1.name
        project_data_2 = project_data()
        project_data_2_dict = project_data_2.model_dump()
        project_data_2_dict.update(name=project_name_1)

        with allure.step('Отправка запроса на создание проекта 1'):
            response = super_admin.api_manager.project_api.create_project(project_data_1.model_dump()).text

        with allure.step('Отправка запроса на создание проекта 2'):
            response = super_admin.api_manager.project_api.create_project(project_data_2_dict,
                                                                          expected_status=HTTPStatus.BAD_REQUEST).text
        with allure.step('Проверка ошибки в теле ответа'):
            with pytest.assume:
                assert f"Project with this name already exists: {project_name_1}" in response

        with allure.step('Отправка запроса на получение информации о всех проектах'):
            get_projects_response = super_admin.api_manager.project_api.get_projects().json()
            project_ids = [project.get('id', "") for project in get_projects_response.get('project', [])]

        with allure.step('Проверка отстутствия проекта с id "{project_data_2.id} в списке проектов'):
            with pytest.assume:
                assert project_data_2.id not in project_ids, \
                    f"Project with '{project_data_2.id}' is present in projects"

    @allure.feature('Управление проектами')
    @allure.story('Создание проекта')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('Проверка невозможности создания проекта без тела запроса')
    @allure.description('Тест проверяет, что проект не создан при отправке запроса без тела')
    def test_project_not_created_without_body(self, super_admin):
        with allure.step('Отправка запроса на создание проекта'):
            response = super_admin.api_manager.project_api.create_project({},
                                                                          expected_status=HTTPStatus.BAD_REQUEST).text
        with allure.step('Проверка ошибки в теле ответа'):
            with pytest.assume:
                assert f"Project name cannot be empty." in response
