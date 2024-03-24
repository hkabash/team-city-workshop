import allure

from pages.agents_page import AgentsPage
from pages.favorite_projects_page import FavoriteProjectsPage
from pages.setup_page import SetupPage


def test_setup(browser_for_setup):
    with allure.step("Сетап"):
        setup_page = SetupPage(browser_for_setup)
        setup_page.setup()
        home_page = FavoriteProjectsPage(browser_for_setup)
        home_page.check_favorite_projects_url()
        home_page.header.check_user_avatar_visible()
        agents_page = AgentsPage(browser_for_setup)
        agents_page.authorize_agent()
