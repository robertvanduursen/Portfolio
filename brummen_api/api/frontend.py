import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def browser():
    # Initialize the WebDriver
    driver = webdriver.Chrome()  # You can use any other WebDriver like Firefox, Edge, etc.
    yield driver
    # Quit the WebDriver after the test
    driver.quit()

def test_button_click(browser):
    # Open the HTML page
    browser.get('http://example.com/page_with_button.html')

    # Find the button element
    button = browser.find_element(By.ID, 'button_id')  # Replace 'button_id' with the actual ID of your button

    # Click the button
    button.click()

    # Optionally, you can wait for some element to change after clicking the button
    # For example, wait for a specific text to appear on the page
    WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.ID, 'result'), 'Button clicked'))

    # Assert that the button click triggered the expected action
    assert 'Button clicked' in browser.find_element(By.ID, 'result').text
