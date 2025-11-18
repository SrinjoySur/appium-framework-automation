import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil


class SearchPage(BasePage):
    """Page object for the Search Results screen."""

    def __init__(self, driver, timeout=20):
        super().__init__(driver, timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def close_popup(self):
        self.logger.info("Attempting to close popup if present.")
        try:
            close_button = WaitUtil.wait_for_element(self.driver, 'xpath', "//a[text()='Continue in Browser']", self.timeout)
            if close_button:
                close_button.click()
                self.logger.info("Closed popup successfully.")
            else:
                self.logger.info("No popup to close.")
        except Exception as e:
            self.logger.error(f"Exception in close_popup: {e}")
            # Popup may not always be present

    def get_search_results(self, text):
        self.logger.info(f"Attempting to get search results for: {text}")
        try:
            locator = f"//p[contains(text(),'{text}')]"
            results = WaitUtil.wait_for_element(self.driver, 'xpath', locator, self.timeout)
            if results:
                self.logger.info(f"Search results found for: {text}")
                return results
            self.logger.error(f"No search results found for: {text}.")
            return []
        except Exception as e:
            self.logger.error(f"Exception in get_search_results: {e}")
            return []