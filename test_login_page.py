from time import sleep

import pytest
from selenium import webdriver

from conftest import BaseTest


class TestLoginPage(BaseTest):

    @pytest.fixture(scope="class")
    def driver(self):
        driver = webdriver.Chrome(
            executable_path=r"C:\Users\lappt\PycharmProjects\QaComplexApp\Drivers\chromedriver.exe")
        yield driver
        driver.close()

    @pytest.fixture(scope="function")
    def logout(self, driver):
        yield
        driver.find_element_by_xpath(".//button[contains(text(), 'Sign Out')]").click()
        sleep(1)

    @pytest.fixture(scope="function")
    def register(self, driver):
        registered_user = self.register_user(driver)
        driver.find_element_by_xpath(".//button[contains(text(), 'Sign Out')]").click()
        sleep(1)
        return registered_user

    def register_user(self, driver):
        """Fill required fields and press button"""
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.debug("Open page")

        # Fill email, login and password fields
        # Fill username
        username_value = f"Name{self.variety}"
        username = driver.find_element_by_xpath(".//input[@id='username-register']")
        username.clear()
        username.send_keys(username_value)

        # Fill email
        email_value = f"user{self.variety}@mail.com"
        email = driver.find_element_by_xpath(".//input[@id='email-register']")
        email.clear()
        email.send_keys(email_value)

        # Fill password
        password_value = f"Password{self.variety}"
        password = driver.find_element_by_xpath(".//input[@id='password-register']")
        password.clear()
        password.send_keys(password_value)

        self.log.debug("Fields were filled")
        sleep(1)

        # Click on Sign Up button
        button = driver.find_element_by_xpath(".//button[@type='submit']").click()
        sleep(1)

        return username_value, email_value, password_value

    def test_empty_fields_login(self, driver):
        """
        - Open start page
        - Clear password and login fields
        - Click on Sigh In button
        - Verify error message
        """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open page")

        # Clear required fields
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        self.log.info("Fields were cleared and filled")

        # Click on Sihn In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify error message
        error_message = driver.find_element_by_xpath(".//div[contains(text(), 'Invalid username / password')]")
        assert error_message.text == 'Invalid username / password'
        self.log.info("Error message match to expected")

    def test_register(self, driver, logout):
        """
        - Open start page
        - Fill email, login and password fields
        - Click on Sign up button
        - Verify register success
        """
        username_value = self.register_user(driver)[0]
        self.log.info("User was registered")

        # Verify register success
        hello_message = driver.find_element_by_xpath(".//h2")
        assert username_value.lower() in hello_message.text
        assert hello_message.text == f"Hello {username_value.lower()}, your feed is empty."
        assert driver.find_element_by_xpath(".//strong").text == username_value.lower()
        self.log.info("Registration was success and verified")

    def test_invalid_fields_login(self, driver):
        """
        - Open start page
        - Clear password and login fields
        - Try to sign with invalid credentials
        - Click on Sigh In button
        - Verify error message
        """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.info("Open page")

        # Clear required fields
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        username.send_keys("sfsdggs@gmail.com")
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        password.send_keys("arqerr342sege2reD")
        self.log.info("Fields were cleared and filled")

        # Click on Sign In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify error message
        error_message = driver.find_element_by_xpath(".//div[contains(text(), 'Invalid username / password')]")
        assert error_message.text == 'Invalid username / password'
        self.log.info("Error message match to expected")

    def test_login(self, register, driver, logout):
        """
        - Open start page
        - Fill login and password fields
        - Click on Sign in button
        - Verify result
        """
        # Open start page
        driver.get("https://qa-complex-app-for-testing.herokuapp.com")
        self.log.debug("Open page")

        username_value, _, password_value = register

        # Clear required fields
        username = driver.find_element_by_xpath(".//input[@placeholder='Username']")
        username.clear()
        username.send_keys(username_value)
        password = driver.find_element_by_xpath(".//input[@placeholder='Password']")
        password.clear()
        password.send_keys(password_value)
        self.log.info("Fields were cleared and filled")

        # Click on Sign In button
        sign_in_button = driver.find_element_by_xpath(".//button[contains(text(), 'Sign In')]")
        sign_in_button.click()
        self.log.info("Clicked on 'Sign In'")

        # Verify register success
        hello_message = driver.find_element_by_xpath(".//h2")
        assert username_value.lower() in hello_message.text
        assert hello_message.text == f"Hello {username_value.lower()}, your feed is empty."
        assert driver.find_element_by_xpath(".//strong").text == username_value.lower()
        self.log.info("Registration was success and verified")
