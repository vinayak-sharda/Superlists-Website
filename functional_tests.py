from selenium import webdriver
import unittest

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
        self.fail('Finish the Test')
        
        #He is invited to enter a to-do item straight away.
        #....rest of story.

if __name__=='main':
    unittest.main(warnings='ignore')
