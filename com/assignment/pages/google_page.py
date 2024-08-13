from selenium.webdriver.common.by import By
from seleniumpagefactory.Pagefactory import PageFactory
from com.assignment.utilities import web_driver_utilities


class GooglePage(PageFactory):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    locators = {
        'search_box': (By.XPATH, "//textarea[@aria-label='Search']"),
        'auto_complete_list': (By.XPATH, "//ul[@role='listbox']/li//div[@role='option']"),
        'searched_results': (By.XPATH, "//div[@data-snhf='0']//span/a/h3")
    }

    def click_google_search_box_and_send_text(self, search_text):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['search_box'])
        search_box = self.driver.find_element(*self.locators['search_box'])
        search_box.click()
        search_box.clear()
        search_box.send_keys(search_text)

    def click_element_from_auto_complete_list(self, matching_text):
        auto_complete_list = web_driver_utilities.wait_for_elements_visible(self.driver,
                                                                            *self.locators['auto_complete_list'])
        element_to_click = [element for element in auto_complete_list if element.text.__contains__(matching_text)]
        element_to_click[0].click()

    def validate_searched_result_matching_text(self, matching_text):
        searched_result_list = web_driver_utilities.wait_for_elements_visible(self.driver,
                                                                              *self.locators['searched_results'])
        print((element.text for element in searched_result_list))
        element_to_validate = [element for element in searched_result_list
                               if element.text.lower().__contains__(matching_text.lower())]
        if len(element_to_validate) > 0:
            return True
        return False
