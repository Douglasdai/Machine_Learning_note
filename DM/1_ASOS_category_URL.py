# -*- coding: utf-8 -*-

from selenium import webdriver

driver = webdriver.Chrome()

driver.get('http://www.asos.com/?hrd=1')

output = driver.find_elements_by_xpath("//a[@class='mu__cta']")
for ele in output:
    print(ele.get_attribute('href'))
