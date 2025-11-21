"""
Debug test to identify actual page elements and help fix locator issues.
Run this test to understand what elements are actually available on the page.
"""
from pages.home_page import HomePage
from pages.search_result import SearchPage
from utils.config_reader import ConfigReader
from utils.debug_util import DebugUtil
import logging
import time
import pytest

logger = logging.getLogger("DebugTest")

class TestDebugElements:
    def test_debug_makemytrip_elements(self, driver):
        """Debug test to identify actual elements on MakeMyTrip homepage."""
        logger.info("=== STARTING DEBUG TEST ===")
        
        try:
            # Initialize utilities
            config = ConfigReader()
            debug_util = DebugUtil(driver)
            
            # Navigate to the website
            base_url = config.get('url', 'base_url', default='https://www.makemytrip.com/')
            logger.info(f"Navigating to: {base_url}")
            driver.get(base_url)
            
            # Wait for page to load
            time.sleep(10)
            
            # Debug context information
            debug_util.get_current_context_info()
            
            # Take initial screenshot
            debug_util.take_debug_screenshot("initial_page.png")
            
            # Debug page loading
            debug_util.wait_and_debug("page to fully load", 5)
            
            # Save page source for inspection
            debug_util.print_page_source("page_source_debug.html")
            
            # Look for Hotels-related elements
            logger.info("\n=== LOOKING FOR HOTELS ELEMENTS ===")
            hotels_elements = debug_util.find_elements_by_text("Hotel", partial=True)
            
            # Look for any clickable elements
            logger.info("\n=== ALL CLICKABLE ELEMENTS ===")
            clickable_elements = debug_util.get_all_clickable_elements()
            
            # Try to find navigation menu items
            logger.info("\n=== LOOKING FOR NAVIGATION MENU ===")
            nav_selectors = [
                "//nav",
                "//ul[contains(@class, 'nav')]",
                "//div[contains(@class, 'menu')]",
                "//a[contains(@data-cy, 'menu')]",
                "[data-cy*='menu']"
            ]
            
            for selector in nav_selectors:
                by_type = 'css_selector' if selector.startswith('[') else 'xpath'
                debug_util.inspect_element_attributes(by_type, selector)
            
            # Look for search-related elements
            logger.info("\n=== LOOKING FOR SEARCH ELEMENTS ===")
            search_elements = debug_util.find_elements_by_text("Search", partial=True)
            
            # Check common input fields
            logger.info("\n=== LOOKING FOR INPUT FIELDS ===")
            input_selectors = [
                "//input",
                "//input[@type='text']",
                "//input[contains(@placeholder, 'city')]",
                "//input[contains(@placeholder, 'where')]"
            ]
            
            for selector in input_selectors:
                debug_util.inspect_element_attributes('xpath', selector)
            
            # Look for any popups or modals
            logger.info("\n=== LOOKING FOR POPUPS/MODALS ===")
            popup_elements = debug_util.find_elements_by_text("Continue", partial=True)
            modal_selectors = [
                "//div[contains(@class, 'modal')]",
                "//div[contains(@class, 'popup')]",
                "//div[contains(@class, 'overlay')]"
            ]
            
            for selector in modal_selectors:
                debug_util.inspect_element_attributes('xpath', selector)
            
            # Take final screenshot
            debug_util.take_debug_screenshot("final_debug.png")
            
            logger.info("=== DEBUG TEST COMPLETED ===")
            
        except Exception as e:
            logger.error(f"Debug test failed: {e}")
            try:
                if 'debug_util' in locals():
                    DebugUtil(driver).take_debug_screenshot("error_debug.png")
            except:
                pass
            raise
    
    def test_step_by_step_interaction(self, driver):
        """Step-by-step interaction test with debugging at each step."""
        logger.info("=== STARTING STEP-BY-STEP DEBUG TEST ===")
        
        try:
            config = ConfigReader()
            debug_util = DebugUtil(driver)
            home_page = HomePage(driver)
            
            # Step 1: Navigate
            base_url = config.get('url', 'base_url', default='https://www.makemytrip.com/')
            logger.info(f"Step 1: Navigating to {base_url}")
            driver.get(base_url)
            time.sleep(5)
            debug_util.take_debug_screenshot("step1_navigation.png")
            
            # Step 2: Wait for page load
            logger.info("Step 2: Waiting for page to load")
            home_page.wait_for_page_load()
            debug_util.wait_and_debug("page elements to stabilize", 3)
            debug_util.take_debug_screenshot("step2_page_loaded.png")
            
            # Step 3: Look for and close popups
            logger.info("Step 3: Looking for popups to close")
            try:
                home_page.close_login_popup()
                debug_util.take_debug_screenshot("step3_popup_closed.png")
            except Exception as e:
                logger.info(f"No popup found or error closing: {e}")
            
            # Step 4: Look for Hotels tab
            logger.info("Step 4: Looking for Hotels tab")
            hotels_found = debug_util.find_elements_by_text("Hotel", partial=True)
            debug_util.take_debug_screenshot("step4_looking_for_hotels.png")
            
            if hotels_found:
                logger.info("Found Hotels-related elements, attempting to click")
                try:
                    home_page.tap_hotels_tab()
                    debug_util.take_debug_screenshot("step4_hotels_clicked.png")
                except Exception as e:
                    logger.error(f"Failed to click Hotels tab: {e}")
            
            # Step 5: Look for search field
            logger.info("Step 5: Looking for search field")
            search_found = debug_util.find_elements_by_text("Search", partial=True)
            debug_util.get_all_clickable_elements()
            debug_util.take_debug_screenshot("step5_search_elements.png")
            
            logger.info("=== STEP-BY-STEP DEBUG COMPLETED ===")
            
        except Exception as e:
            logger.error(f"Step-by-step debug failed: {e}")
            try:
                DebugUtil(driver).take_debug_screenshot("step_error.png")
            except:
                pass
            raise

if __name__ == "__main__":
    # Can be run independently for debugging
    pass