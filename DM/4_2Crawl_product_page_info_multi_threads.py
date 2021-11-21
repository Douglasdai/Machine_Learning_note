# -*- coding: utf-8 -*-

import os
import queue
import re
import time
import urllib.request
import threading

from selenium import webdriver

ISOTIMEFORMAT = '%Y-%m-%d %X'  # Time setup

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开启线程：" + self.name)
        process_data(self.name, self.q)
        print("退出线程：" + self.name)


def process_data(thread_name, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()
            print("%s processing %s" % (thread_name, data))
            try:
                craw_product_contents(data)
            except:
                print('Error', data)
        else:
            queueLock.release()
        time.sleep(1)


def saveImgs(driver, img_path, img_url_list):
    img_num = 0
    if not os.path.exists(img_path):  # 判断文件是否存在，返回布尔值
        os.makedirs(img_path)

    while img_num < len(img_url_list):
        image_url = img_url_list[img_num]
        save_path = img_path + str(img_num) + '.jpg'

        # 换种方式保存图片
        img_data = urllib.request.urlopen(image_url).read()
        image_file = open(save_path, "wb")
        image_file.write(img_data)
        image_file.close()

        # urlretrieve(image_url, save_path)
        img_num = img_num + 1
    return img_num


def craw_product_contents(product_url):
    product_info_list = []
    driver = webdriver.Chrome()
    driver.get(product_url)
    #change the local country choose the HKD as the currency
    # country_element = driver.find_element_by_xpath("//button[@class='w9hgW1d _19PGtzt']")
    # driver.implicitly_wait(5)
    # country_element.click()
    #
    # country_element = driver.find_element_by_xpath("//select[@id='country']/option[@value='CN']")
    # driver.implicitly_wait(5)
    # country_element.click()
    #
    # save_country_button = driver.find_element_by_xpath("//button[@data-testid='save-country-button']")
    # save_country_button.click()
    # time.sleep(10)
    # print('change currency √')

    # re 是 python 自带的正则表达式包
    url_product_id = re.findall(r'[0-9]{7}', product_url)[0]
    product_info_list.append(url_product_id)

    # show more
    show_more = driver.find_element_by_xpath("//a[@class='show']")
    if show_more.is_enabled():
        show_more.click()

    # breadcrumb
    breadcrumb = ''
    breadcrumb_eles = driver.find_elements_by_xpath("//div[@class='_2xLfY']/ul/li")
    for breadcrumb_ele in breadcrumb_eles:
        breadcrumb = breadcrumb + breadcrumb_ele.text + '/'
    breadcrumb = breadcrumb.strip('/')
    product_info_list.append(breadcrumb)

    # product URL
    product_info_list.append(product_url)

    # URL state is 1
    product_url_stat = 1
    product_info_list.append(product_url_stat)

    # product code
    product_code = ''
    product_code = driver.find_element_by_xpath("//div[@class='product-code']/p").text
    product_info_list.append(product_code)

    # product website
    product_website = 'http://www.asos.com/'
    product_info_list.append(product_website)

    # product gender
    gender = 0
    if 'Men' in breadcrumb:
        gender = 1
    else:
        gender = 0
    product_info_list.append(gender)

    # product_brand
    product_brand = 'ASOS'
    product_info_list.append(product_brand)

    # product_craw_time 爬取产品时间
    product_craw_time = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))  # 获取当前时区时间格式 2016-08-02 21:46:38
    product_info_list.append(product_craw_time)

    # product title
    product_title = ''
    product_title = driver.find_element_by_xpath("//div[@class='product-hero']/h1").text
    product_info_list.append(product_title)
    print('product title √')

    # product delivery
    product_delivery = 'can not find delivery'
    # product delivery 是通过 JS 生成的，find_element_by_xpath 找不到它
    # product_delivery = driver.find_element_by_xpath("//a[@class='product-delivery']/span").text
    product_info_list.append(product_delivery)

    # product price
    product_price = 0
    # 通过 data-id 定位，以便兼容打折商品
    product_price = driver.find_element_by_xpath("//span[@data-id='current-price']").text
    product_info_list.append(product_price)
    print('product price √')

    # product description
    product_description = ''
    product_description = driver.find_element_by_xpath("//div[@class='product-description']/p").text.strip()
    # product about product material
    product_material = ''
    product_material = driver.find_element_by_xpath("//div[@class='about-me']/p").text.strip()
    product_description = product_material + ';;' + product_description
    product_info_list.append(product_description.strip(';;'))
    print('product description √')

    # product select size can be null
    size = ''
    product_size = driver.find_element_by_xpath("//div[@class='colour-size-select']").find_elements_by_xpath(
        "//select[@data-id='sizeSelect']/option")
    for ele in product_size:
        if 'Not' not in ele.text and 'Please' not in ele.text:
            size = size + ele.text + ';;'
    size = size.strip(';;')
    product_info_list.append(size)
    print('product size √')

    # product care INFO
    product_care = ''
    product_care = driver.find_element_by_xpath("//div[@class='care-info']/p").text.strip()
    product_info_list.append(product_care)

    # product colour
    product_colour = ''
    product_colour = driver.find_element_by_xpath("//span[@class='product-colour']").text
    product_info_list.append(product_colour)

    # threre are at most 3 right-arrow button, click it if it is clickable
    right_arrows = driver.find_elements_by_xpath("//a[@class='arrow right-arrow active']")
    if len(right_arrows) > 1:
        right_arrows[1].click()
        right_arrows[1].click()
        right_arrows[1].click()
        right_arrows[1].click()
    if len(right_arrows) > 2:
        right_arrows[2].click()
        right_arrows[2].click()
        right_arrows[2].click()
        right_arrows[2].click()

    # buy the look
    buy_the_look_list = ''
    # look_list = []
    # buy_the_look_componet = driver.find_element_by_xpath("//div[@class='component buy-the-look']")
    # buy_the_look = buy_the_look_componet.find_elements_by_xpath("//div[@class='btl-product-details']/a")
    # for ele in buy_the_look:
    #     if ele.get_attribute('href') is not None and 'complete' in ele.get_attribute('href'):
    #         if ele.get_attribute('href') not in look_list:
    #             look_list.append(ele.get_attribute('href'))
    # buy_the_look_list = ';;'.join(look_list)
    # product_info_list.append(buy_the_look_list)

    # you may also like
    you_may_also_like_list = ''
    like_list = []
    you_may_also_like_component = driver.find_element_by_xpath("//div[@class='_2xLfY']")
    you_may_also_like = you_may_also_like_component.find_elements_by_xpath("//ul[@class='_1DrUB']/li/div/a")

    for ele in you_may_also_like:
        if ele.get_attribute('href') is not None and 'recommend' in ele.get_attribute('href'):
            if ele.get_attribute('href') not in like_list:
                like_list.append(ele.get_attribute('href'))
    you_may_also_like_list = ';;'.join(like_list)
    product_info_list.append(you_may_also_like_list)
    print('product you may also like √')

    # product IMGs
    img_url_list = []
    ele_imgs = driver.find_elements_by_xpath("//img[@class='gallery-image']")
    for ele in ele_imgs:
        img_url_list.append(ele.get_attribute("src"))
    img_url_list = list(set(img_url_list))

    img_path = './Unclassified'
    # if len(breadcrumb) > 0:
    #     img_path = '/'.join(breadcrumb.split('/')[0:-1])

    img_number = saveImgs(driver, ROOTPATH + img_path + '/' + str(url_product_id) + "/", img_url_list)
    product_info_list.append(img_number)
    product_info_list.append(img_path + '/' + str(url_product_id) + "/")

    # save the info on file
    text_content = [repr(str(i)) for i in product_info_list]
    with open('D:/Machine_Learning_note/DM/text_content.txt', 'a', encoding='utf8') as f:
        f.write('\t'.join(text_content) + '\n')

    #     product_details_data = (url_product_id, breadcrumb, product_url, product_url_stat, product_code, product_website,
    #                             gender, product_brand, product_craw_time,
    #                             product_title, product_delivery, product_price, product_description, size,
    #                             product_care, product_colour, img_number, buy_the_look_list, you_may_also_like_list)
    driver.close()
    return product_info_list


#     cursor.execute(sql_update_content, product_data)
#     db.commit()#需要这一句才能保存到数据库中

if __name__ == '__main__':
    product_URLs = open("D:/Machine_Learning_note/DM/product_url.txt").readlines()
    ROOTPATH = "D:/Machine_Learning_note/DM/"

    #     db = pymysql.connect("localhost","root","123456","testdb", charset="utf8")
    #     cursor = db.cursor()
    #
    threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6", "Thread-7", "Thread-8",
                  "Thread-9", "Thread-10", "Thread-11", "Thread-12", "Thread-13", "Thread-14", "Thread-15", "Thread-16",
                  "Thread-17", "Thread-18", "Thread-19", "Thread-20"]

    queueLock = threading.Lock()
    workQueue = queue.Queue(len(product_URLs) + len(threadList))

    threads = []
    threadID = 1

    # 创建新线程
    for tName in range(len(threadList)):
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    for product_url in product_URLs:
        workQueue.put(product_url.strip('\n'))
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()

    print("退出主线程")
#     db.close()
