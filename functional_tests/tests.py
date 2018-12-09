from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text , [row.text for row in rows]) 
                return
            except( AssertionError, WebDriverException) as e:
                if time.time() - start_time >MAX_WAIT:
                    raise e
                time.sleep(0.5)


    def test_can_start_a_list_and_retrieve_it_later(self):
        #Vinayak has heard about a cool new online to-do app. He goes to check out its homepage.
        self.browser.get(self.live_server_url)
        
        # He notices "to-do lists" in page title
        self.assertIn('To-Do',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

        #He is invited to enter a to-do item straight away.
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),'Enter a to-do item'
        )

        # He types "Buy Peacock Feathers" into the text-box.
        input_box.send_keys('Buy Peacock Feathers')

        # When he hits enter, the page updates and lists '1:Buy Peacock Feathers'
        # as an item in to-do list table.

        input_box.send_keys(Keys.ENTER)
    

        self.wait_for_row_in_list_table('1:Buy Peacock Feathers')
        
        #There is a ext box inviting him to enter next item. He enters
        # 'Use peacock feather to make a fly.'

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)
        

        # The page updates again and now shows both items on her list.

        self.wait_for_row_in_list_table('1:Buy Peacock Feathers')
        self.wait_for_row_in_list_table('2:Use peacock feather to make a fly')

        # Satisfied, he goes to sleep.

    
    def test_multiple_users_can_start_lists_at_different_urls(self):
        #Vinayak starts a new To-Do list.
        self.browser.get(self.live_server_url)
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy Peacock Feathers')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:Buy Peacock Feathers")


        # He notices that his list has a unique URL.
        vinayak_list_url = self.browser.current_url
        self.assertRegex(vinayak_list_url,'/lists/.+')

        # Now, a new user, Minku comes along to the site.

        ## We use a new browser session to make sure that no information is coming from 
        ## cookies of Vinayak's list
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Minku visits the home page. There is no sign of Vinayak's list.

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feathers',page_text)
        self.assertNotIn('make a fly',page_text)

        # Minku starts a new list by entering a new item. 
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy milk')
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1:Buy milk")

        # Minku gets his own unique URL.
        minku_list_url = self.browser.current_url
        self.assertRegex(minku_list_url,'/lists/.+')
        self.assertNotEqual(vinayak_list_url, minku_list_url)

        # Again, there is no sign of Vinayak's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy Peacock Feathers',page_text)
        self.assertIn('Buy milk',page_text)

        #Satisfied, they both go back to sleep.
