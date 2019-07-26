#coding: utf8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
def crawler():
    # 创建chrome浏览器驱动，无头模式
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--start-maximized");
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver",
                              chrome_options=chrome_options)

    # 加载界面
    driver.get("https://www.autohome.com.cn/car/")
    time.sleep(3)

    # 获取页面初始高度
    js = "return action=document.body.scrollHeight"
    height = driver.execute_script(js)

    # 将滚动条调整至页面底部
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)

    # 定义初始时间戳（秒）
    t1 = int(time.time())

    # 定义循环标识，用于终止while循环
    status = True

    # 重试次数
    num = 0

    while status:
        # 获取当前时间戳（秒）
        t2 = int(time.time())
        # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
        if t2 - t1 < 30:
            new_height = driver.execute_script(js)
            if new_height > height:
                time.sleep(1)
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                # 重置初始页面高度
                height = new_height
                # 重置初始时间戳，重新计时
                t1 = int(time.time())
        elif num < 3:  # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
            time.sleep(3)
            num = num + 1
        else:  # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
            print("滚动条已经处于页面最下方！")
            status = False
            # 滚动条调整至页面顶部
            driver.execute_script('window.scrollTo(0, 0)')
            break

    # 打印页面源码
    content = driver.page_source
    return content
if __name__ == '__main__':
    allline=crawler()
    '''f=open("all.txt","r",encoding="utf-8")
    allline=f.readlines()
    allline=' '.join(allline)'''
    res_tr = r"cname=\"(.* ?)\" style="
    car_brands = re.findall(res_tr,allline)
    allcar_brand={}
    f1=open("car_brand.dict","w",encoding="utf-8")
    for car_brand in car_brands:
        if( car_brand not in allcar_brand):
            allcar_brand[car_brand]=""
            f1.write(car_brand+"\n")
    res_tr = r"\">(.* ?)</a></h4>"
    cars = re.findall(res_tr,allline)
    all_car={}
    f2=open("car.dict","w",encoding="utf-8")
    for car in cars:
        if( len (car) <15 and car not in all_car):
            all_car[car]=""
            f2.write(car+'\n')




