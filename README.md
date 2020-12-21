# unittest_126email
一、Python环境搭建（Windows）
1.安装Python
地址：https://www.python.org/downloads/
2.配置环境变量
“右键计算机-属性-高级系统设置-高级-环境变量-系统变量，path中增加python的路径”
检验：打开cmd命令，输入“python -V",显示版本号说明安装正常。
二、安装selenium
win+R，输入cmd，输入pip install selenium -i https://pypi.douban.com/simple/
三、安装浏览器驱动
1.Chromedriver
下载地址：http://npm.taobao.org/mirrors/chromedriver/
webdriver 和chrome版本要对应，避免出现浏览器闪退或者版本冲突等问题
浏览器版本查看方法：'右侧三点'-帮助-关于Google Chrome。目前最新版本为版本 87.0.4280.88（正式版本)
2.配置环境变量
将下载完成的Chrome driver解压得到 .exe 文件，将该文件放到谷歌的安装目录中，我的路径是在C:\Program Files\Google\Chrome\Application 这里。
这里提供一个查找自己浏览器安装路径的方法：首先找到桌面快捷方式，右键点击图标选择属性，复制‘目标’中的链接即为安装目录。
“右键计算机-属性-高级系统设置-高级-环境变量-系统变量，path中增加chromedriver的路径”
检验：win+R输入cmd命令，输入”chromedriver“，显示******ChromeDriver was started successfully.说明安装正常.
四、测试
from selenuim import webdriver 
import time  
driver = webdriver.Chrome()  
driver.get('http://www.baidu.com')  
time.sleep(3)  
driver.quit() 

