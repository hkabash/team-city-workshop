import allure

from pages.base_page import BasePage


class FavoriteProjectsPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page_url = '/favorite/projects'
        self.create_project_selector = 'a[data-test="create-project"]'
        self.new_project_dropdown_item_selector = 'a[class *="ring-list-item"]:has-text("New Project...")'

    @allure.step("Клик на кнопку Create project")
    def click_create_project_button(self):
        self.actions.click_button(self.create_project_selector)

    def click_plus_icon_next_to_project(self, project_id):
        with allure.step(f"Клик на '+' кнопку для проекта c id '{project_id}'"):
            selector = f'[data-project-id="{project_id}"] [class *="Subproject__addBuildConfiguration"]'
            self.actions.click_button(selector)

    def click_new_project_from_dropdown(self, project_id):
        with allure.step(f"Для проекта c id '{project_id}' выбрать New project"):
            self.click_plus_icon_next_to_project(project_id)
            self.actions.wait_for_selector(self.new_project_dropdown_item_selector)
            self.actions.click_button(self.new_project_dropdown_item_selector)

    @allure.step("Проверка URL страницы favorite projects")
    def check_favorite_projects_url(self):
        self.actions.wait_for_url_change(self.page_url)
        self.actions.wait_for_page_load()
