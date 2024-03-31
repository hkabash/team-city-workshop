import allure
from pages.base_page import BasePage


class CreateProjectFromUrlPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = ('/admin/objectSetup.html?init=1&objectType=PROJECT&cameFromUrl'
                         '=%2Fadmin%2FcreateObjectMenu.html%3FprojectId%3D_Root%26showMode%3DcreateProjectMenu%26')
        self.project_name_selector = "input#projectName"
        self.build_config_name_selector = "input#buildTypeName"
        self.proceed_button_selector = "input[name=createProject]:has-text('Proceed')"

    @allure.step("Ввод имени проекта")
    def input_project_name(self, name):
        self.actions.input_text(self.project_name_selector, name)

    @allure.step("Ввод имени билд-конфигурации")
    def input_build_config_name(self, name):
        self.actions.input_text(self.build_config_name_selector, name)

    @allure.step("Нажатие кнопки Proceed")
    def click_proceed_button(self):
        self.actions.click_button(self.proceed_button_selector)
