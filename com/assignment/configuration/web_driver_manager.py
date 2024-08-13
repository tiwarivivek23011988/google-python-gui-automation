import os
import threading
from selenium import webdriver
from com.assignment.configuration.web_driver_options_manager import WebDriverOptionsManager
from com.assignment.utilities.file_operations_utility import FileOperationsUtility
from com.assignment.utilities.json_parser_utility import JsonParserUtility


class CustomWebDriverManager:
    _thread_local = threading.local()

    @staticmethod
    def get_driver(browser_name):
        if not hasattr(CustomWebDriverManager._thread_local, 'driver'):
            driver = CustomWebDriverManager._create_driver(browser_name)
            CustomWebDriverManager._thread_local.driver = driver
        return CustomWebDriverManager._thread_local.driver

    @staticmethod
    def quit_driver():
        if hasattr(CustomWebDriverManager._thread_local, 'driver'):
            CustomWebDriverManager._thread_local.driver.quit()
            del CustomWebDriverManager._thread_local.driver

    @staticmethod
    def _create_driver(browser_name):
        service, options = WebDriverOptionsManager.get_driver_options(browser_name)
        file_path = FileOperationsUtility.find_file_in_directory(FileOperationsUtility.get_project_root(), "data.json")
        json_data = JsonParserUtility.parse_json(file_path)
        execution_type = json_data['run_type']
        if execution_type == 'local':
            if browser_name == 'chrome':
                return webdriver.Chrome(service, options)
            elif browser_name == 'firefox':
                return webdriver.Firefox(service, options)
            elif browser_name == 'edge':
                return webdriver.Edge(service, options)
        else:
            selenium_grid_url = os.getenv('SELENIUM_GRID_URL', json_data['grid_url'])
            return webdriver.Remote(command_executor=selenium_grid_url, options=options)
