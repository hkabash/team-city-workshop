import allure
from pages.base_page import BasePage


class DiscoverRunnersPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = f'/admin/discoverRunners'
        self.unprocessed_object_created_message_selector = "#unprocessed_objectsCreated"

    @allure.step("Проверка url страницы discoverRunners")
    def check_discover_runners_page_url(self):
        self.actions.check_url(self.page_url, equal=False)

    @allure.step("Проверка текста об успешно созданных объектах")
    def check_project_and_build_config_created_message(self, project_name, build_config_name, repo_url):
        message = (f'New project "{project_name}", build configuration "{build_config_name}" '
                   f'and VCS root "{repo_url}#refs/heads/main" have been successfully created.')
        self.actions.assert_text_in_element(self.unprocessed_object_created_message_selector, message)
