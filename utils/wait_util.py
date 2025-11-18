import time
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from typing import Optional

class WaitUtil:
    """
    Utility class for waiting for elements in Appium-based automation.
    """
    @staticmethod
    def wait_for_element(driver: WebDriver, by: str, locator: str, timeout: int = 20, poll_frequency: float = 0.5) -> Optional[WebElement]:
        """
        Wait for an element to be present and visible within the given timeout.

        Args:
            driver (WebDriver): The Appium driver instance.
            by (str): Locator strategy (e.g., 'id', 'xpath', 'accessibility_id').
            locator (str): The locator value.
            timeout (int): Maximum time to wait for the element.
            poll_frequency (float): How often to poll for the element.

        Returns:
            WebElement if found, else None.
        """
        end_time = time.time() + timeout
        by_strategy = getattr(AppiumBy, by.upper())
        while time.time() < end_time:
            try:
                element = driver.find_element(by_strategy, locator)
                if element.is_displayed():
                    return element
            except Exception:
                pass
            time.sleep(poll_frequency)
        return None

    @staticmethod
    def wait_for_element_to_disappear(driver: WebDriver, by: str, locator: str, timeout: int = 20, poll_frequency: float = 0.5) -> bool:
        """
        Wait for an element to disappear from the screen within the given timeout.

        Args:
            driver (WebDriver): The Appium driver instance.
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int): Maximum time to wait for the element to disappear.
            poll_frequency (float): How often to poll for the element.

        Returns:
            True if the element disappears, False otherwise.
        """
        end_time = time.time() + timeout
        by_strategy = getattr(AppiumBy, by.upper())
        while time.time() < end_time:
            try:
                element = driver.find_element(by_strategy, locator)
                if not element.is_displayed():
                    return True
            except Exception:
                return True  # Element not found
            time.sleep(poll_frequency)
        return False
