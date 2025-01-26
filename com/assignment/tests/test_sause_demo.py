import logging
import pytest
import time

logger = logging.getLogger(__name__)

from com.assignment.pages.sause_demo_page import SauceDemo
from com.assignment.pages.sauce_product_page import SauceProduct

PAGE_URL="https://www.saucedemo.com/"

# Parameterize the test classes
@pytest.fixture
def login_and_navigate_to_sauce_demo(driver, request):
    username = request.param.get("username", "standard_user")
    password = request.param.get("password", "secret_sauce")
    # Initialize the Page Object
    sauce_demo_page = SauceDemo(driver)
    # Navigate to sauce demo
    driver.get(PAGE_URL)
    # Example test interaction
    sauce_demo_page.click_username_textbox_and_send_text(username)
    sauce_demo_page.click_password_textbox_and_send_text(password)
    sauce_demo_page.click_submit_button()


@pytest.mark.parametrize("login_and_navigate_to_sauce_demo",
                         [{"username": "standard_user", "password": "secret_sauce"}],
                         indirect=True)
class TestSauceDemoWithStandardUser:
    def test_sauce_demo_for_first_product_in_the_sorted_cart(self, driver, test_data, login_and_navigate_to_sauce_demo):
        sauce_product_page = SauceProduct(driver)
        sauce_product_page.select_sort_option_from_sort_text("Price (low to high)")
        item_price = sauce_product_page.click_add_to_cart_and_return_item_price(0)
        sauce_product_page.navigate_to_cart_page()
        item_price_list, length_of_cart = sauce_product_page.return_item_price_list_and_length_of_cart_from_checkout_page()
        sauce_product_page.continue_shopping()
        assert  item_price_list[0] == item_price
        assert length_of_cart == 1

    def test_sauce_demo_for_second_product_in_the_sorted_cart(self, driver, test_data, login_and_navigate_to_sauce_demo):
        sauce_product_page = SauceProduct(driver)
        sauce_product_page.select_sort_option_from_sort_text("Price (low to high)")
        item_price = sauce_product_page.click_add_to_cart_and_return_item_price(1)
        sauce_product_page.navigate_to_cart_page()
        item_price_list, length_of_cart = sauce_product_page.return_item_price_list_and_length_of_cart_from_checkout_page()
        assert item_price_list[0] == item_price
        assert length_of_cart == 1
        sauce_product_page.click_checkout_button()
        sauce_product_page.enter_first_name('first_name')
        sauce_product_page.enter_last_name('last_name')
        sauce_product_page.enter_zip_code(411031)
        sauce_product_page.submit_user_information()
        item_prices = sauce_product_page.get_price_list()
        assert len(item_prices)==1
        assert item_prices[0]==item_price
        sauce_product_page.click_on_finish_button()
        success_message, order_dispatched_message = sauce_product_page.get_order_status_related_text()
        assert success_message == 'Thank you for your order!'
        assert  order_dispatched_message == 'Your order has been dispatched, and will arrive just as fast as the pony can get there!'
        sauce_product_page.click_on_back_to_home_button()

@pytest.mark.parametrize("login_and_navigate_to_sauce_demo",
                         [{"username": "locked_out_user", "password": "secret_sauce"}],
                         indirect=True)
class TestSauceDemoWithLockedUser:
    #is_logged_in = False
    def test_login_with_locked_out_user_message(self, driver, login_and_navigate_to_sauce_demo):
        sauce_demo_page = SauceDemo(driver)
        error_text = sauce_demo_page.return_locked_user_error()
        assert error_text == 'Epic sadface: Sorry, this user has been locked out.'

@pytest.mark.parametrize("login_and_navigate_to_sauce_demo",
                         [{"username": "performance_glitch_user", "password": "secret_sauce"},
                          {"username": "standard_user", "password": "secret_sauce"}],
                         indirect=True)
