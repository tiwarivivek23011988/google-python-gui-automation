import pytest
from com.assignment.pages.google_page import GooglePage


def test_google_search(driver, browser, test_data):

    # Navigate to Google
    driver.get("https://www.google.com")

    # Initialize the Page Object
    google_page = GooglePage(driver)

    # Example test interaction
    google_page.click_google_search_box_and_send_text("astronomer")
    google_page.click_element_from_auto_complete_list("astronomer")

    # Add assertions as needed
    assert google_page.validate_searched_result_matching_text("astronomer")
