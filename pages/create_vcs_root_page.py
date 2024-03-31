import allure

from pages.base_page import BasePage


class CreateVcsRootPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = f'/admin/editVcsRoot.html'
        self.build_config_created_message_selector = "#unprocessed_buildTypeCreated"
        self.build_config_created_message_text = (f'Build configuration successfully created. '
                                                  f'You can now configure VCS roots.')

    @allure.step("Проверка url страницы добавления vcs root для билд-конфигурации")
    def check_vcs_root_creation_page_url(self):
        self.actions.check_url(self.page_url, equal=False)

    @allure.step("Проверка текста об успешно созданной билд-конфигурации на странице добавления vcs root")
    def check_build_config_created_message(self):
        self.actions.assert_text_in_element(self.build_config_created_message_selector,
                                            self.build_config_created_message_text)
