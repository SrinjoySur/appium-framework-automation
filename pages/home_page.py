

from pages.base_page import BasePage
from utils.wait_util import WaitUtil


class HomePage(BasePage):
    """
    Page object for the Home screen of the app, inherits from BasePage.
    Add Home-specific actions and element locators here.
    """

    def __init__(self, driver, timeout=20):
        """
        Initialize HomePage with driver and timeout.
        Args:
            driver: Appium driver instance.
            timeout (int): Default timeout for waits.
        """
        super().__init__(driver, timeout)

    def tap_hotels_tab(self):
        """
        Tap the Hotels tab on the Home page.
        Raises:
            Exception: If the Hotels tab is not found.
        """
        self.logger.info("Attempting to tap Hotels tab.")
        try:
            hotels_button = WaitUtil.wait_for_element(self.driver, 'xpath', "//a[@data-cy='menu_item_clicked_1']",self.timeout)
            if hotels_button:
                hotels_button.click()
                self.logger.info("Tapped Hotels tab successfully.")
            else:
                self.logger.error("Hotels tab not found on Home Page.")
                raise Exception("Hotels tab not found on Home Page.")
        except Exception as e:
            self.logger.error(f"Exception in tap_hotels_tab: {e}")
            raise

    def close_login_popup(self):
        """
        Close the login popup if present on the Home page.
        """
        close_button = WaitUtil.wait_for_element(self.driver, 'xpath', "//span[@data-cy='loginBottomsheetCrossClick']",
                                                 self.timeout)
        if close_button:
            close_button.click()

    def click_search_field(self):
        """
        Click the search field on the Home page.
        Raises:
            Exception: If the search field is not found.
        """
        self.logger.info("Attempting to click search field.")
        try:
            search_field = WaitUtil.wait_for_element(self.driver, 'xpath',
                                                     "(//button[text()='Near me']/parent::div/preceding-sibling::div/span)[2]",
                                                     self.timeout)
            if search_field:
                search_field.click()
                self.logger.info("Clicked search field successfully.")
            else:
                self.logger.error("Search field not found on Home Page.")
                raise Exception("Search field not found on Home Page.")
        except Exception as e:
            self.logger.error(f"Exception in click_search_field: {e}")
            raise

    def enter_search_text(self, text):
        """
        Enter search text into the search input field.
        Args:
            text (str): The text to enter.
        Raises:
            Exception: If the search input is not found.
        """
        self.logger.info(f"Attempting to enter search text: {text}")
        try:
            search_input = WaitUtil.wait_for_element(self.driver, 'xpath', "//input[@id='autoSuggestWidget']",
                                                     self.timeout)
            if search_input:
                search_input.send_keys(text)
                self.logger.info(f"Entered search text: {text}")
            else:
                self.logger.error("Search input not found on Home Page.")
                raise Exception("Search input not found on Home Page.")
        except Exception as e:
            self.logger.error(f"Exception in enter_search_text: {e}")
            raise

    def select_first_suggestion(self):
        """
        Select the first suggestion from the search dropdown.
        Raises:
            Exception: If the first suggestion is not found.
        """
        self.logger.info("Attempting to select first suggestion.")
        try:
            suggestion = WaitUtil.wait_for_element(self.driver, 'xpath', "//ul[@id='ui-id-1']/li[1]", self.timeout)
            if suggestion:
                suggestion.click()
                self.logger.info("Selected first suggestion successfully.")
            else:
                self.logger.error("First suggestion not found.")
                raise Exception("First suggestion not found.")
        except Exception as e:
            self.logger.error(f"Exception in select_first_suggestion: {e}")
            raise

    def select_tomorrow_date(self):
        """
        Select tomorrow's date in the date picker.
        Raises:
            Exception: If the date element is not found.
        """
        self.logger.info("Attempting to select tomorrow's date.")
        try:
            tomorrow_date = WaitUtil.wait_for_element(self.driver, 'xpath',
                                                      "//td[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))][2]",
                                                      self.timeout)
            if tomorrow_date:
                tomorrow_date.click()
                self.logger.info("Selected tomorrow's date successfully.")
            else:
                self.logger.error("Tomorrow's date not found.")
                raise Exception("Tomorrow's date not found.")
        except Exception as e:
            self.logger.error(f"Exception in select_tomorrow_date: {e}")
            raise

    def tap_search_button(self):
        """
        Tap the search button to initiate the hotel search.
        Raises:
            Exception: If the search button is not found.
        """
        self.logger.info("Attempting to tap search button.")
        try:
            search_button = WaitUtil.wait_for_element(self.driver, 'xpath', "//button[@id='hsw_search_button']",
                                                      self.timeout)
            if search_button:
                search_button.click()
                self.logger.info("Tapped search button successfully.")
            else:
                self.logger.error("Search button not found.")
                raise Exception("Search button not found.")
        except Exception as e:
            self.logger.error(f"Exception in tap_search_button: {e}")
            raise
