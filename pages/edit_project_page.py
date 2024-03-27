import allure
from pages.base_page import BasePage


class EditProjectPage(BasePage):
    def __init__(self, page, project_id, project_name):
        super().__init__(page)
        self.page_url = f'/admin/editProject.html?projectId={project_id}'
        self.project_created_message_selector = "#message_projectCreated"
        self.project_created_message_text = (f'Project "{project_name}" has been successfully created. '
                                             'You can now create a build configuration.')

    @allure.step("Проверка url страницы редактирования проекта")
    def check_edit_project_url(self):
        self.actions.wait_for_url_change(self.page_url)

    @allure.step("Проверка текста об успешно созданном проекте на странице редактирования")
    def check_project_created_message(self, project_name=None, parent_project=None):
        if parent_project is None:
            self.actions.assert_text_in_element(self.project_created_message_selector, self.project_created_message_text)
        else:
            message = self.project_created_message_text.replace(project_name, f"{parent_project} / {project_name}")
            self.actions.assert_text_in_element(self.project_created_message_selector, message)
