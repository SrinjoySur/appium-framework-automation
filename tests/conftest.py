import os
import logging
import pytest
import allure
from drivers.driver_manager import DriverManager
from utils.config_reader import ConfigReader


def pytest_configure(config):
    project_root = os.path.dirname(os.path.dirname(__file__))
    log_dir = os.path.join(project_root, 'logs', 'app_logs')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'test_run.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get('driver', None)
        if driver:
            from utils.config_reader import ConfigReader
            config = ConfigReader()
            base_directory = config.get('screenshot', 'directory', default='screenshots') or 'screenshots'
            failed_directory = os.path.join(base_directory, 'failed_tests')
            filename_format = config.get('screenshot', 'filename_format', default='screenshot_{timestamp}.png') or 'screenshot_{timestamp}.png'
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = filename_format.format(timestamp=timestamp)
            screenshot_path_failed = os.path.join(failed_directory, filename)
            os.makedirs(failed_directory, exist_ok=True)
            driver.save_screenshot(screenshot_path_failed)
            if os.path.exists(screenshot_path_failed):
                with open(screenshot_path_failed, 'rb') as image_file:
                    allure.attach(image_file.read(), name=filename, attachment_type=allure.attachment_type.PNG)
                logging.getLogger('pytest').info(f"Screenshot attached to Allure: {screenshot_path_failed}")
            else:
                logging.getLogger('pytest').error(f"Failed to take screenshot on test failure. Expected at: {screenshot_path_failed}")


@pytest.fixture(scope='function')
def driver(request):
    config = ConfigReader()
    server_url = config.get('appium', 'server_url')
    if not server_url:
        raise ValueError("Appium server URL is not configured")
    capabilities_file = getattr(request, 'param', None) or config.get('appium', 'default_capabilities_file')
    if not capabilities_file:
        raise ValueError("Capabilities file is not configured")
    manager = DriverManager(server_url)
    capabilities = manager.load_capabilities_from_yaml(capabilities_file)
    drv = manager.create_driver(capabilities)
    yield drv
    manager.quit_driver()
