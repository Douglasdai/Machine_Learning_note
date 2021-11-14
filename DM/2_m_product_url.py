import lxml.html
from selenium import webdriver
import time
from multiprocessing.dummy import Pool

driver = webdriver.Chrome(r'D:\\Machine_Learning_note\\DM\\chromedriver.exe')
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches",["enable-logging"])
option.add_argument('ignore-certificate-errors')


def get_product_url(i):
    basic_url = "https://www.asos.com/women/sale/dresses/cat/?cid=5235&ctaref=hp%7Cww%7Csale%7Ccarousel%7C1%7Ccategory%7Cdresses"
    append_url = '&page=' + str(i)
    driver.get(basic_url + append_url)
    time.sleep(5)

    selector = lxml.html.fromstring(driver.page_source)
    product_list = selector.xpath(
        r"/html/body/div[2]/div/main/div/div/div/div[2]/div/div[1]/section/article[contains(@id,'product-')]//a/@href")

    with open('D:\\Machine_Learning_note\\DM\\product_url_women.txt', 'a')as f:
        for product_url in product_list:
            f.write(product_url)
            f.write('\n')


if __name__ == '__main__':
    pool = Pool(10)
    print("线程池创建完毕")
    pool.map(get_product_url, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print("多线程爬取结束")