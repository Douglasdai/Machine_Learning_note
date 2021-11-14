from selenium import webdriver
from time import sleep


driver = webdriver.Chrome()
driver.get("https://www.baidu.com") # 打印当前页面title
title = driver.title
now_url = driver.current_url
driver.find_element_by_id("kw").send_keys("selenium")
driver.find_element_by_id("su").click()
sleep(1)
title = driver.title
now_url = driver.current_url
user = driver.find_element_by_class_name('nums').text
