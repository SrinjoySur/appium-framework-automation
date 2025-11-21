"""
Quick debug test to see what happens after clicking "Near me" button
"""
from pages.home_page import HomePage
from utils.config_reader import ConfigReader
from utils.debug_util import DebugUtil
import logging
import time

logger = logging.getLogger("QuickDebug")

class TestQuickDebug:
    def test_debug_after_near_me_click(self, driver):
        """Debug what happens after clicking Near me button."""
        logger.info("=== Quick Debug After Near Me Click ===")
        
        try:
            config = ConfigReader()
            debug_util = DebugUtil(driver)
            home_page = HomePage(driver)
            
            # Navigate to MakeMyTrip
            base_url = config.get('url', 'base_url', default='https://www.makemytrip.com/')
            driver.get(base_url)
            time.sleep(5)
            
            # Close popup and click Hotels
            home_page.close_login_popup()
            time.sleep(2)
            home_page.tap_hotels_tab()
            time.sleep(3)
            
            # Take screenshot before clicking Near me
            debug_util.take_debug_screenshot("before_near_me.png")
            
            # Click Near me button
            near_me_btn = driver.find_element('xpath', "//button[text()='Near me']")
            near_me_btn.click()
            logger.info("Clicked Near Me button")
            time.sleep(5)  # Wait for any changes
            
            # Take screenshot after clicking
            debug_util.take_debug_screenshot("after_near_me.png")
            
            # Debug current page structure
            logger.info("=== Examining page after Near Me click ===")
            
            # Look for any input fields
            try:
                inputs = driver.find_elements('xpath', "//input")
                logger.info(f"Found {len(inputs)} input elements:")
                for i, inp in enumerate(inputs):
                    try:
                        placeholder = inp.get_attribute('placeholder') or 'No placeholder'
                        id_attr = inp.get_attribute('id') or 'No id'
                        name_attr = inp.get_attribute('name') or 'No name'
                        class_attr = inp.get_attribute('class') or 'No class'
                        visible = inp.is_displayed()
                        logger.info(f"  Input {i+1}: ID='{id_attr}', Name='{name_attr}', Placeholder='{placeholder}', Class='{class_attr}', Visible={visible}")
                    except:
                        logger.info(f"  Input {i+1}: Could not get attributes")
            except Exception as e:
                logger.info(f"Error finding inputs: {e}")
            
            # Look for any text or elements containing "city", "location", etc.
            search_terms = ["city", "location", "destination", "where"]
            for term in search_terms:
                try:
                    elements = driver.find_elements('xpath', f"//*[contains(text(), '{term}')]")
                    if elements:
                        logger.info(f"Found {len(elements)} elements containing '{term}':")
                        for i, elem in enumerate(elements[:3]):  # Show first 3
                            try:
                                tag = elem.tag_name
                                text = elem.text[:50] if elem.text else 'No text'
                                logger.info(f"  {term} element {i+1}: {tag} - '{text}'")
                            except:
                                pass
                except:
                    pass
            
            # Check current URL and title
            logger.info(f"Current URL: {driver.current_url}")
            logger.info(f"Current Title: {driver.title}")
            
            # Look for clickable elements
            clickable = debug_util.get_all_clickable_elements()
            
            # Check if URL changed (might have navigated somewhere)
            if "hotels" in driver.current_url and "makemytrip.com" in driver.current_url:
                logger.info("✅ Successfully on hotels page - may not need text input")
                logger.info("This might be a 'nearby hotels' search that doesn't require city input")
                return True
            
        except Exception as e:
            logger.error(f"Debug failed: {e}")
            try:
                DebugUtil(driver).take_debug_screenshot("debug_error.png")
            except:
                pass
            raise