from pages.home_page import HomePage
from pages.search_result import SearchPage
from utils.config_reader import ConfigReader
import logging
import time

logger = logging.getLogger("TestSearchResult")

class TestSearchResult:
    def test_search_hotel_in_bangalore(self, driver):
        """Test searching for hotels in Bangalore with enhanced error handling."""
        logger.info("Starting hotel search test for Bangalore")
        
        try:
            # Initialize page objects
            home_page = HomePage(driver)
            search_page = SearchPage(driver)
            config = ConfigReader()
            
            # Navigate to the website
            base_url = config.get('url', 'base_url', default='https://www.makemytrip.com/')
            logger.info(f"Navigating to: {base_url}")
            driver.get(base_url)
            
            # Wait for page to load
            time.sleep(5)
            home_page.wait_for_page_load()
            
            # Close any initial popups
            home_page.close_login_popup()
            time.sleep(2)
            
            # Navigate to Hotels section
            home_page.tap_hotels_tab()
            time.sleep(2)
            
            # Interact with search field
            home_page.click_search_field()
            time.sleep(2)
            
            # Enter search text
            home_page.enter_search_text("Bangalore")
            time.sleep(3)
            
            # Select suggestion
            home_page.select_first_suggestion()
            time.sleep(2)
            
            # Select date (if date picker appears)
            try:
                home_page.select_tomorrow_date()
                time.sleep(2)
            except Exception as e:
                logger.info(f"Date selection skipped or not required: {e}")
            
            # Perform search
            home_page.tap_search_button()
            time.sleep(5)  # Wait for search results to load
            
            # Handle any popups on results page
            search_page.close_popup()
            time.sleep(2)
            
            # Verify search results
            results = search_page.get_search_results("Bangalore")
            assert results, "No search results found for Bangalore."
            
            logger.info("Search results for Bangalore validated successfully.")
            
        except Exception as e:
            logger.error(f"Test failed with exception: {e}")
            # Take screenshot for debugging
            try:
                screenshot_path = f"screenshots/failed_tests/test_failure_{int(time.time())}.png"
                driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved: {screenshot_path}")
            except:
                pass
            raise
