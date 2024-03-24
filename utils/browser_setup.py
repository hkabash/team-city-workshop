import allure
from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv

load_dotenv(override=True)
browser_width = int(os.getenv('BROWSER_WIDTH', '800'))
browser_height = int(os.getenv('BROWSER_HEIGHT', '600'))
headless_mode = os.getenv('HEADLESS', 'True') == 'True'


class BrowserSetup:
    @classmethod
    def setup(cls, browser_type="chromium", headless=headless_mode):
        expect.set_default_timeout(30000)
        playwright = sync_playwright().start()
        browser = getattr(playwright, browser_type).launch(headless=headless)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()
        page.set_viewport_size({"width": browser_width, "height": browser_height})
        return playwright, browser, context, page

    @classmethod
    @allure.step("Teardown: closing browser, stopping playwright, saving trace.zip file")
    def teardown(cls, context, browser, playwright, test_name):
        trace_file = f'result/{test_name}_trace.zip'
        context.tracing.stop(path=trace_file)
        browser.close()
        playwright.stop()
        # Добавляем трассировку как вложение в Allure
        with allure.step("Generating trace.zip file"):
            with open(trace_file, 'rb') as f:
                allure.attach(f.read(), name=test_name + "_trace.zip", attachment_type='application/zip')
