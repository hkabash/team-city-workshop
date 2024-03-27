import allure

from pages.base_page import BasePage
from resources.user_creds import AdminClass


class FirstStartWindow(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.proceed_button_selector = "input#proceedButton"
        self.restore_from_backup_button_selector = "input#restoreButton"

    @allure.step("Клик Proceed")
    def proceed_step(self):
        self.actions.click_button(self.proceed_button_selector)


class Loading(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.loading_icon_selector = ".stage-status__icon"

    @allure.step("Ожидание появления и исчезновения иконки загрузки")
    def wait_loading(self):
        self.actions.is_element_visible(self.loading_icon_selector)
        self.actions.wait_for_disappear_selector(self.loading_icon_selector, timeout=60000)


class Agreement(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = "/showAgreement.html"
        self.accept_checkbox_selector = "input#accept"
        self.continue_selector = '[class="continueBlock"] input[name="Continue"]'

    @allure.step("Клик на чекбокс 'Accept license agreement'")
    def click_accept_checkbox(self):
        self.actions.click_button(self.accept_checkbox_selector)

    @allure.step("Клик Continue")
    def continue_agreement(self):
        self.actions.is_button_active(self.continue_selector)
        self.actions.click_button(self.continue_selector)


class SetupUser(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.username_selector = "input#input_teamcityUsername"
        self.password_selector = "input#password1"
        self.confirm_password_selector = "input#retypedPassword"
        self.create_account_selector = "input.loginButton"

    @allure.step("Заполнение поля username, password, confirm password")
    def populate_user_data(self, username, password):
        self.actions.wait_for_selector(self.username_selector)
        self.actions.input_text(self.username_selector, username)
        self.actions.input_text(self.password_selector, password)
        self.actions.input_text(self.confirm_password_selector, password)

    @allure.step("Клик Create Account")
    def create_user(self):
        self.actions.click_button(self.create_account_selector)


class SetupPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_start_window = FirstStartWindow(self.page)
        self.loading = Loading(self.page)
        self.agreement = Agreement(self.page)
        self.setup_user = SetupUser(self.page)

    def setup(self, username="admin", password="admin"):
        self.actions.navigate(self.page_url)
        self.actions.wait_for_page_load()
        self.first_start_window.proceed_step()
        self.loading.wait_loading()
        self.first_start_window.proceed_step()
        self.loading.wait_loading()
        self.actions.check_url(self.agreement.page_url)
        self.agreement.click_accept_checkbox()
        self.agreement.continue_agreement()
        self.actions.wait_for_page_load()
        self.setup_user.populate_user_data(username, password)
        self.setup_user.create_user()
        self.actions.wait_for_page_load()
