import allure
from pages.base_page import BasePage
from pages.components.menu_list_create import MenuListCreateFragment


class CreateBuildConfigFormFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.parent_project_dropdown_selector = "button[data-test-project-select-anchor]"
        self.build_config_name_selector = "input#buildTypeName"
        self.build_config_id_selector = "input#buildTypeExternalId"
        self.build_config_description_selector = "input#description"
        self.create_build_config_button = "input[name=createBuildType]"
        self.name_error_selector = "#error_buildTypeName"
        self.build_config_id_error_selector = "#error_buildTypeExternalId"
        self.show_advanced_options_toggle = ("#advancedSettingsToggle_createBuildTypeForm"
                                             ":has-text('Show advanced options')")

    def input_build_config_details(self, name, build_config_id, description):
        with allure.step("Ввод данных для создания билд-конфигурации"):
            self.actions.wait_for_selector(self.build_config_name_selector)
            self.actions.input_text(self.build_config_name_selector, name)
            self.actions.input_text(self.build_config_id_selector, build_config_id)
            self.actions.input_text(self.build_config_description_selector, description)

    def click_create_build_config_button(self):
        with allure.step("Нажатие кнопки создания билд-конфигурации"):
            self.actions.click_button(self.create_build_config_button)

    def check_name_error(self, error_text):
        with allure.step(f"Проверка текста ошибки {error_text} под полем Name"):
            self.actions.assert_text_in_element(self.name_error_selector, error_text)

    def check_build_config_id_error(self, error_text):
        with allure.step(f"Проверка текста ошибки под полем Build configuration ID"):
            self.actions.assert_text_in_element(self.build_config_id_error_selector, error_text)


class CreateBuildConfigPage(BasePage):
    def __init__(self, page, project_id):
        super().__init__(page)
        self.page_url = (f'/admin/createObjectMenu.html?projectId={project_id}&showMode=createBuildTypeMenu&'
                         f'cameFromUrl=%2Fadmin%2FeditProject.html%3FprojectId%3D{project_id}')
        self.menu_list_create = MenuListCreateFragment(self.actions)
        self.create_manually_form = CreateBuildConfigFormFragment(page)

    def go_to_creation_page(self):
        with allure.step("Переход на страницу создания билд-конфигурации"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    def create_build_config_manually(self, name, build_config_id, description):
        self.menu_list_create.click_create_manually()
        self.create_manually_form.input_build_config_details(name, build_config_id, description)
        self.create_manually_form.click_create_build_config_button()
