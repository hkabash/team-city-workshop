from swagger_coverage_py.reporter import CoverageReporter

from api.api_manager import ApiManager
import pytest
import requests
from data.build_config_data import BuildConfigData, BuildConfigResponseModel
from data.build_run_data import BuildConfigRunData
from data.project_data import ProjectData, ProjectResponseModel
from data.user_data import UserData
from entities.user import User, Role
from enums.browser import BROWSERS
from pages.favorite_projects_page import FavoriteProjectsPage
from pages.login_page import LoginPage
from resources.user_creds import SuperAdminCreds, AdminClass
from utils.browser_setup import BrowserSetup
from playwright.sync_api import expect
from enums.host import BASE_URL


expect.set_options(timeout=30_000)


# @pytest.fixture(scope="session", autouse=True)
# def setup_swagger_coverage():
#     reporter = CoverageReporter(api_name="teamcityapi", host=BASE_URL)
#     reporter.cleanup_input_files()
#     reporter.setup("/app/rest/swagger.json")
#     yield
#     reporter.generate_report()


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage(request):
    # Получаем все тесты с маркировкой no_swagger_coverage
    marked_items = [item for item in request.session.items if item.get_closest_marker('no_swagger_coverage')]

    # Проверяем, есть ли запланированные к выполнению тесты с этой маркировкой
    if not marked_items:
        reporter = CoverageReporter(api_name="teamcityapi", host=BASE_URL)
        reporter.cleanup_input_files()
        reporter.setup("/app/rest/swagger.json")
        yield
        reporter.generate_report()
    else:
        # Пропускаем выполнение фикстуры, если есть тест с маркировкой no_swagger_coverage
        yield


@pytest.fixture(params=BROWSERS)
def page(request):
    playwright, browser, context, page = BrowserSetup.setup(browser_type=request.param)
    yield page
    test_name = request.node.name
    BrowserSetup.teardown(context, browser, playwright, test_name)


@pytest.fixture
def browser_for_setup(request):
    playwright, browser, context, page = BrowserSetup.setup()
    yield page
    test_name = request.node.name
    BrowserSetup.teardown(context, browser, playwright, test_name)


@pytest.fixture
def login(page):
    login_page = LoginPage(page)
    login_page.login(username="admin", password="admin")
    home_page = FavoriteProjectsPage(page)
    home_page.check_favorite_projects_url()
    home_page.header.check_user_avatar_visible()


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()
    super_admin = User(SuperAdminCreds.USERNAME, SuperAdminCreds.PASSWORD, new_session, ["SUPER_ADMIN", "g"])
    super_admin.api_manager.auth_api.auth_and_get_csrf_token(super_admin.creds)
    return super_admin


@pytest.fixture
def user_create(user_session, super_admin):
    created_users_pool = []

    def _user_create(role):
        user_data = UserData.create_user_data(role, scope="g")
        super_admin.api_manager.user_api.create_user(user_data)
        new_session = user_session()
        created_users_pool.append(user_data['username'])
        return User(user_data['username'], user_data['password'], new_session, [Role(role)])

    yield _user_create

    for username in created_users_pool:
        super_admin.api_manager.user_api.delete_user(username)


@pytest.fixture
def project_data(super_admin, request):
    project_id_pool = []

    def _project_data():
        project_data_name_only = request.node.get_closest_marker('project_data_name_only')
        if project_data_name_only is None or project_data_name_only.args[0] is False:
            project = ProjectData.create_project_data()
            project_id = project.id
        else:
            project = ProjectData.create_project_data_name_only()
            project_id = project.name.capitalize()
        project_id_pool.append(project_id)
        return project

    yield _project_data

    for project_id in project_id_pool:
        super_admin.api_manager.project_api.clean_up_project(project_id)


@pytest.fixture
def created_project_data(super_admin, project_data):
    """ Создает проект с использованием данных из фикстуры project_data"""
    project_data = project_data()
    response = super_admin.api_manager.project_api.create_project(project_data.model_dump()).text
    project_response = ProjectResponseModel.model_validate_json(response)
    return project_response


@pytest.fixture
def build_config_data(super_admin, created_project_data, request):
    project_id = created_project_data.id
    project_id_and_name_only = request.node.get_closest_marker('project_id_and_name_only')
    if project_id_and_name_only is None or project_id_and_name_only.args[0] is False:
        build_config = BuildConfigData.create_build_config_data(project_id=project_id)
    else:
        build_config = BuildConfigData.create_build_config_data_with_required_fields_only(project_id=project_id)
    return build_config


@pytest.fixture
def created_build_config_data(super_admin, build_config_data):
    """ Создает билд-конфигурацию с использованием данных из фикстуры build_config_data"""
    response = super_admin.api_manager.build_config_api.create_build_config(build_config_data.model_dump()).text
    build_config_response = BuildConfigResponseModel.model_validate_json(response)
    return build_config_response


@pytest.fixture
def build_run_data(super_admin, created_build_config_data):
    build_config_id = created_build_config_data.id
    build_run_data = BuildConfigRunData.create_build_run_data(build_config_id=build_config_id)
    return build_run_data
