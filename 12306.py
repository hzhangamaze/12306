from splinter.browser import Browser
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import traceback

areatocode = {"上海": "SHH", "北京": "BJP", "南京": "NJH", "昆山": "KSH", "杭州": "HZH", "桂林": "GLZ"}

#席别
seat_type_dic={'1':'硬座','2':'软座','3':'硬卧','4':'软卧','6':'高级软卧','F':'动卧','0':'二等座','M':'一等座','9':'商务座/特等座'}
seat_type_list=['1-硬座','2-软座','3-硬卧','4-软卧','6-高级软卧','F-动卧','0-二等座','M-一等座','9-商务座/特等座']
# 城市cookie字典
city_list = {
    '北京': '%u5317%u4EAC%2CBJP',  # 北京
    '上海': '%u4E0A%u6D77%2CSHH',
    '天津': '%u5929%u6D25%2CTJP',
    '南宁': '%u5357%u5B81%2CNNZ',  # 南宁
    '武汉': '%u6B66%u6C49%2CWHN',  # 武汉
    '长沙': '%u957F%u6C99%2CCSQ',  # 长沙
    '太原': '%u592A%u539F%2CTYV',  # 太原
    '运城': '%u8FD0%u57CE%2CYNV',  # 运城
    '广州南': '%u5E7F%u5DDE%u5357%2CIZQ',  # 广州南
    '梧州南': '%u68A7%u5DDE%u5357%2CWBZ',  # 梧州南

    }


class Buy_Tickets(object):
    # 定义实例属性，初始化
    def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
        self.username = username
        self.passwd = passwd
        # 车次，0代表所有车次，依次从上到下，1代表所有车次，依次类推
        self.order = order
        # 乘客名
        self.passengers = passengers
        # 起始地和终点
        self.starts = starts
        self.ends = ends
        # 日期
        self.dtime = dtime
        # self.xb = xb
        # self.pz = pz
        self.login_url = 'https://kyfw.12306.cn/otn/login/init'
        self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.submitorder_url='https://kyfw.12306.cn/otn/confirmPassenger/initDc'
        self.driver_name = 'firefox'###
        self.executable_path = 'D:\selenium\geckodriver.exe'###

    # 登录功能实现
    def login(self):
        self.driver.visit(self.login_url)
        self.driver.fill('loginUserDTO.user_name', self.username)
        # sleep(1)
        self.driver.fill('userDTO.password', self.passwd)
        # sleep(1)
        print('请输入验证码...')
        while True:
            if self.driver.url != self.initMy_url:
                sleep(1)
            else:
                break

    # 买票功能实现
    def start_buy(self):
        self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
        # 窗口大小的操作
        self.driver.driver.maximize_window()
        self.login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始购票...')
            sleep(1)
            # 加载查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.starts})
            self.driver.cookies.add({"_jc_save_toStation": self.ends})
            self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
            self.driver.reload()
            count = 0
            if self.order != 0:
                while self.driver.url == self.ticket_url:
                    print(str(type(self.driver.find_by_text('查询').value))+self.driver.find_by_text('查询').value)
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        if self.driver.find_by_text(train_number[0]):
                            train_number_info=self.driver.find_by_text(train_number[0])
                            print(type(train_number_info))
                            print(type(train_number_info.html))
                            print(str(train_number_info))
                            print(train_number_info.html)
                            print(train_number_info.first['id'])
                            sleep(2)

                        self.driver.find_by_text('预订')[self.order - 1].click()
                        sleep(3)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            else:
                while self.driver.url == self.ticket_url:
                    self.driver.find_by_text('查询').click()
                    count += 1
                    print('第%d次点击查询...' % count)
                    try:
                        for i in self.driver.find_by_text('预订'):
                            i.click()
                            sleep(1)
                    except Exception as e:
                        print(e)
                        print('预订失败...')
                        continue
            print('开始预订...')
            sleep(1)
            print('开始选择用户...')#学生票的问题还没解决
            #sleep(5)
            '''
            self.driver.find_by_id('normalPassenger_0').last.click()
            if self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id'):
                self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id').click()
            '''
            for j in range(0,len(passengers)):
                print(passengers[0])
                print(str(passengers[0] + '(学生)'))
                self.driver.find_by_id('quickQueryPassenger_id').click()
                self.driver.find_by_id('quickQueryPassenger_id').fill(str(passengers[0]))
                #print('id's type:'+self.driver.find_by_id('submit_quickQueryPassenger').value)
                self.driver.find_by_id('submit_quickQueryPassenger').click()

                # 选择坐席
                print("type(find_by_xpath...):"
                      +str(type(self.driver.find_by_xpath('//select[@id="%s"]/option[@value="%s"]'
                                                     %("seatType_"+str(j+1), seat_type[j])))))
                #<class 'splinter.element_list.ElementList'>是一个列表
                # (List of elements. Each member of the list is (usually) an instance of ElementAPI)

                self.driver.find_by_xpath(
                   '//select[@id="%s"]/option[@value="%s"]'%("seatType_"+str(j+1), seat_type[j])).click()
                # self.driver.find_by_xpath('//select[@id="seatType_1"]/option[@value="1"]')._element.click()    #ok
                #self.driver.find_by_xpath(
                #    '//select[@id="%s"]/option[@value="%s"]'%("seatType_"+str(j1+1),seat_type[j1])).first.click()   #ok
                #self.driver.driver.find_element_by_id('seatType_1').click()   #ok
                #self.driver.driver.find_element_by_id('seatType_1').select_by_value("1")  #no

                '''
                selects=self.driver.find_by_tag('select')
                selects[0].select("1")
                print('selected!')
                #'ElementList' object has no attribute '_element'  ???
                '''

                for i in range(0, 10):
                    #选择乘客，与坐席一一对应
                    if self.driver.find_by_id(str('normalPassenger_'+str(i))):
                        self.driver.find_by_id('normalPassenger_'+str(i)).click()
                        if self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id'):
                            self.driver.find_by_id('qd_closeDefaultWarningWindowDialog_id').click()
                        else:
                            self.driver.find_by_id('dialog_xsertcj_ok').click()
                        i=10

                #在学生票购买时段却不想买学生票的问题未解决
                sleep(0.5)


            sleep(2)
            print('提交订单...')
            # sleep(1)
            # self.driver.find_by_text(self.pz).click()
            # sleep(1)
            # self.driver.find_by_text(self.xb).click()
            # sleep(1)
            element=self.driver.find_by_id('submitOrder_id')
            print('type(find_by_id...):'+str(type(element)))
            self.driver.find_by_id('submitOrder_id').click()  # ==element.click()
            sleep(2)
            print('确认选座...')
            element=self.driver.find_by_id('qr_submit_id')
            element.click()
            print('预订成功...')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    # 用户名
    username = '18810655751'
    # 密码
    password = 'zhh19010101'
    # 车次选择，0代表所有车次
    order = 1
    # 乘客名，比如passengers = ['丁小红', '丁小明']
    passengers = ['张虎']
    print(seat_type_list)
    seat_type=['1']
    # 日期，格式为：'2018-01-20'
    dtime = '2018-11-11'
    # 出发地(需填写cookie值)
    starts = "北京"
    starts=city_list[starts]
    # 目的地(需填写cookie值)
    ends = "天津"
    ends = city_list[ends]

    train_number=['C2201']

    # xb =['硬座座']
    # pz=['成人票']

    Buy_Tickets(username, password, order, passengers, dtime, starts, ends).start_buy()
