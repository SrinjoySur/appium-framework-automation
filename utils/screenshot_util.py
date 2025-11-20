import logging
from appium.webdriver.webdriver import WebDriver
from utils.config_reader import ConfigReader
import os
from datetime import datetime

class ScreenshotUtil:
    """
    Utility class for taking screenshots, especially on test failure.
    """
    @staticmethod
    def take_screenshot_on_failure(driver: WebDriver) -> None:
        """
        Take a screenshot using the provided driver and save it to the failed_tests directory under screenshots.
        The filename and directory are read from the config file, but always use screenshots/failed_tests for failed tests.

        Args:
            driver (WebDriver): The Appium driver instance.
        """
        try:
            config = ConfigReader()
            base_directory = config.get('screenshot', 'directory', default='screenshots') or 'screenshots'
            failed_directory = os.path.join(base_directory, 'failed_tests')
            filename_format = config.get('screenshot', 'filename_format', default='screenshot_{timestamp}.png') or 'screenshot_{timestamp}.png'
            # Ensure failed_tests directory exists
            os.makedirs(failed_directory, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = filename_format.format(timestamp=timestamp)
            file_path = os.path.join(failed_directory, filename)
            driver.save_screenshot(file_path)
            logging.getLogger("ScreenshotUtil").info(f"Screenshot saved to {file_path}")
        except Exception as e:
            logging.getLogger("ScreenshotUtil").error(f"Failed to take screenshot: {e}")
