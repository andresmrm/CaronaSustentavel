#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Copyright 2013 Carona Sustentavel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#-----------------------------------------------------------------------------

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time, unittest

def is_alert_present(wd):
    try:
        wd.switch_to_alert().text
        return True
    except:
        return False

class login(unittest.TestCase):
    def setUp(self):	
		desired_capabilities = webdriver.DesiredCapabilities.FIREFOX       

        self.wd = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://andremontoiab:d95e5825-a4d4-4a27-9b6e-3b899f5b09e1@ondemand.saucelabs.com:80/wd/hub"
        )		 
        self.wd.implicitly_wait(60)
    
    def test_login(self):
        success = True
        wd = self.wd
        wd.get("http://carona-sustentavel.rhcloud.com/login")
        wd.find_element_by_id("deformField1").click()
        wd.find_element_by_id("deformField1").clear()
        wd.find_element_by_id("deformField1").send_keys("test")
        wd.find_element_by_id("deformField2").click()
        wd.find_element_by_id("deformField2").clear()
        wd.find_element_by_id("deformField2").send_keys("11111")
        wd.find_element_by_css_selector("#deformEntrar").click()
        self.assertTrue(success)
    
    def tearDown(self):
        self.wd.quit()

if __name__ == '__main__':
    unittest.main()
