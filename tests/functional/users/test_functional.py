from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from core.models.user import User

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')


class ChromeFunctionalTestCases(StaticLiveServerTestCase):
    """Functional tests using the Chrome web browser in headless mode."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome(chrome_options=chrome_options)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.close()

    def setUp(self):

        User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

    def connect_user(self):
        self.driver.get(self.live_server_url)
        self.driver.find_element_by_id('id_login').click()

        self.driver.find_element_by_id('id_username').send_keys(
            "testuser1"
        )
        self.driver.find_element_by_id('id_password').send_keys(
            "1X<ISRUkw+tuK"
        )
        self.driver.find_element_by_id(
            'id_button_login').send_keys(Keys.RETURN)

    def test_user_update_profile(self):
        self.connect_user()

        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, "#profile_id"))).click()

        self.driver.find_element_by_id('id_username').clear()
        self.driver.find_element_by_id('id_email').clear()

        self.driver.find_element_by_id(
            'id_username').send_keys('testuser1_updated')
        self.driver.find_element_by_id('id_email').send_keys(
            'testuser1_updated@gmail.com')

        update_button = self.driver.find_element_by_id('update_button_id')

        update_button.click()

        user = User.objects.get(user_id='1')

        self.assertEqual(user.username, 'testuser1_updated')
        self.assertEqual(user.email, 'testuser1_updated@gmail.com')
