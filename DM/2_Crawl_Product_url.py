"""
Created on 2016年10月11日
change:2021-11-11
Crawl product url.

Entrence: the 1st layer of categories.
@author: dsc
"""

import queue
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sys
exitFlag = 0


# MyThread 继承自 python 自带的 threading
class MyThread(threading.Thread):
    def __init__(self, thread_id, name, queue):
        print("ID:", thread_id, "Name:", name, "Queue:", queue)
        # 调用父类的初始化方法
        super(MyThread, self).__init__()
        self.threadID = thread_id
        self.name = name
        self.queue = queue

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.queue)
        print("退出线程：" + self.name)


def process_data(thread_name, queue):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = queue.get()
            queueLock.release()
            print("%s processing %s" % (thread_name, data))
            crawl(data)
        else:
            queueLock.release()
        time.sleep(1)


def write_page_url(driver, product_url_txt):
    # product_list = driver.find_elements_by_xpath("//a[@class='product product-link ']")
    product_list = driver.find_elements_by_xpath("//a[@class='_3TqU78D']")
    for ele_product_list in product_list:
        # product_url_txt.write
        #         print(ele_product_list.get_attribute("href"))
        product_url_txt.write(ele_product_list.get_attribute("href") + "\n")


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


# start of the main function, the input is the category page url

def crawl(page_url):
    #     driver = webdriver.PhantomJS()
    driver = webdriver.Chrome()
    driver.get(page_url)
    #     try:
    #         button_close = driver.find_element_by_xpath("//input[@id='btnClose']")
    #         button_close.click()
    #     except:
    #         print("error")
    # 换成每页显示204项
    #     try:
    #         change_view = driver.find_element_by_xpath("//a[@class='change-view']")
    #         change_view.click()
    #     except:
    #         print("unclickable")
    #     WebDriverWait(driver, 5)
    # 换成每页显示204项
    write_page_url(driver, product_url_txt)

    page_number = 1
    while True:
        page_string = '&page=' + str(page_number) + '&pgesize=204'
        driver.get(page_url + page_string)

        if check_exists_by_xpath(driver, "//a[@class='change-view']"):
            write_page_url(driver, product_url_txt)
        else:
            break

        if check_exists_by_xpath(driver, "//div[@class='alert-content']"):
            driver.implicitly_wait(10)

        page_number += 1
    # quit the driver
    driver.quit()


if __name__ == '__main__':
    # 先清空 txt
    product_url_txt = open('./product_url_women.txt', 'w').close()
    product_url_txt = open('./product_url_women.txt', 'a')
    # print(os.path.abspath)
    path = 'D:\\Machine_Learning_note\\DM'
    file = open(path+"\\asos_category_url.txt")
    # url = 'http://www.hm.com/hk/en/product/54618?article=54618-B&pge=1/&pgesize=204'
    lines = file.readlines()
    file.close()

    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8",
                  "Thread-9", "Thread-10"]
    nameList = lines
    queueLock = threading.Lock()
    workQueue = queue.Queue(len(nameList) + len(threadList))
    threads = []
    threadID = 1

    # 创建新线程
    for tName in range(len(threadList)):
        thread = MyThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for word in nameList:
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")

    product_url_txt.close()
