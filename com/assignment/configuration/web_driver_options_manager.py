from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService


class WebDriverOptionsManager:

    @staticmethod
    def get_driver_options(browser_name):
        if browser_name == 'chrome':
            chrome_options = ChromeOptions()
            chrome_options.accept_insecure_certs = True
            chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
            service = ChromeService()
            options = chrome_options
        elif browser_name == 'firefox':
            firefox_options = FirefoxOptions()
            firefox_options.accept_insecure_certs = True
            service = FirefoxService()
            options = firefox_options
        elif browser_name == 'edge':
            edge_options = EdgeOptions()
            edge_options.accept_insecure_certs = True
            service = EdgeService()
            options = edge_options
        else:
            raise ValueError(f"Browser {browser_name} is not supported")

        # Debugging print statements
        print(f"Options: {options}")
        print(f"Service: {service}")
        print(f"type(Options): {type(options)}")
        print(f"type(Service): {type(service)}")

        if options is None:
            raise RuntimeError(f"Options for {browser_name} could not be initialized")

        return service, options
