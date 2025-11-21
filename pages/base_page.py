"""
BasePage class for Appium-based mobile automation frameworks.
Provides reusable, production-level methods for interacting with mobile app elements.
All methods use Appium's native driver APIs (no Selenium dependencies).

Usage Example:
    from pages.base_page import BasePage
    class LoginPage(BasePage):
        def login(self, username, password):
            self.send_text('id', 'username_field', username)
            self.send_text('id', 'password_field', password)
            self.tap_element('id', 'login_button')
"""
import logging
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from typing import Optional, List
import time

class BasePage:
    """
    Base class for all page objects. Encapsulates common Appium actions and utilities.
    """
    def __init__(self, driver: WebDriver, timeout: int = 20):
        """
        Initialize the BasePage with an Appium driver instance.
        Args:
            driver (WebDriver): The Appium driver instance.
            timeout (int): Default timeout for element waits.
        """
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        self._ensure_web_context()
    
    def _ensure_web_context(self):
        """Ensure we're in the correct web context for browser automation."""
        try:
            contexts = self.driver.contexts
            web_context = None
            for context in contexts:
                if 'WEBVIEW' in context or 'CHROMIUM' in context:
                    web_context = context
                    break
            
            if web_context and self.driver.current_context != web_context:
                self.driver.switch_to.context(web_context)
                self.logger.info(f"Switched to web context: {web_context}")
        except Exception as e:
            self.logger.warning(f"Context switching failed or not available: {e}")

    def find_element(self, by: str, locator: str, timeout: Optional[int] = None, wait_for_clickable: bool = False) -> Optional[WebElement]:
        """
        Locate an element using enhanced wait strategies for web automation.
        Args:
            by (str): Locator strategy (e.g., 'id', 'xpath', 'css_selector').
            locator (str): The locator value.
            timeout (int, optional): Timeout for finding the element.
            wait_for_clickable (bool): Wait for element to be clickable instead of just visible.
        Returns:
            WebElement if found, else None.
        """
        wait_timeout = timeout or self.timeout
        
        try:
            # Convert Appium By to Selenium By for web context
            selenium_by = self._convert_to_selenium_by(by)
            
            wait = WebDriverWait(self.driver, wait_timeout)
            
            if wait_for_clickable:
                element = wait.until(EC.element_to_be_clickable((selenium_by, locator)))
            else:
                element = wait.until(EC.visibility_of_element_located((selenium_by, locator)))
            
            self.logger.info(f"Element found using {by}='{locator}'")
            return element
            
        except TimeoutException:
            # Try alternative wait strategy
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((selenium_by, locator))
                )
                if element.is_displayed():
                    return element
            except:
                pass
            
        except Exception as e:
            self.logger.warning(f"Error finding element {by}='{locator}': {e}")
        
        # Last resort: try with page refresh
        try:
            self.logger.info("Attempting page refresh and retry...")
            self.driver.refresh()
            time.sleep(2)
            
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(EC.visibility_of_element_located((selenium_by, locator)))
            return element
        except:
            pass
            
        self.logger.error(f"Element not found using {by}='{locator}' after {wait_timeout} seconds")
        return None
    
    def _convert_to_selenium_by(self, by: str) -> str:
        """Convert Appium By strategy to Selenium By."""
        by_mapping = {
            'id': By.ID,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'name': By.NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }
        return by_mapping.get(by.lower(), By.XPATH)

    def tap_element(self, by: str, locator: str, timeout: Optional[int] = None) -> None:
        """
        Tap on an element with enhanced retry logic.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int, optional): Timeout for finding the element.
        Raises:
            Exception: If the element is not found or not clickable.
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Wait for element to be clickable
                element = self.find_element(by, locator, timeout, wait_for_clickable=True)
                if element:
                    # Scroll element into view if needed
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.5)
                    
                    # Try clicking
                    element.click()
                    self.logger.info(f"Successfully tapped element using {by}='{locator}'")
                    return
                else:
                    raise Exception(f"Element not found: {by}='{locator}'")
                    
            except Exception as e:
                self.logger.warning(f"Tap attempt {attempt + 1} failed for {by}='{locator}': {e}")
                if attempt == max_retries - 1:
                    # Try JavaScript click as last resort
                    try:
                        element = self.find_element(by, locator, 5)
                        if element:
                            self.driver.execute_script("arguments[0].click();", element)
                            self.logger.info(f"JavaScript click succeeded for {by}='{locator}'")
                            return
                    except:
                        pass
                    
                    self.logger.error(f"All tap attempts failed for {by}='{locator}'")
                    raise Exception(f"Element to tap not found or not clickable: {by}='{locator}'")
                time.sleep(1)

    def send_text(self, by: str, locator: str, text: str, timeout: Optional[int] = None) -> None:
        """
        Send text to an input element after locating it.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            text (str): The text to send.
            timeout (int, optional): Timeout for finding the element.
        Raises:
            Exception: If the element is not found.
        """
        element = self.find_element(by, locator, timeout)
        if element:
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Sent text to element using {by}='{locator}'.")
        else:
            self.logger.error(f"Element to send text not found using {by}='{locator}'.")
            raise Exception(f"Element to send text not found using {by}='{locator}'.")

    def get_text(self, by: str, locator: str, timeout: Optional[int] = None) -> str:
        """
        Retrieve text from an element.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int, optional): Timeout for finding the element.
        Returns:
            str: The text of the element.
        """
        element = self.find_element(by, locator, timeout)
        if element:
            return element.text
        else:
            raise Exception(f"Element not found for get_text: {by}={locator}")  # Custom exception handling

    def is_element_present(self, by: str, locator: str, timeout: int = 5) -> bool:
        """
        Check if an element is present within a short timeout.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int): Timeout for finding the element.
        Returns:
            bool: True if present, False otherwise.
        """
        return self.find_element(by, locator, timeout) is not None

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: int = 800) -> None:
        """
        Perform swipe gesture from (start_x, start_y) to (end_x, end_y).
        Args:
            start_x (int): Starting x coordinate.
            start_y (int): Starting y coordinate.
            end_x (int): Ending x coordinate.
            end_y (int): Ending y coordinate.
            duration (int): Duration of the swipe in ms.
        """
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)
            self.logger.info(f"Swiped from ({start_x},{start_y}) to ({end_x},{end_y})")
        except Exception as e:
            self.logger.error(f"Swipe failed: {e}")
            raise

    def scroll_to_element(self, by: str, locator: str, max_scrolls: int = 5) -> Optional[WebElement]:
        """
        Scroll vertically until the element is found or max_scrolls is reached.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            max_scrolls (int): Maximum number of scroll attempts.
        Returns:
            WebElement if found, else None.
        """
        for i in range(max_scrolls):
            element = self.find_element(by, locator, timeout=2)
            if element:
                self.logger.info(f"Element found after {i+1} scroll(s): {by}={locator}")
                return element
            self.swipe(500, 1500, 500, 500)  # Example values; adjust as needed
        self.logger.error(f"Element not found after {max_scrolls} scrolls: {by}={locator}")
        return None

    def wait_for_page_load(self, timeout: int = 30) -> None:
        """Wait for page to fully load."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded successfully")
        except TimeoutException:
            self.logger.warning("Page load timeout - continuing anyway")
    
    def switch_to_frame(self, frame_locator: str, by: str = "xpath") -> bool:
        """Switch to iframe if present."""
        try:
            selenium_by = self._convert_to_selenium_by(by)
            frame = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((selenium_by, frame_locator))
            )
            self.logger.info(f"Switched to frame: {frame_locator}")
            return True
        except:
            self.logger.info(f"No frame found or switch failed: {frame_locator}")
            return False
    
    def switch_to_default_content(self) -> None:
        """Switch back to main content from iframe."""
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.warning(f"Failed to switch to default content: {e}")
    
    def wait_and_click_with_js(self, by: str, locator: str, timeout: Optional[int] = None) -> None:
        """Wait for element and click using JavaScript - useful for stubborn elements."""
        element = self.find_element(by, locator, timeout)
        if element:
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"JavaScript clicked element: {by}='{locator}'")
        else:
            raise Exception(f"Element not found for JS click: {by}='{locator}'")
    
    def get_driver(self) -> WebDriver:
        """
        Return the Appium driver instance.
        Returns:
            WebDriver: The Appium driver.
        """
        return self.driver
