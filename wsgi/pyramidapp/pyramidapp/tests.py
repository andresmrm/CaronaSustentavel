from selenium import selenium
import unittest, time, re

class login(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.selenium = selenium('ondemand.saucelabs.com',80,"""{"username": "andremontoiab","access-key": "d95e5825-a4d4-4a27-9b6e-3b899f5b09e1","os": "Windows 2003","browser": "firefox","browser-version": "7","name": "Carona Sustentavel"}""",'http://carona-sustentavel.rhcloud.com')
        self.selenium.start()			
    
    def login(self):
        self = self.selenium
        self.open("/login")
        self.wait_for_page_to_load("60000")
        self.click("id=content")
        self.type("id=deformField1", "test")
        self.type("id=deformField2", "11111")
        self.click("css=#deformEntrar")
        self.wait_for_page_to_load("60000")
        self.click("xpath=//div[@class='mainContent']//li[.='Altura: 1.0']")

    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
