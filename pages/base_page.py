from playwright.sync_api import Page
from enums.host import BASE_URL
from pages.actions.page_actions import PageActions
from pages.components.header import Header


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._base_url = BASE_URL
        self._endpoint = ""
        self.actions = PageActions(page)
        self.header = Header(self.actions)

    @property
    def page_url(self):
        return self._base_url + self._endpoint

    @page_url.setter
    def page_url(self, endpoint):
        self._endpoint = endpoint
