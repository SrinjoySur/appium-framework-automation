import os
import yaml

class ConfigReader:
    """
    Utility class for reading YAML configuration files for the framework.
    """
    def __init__(self, config_path=None):
        """
        Initialize ConfigReader with the path to the config YAML file.
        Args:
            config_path (str, optional): Path to the config YAML file. Defaults to 'configs/config.yaml'.
        """
        if config_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, 'configs', 'config.yaml')
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self):
        """
        Load the YAML configuration file.
        Returns:
            dict: The loaded configuration data.
        """
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, *keys, default=None):
        """
        Retrieve a value from the configuration using a sequence of keys.
        Args:
            *keys: Sequence of keys to traverse the config dict.
            default: Value to return if the key path is not found.
        Returns:
            The value from the config, or default if not found.
        """
        data = self.config
        for key in keys:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return default
        return data
