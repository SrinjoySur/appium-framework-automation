import time
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import Optional
import logging

class WaitUtil:
    """
    Utility class for waiting for elements in Appium-based automation.
    """
    @staticmethod
    def wait_for_element(driver: WebDriver, by: str, locator: str, timeout: int = 20, poll_frequency: float = 0.5) -> Optional[WebElement]:
        """
        Enhanced wait for element with multiple strategies for web automation.

        Args:
            driver (WebDriver): The Appium driver instance.
            by (str): Locator strategy (e.g., 'id', 'xpath', 'css_selector').
            locator (str): The locator value.
            timeout (int): Maximum time to wait for the element.
            poll_frequency (float): How often to poll for the element.

        Returns:
            WebElement if found, else None.
        """
        logger = logging.getLogger('WaitUtil')
        
        # Convert to Selenium By for web context
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
        
        selenium_by = by_mapping.get(by.lower(), By.XPATH)
        
        # Strategy 1: Wait for visibility
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.visibility_of_element_located((selenium_by, locator)))
            logger.info(f"Element found using visibility wait: {by}='{locator}'")
            return element
        except TimeoutException:
            logger.warning(f"Visibility wait timeout for {by}='{locator}'")
        
        # Strategy 2: Wait for presence (element in DOM but might not be visible)
        try:
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((selenium_by, locator)))
            if element.is_displayed():
                logger.info(f"Element found using presence wait: {by}='{locator}'")
                return element
        except TimeoutException:
            logger.warning(f"Presence wait timeout for {by}='{locator}'")
        
        # Strategy 3: Manual polling with page interactions
        end_time = time.time() + min(timeout, 15)
        attempts = 0
        while time.time() < end_time:
            try:
                # Try to find element
                if by.lower() == 'xpath':
                    element = driver.find_element(By.XPATH, locator)
                elif by.lower() == 'id':
                    element = driver.find_element(By.ID, locator)
                else:
                    element = driver.find_element(selenium_by, locator)
                
                if element and element.is_displayed():
                    logger.info(f"Element found using manual polling: {by}='{locator}'")
                    return element
                
            except Exception as e:
                attempts += 1
                
                # Try some recovery actions every few attempts
                if attempts % 3 == 0:
                    try:
                        # Scroll page or wait a bit longer
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                        time.sleep(1)
                    except:
                        pass
            
            time.sleep(poll_frequency)
        
        logger.error(f"Element not found after all strategies: {by}='{locator}'")
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
        by_mapping = {
            'id': By.ID,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'name': By.NAME
        }
        
        selenium_by = by_mapping.get(by.lower(), By.XPATH)
        
        try:
            WebDriverWait(driver, timeout).until_not(
                EC.visibility_of_element_located((selenium_by, locator))
            )
            return True
        except TimeoutException:
            return False
    
    @staticmethod
    def wait_for_clickable(driver: WebDriver, by: str, locator: str, timeout: int = 20) -> Optional[WebElement]:
        """
        Wait for an element to be clickable.
        
        Args:
            driver (WebDriver): The Appium driver instance.
            by (str): Locator strategy.
            locator (str): The locator value.
            timeout (int): Maximum time to wait.
            
        Returns:
            WebElement if clickable, else None.
        """
        by_mapping = {
            'id': By.ID,
            'xpath': By.XPATH,
            'css_selector': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'name': By.NAME
        }
        
        selenium_by = by_mapping.get(by.lower(), By.XPATH)
        
        try:
            wait = WebDriverWait(driver, timeout)
            element = wait.until(EC.element_to_be_clickable((selenium_by, locator)))
            return element
        except TimeoutException:
            return None
    
    @staticmethod 
    def wait_for_page_ready(driver: WebDriver, timeout: int = 30) -> bool:
        """
        Wait for page to be in ready state.
        
        Args:
            driver (WebDriver): The Appium driver instance.
            timeout (int): Maximum time to wait.
            
        Returns:
            True if page is ready, False otherwise.
        """
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