class TestSauceDemoWithPerformanceUser:

    def test_loading_time_of_each_page(self, driver, login_and_navigate_to_sauce_demo):
        # Enable Performance Logging
        driver.execute_cdp_cmd("Performance.enable", {})
        sauce_product_page = SauceProduct(driver)
        sauce_product_page.click_add_to_cart_and_return_item_price(0)
        start_time = time.time()
        sauce_product_page.navigate_to_cart_page()
        end_time = time.time()
        # Capture lifecycle events
        events = driver.execute_cdp_cmd("Performance.getMetrics", {})
        metric_data = {m["name"]: m["value"] for m in events["metrics"]}

        # Calculate key metrics
        navigation_start = metric_data.get("NavigationStart", 0)
        dom_content_loaded = metric_data.get("DomContentLoaded", 0)
        first_meaningful_paint = metric_data.get("FirstMeaningfulPaint", 0)

        url = driver.current_url
        # Print events
        logger.info(f"Performance Metrics Are: NavigationStart -> {navigation_start} : DomContentLoaded -> {dom_content_loaded} : FirstMeaningfulPaint -> {first_meaningful_paint} : url -> {url} page load time : {dom_content_loaded-navigation_start}")

        # Calculate total time taken
        logger.info(f"Page Load Time (s): for cart url -> {url} is', {end_time - start_time}")

        start_time = time.time()

        sauce_product_page.click_checkout_button()

        end_time = time.time()

        # Capture lifecycle events
        events = driver.execute_cdp_cmd("Performance.getMetrics", {})
        metric_data = {m["name"]: m["value"] for m in events["metrics"]}

        # Calculate key metrics
        navigation_start = metric_data.get("NavigationStart", 0)
        dom_content_loaded = metric_data.get("DomContentLoaded", 0)
        first_meaningful_paint = metric_data.get("FirstMeaningfulPaint", 0)

        url = driver.current_url

        # Print events
        logger.info(f"Performance Metrics Are: NavigationStart -> {navigation_start} : DomContentLoaded -> {dom_content_loaded} : FirstMeaningfulPaint -> {first_meaningful_paint} : url -> {url} page load time : {dom_content_loaded - navigation_start}")

        # Calculate total time taken
        logger.info(f"Page Load Time (s): for checkout-step-one url -> {url} is', {end_time - start_time}")

        start_time = time.time()

        sauce_product_page.enter_first_name('first_name')
        sauce_product_page.enter_last_name('last_name')
        sauce_product_page.enter_zip_code(411031)
        sauce_product_page.submit_user_information()

        end_time = time.time()
        # Capture lifecycle events
        events = driver.execute_cdp_cmd("Performance.getMetrics", {})
        metric_data = {m["name"]: m["value"] for m in events["metrics"]}

        # Calculate key metrics
        navigation_start = metric_data.get("NavigationStart", 0)
        dom_content_loaded = metric_data.get("DomContentLoaded", 0)
        first_meaningful_paint = metric_data.get("FirstMeaningfulPaint", 0)

        url = driver.current_url

        # Print events
        logger.info(f"Performance Metrics Are: NavigationStart -> {navigation_start} : DomContentLoaded -> {dom_content_loaded} : FirstMeaningfulPaint -> {first_meaningful_paint} : url -> {url} page load time : {dom_content_loaded - navigation_start}")

        # Calculate total time taken
        logger.info(f"Page Load Time (s): for checkout-step-two page url -> {url} is', {end_time - start_time}")

        start_time = time.time()

        sauce_product_page.click_on_finish_button()

        end_time = time.time()

        # Capture lifecycle events
        events = driver.execute_cdp_cmd("Performance.getMetrics", {})
        metric_data = {m["name"]: m["value"] for m in events["metrics"]}

        # Calculate key metrics
        navigation_start = metric_data.get("NavigationStart", 0)
        dom_content_loaded = metric_data.get("DomContentLoaded", 0)
        first_meaningful_paint = metric_data.get("FirstMeaningfulPaint", 0)

        url = driver.current_url

        # Print events
        logger.info(f"Performance Metrics Are: NavigationStart -> {navigation_start} : DomContentLoaded -> {dom_content_loaded} : FirstMeaningfulPaint -> {first_meaningful_paint} : url -> {url} page load time : {dom_content_loaded - navigation_start}")

        # Calculate total time taken
        logger.info(f"Page Load Time (s): for checkout-complete url -> {url} is', {end_time - start_time}")

        start_time = time.time()

        sauce_product_page.click_on_back_to_home_button()

        end_time = time.time()

        # Capture lifecycle events
        events = driver.execute_cdp_cmd("Performance.getMetrics", {})
        metric_data = {m["name"]: m["value"] for m in events["metrics"]}

        # Calculate key metrics
        navigation_start = metric_data.get("NavigationStart", 0)
        dom_content_loaded = metric_data.get("DomContentLoaded", 0)
        first_meaningful_paint = metric_data.get("FirstMeaningfulPaint", 0)

        url = driver.current_url

        # Print events
        logger.info(f"Performance Metrics Are: NavigationStart -> {navigation_start} : DomContentLoaded -> {dom_content_loaded} : FirstMeaningfulPaint -> {first_meaningful_paint} : url -> {url} page load time : {dom_content_loaded - navigation_start}")

        # Calculate total time taken
        logger.info(f"Page Load Time (s): for inventory url -> {url} is', {end_time - start_time}")

@pytest.fixture(scope="class")
def logout_of_sauce_demo_page(driver):
    sauce_demo_page = SauceDemo(driver)
    sauce_demo_page.click_on_side_navigation_bar()
    sauce_demo_page.logout_of_sauce_demo()