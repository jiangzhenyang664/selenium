# -*- codeing = utf-8 -*-
# @Time : 2021/1/9 20:39
# @Author : jzy
# @File : qixin.py
# @Software : PyCharm
from selenium import webdriver
import time
from lxml import etree
import csv
import logging


def save_data(parse_html):
    tb_list = parse_html.xpath('//*[@id="courtNotice"]/table/tbody/tr')
    for tr in tb_list:
        # 捕获少量数据结构不同的数据（缺少数据项）
        number = (tr.xpath('./td[1]/text()'))[0]
        try:
            law_date = (tr.xpath('./td[2]/text()'))[0]
            reason = (tr.xpath('./td[3]/text()'))[0]
            identity = (tr.xpath('./td[4]/text()'))[0]
            content1 = ((tr.xpath('./td[5]//text()'))[0]).replace('\xa0\xa0','')
            content2 = (tr.xpath('./td[5]//text()'))[1]
            content3 = ((tr.xpath('./td[5]//text()'))[2]).replace('\xa0\xa0','')
            content4 = (tr.xpath('./td[5]//text()'))[3]
            content5 = (tr.xpath('./td[5]//text()'))[5]

            content_complainant = content1 + content2
            content_defendant = content3 +content4 +content5
            with open('qixind_ata.csv', 'a+', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([number, law_date, reason, identity, content_complainant+'\\n'+content_defendant])
                f.close()
        except IndexError:
            logger.info('序号为 %s 的信息捕获失败.' % number)
            fail.append(number)
            continue


def get_html(driver):
    html = driver.page_source
    return etree.HTML(html)


if __name__ == '__main__' :
    # 配制日志文件
    logger = logging.getLogger("jzy")
    LOG_FORMAT = "%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s"
    DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
    logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)


    # 页面验证框css属性值
    submit_message1 = ['modal fade app-geetest-dialog in']

    # 每次验证之后页面div数量多一个，记录验证次数，首次是7
    i = 7

    # 数组定义用来存储捕获失败的序号,程序捕获不到第二页和第三页的数据
    fail = [6,7,8,9,10,11,12,13,14,15]

    # 浏览器设置
    driver = webdriver.Chrome()
    driver.get('https://www.qixin.com/risk/9088b55b-7217-40b4-9bd7-9719fe347b81')
    driver.maximize_window()
    driver.execute_script('window.scrollTo(0,3000)')

    # 准备文件
    with open('qixin_data.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '开庭日期', '案由', '身份', '当事人'])
        f.close()

    # 获取第一页数据
    parse_html = get_html(driver)
    save_data(parse_html)

    # 获取第4页及后面的数据
    for x in range(2700):
        element = driver.find_element_by_xpath('//*[@id="courtNotice"]/div[2]/div[2]/nav/ul/li[5]/a')
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        parse_html = get_html(driver)
        try:
            print((parse_html.xpath('/html/body/div['+str(i)+']/@class'))[0])
            while (parse_html.xpath('/html/body/div[7]/@class'))[0] == submit_message1[0]:
                 logger.info('需手动介入验证，或采用商业超级鹰自动验证')
                 time.sleep(60)
                 parse_html = get_html(driver)
            i += 1
            save_data(parse_html)
        except IndexError:
            save_data(parse_html)
    # 控制台输出捕获失败的序号
    print(fail)


