from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from core.models.category import Category
from core.models.product import Product
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
        # cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.driver.close()

    def setUp(self):

        User.objects.create_user(
            username='testuser1', password='1X<ISRUkw+tuK')

        p1 = Product.product_objects.create_product(
            barcode=1,
            product_name="product_name_1",
            nutriscore_grade="D",
            product_description="Product description",
            off_url="www.off.com",
            image_url="www.image_url.com")

        p2 = Product.product_objects.create_product(
            barcode=2,
            product_name="product_name_2",
            nutriscore_grade="A",
            product_description="Product description",
            off_url="www.off.com",
            image_url="www.image_url.com")

        c1 = Category.category_objects.create_category('category_one')
        c2 = Category.category_objects.create_category('category_two')
        p1.categories.add(c1, c2)
        p2.categories.add(c1, c2)

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

    def test_user_search_product(self):
        self.connect_user()

        add_url = self.live_server_url + \
            ("%s?product=product_name_1" % reverse('substitute'))

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'id_search')))

        self.driver.find_element_by_id('id_search').send_keys('product_name_1')
        self.driver.find_element_by_id('id_search').send_keys(Keys.RETURN)

        self.assertEquals(self.driver.current_url, add_url)
        self.assertTrue(self.driver.find_element_by_id('card_2'))

    def test_user_save_substitute(self):
        self.connect_user()

        self.driver.find_element_by_id('id_search').send_keys('product_name_1')
        self.driver.find_element_by_id('id_search').send_keys(Keys.RETURN)

        save_button = self.driver.find_element_by_id('save_substitute_2')

        save_button.click()
        favourite = User.objects.get(username='testuser1').product_set.first()

        self.assertEqual(favourite.barcode, 2)

    def test_user_search_product_autocomplete(self):
        self.connect_user()

        add_url = self.live_server_url + \
            ("%s?product=p" % reverse('substitute'))
        self.driver.find_element_by_id('id_search').send_keys('p')

        self.driver.find_element_by_id(
            'id_search').send_keys(Keys.DOWN + Keys.RETURN)

        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH,
             '//h1[@class="text-uppercase text-black font-weight-bold"]')))

        product_name = self.driver.find_elements_by_xpath(
            '//h1[@class="text-uppercase text-black font-weight-bold"]'
        )[0].text

        self.assertEquals(self.driver.current_url, add_url)
        self.assertTrue(self.driver.find_element_by_id('card_2'))
        self.assertEquals(product_name, "product_name_1")
