# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import HTMLTestRunner
#导入unittest包
import unittest, time, re

#SearchTest类继承自unittest.TestCase，表明这是一个测试案例
class TestCases(unittest.TestCase):
    #setUp用于初始化工作
    def setUp(self):
        self.option = webdriver.ChromeOptions()
        self.option.add_experimental_option("detach",True)
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.126.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def action(self,username,password):
        driver = self.driver
        driver.get(self.base_url)
        # 每个time.sleep的目的是等待页面完全加载，避免捕获不到元素而报错，数值可调，单位是秒，但不建议调节到3以下
        time.sleep(3)
        # 第一个坑，账号密码输入的地方为iframe，无法直接捕获到，得需要转移焦点到对应的iframe中，再捕获相应元素
        iframe = driver.find_elements_by_tag_name("iframe")[0]
        driver.switch_to_frame(iframe)
        email = driver.find_element_by_name('email')
        email.send_keys(username)
        driver.find_element_by_name("password").send_keys(password)
        driver.find_element_by_id("dologin").click()
        # 点击 写信 按钮。这个按钮不好找，网页为了防止自动化测试 把很多元素的id和class都动态设置，所以用了一个比较少用的css选择器
        time.sleep(3)
        goWrite = driver.find_elements_by_css_selector("li[role=\"button\"]")
        goWrite[1].click()
        # 设置邮件的收件人和title。这两个元素同样不好定位
        time.sleep(2)
        driver.find_elements_by_css_selector("input[role=\"combobox\"]")[0].send_keys("437515758@qq.com")
        driver.find_elements_by_class_name("nui-ipt-input")[2].send_keys("Title of the Letter")
        # 第二个坑，邮件正文部分 依然是iframe，同样需要转移
        driver.switch_to_frame(driver.find_element_by_class_name("APP-editor-iframe"))
        contentString = "Hello Python!"
        driver.find_element_by_tag_name("body").send_keys(contentString)
        # 第三个坑，发送 按钮在上层，还得需要下面第一句来实现从当前iframe中往上跳一层
        driver.switch_to_default_content()
        driver.find_element_by_xpath("//*[text()='发送']").click()
        # 等待邮件发送
        time.sleep(2)
        # pass

    #以test开头的是我们的测试脚本
    @staticmethod
    def getTestFunc(arg1,arg2):
        def func(self):
            print(arg1,arg2)
            self.action(arg1,arg2)
        return func

        

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    #在每个测试方法后执行，完成清理工作
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
def __generateTestCases():
    global test_data
    test_data = [
        {"username":"zzz2299", "password":"111111.a"},
        {"username":"zz3977", "password":"123456"},
        {"username":"zz3977", "password":"111111.a"},
        {"username":"zz3977", "password":"111111"},
        {"username":"wr17829", "password":"123456"},
    ]
    for data in test_data:
        arg1,arg2 = data['username'],data['password']
        # print(arg1,arg2)
        setattr(TestCases,
                'test_email_%s_%s' %(arg1,arg2[:6]),
                TestCases.getTestFunc(arg1,arg2))

__generateTestCases()
#整个测试过程集中在unittest的main()模块中，其默认执行以test开头的方法
if __name__ == "__main__":
    test_data = []
    suite = unittest.TestSuite()

    for data in test_data:
        arg1, arg2 = data['username'], data['password']
        print(arg1,arg2)
        suite.addTest(TestCases('test_email_%s_%s' %(arg1,arg2[:6])))
    with open('testreport.html', 'wb') as f:
        runner = HTMLTestRunner.HTMLTestRunner(stream=f,title='unittest用例标题',description='关于126邮箱的用例')
        runner.run(suite)
