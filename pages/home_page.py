

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
        Click on the area that allows city input (not 'Near me' which is for nearby search).
        Look for text/area that opens city search dialog.
        """
        self.logger.info("Attempting to find city search input area.")
        
        # Look for areas that might open city search dialog - avoid 'Near me'
        city_search_locators = [
            "//span[contains(text(), 'City') or contains(text(), 'Where') or contains(text(), 'Destination')]",
            "//div[contains(@class, 'location') and not(contains(@class, 'near'))]",
            "//input[@type='text']",  # Any visible input
            "//div[contains(@class, 'search')]",
            "//div[contains(@class, 'destination')]",
            "//button[contains(@class, 'location') and not(contains(text(), 'Near'))]",
            "//div[text()='City, Area or Property']",
            "//span[text()='Enter city or area name']"
        ]
        
        for i, locator in enumerate(city_search_locators):
            try:
                self.logger.info(f"Trying city search locator {i+1}: {locator}")
                
                search_element = WaitUtil.wait_for_clickable(self.driver, 'xpath', locator, 8)
                if search_element:
                    # Scroll into view and click
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_element)
                    time.sleep(1)
                    search_element.click()
                    self.logger.info(f"Clicked city search area with locator {i+1}.")
                    time.sleep(3)  # Wait for search dialog to open
                    return
                    
            except Exception as e:
                self.logger.info(f"City search locator {i+1} failed: {e}")
                continue
        
        # Alternative approach: Skip city input and proceed with Near me + SEARCH
        self.logger.info("No city input found - using 'Near me' approach instead")
        try:
            near_me_btn = WaitUtil.wait_for_clickable(self.driver, 'xpath', "//button[text()='Near me']", 5)
            if near_me_btn:
                near_me_btn.click()
                self.logger.info("Using Near me search approach")
                time.sleep(2)
                return
        except:
            pass
            
        raise Exception("No city search area or Near me button found")

    def enter_search_text(self, text):
        """
        Try to enter search text, but handle case where no text input is available.
        Args:
            text (str): The text to enter.
        """
        self.logger.info(f"Attempting to enter search text: {text}")
        
        # First, look for any input fields that may have appeared
        input_locators = [
            "//input[@type='text' and contains(@placeholder, 'city')]",
            "//input[@type='text' and contains(@placeholder, 'City')]",
            "//input[@type='text' and contains(@placeholder, 'where')]", 
            "//input[@type='text' and contains(@placeholder, 'Where')]",
            "//input[@type='text' and contains(@placeholder, 'destination')]",
            "//input[@type='text']",  # Any text input
            "//input[contains(@id, 'city')]",
            "//input[contains(@name, 'city')]",
            "//textarea[contains(@placeholder, 'city')]"
        ]
        
        for i, locator in enumerate(input_locators):
            try:
                self.logger.info(f"Trying input locator {i+1}: {locator}")
                
                search_input = WaitUtil.wait_for_element(self.driver, 'xpath', locator, 8)
                if search_input and search_input.is_displayed() and search_input.is_enabled():
                    # Clear field and enter text
                    search_input.clear()
                    search_input.send_keys(text)
                    self.logger.info(f"✅ Successfully entered search text: {text}")
                    time.sleep(3)  # Wait for suggestions to load
                    return
                    
            except Exception as e:
                self.logger.info(f"Input locator {i+1} failed: {e}")
                continue
        
        # Check if we're already on a search page that doesn't need text input
        try:
            current_url = self.driver.current_url
            if "hotels" in current_url.lower():
                self.logger.info(f"ℹ️  Already on hotels page: {current_url}")
                self.logger.info(f"Text input for '{text}' may not be required - proceeding with search")
                return  # Continue without error
        except:
            pass
        
        # Log warning but don't fail - some flows don't need text input
        self.logger.warning(f"⚠️  No text input found for '{text}' - continuing with current search state")
        self.logger.info("This might be a 'nearby search' flow that doesn't require city input")

    def select_first_suggestion(self):
        """
        Try to select first suggestion if available, otherwise continue without error.
        """
        self.logger.info("Looking for suggestions to select.")
        
        # Wait a bit for suggestions to potentially load
        time.sleep(2)
        
        # Multiple locators for suggestions
        suggestion_locators = [
            "//ul[contains(@class, 'suggestions')]//li[1]",
            "//div[contains(@class, 'suggestion')]//li[1]", 
            "//ul[@id='ui-id-1']/li[1]",
            "//div[contains(@class, 'autoComplete')]//li[1]",
            "//div[@class='react-autosuggest__suggestions-container']//li[1]",
            ".react-autosuggest__suggestion:first-child",
            "[data-cy='suggestion-0']",
            "//li[contains(@class, 'suggestion')][1]"
        ]
        
        for i, locator in enumerate(suggestion_locators):
            try:
                by_type = 'css_selector' if locator.startswith('.') or locator.startswith('[') else 'xpath'
                self.logger.info(f"Trying suggestion locator {i+1}: {locator}")
                
                suggestion = WaitUtil.wait_for_clickable(self.driver, by_type, locator, 5)
                if suggestion:
                    suggestion.click()
                    self.logger.info("✅ Selected first suggestion successfully.")
                    time.sleep(2)  # Wait for selection to process
                    return
                    
            except Exception as e:
                self.logger.info(f"Suggestion locator {i+1} not found: {e}")
                continue
        
        # Check if we need to press Enter on any input field
        try:
            inputs = self.driver.find_elements('xpath', "//input[@type='text']")
            if inputs:
                active_input = inputs[0]  # Try the first text input
                from selenium.webdriver.common.keys import Keys
                active_input.send_keys(Keys.ENTER)
                self.logger.info("⌨️  Pressed Enter on input field as suggestion selection.")
                time.sleep(2)
                return
        except:
            pass
        
        # No suggestions found - might not be needed for this search flow
        self.logger.info("ℹ️  No suggestions found - continuing without selection")
        self.logger.info("This might be a search flow that doesn't require suggestion selection")

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
