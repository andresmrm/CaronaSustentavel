from selenium import selenium
import unittest, time, re

class selenium_1(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium("http", //andremontoiab, "*chrome", "http://carona-sustentavel.rhcloud.com")
        self.selenium.start()
    
    def test_selenium_1(self):
        sel = self.selenium
        sel.open("/login")
        sel.wait_for_page_to_load("60000")
        sel.click("css=div.inner1")
        sel.type("id=deformField1", "test")
        sel.type("id=deformField2", "11111")
        sel.click("css=#deformEntrar")
        sel.wait_for_page_to_load("60000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
