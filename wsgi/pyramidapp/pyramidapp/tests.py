#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import selenium
import unittest, time, re

class navegacao_2(unittest.TestCase):
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
		
    def test_navegacao(self):
        self = self.selenium
        self.open("/login")
        self.wait_for_page_to_load("60000")
        self.click("id=content")
        self.type("id=deformField1", "test")
        self.type("id=deformField2", "11111")		
        self.click("css=#deformEntrar")
        self.wait_for_page_to_load("60000")
        self.click(u"link=Usuários")
        self.wait_for_page_to_load("60000")
        self.type("id=deformField1", "bolha")
        self.click("id=deformBuscar")
        self.wait_for_page_to_load("60000")
        self.click("link=Caronas")
        self.wait_for_page_to_load("60000")
        self.type("id=deformField1", "Jau")
        self.click("id=deformBuscar")
        self.wait_for_page_to_load("60000")
        self.click("link=Jau -> Campo Grande")
        self.wait_for_page_to_load("60000")
        self.click("link=home")
        self.wait_for_page_to_load("60000")
		
    def test_navegacao_2(self):
        self = self.selenium
        self.open("/login")
        self.wait_for_page_to_load("60000")
        self.click("id=content")        
        self.type("id=deformField1", "test")
        self.type("id=deformField2", "11111")
        self.click("css=#deformEntrar")
        self.wait_for_page_to_load("60000")
        self.click("link=Troque seus Pontos Verdes")
        self.wait_for_page_to_load("60000")
        self.click(u"link=Usuários")
        self.wait_for_page_to_load("60000")
        self.click("link=bolha")
        self.wait_for_page_to_load("60000")
        self.click("xpath=//div[@class='mainContent']/div/ul/ul/li[2]/a/img")
        self.wait_for_page_to_load("60000")
    
    def tearDown(self):
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
