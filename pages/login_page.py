import allure
from pages.base_page import BasePage


class LoginFormFragment(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_selector = "input#username"
        self.password_selector = "input#password"
        self.login_button = "input.btn.loginButton"

    def input_username(self, username):
        with allure.step("Ввод username"):
            self.actions.wait_for_selector(self.username_selector)
            self.actions.input_text(self.username_selector, username)

    def input_password(self, password):
        with allure.step("Ввод password"):
            self.actions.wait_for_selector(self.password_selector)
            self.actions.input_text(self.password_selector, password)

    def click_login_button(self):
        with allure.step("Нажатие кнопки Log in"):
            self.actions.click_button(self.login_button)


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/login.html"
        self.login_form = LoginFormFragment(page)

    def go_to_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.actions.navigate(self.page_url)
            self.actions.wait_for_page_load()

    @allure.step("Логин в приложение")
    def login(self, username, password):
        self.go_to_login_page()
        self.login_form.input_username(username)
        self.login_form.input_password(password)
        self.login_form.click_login_button()
