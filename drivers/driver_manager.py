"""
DriverManager class for managing the lifecycle of Appium driver instances.
Minimal, scalable, and ready for future extension.
"""
import os
import yaml
from typing import Dict, Any, Optional
from appium.webdriver.webdriver import WebDriver
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from appium.options.common.base import AppiumOptions

class DriverManager:
    """
    Manages the lifecycle of Appium driver instances.
    Loads capabilities from YAML files and provides driver management utilities.
    """
    def __init__(self, server_url: str):
        """
        Initialize DriverManager with the Appium server URL.
        Args:
            server_url (str): The Appium server URL.
        """
        self._server_url = server_url
        self._driver: Optional[WebDriver] = None

    def load_capabilities_from_yaml(self, yaml_filename: str) -> Dict[str, Any]:
        """
        Load capabilities from a YAML file in config/capabilities.
        Args:
            yaml_filename (str): The YAML file name (e.g., 'chrome.yml').
        Returns:
            dict: Capabilities dictionary.
        Raises:
            FileNotFoundError, yaml.YAMLError
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_path = os.path.join(base_dir, 'configs', 'capabilities', yaml_filename)
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"Capabilities YAML file not found: {yaml_path}")
        with open(yaml_path, 'r') as f:
            capabilities = yaml.safe_load(f)
        if not isinstance(capabilities, dict):
            raise yaml.YAMLError(f"Invalid YAML structure in {yaml_path}")
        return capabilities

    def _create_options_from_capabilities(self, capabilities: Dict[str, Any]) -> AppiumOptions:
        """
        Convert capabilities dictionary to appropriate Options object.
        Args:
            capabilities (dict): Capabilities dictionary from YAML.
        Returns:
            BaseOptions: Platform-specific options object.
        """
        platform_name = capabilities.get('platformName', '').lower()
        
        if platform_name == 'android':
            options = UiAutomator2Options()
        elif platform_name == 'ios':
            options = XCUITestOptions()
        else:
            # For other platforms, use UiAutomator2Options as default
            # You can extend this for other platforms like Windows, etc.
            options = UiAutomator2Options()
        
        # Load all capabilities into the options object
        options.load_capabilities(capabilities)
        return options

    def create_driver(self, capabilities: Dict[str, Any]) -> WebDriver:
        """
        Instantiate a new Appium driver with the given capabilities dictionary.
        Quits any existing driver before creating a new one.
        Args:
            capabilities (dict): Desired capabilities for the driver.
        Returns:
            WebDriver: The Appium driver instance.
        """
        self.quit_driver()
        
        # Convert capabilities dict to Options object
        options = self._create_options_from_capabilities(capabilities)
        
        self._driver = webdriver.Remote(
            command_executor=self._server_url,
            options=options
        )
        return self._driver

    def get_driver(self) -> Optional[WebDriver]:
        """
        Return the current Appium driver instance, if any.
        Returns:
            WebDriver or None: The Appium driver instance or None if not created.
        """
        return self._driver

    def quit_driver(self) -> None:
        """
        Quit and clean up the current driver instance, if any.
        """
        if self._driver:
            self._driver.quit()
            self._driver = None
