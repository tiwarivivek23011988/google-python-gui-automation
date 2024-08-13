from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


def wait_for_element_clickable(driver, by, value, timeout=30):
    """
    Wait until the element specified by (by, value) is clickable.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: The WebElement if found and clickable.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.element_to_be_clickable((by, value)))


def wait_for_element_present(driver, by, value, timeout=30):
    """
    Wait until the element specified by (by, value) is present in the DOM.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: The WebElement if found.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.presence_of_element_located((by, value)))


def wait_for_element_visible(driver, by, value, timeout=30):
    """
    Wait until the element specified by (by, value) is visible.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: The WebElement if found and visible.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.visibility_of_element_located((by, value)))


def wait_for_element_invisible(driver, by, value, timeout=30):
    """
    Wait until the element specified by (by, value) is invisible.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: True if the element is invisible, False otherwise.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.invisibility_of_element_located((by, value)))


def wait_for_element_text_to_contain(driver, by, value, text, timeout=30):
    """
    Wait until the text of the element specified by (by, value) contains the given substring.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param text: The substring to check for within the element's text.
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: The WebElement if the text contains the substring.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(ec.text_to_be_present_in_element((by, value), text))


def wait_for_element_attribute_to_be(driver, by, value, attribute, expected_value, timeout=30):
    """
    Wait until the specified attribute of the element has the expected value.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the element (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param attribute: The name of the attribute.
    :param expected_value: The expected value of the attribute.
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: The WebElement if the attribute matches the expected value.
    """
    wait = WebDriverWait(driver, timeout)
    return wait.until(lambda web_driver: web_driver.find_element(by, value).get_attribute(attribute) == expected_value)


def wait_for_elements_visible(driver, by, value, timeout=30):
    """
    Wait until all elements specified by (by, value) are visible.

    :param driver: The WebDriver instance.
    :param by: The method used to locate the elements (e.g., By.XPATH).
    :param value: The locator value (e.g., the XPath or CSS selector).
    :param timeout: The maximum time to wait for the condition (in seconds).
    :return: A list of WebElements that are visible.
    """
    wait = WebDriverWait(driver, timeout)
    elements = wait.until(ec.visibility_of_all_elements_located((by, value)))
    return elements
