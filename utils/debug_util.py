"""
Debug utility for inspecting web elements and page structure in Appium tests.
Helps identify correct locators when elements are not found.
"""
import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class DebugUtil:
    """Utility class for debugging web elements and page structure."""
    
    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger('DebugUtil')
    
    def print_page_source(self, filename=None):
        """Print or save the current page source for inspection."""
        try:
            page_source = self.driver.page_source
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(page_source)
                self.logger.info(f"Page source saved to: {filename}")
            else:
                print("=== PAGE SOURCE ===")
                print(page_source[:2000])  # Print first 2000 characters
                print("=== END PAGE SOURCE ===")
        except Exception as e:
            self.logger.error(f"Error getting page source: {e}")
    
    def find_elements_by_text(self, text, partial=True):
        """Find all elements containing specific text."""
        try:
            if partial:
                xpath = f"//*[contains(text(), '{text}')]"
            else:
                xpath = f"//*[text()='{text}']"
            
            elements = self.driver.find_elements(By.XPATH, xpath)
            self.logger.info(f"Found {len(elements)} elements containing text '{text}':")
            
            for i, element in enumerate(elements):
                try:
                    tag_name = element.tag_name
                    class_name = element.get_attribute('class') or 'No class'
                    id_attr = element.get_attribute('id') or 'No id'
                    self.logger.info(f"  {i+1}. Tag: {tag_name}, Class: {class_name}, ID: {id_attr}")
                except:
                    self.logger.info(f"  {i+1}. Could not get element attributes")
            
            return elements
        except Exception as e:
            self.logger.error(f"Error finding elements by text: {e}")
            return []
    
    def inspect_element_attributes(self, by_type, locator):
        """Inspect all attributes of an element."""
        try:
            by_mapping = {
                'id': By.ID,
                'xpath': By.XPATH,
                'css_selector': By.CSS_SELECTOR,
                'class_name': By.CLASS_NAME,
                'tag_name': By.TAG_NAME,
                'name': By.NAME
            }
            
            selenium_by = by_mapping.get(by_type.lower(), By.XPATH)
            element = self.driver.find_element(selenium_by, locator)
            
            self.logger.info(f"Element found with {by_type}='{locator}':")
            self.logger.info(f"  Tag: {element.tag_name}")
            self.logger.info(f"  Text: {element.text}")
            self.logger.info(f"  Visible: {element.is_displayed()}")
            self.logger.info(f"  Enabled: {element.is_enabled()}")
            
            # Common attributes
            attributes = ['id', 'class', 'name', 'type', 'value', 'placeholder', 'data-cy', 'href']
            for attr in attributes:
                value = element.get_attribute(attr)
                if value:
                    self.logger.info(f"  {attr}: {value}")
            
            return element
        except NoSuchElementException:
            self.logger.warning(f"Element not found: {by_type}='{locator}'")
            return None
        except Exception as e:
            self.logger.error(f"Error inspecting element: {e}")
            return None
    
    def get_all_clickable_elements(self):
        """Find all potentially clickable elements on the page."""
        try:
            clickable_tags = ['button', 'a', 'input[type="submit"]', 'input[type="button"]']
            all_clickable = []
            
            for tag in clickable_tags:
                if tag.startswith('input'):
                    elements = self.driver.find_elements(By.CSS_SELECTOR, tag)
                else:
                    elements = self.driver.find_elements(By.TAG_NAME, tag)
                
                for element in elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            text = element.text or element.get_attribute('value') or 'No text'
                            class_name = element.get_attribute('class') or 'No class'
                            id_attr = element.get_attribute('id') or 'No id'
                            all_clickable.append({
                                'tag': element.tag_name,
                                'text': text[:50],  # Limit text length
                                'class': class_name[:50],
                                'id': id_attr,
                                'element': element
                            })
                    except:
                        continue
            
            self.logger.info(f"Found {len(all_clickable)} clickable elements:")
            for i, elem_info in enumerate(all_clickable[:10]):  # Show first 10
                self.logger.info(f"  {i+1}. {elem_info['tag']} - Text: '{elem_info['text']}' - Class: '{elem_info['class']}' - ID: '{elem_info['id']}'")
            
            return all_clickable
        except Exception as e:
            self.logger.error(f"Error finding clickable elements: {e}")
            return []
    
    def wait_and_debug(self, expected_element_desc="target element", wait_time=10):
        """Wait and continuously debug what's on the page."""
        self.logger.info(f"Waiting {wait_time} seconds for '{expected_element_desc}' to appear...")
        
        for i in range(wait_time):
            self.logger.info(f"Debug check {i+1}/{wait_time}")
            
            # Get page title and URL
            try:
                title = self.driver.title
                url = self.driver.current_url
                self.logger.info(f"  Page: {title} - URL: {url}")
            except:
                pass
            
            # Check if page has loaded
            try:
                ready_state = self.driver.execute_script("return document.readyState")
                self.logger.info(f"  Page ready state: {ready_state}")
            except:
                pass
            
            time.sleep(1)
    
    def take_debug_screenshot(self, filename=None):
        """Take a screenshot for debugging."""
        try:
            if not filename:
                filename = f"debug_screenshot_{int(time.time())}.png"
            
            screenshot_path = f"screenshots/{filename}"
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Debug screenshot saved: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"Error taking screenshot: {e}")
            return None
    
    def get_current_context_info(self):
        """Get information about current Appium context."""
        try:
            contexts = self.driver.contexts
            current_context = self.driver.current_context
            self.logger.info(f"Available contexts: {contexts}")
            self.logger.info(f"Current context: {current_context}")
            return contexts, current_context
        except Exception as e:
            self.logger.error(f"Error getting context info: {e}")
            return None, None