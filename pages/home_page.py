

from pages.base_page import BasePage
from utils.wait_util import WaitUtil
import time


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
        Tap the Hotels tab on the Home page with enhanced wait strategies.
        Raises:
            Exception: If the Hotels tab is not found.
        """
        self.logger.info("Attempting to tap Hotels tab.")
        
        # Wait for page to load first
        self.wait_for_page_load()
        
        # Try multiple locators for the hotels tab
        locators = [
            "//a[@data-cy='menu_item_clicked_1']",
            "//a[contains(@class, 'menu_item') and contains(text(), 'Hotels')]",
            "//nav//a[contains(text(), 'Hotels')]",
            "[data-cy='menu_item_clicked_1']"
        ]
        
        for i, locator in enumerate(locators):
            try:
                by_type = 'css_selector' if locator.startswith('[') else 'xpath'
                self.logger.info(f"Trying locator {i+1}: {locator}")
                
                hotels_button = WaitUtil.wait_for_clickable(self.driver, by_type, locator, 15)
                if hotels_button:
                    # Scroll element into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", hotels_button)
                    time.sleep(1)
                    hotels_button.click()
                    self.logger.info("Tapped Hotels tab successfully.")
                    return
                    
            except Exception as e:
                self.logger.warning(f"Failed with locator {i+1}: {e}")
                continue
        
        # Last resort: try with JavaScript
        try:
            self.wait_and_click_with_js('xpath', "//a[@data-cy='menu_item_clicked_1']")
            self.logger.info("Hotels tab clicked with JavaScript.")
            return
        except:
            pass
            
        raise Exception("Hotels tab not found with any strategy")

    def close_login_popup(self):
        """
        Close the login popup if present on the Home page.
        """
        self.logger.info("Checking for login popup to close.")
        
        # Multiple possible close button locators
        close_locators = [
            "//span[@data-cy='loginBottomsheetCrossClick']",
            "//button[contains(@class, 'close')]",
            "//div[contains(@class, 'modal')]//button[contains(@class, 'close')]",
            "[data-cy='loginBottomsheetCrossClick']"
        ]
        
        for locator in close_locators:
            try:
                by_type = 'css_selector' if locator.startswith('[') else 'xpath'
                close_button = WaitUtil.wait_for_element(self.driver, by_type, locator, 5)
                if close_button:
                    close_button.click()
                    self.logger.info("Login popup closed successfully.")
                    time.sleep(1)  # Wait for popup to disappear
                    return
            except:
                continue
        
        self.logger.info("No login popup found or already closed.")

    def click_search_field(self):
        """
        Click on the location/city selection area (the 'Near me' button area).
        Raises:
            Exception: If the search area is not found.
        """
        self.logger.info("Attempting to click location/city search area.")
        
        # Based on actual page structure, look for the 'Near me' button and surrounding area
        location_locators = [
            "//button[text()='Near me']",
            "//button[contains(@class, 'nearMeBtn')]",
            "//div[contains(@class, 'nearMeBtn')]",
            "//button[contains(text(), 'Near')]",
            "//div[.//button[text()='Near me']]",  # Parent div of Near me button
            "//span[text()='City, Area or Property']",
            "//div[contains(@class, 'location')]//button"
        ]
        
        for i, locator in enumerate(location_locators):
            try:
                self.logger.info(f"Trying location selector {i+1}: {locator}")
                
                location_element = WaitUtil.wait_for_clickable(self.driver, 'xpath', locator, 10)
                if location_element:
                    # Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", location_element)
                    time.sleep(1)
                    location_element.click()
                    self.logger.info(f"Clicked location selector successfully with locator {i+1}.")
                    time.sleep(2)  # Wait for location dialog to open
                    return
                    
            except Exception as e:
                self.logger.warning(f"Location selector {i+1} failed: {e}")
                continue
        
        raise Exception("Location/city search area not found with any strategy")

    def enter_search_text(self, text):
        """
        Enter search text after opening the location search dialog.
        Args:
            text (str): The text to enter.
        Raises:
            Exception: If the search input is not found.
        """
        self.logger.info(f"Attempting to enter search text: {text}")
        
        # After clicking the location area, look for the input field that appears
        input_locators = [
            "//input[@id='react-autowhatever-1-section-0-item-0']",  # Common MakeMyTrip input
            "//input[contains(@placeholder, 'Enter city')]",
            "//input[contains(@placeholder, 'City')]", 
            "//input[contains(@placeholder, 'Where')]",
            "//input[@type='text' and @class]",  # Any text input with class
            "//div[contains(@class, 'search')]//input",
            "//input[contains(@id, 'city')]",
            "//input[contains(@name, 'city')]"
        ]
        
        for i, locator in enumerate(input_locators):
            try:
                self.logger.info(f"Trying input locator {i+1}: {locator}")
                
                search_input = WaitUtil.wait_for_element(self.driver, 'xpath', locator, 15)
                if search_input:
                    # Clear field and enter text
                    search_input.clear()
                    search_input.send_keys(text)
                    self.logger.info(f"Entered search text: {text}")
                    time.sleep(3)  # Wait for suggestions to load
                    return
                    
            except Exception as e:
                self.logger.warning(f"Input locator {i+1} failed: {e}")
                continue
        
        # Fallback: try to find any focused input field
        try:
            self.logger.info("Trying to find any active/focused input field")
            active_input = self.driver.execute_script("return document.activeElement;")
            if active_input and active_input.tag_name.lower() == 'input':
                active_input.clear()
                active_input.send_keys(text)
                self.logger.info(f"Entered text in active input: {text}")
                time.sleep(3)
                return
        except Exception as e:
            self.logger.warning(f"Active element approach failed: {e}")
        
        raise Exception("Search input field not found with any strategy")

    def select_first_suggestion(self):
        """
        Select the first suggestion from the search dropdown with multiple strategies.
        Raises:
            Exception: If the first suggestion is not found.
        """
        self.logger.info("Attempting to select first suggestion.")
        
        # Wait a bit for suggestions to load
        time.sleep(2)
        
        # Multiple locators for suggestions
        suggestion_locators = [
            "//ul[@id='ui-id-1']/li[1]",
            "//ul[contains(@class, 'suggestion')]/li[1]",
            "//div[contains(@class, 'autoComplete')]//li[1]",
            "//div[@class='react-autosuggest__suggestions-container']//li[1]",
            ".react-autosuggest__suggestion:first-child",
            "[data-cy='suggestion-0']"
        ]
        
        for i, locator in enumerate(suggestion_locators):
            try:
                by_type = 'css_selector' if locator.startswith('.') or locator.startswith('[') else 'xpath'
                self.logger.info(f"Trying suggestion locator {i+1}: {locator}")
                
                suggestion = WaitUtil.wait_for_clickable(self.driver, by_type, locator, 15)
                if suggestion:
                    suggestion.click()
                    self.logger.info("Selected first suggestion successfully.")
                    time.sleep(1)  # Wait for selection to process
                    return
                    
            except Exception as e:
                self.logger.warning(f"Suggestion locator {i+1} failed: {e}")
                continue
        
        # If no suggestion found, try pressing Enter on the input field
        try:
            search_input = WaitUtil.wait_for_element(self.driver, 'xpath', "//input[@id='autoSuggestWidget']", 5)
            if search_input:
                from selenium.webdriver.common.keys import Keys
                search_input.send_keys(Keys.ENTER)
                self.logger.info("Pressed Enter on search field as fallback.")
                return
        except:
            pass
            
        raise Exception("First suggestion not found with any strategy")

    def select_tomorrow_date(self):
        """
        Select tomorrow's date in the date picker with multiple strategies.
        Raises:
            Exception: If the date element is not found.
        """
        self.logger.info("Attempting to select tomorrow's date.")
        
        # Multiple locators for date selection
        date_locators = [
            "//td[contains(@class, 'DayPicker-Day') and not(contains(@class, 'disabled'))][2]",
            "//div[contains(@class, 'date-picker')]//td[not(contains(@class, 'disabled'))][2]",
            "//button[contains(@class, 'day') and not(contains(@class, 'disabled'))][2]",
            ".DayPicker-Day:not(.DayPicker-Day--disabled):nth-child(2)"
        ]
        
        for i, locator in enumerate(date_locators):
            try:
                by_type = 'css_selector' if locator.startswith('.') else 'xpath'
                self.logger.info(f"Trying date locator {i+1}: {locator}")
                
                tomorrow_date = WaitUtil.wait_for_clickable(self.driver, by_type, locator, 15)
                if tomorrow_date:
                    tomorrow_date.click()
                    self.logger.info("Selected tomorrow's date successfully.")
                    return
                    
            except Exception as e:
                self.logger.warning(f"Date locator {i+1} failed: {e}")
                continue
        
        self.logger.warning("Date picker might not be required or already set.")

    def tap_search_button(self):
        """
        Tap the SEARCH button that was identified in debug output.
        Raises:
            Exception: If the search button is not found.
        """
        self.logger.info("Attempting to tap search button.")
        
        # Based on debug output, look for the actual SEARCH button
        button_locators = [
            "//button[text()='SEARCH']",
            "//button[contains(@class, 'button') and contains(text(), 'SEARCH')]",
            "//button[contains(@class, 'rip') and text()='SEARCH']",
            "//button[contains(@class, 'lato') and contains(text(), 'SEARCH')]",
            "//input[@type='submit']",
            "//button[contains(text(), 'Search')]",  # Case insensitive
            "//a[contains(text(), 'SEARCH')]"
        ]
        
        for i, locator in enumerate(button_locators):
            try:
                self.logger.info(f"Trying search button locator {i+1}: {locator}")
                
                search_button = WaitUtil.wait_for_clickable(self.driver, 'xpath', locator, 15)
                if search_button:
                    # Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_button)
                    time.sleep(1)
                    search_button.click()
                    self.logger.info(f"Tapped search button successfully with locator {i+1}.")
                    return
                    
            except Exception as e:
                self.logger.warning(f"Search button locator {i+1} failed: {e}")
                continue
        
        raise Exception("Search button not found with any strategy")
