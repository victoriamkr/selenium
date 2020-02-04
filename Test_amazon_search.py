import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


from Resources.Locators import *
from Resources.test_data import *

# open amazon.com, verify the page is opened
driver = webdriver.Chrome()
driver.get(TestData.base_url)
driver.maximize_window()
assert TestData.home_page_title in driver.title

driver.implicitly_wait(3)

# type testing in the search box, verify the element is found
driver.find_element(By.ID, Locators.search_textbox).send_keys(TestData.search_item + Keys.RETURN)
time.sleep(3)
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH, Locators.search_result_link)))

# click on the ebook link
driver.find_element(By.XPATH, Locators.search_result_link).click()

# wait till product detail is visible (add to cart) and click it
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, Locators.add_to_cart_button)))

driver.find_element(By.ID, Locators.add_to_cart_button).click()

# verify next page is opened, proceed to checkout is visible, click on it
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, Locators.proceed_to_checkout_button)))

driver.find_element(By.ID, Locators.proceed_to_checkout_button).click()

# verify the use must login to continue, input the test data
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, Locators.mail_input)))

# login input
driver.find_element(By.ID, Locators.mail_input).send_keys(TestData.test_mail)
driver.find_element(By.ID, Locators.continue_button).click()

# password input
WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.ID, Locators.password)))

driver.find_element(By.ID, Locators.password).send_keys(TestData.password)

driver.find_element(By.ID, Locators.sign_in_button).click()

# verify user must type the captcha, and alert is present, type the password and characters

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.CLASS_NAME, Locators.allert_message)))


def check_exists_by_class_name(class_name):
    try:
        driver.find_element(By.CLASS_NAME, Locators.captcha)
    except NoSuchElementException:
        return False
    return True

# type password
driver.find_element(By.ID, Locators.password).send_keys(TestData.password)
# type characters
driver.find_element(By.ID, Locators.type_char).send_keys(TestData.characters)
driver.find_element(By.ID, Locators.sign_in_submit).click()

# verify user can't log in as the characters are invalid
warning = driver.find_element_by_class_name(Locators.allert_content).text
assert warning == "Enter the characters as they are given in the challenge."

driver.quit()