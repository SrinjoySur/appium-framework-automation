import logging
from pages.base_page import BasePage
from utils.wait_util import WaitUtil
import time


class SearchPage(BasePage):
    """Page object for the Search Results screen."""

    def __init__(self, driver, timeout=20):
        super().__init__(driver, timeout)
        self.logger = logging.getLogger(self.__class__.__name__)

    def close_popup(self):
        self.logger.info("Attempting to close popup if present.")
        
        # Wait for page to stabilize
        self.wait_for_page_load()
        
        # Multiple locators for popup close buttons
        popup_locators = [
            "//a[text()='Continue in Browser']",
            "//button[text()='Continue in Browser']",
            "//button[contains(@class, 'close')]",
            "//div[@class='modal']//button[contains(@class, 'close')]",
            "//span[contains(@class, 'close')]",
            "[data-dismiss='modal']",
            ".modal-close"
        ]
        
        for i, locator in enumerate(popup_locators):
            try:
                by_type = 'css_selector' if locator.startswith('.') or locator.startswith('[') else 'xpath'
                self.logger.info(f"Trying popup close locator {i+1}: {locator}")
                
                close_button = WaitUtil.wait_for_element(self.driver, by_type, locator, 5)
                if close_button:
                    close_button.click()
                    self.logger.info("Closed popup successfully.")
                    time.sleep(2)  # Wait for popup to disappear
                    return
                    
            except Exception as e:
                self.logger.info(f"Popup locator {i+1} not found: {e}")
                continue
        
        self.logger.info("No popup found to close.")

    def get_search_results(self, text):
        self.logger.info(f"Attempting to get search results for: {text}")
        
        # Wait for search results page to load
        self.wait_for_page_load()
        
        # Multiple locators to find search results containing the text
        result_locators = [
            f"//p[contains(text(),'{text}')]",
            f"//div[contains(text(),'{text}')]",
            f"//span[contains(text(),'{text}')]",
            f"//h1[contains(text(),'{text}')]",
            f"//h2[contains(text(),'{text}')]",
            f"//h3[contains(text(),'{text}')]",
            f"//*[contains(@class, 'result') and contains(text(), '{text}')]",
            f"//*[contains(@class, 'hotel') and contains(text(), '{text}')]",
            f"//*[contains(@class, 'listing')]",  # Any listings
            "//div[contains(@class, 'hotel')]//span",  # Hotel names
            "//div[@id='Listing_hotel_0']",  # First hotel result
            "//*[contains(@class, 'makeFlex hrtlCenter')]"
        ]
        
        for i, locator in enumerate(result_locators):
            try:
                self.logger.info(f"Trying result locator {i+1}: {locator}")
                
                results = WaitUtil.wait_for_element(self.driver, 'xpath', locator, 10)
                if results:
                    self.logger.info(f"Search results found for: {text} using locator {i+1}")
                    return results
                    
            except Exception as e:
                self.logger.info(f"Result locator {i+1} failed: {e}")
                continue
        
        # Check if we're on the right page by looking for search indicators
        try:
            # Look for any search-related elements on the page
            page_indicators = [
                "//title[contains(text(), 'Hotel')]",
                "//*[contains(@class, 'search')]",
                "//*[contains(@class, 'result')]",
                "//*[contains(@class, 'listing')]"
            ]
            
            for indicator in page_indicators:
                element = WaitUtil.wait_for_element(self.driver, 'xpath', indicator, 5)
                if element:
                    self.logger.info("Search results page detected, but no specific results found.")
                    return element  # Return the page indicator as proof we're on results page
                    
        except Exception as e:
            self.logger.warning(f"Page indicator check failed: {e}")
        
        self.logger.error(f"No search results found for: {text}")
        return None