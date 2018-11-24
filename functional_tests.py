from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self):
        self.browser.quit()
   
    def test_can_start_a_list_and_retrieve_it_later(self):
        #Vinayak has heard about a cool new online to-do app. He goes to check out its homepage.
        self.browser.get("http://localhost:8000")
        
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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertTrue(
            any(row.text=='1:Buy Peacock Feathers' for row in rows),
            "New to-do item did not appear in the table"
        )

        
        #....rest of story.

        self.fail('Finish the Test')

if __name__=='main':
    unittest.main(warnings='ignore')
