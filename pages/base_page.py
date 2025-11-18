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
from typing import Optional
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

    def find_element(self, by: str, locator: str, timeout: Optional[int] = None) -> Optional[WebElement]:
        """
        Locate an element using the given strategy and locator.
        Args:
            by (str): Locator strategy (e.g., 'id', 'xpath', 'accessibility id').
            locator (str): The locator value.
            timeout (int, optional): Timeout for finding the element.
        Returns:
            WebElement if found, else None.
        """
        end_time = time.time() + (timeout or self.timeout)
        while time.time() < end_time:
            try:
                element = self.driver.find_element(getattr(AppiumBy, by.upper()), locator)
                if element.is_displayed():
                    return element
            except Exception as e:
                self.logger.warning(f"Element not found using {by}='{locator}': {e}")
            time.sleep(0.5)
        self.logger.error(f"Timeout: Element not found using {by}='{locator}' after {timeout or self.timeout} seconds.")
        return None

    def tap_element(self, by: str, locator: str, timeout: Optional[int] = None) -> None:
        """
        Tap on an element after locating it.
        Args:
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int, optional): Timeout for finding the element.
        Raises:
            Exception: If the element is not found.
        """
        element = self.find_element(by, locator, timeout)
        if element:
            element.click()
            self.logger.info(f"Tapped element using {by}='{locator}'.")
        else:
            self.logger.error(f"Element to tap not found using {by}='{locator}'.")
            raise Exception(f"Element to tap not found using {by}='{locator}'.")

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

    def get_driver(self) -> WebDriver:
        """
        Return the Appium driver instance.
        Returns:
            WebDriver: The Appium driver.
        """
        return self.driver
