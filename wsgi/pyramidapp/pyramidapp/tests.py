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

import unittest
from selenium import webdriver


class Selenium2OnSauce(unittest.TestCase):

    def setUp(self):
        desired_capabilities = webdriver.DesiredCapabilities.Firefox
        desired_capabilities['version'] = '21.0'
        desired_capabilities['platform'] = 'LINUX'
        desired_capabilities['name'] = 'Testing Selenium 2 in Python at Sauce'

        self.driver = webdriver.Remote(
            desired_capabilities=desired_capabilities,
            command_executor="http://andremontoiab:d95e5825-a4d4-4a27-9b6e-3b899f5b09e1@ondemand.saucelabs.com:80/wd/hub"
        )
        self.driver.implicitly_wait(30)

    def test_sauce(self):
        self.driver.get('http://carona-sustentavel.rhcloud.com/')
        self.assertTrue("I am a page title - Sauce Labs" in self.driver.title)
        comments = self.driver.find_element_by_id('comments')
        comments.send_keys('Hello! I am some example comments.'
                           ' I should be in the page after submitting the form')
        self.driver.find_element_by_id('submit').click()

        commented = self.driver.find_element_by_id('your_comments')
        self.assertTrue('Your comments: Hello! I am some example comments.'
                        ' I should be in the page after submitting the form'
                        in commented.text)
        body = self.driver.find_element_by_xpath('//body')
        self.assertFalse('I am some other page content' in body.text)
        self.driver.find_elements_by_link_text('i am a link')[0].click()
        body = self.driver.find_element_by_xpath('//body')
        self.assertTrue('I am some other page content' in body.text)

    def tearDown(self):
        print("Link to your job: https://saucelabs.com/jobs/%s" % self.driver.session_id)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
