import allure
from pages.base_page import BasePage
from pages.components.menu_list_create import MenuListCreateFragment


class ResNavigationFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.last_parent_project_link = '[class="last project"]'

    def check_last_parent_project_link(self, expected_parent_name):
        with allure.step(f"Проверка наличия текста {expected_parent_name} в Last Parent Project Link"):
            self.actions.assert_text_in_element(self.last_parent_project_link, expected_parent_name)


class ParentProjectFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.parent_project_dropdown_selector = "button[data-test-project-select-anchor]"

    def check_parent_project_dropdown_visible(self):
        with allure.step("Проверка видимости дропдауна Parent Project"):
            self.actions.is_element_visible(self.parent_project_dropdown_selector)

    def check_parent_project(self, expected_parent_name):
        with allure.step(f"Проверка наличия текста {expected_parent_name} в Parent Project"):
            self.actions.assert_text_in_element(self.parent_project_dropdown_selector, expected_parent_name)


class CreateProjectManuallyFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.project_name_selector = "input#name"
        self.project_id_selector = "input#externalId"
        self.project_description_selector = "input#description"
        self.create_project_button = "input#createProject"
        self.name_error_selector = "#errorName"
        self.project_id_error_selector = "#errorExternalId"

    def input_project_details(self, name, project_id, description):
        with allure.step("Ввод данных для создания проекта"):
            self.actions.wait_for_selector(self.project_name_selector)
            self.actions.input_text(self.project_name_selector, name)
            self.actions.input_text(self.project_id_selector, project_id)
            self.actions.input_text(self.project_description_selector, description)

    def click_create_project_button(self):
        with allure.step("Нажатие кнопки создания проекта"):
            self.actions.click_button(self.create_project_button)

    def check_project_name_input_visible(self):
        with allure.step("Проверка видимости поля Name"):
            self.actions.is_element_visible(self.project_name_selector)

    def check_project_id_input_visible(self):
        with allure.step("Проверка видимости поля Project ID"):
            self.actions.is_element_visible(self.project_id_selector)

    def check_project_description_input_visible(self):
        with allure.step("Проверка видимости поля Description"):
            self.actions.is_element_visible(self.project_description_selector)

    def check_project_create_button_visible(self):
        with allure.step("Проверка видимости кнопки Create"):
            self.actions.is_element_visible(self.create_project_button)

    def check_name_error(self, error_text):
        with allure.step(f"Проверка текста ошибки {error_text} под полем Name"):
            self.actions.assert_text_in_element(self.name_error_selector, error_text)

    def check_project_id_error(self, error_text):
        with allure.step(f"Проверка текста ошибки под полем Project Id"):
            self.actions.assert_text_in_element(self.project_id_error_selector, error_text)


class CreateProjectFromUrlFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.repository_url_selector = "input#url"
        self.username_selector = "input#username"
        self.password_selector = "input#password"
        self.proceed_button_selector = "[name = createProjectFromUrl]:has-text('Proceed')"

    def input_repo_url(self, repo_url):
        with allure.step("Ввод в поле Repository URL"):
            self.actions.wait_for_selector(self.repository_url_selector)
            self.actions.input_text(self.repository_url_selector, repo_url)

    def click_proceed_button(self):
        with allure.step("Нажатие кнопки Proceed"):
            self.actions.click_button(self.proceed_button_selector)


class CreateProjectPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/createObjectMenu.html?projectId=_Root&showMode=createProjectMenu'
                         '&cameFromUrl=http%3A%2F%2Flocalhost%3A8111%2Ffavorite%2Fprojects')
        self.menu_list_create = MenuListCreateFragment(self.actions)
        self.res_navigation_fragment = ResNavigationFragment(page)
        self.parent_project_fragment = ParentProjectFragment(page)
        self.create_manually_form = CreateProjectManuallyFragment(page)
        self.create_from_url_form = CreateProjectFromUrlFragment(page)

    def check_project_creation_page_url(self, url=None):
        if url is None:
            url = self.page_url
        self.actions.check_url(url, equal=False)

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания проекта"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_project_manually(self, name, project_id, description):
        self.menu_list_create.click_create_manually()
        self.create_manually_form.input_project_details(name, project_id, description)
        self.create_manually_form.click_create_project_button()

    def check_create_project_manually_page_elements(self):
        self.menu_list_create.check_create_from_url_visible()
        self.menu_list_create.check_manually_visible()
        self.create_manually_form.check_project_name_input_visible()
        self.create_manually_form.check_project_id_input_visible()
        self.create_manually_form.check_project_description_input_visible()
        self.create_manually_form.check_project_create_button_visible()

    def create_project_from_url(self, url):
        self.menu_list_create.click_create_from_url()
        self.create_from_url_form.input_repo_url(url)
        self.create_from_url_form.click_proceed_button()
