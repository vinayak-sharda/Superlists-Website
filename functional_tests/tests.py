from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from django.test import LiveServerTestCase

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text , [row.text for row in rows]) 
   
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
        time.sleep(1)

        self.check_for_row_in_list_table('1:Buy Peacock Feathers')
        
        #There is a ext box inviting him to enter next item. He enters
        # 'Use peacock feather to make a fly.'

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feather to make a fly')
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again and now shows both items on her list.

        self.check_for_row_in_list_table('1:Buy Peacock Feathers')
        self.check_for_row_in_list_table('2:Use peacock feather to make a fly')


        #....rest of story.

        self.fail('Finish the Test')