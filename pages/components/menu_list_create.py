import allure
from pages.actions.page_actions import PageActions


class MenuListCreateFragment:
    def __init__(self, actions: PageActions):
        self.actions = actions
        self.create_from_url_selector = "a.createOption:has-text('From a repository URL')"
        self.create_manually_selector = "a.createOption:has-text(' Manually')"

    @allure.step("Выбор создания проекта по URL")
    def click_create_from_url(self):
        self.actions.click_button(self.create_from_url_selector)

    @allure.step("Выбор создания проекта мануально")
    def click_create_manually(self):
        self.actions.is_button_active(self.create_manually_selector)
        self.actions.click_button(self.create_manually_selector)

    @allure.step("Проверка активности кнопки создания проекта по URL")
    def check_create_from_url_active(self):
        self.actions.is_button_active(self.create_from_url_selector)

    @allure.step("Проверка активности кнопки создания проекта мануально")
    def check_create_manually_active(self):
        self.actions.is_button_active(self.create_manually_selector)

    @allure.step("Проверка видимости кнопки мануально")
    def check_manually_visible(self):
        self.actions.is_element_visible(self.create_manually_selector)

    @allure.step("Проверка видимости кнопки создания проекта по URL")
    def check_create_from_url_visible(self):
        self.actions.is_element_visible(self.create_manually_selector)
