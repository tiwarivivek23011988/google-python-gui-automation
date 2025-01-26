from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory
from com.assignment.utilities import web_driver_utilities


class SauceDemo(PageFactory):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    locators = {
        'username': (By.ID, "user-name"),
        'password': (By.ID, "password"),
        'submit': (By.ID, "login-button"),
        'side_navigation_button': (By.ID, "react-burger-menu-btn"),
        'logout': (By.ID, "logout_sidebar_link"),
        'locked_user_error': (By.XPATH, "//h3[@data-test='error']")
    }

    def click_username_textbox_and_send_text(self, search_text):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['username'])
        username_box = self.driver.find_element(*self.locators['username'])
        username_box.click()
        username_box.clear()
        username_box.send_keys(search_text)

    def click_password_textbox_and_send_text(self, search_text):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['password'])
        password_box = self.driver.find_element(*self.locators['password'])
        password_box.click()
        password_box.clear()
        password_box.send_keys(search_text)

    def click_submit_button(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['submit'])
        submit_button = self.driver.find_element(*self.locators['submit'])
        submit_button.click()

    def click_element_from_auto_complete_list(self, matching_text):
        auto_complete_list = web_driver_utilities.wait_for_elements_visible(self.driver,
                                                                            *self.locators['auto_complete_list'])
        element_to_click = [element for element in auto_complete_list if element.text.__contains__(matching_text)]
        element_to_click[0].click()

    def click_on_side_navigation_bar(self):
        web_driver_utilities.wait_for_element_visible(self.driver, *self.locators['side_navigation_button'])
        side_navigation_element = self.driver.find_element(*self.locators['side_navigation_button'])
        side_navigation_element.click()

    def logout_of_sauce_demo(self):
        web_driver_utilities.wait_for_element_visible(self.driver, *self.locators['logout'])
        logout_element = self.driver.find_element(*self.locators['logout'])
        logout_element.click()

    def return_locked_user_error(self):
        web_driver_utilities.wait_for_element_visible(self.driver, *self.locators['locked_user_error'])
        locked_user_error_element = self.driver.find_element(*self.locators['locked_user_error'])
        return locked_user_error_element.text