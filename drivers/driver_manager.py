"""
DriverManager class for managing the lifecycle of Appium driver instances.
Minimal, scalable, and ready for future extension.
"""
from appium import webdriver
from typing import Optional, Dict, Any
import yaml
import os

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
        self._driver: Optional[webdriver.Remote] = None

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

    def create_driver(self, capabilities: Dict[str, Any]) -> webdriver.Remote:
        """
        Instantiate a new Appium driver with the given capabilities dictionary.
        Quits any existing driver before creating a new one.
        Args:
            capabilities (dict): Desired capabilities for the driver.
        Returns:
            webdriver.Remote: The Appium driver instance.
        """
        self.quit_driver()
        self._driver = webdriver.Remote(
            command_executor=self._server_url,
            capabilities=capabilities
        )
        return self._driver

    def get_driver(self) -> Optional[webdriver.Remote]:
        """
        Return the current Appium driver instance, if any.
        Returns:
            webdriver.Remote or None: The Appium driver instance or None if not created.
        """
        return self._driver

    def quit_driver(self) -> None:
        """
        Quit and clean up the current driver instance, if any.
        """
        if self._driver:
            self._driver.quit()
            self._driver = None
