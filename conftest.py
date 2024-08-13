import threading
import logging

import pytest
import allure
from com.assignment.utilities.file_operations_utility import FileOperationsUtility
from com.assignment.utilities.json_parser_utility import JsonParserUtility
from com.assignment.utilities.process_manager_utility import WebDriverProcessManager
from allure_commons.types import AttachmentType
from com.assignment.configuration.web_driver_manager import CustomWebDriverManager

logger = logging.getLogger(__name__)

# Define a lock to ensure thread safety
report_lock = threading.Lock()
delete_lock = threading.Lock()
cleanup_lock = threading.Lock()

file_path = FileOperationsUtility.find_file_in_directory(FileOperationsUtility.get_project_root(), "data.json")
json_data = JsonParserUtility.parse_json(file_path)
execution_type = json_data['run_type']


@pytest.fixture(scope="function")
def driver(request, browser):
    if browser in ["chrome", "firefox", "edge"]:
        driver = CustomWebDriverManager.get_driver(browser)
        WebDriverProcessManager.get_instance().add_process(driver)
    else:
        raise ValueError(f"Browser {browser} is not supported")

    yield driver
    CustomWebDriverManager.quit_driver()


@pytest.fixture(scope="function", autouse=True)
def teardown(request):
    """Teardown function to clean up WebDriver processes."""
    if execution_type == 'local':
        with cleanup_lock:
            def finalize():
                WebDriverProcessManager.get_instance().cleanup()

            request.addfinalizer(finalize)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    with report_lock:
        if call.when == 'call':
            outcome = 'passed' if call.excinfo is None else 'failed'
            if outcome == 'failed':
                driver = item.funcargs.get('driver')
                if driver:
                    try:
                        screenshot = driver.get_screenshot_as_png()
                        allure.attach(screenshot, name='screenshot', attachment_type=AttachmentType.PNG)
                        page_source = driver.page_source
                        allure.attach(page_source, name='page_source', attachment_type=AttachmentType.TEXT)
                    except Exception as e:
                        logger.error(f"Error capturing screenshot or page source: {e}")


@pytest.hookimpl(tryfirst=True)
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="",  # Default to empty if not provided
        help="Comma-separated list of browsers to use (e.g., chrome,firefox,edge)"
    )
    parser.addoption(
        "--json-data",
        action="store",
        default=FileOperationsUtility.find_file_in_directory(FileOperationsUtility.get_project_root(), "data.json"),
        help="Path to the JSON file containing browser list if --browser is not provided"
    )


@pytest.fixture(scope="session")
def test_data(request):
    json_file_path = request.config.getoption("--json-data")
    if json_file_path:
        return JsonParserUtility.parse_json(json_file_path)
    return {"browsers": []}  # Return empty list if no JSON file is provided


@pytest.hookimpl(tryfirst=True)
def pytest_generate_tests(metafunc):
    browser_list = []

    # Handle browser fixture
    if 'browser' in metafunc.fixturenames:
        # Retrieve browser list from command line
        browser_option = metafunc.config.getoption("--browser")
        if browser_option:
            browser_list = browser_option.split(',')
        else:
            # No command line option provided, check JSON data
            json_file_path = metafunc.config.getoption("--json-data")
            if json_file_path:
                test_data = JsonParserUtility.parse_json(json_file_path)
                browser_list = test_data.get('browsers', [])
            # Note: No default value is set here; if `browser_list` is empty, it will be handled in test setup

        metafunc.parametrize('browser', browser_list)

    # Handle test_data fixture
    if 'test_data' in metafunc.fixturenames:
        json_file_path = metafunc.config.getoption("--json-data")
        if json_file_path:
            data = JsonParserUtility.parse_json(json_file_path)
            test_data = data.get('test_data', [])
        else:
            test_data = []

        # Provide default browser if test_data does not provide any browsers
        if not test_data:
            test_data = ["chrome"]

        metafunc.parametrize('test_data', test_data)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    if execution_type == 'local':
        with delete_lock:
            # Access command-line options
            results_directory = config.getoption("--alluredir")
            if results_directory:
                if (FileOperationsUtility.find_directory(results_directory)
                        is not None):
                    FileOperationsUtility.delete_directory(results_directory)
                else:
                    logger.warning(f'Allure directory does not exist')
            else:
                logger.warning(f'Allure directory is not provided from command-line')

            other_directories = FileOperationsUtility.find_directories_with_file_pattern(
                FileOperationsUtility.get_project_root(), "allure*")

            if other_directories:
                for directory in other_directories:
                    FileOperationsUtility.delete_directory(directory)
            else:
                logger.warning(f'Allure directories are clean')
