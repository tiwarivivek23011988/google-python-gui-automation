#product_sort_container
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from seleniumpagefactory.Pagefactory import PageFactory
from com.assignment.utilities import web_driver_utilities


class SauceProduct(PageFactory):
    listOfItems=[]
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    locators = {
        'product_sort': (By.CLASS_NAME, "product_sort_container"),
        'product_price_list': (By.XPATH, "//div[@class='inventory_item_price']"),
        'shopping_cart_link': (By.XPATH, "//a[@class='shopping_cart_link']"),
        'cart_item_list': (By.XPATH, "//div[@class='cart_item']"),
        'continue_shopping': (By.ID, "continue-shopping"),
        'checkout_button': (By.ID, "checkout"),
        'first_name': (By.ID, "first-name"),
        'last_name': (By.ID, "last-name"),
        'zip_code': (By.ID, "postal-code"),
        'submit_user_info_button': (By.ID, "continue"),
        'overview_page_finish_button': (By.ID, "finish"),
        'success_message': (By.CLASS_NAME, "complete-header"),
        'order_dispatched_text': (By.CLASS_NAME, "complete-text"),
        'back_to_home': (By.ID, "back-to-products")
    }
    # //div[@class='inventory_item_price']/following-sibling::button
    def select_sort_option_from_sort_text(self, option_text):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['product_sort'])
        product_sort = self.driver.find_element(*self.locators['product_sort'])
        product_sort.click()
        select = Select(product_sort)
        select.select_by_visible_text(option_text)

    def get_price_list(self):
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['product_price_list'])
        items_price_elements = self.driver.find_elements(*self.locators['product_price_list'])
        items_price = []
        for item_element in items_price_elements:
            items_price.append(item_element.text)
        for index in range(len(items_price)):
            items_price[index] = re.sub(r"[^0-9.\-+]", "", items_price[index])
        return  items_price

    def return_element_price_and_cart_element(self):
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['product_price_list'])
        items_price_elements = self.driver.find_elements(*self.locators['product_price_list'])
        items_price = self.get_price_list()
        # Find the corresponding add-to-cart button for each price element
        add_cart_elements = [
            price_element.find_element(By.XPATH, './following-sibling::button')
            for price_element in items_price_elements
        ]
        return items_price, add_cart_elements

    def click_add_to_cart_and_return_item_price(self, index):
        items_price, add_cart_elements = self.return_element_price_and_cart_element()
        for index_seq in range(len(items_price)):
            items_price[index_seq]=re.sub(r"[^0-9.\-+]", "", items_price[index_seq])
        is_sorted = items_price == sorted(items_price)
        price_add_cart_map = {}
        if not is_sorted:
            for index_seq in range(len(items_price)):
                price_add_cart_map[items_price[index_seq]]=add_cart_elements[index_seq]
            items_price.sort()
            for index_seq in range(len(add_cart_elements)):
                add_cart_elements[index_seq]=price_add_cart_map[items_price[index_seq]]
        for item in add_cart_elements:
            if item.text != 'Add to cart':
                item.click()
        add_cart_elements[index].click()
        return items_price[index]

    def navigate_to_cart_page(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['shopping_cart_link'])
        cart_element = self.driver.find_element(*self.locators['shopping_cart_link'])
        cart_element.click()

    def return_item_price_list_and_length_of_cart_from_checkout_page(self):
        items_price_list, added_cart_elements = self.return_element_price_and_cart_element()
        return items_price_list, len(added_cart_elements)

    def continue_shopping(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['continue_shopping'])
        continue_shopping_element = self.driver.find_element(*self.locators['continue_shopping'])
        continue_shopping_element.click()

    def click_checkout_button(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['checkout_button'])
        checkout_button_element = self.driver.find_element(*self.locators['checkout_button'])
        checkout_button_element.click()

    def enter_first_name(self, first_name):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['first_name'])
        first_name_element = self.driver.find_element(*self.locators['first_name'])
        first_name_element.send_keys(first_name)

    def enter_last_name(self, last_name):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['last_name'])
        last_name_element = self.driver.find_element(*self.locators['last_name'])
        last_name_element.send_keys(last_name)

    def enter_zip_code(self, zip_code):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['zip_code'])
        zip_code_element = self.driver.find_element(*self.locators['zip_code'])
        zip_code_element.send_keys(zip_code)

    def submit_user_information(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['submit_user_info_button'])
        continue_button_element = self.driver.find_element(*self.locators['submit_user_info_button'])
        continue_button_element.click()

    def return_prices_list_from_overview_page(self):
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['product_price_list'])
        items_price = self.driver.find_elements(*self.locators['product_price_list'])
        for index in range(len(items_price)):
            items_price[index]=re.sub(r"[^0-9.\-+]", "", items_price[index])
        return items_price

    def click_on_finish_button(self):
        web_driver_utilities.wait_for_element_clickable(self.driver, *self.locators['overview_page_finish_button'])
        overview_page_finish_button_element = self.driver.find_element(*self.locators['overview_page_finish_button'])
        overview_page_finish_button_element.click()

    def get_order_status_related_text(self):
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['success_message'])
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['order_dispatched_text'])
        success_message_element = self.driver.find_element(*self.locators['success_message'])
        order_dispatched_element = self.driver.find_element(*self.locators['order_dispatched_text'])
        return success_message_element.text, order_dispatched_element.text

    def click_on_back_to_home_button(self):
        web_driver_utilities.wait_for_elements_visible(self.driver, *self.locators['back_to_home'])
        back_to_home_element = self.driver.find_element(*self.locators['back_to_home'])
        back_to_home_element.click()