import os, platform
from common.data_classes import *

SUCCESS = 'Success'
FAIL = 'Fail'
INSTALL_SPECIAL_DEVICES = ["OPPO A59m", "OPPO A37m", "OPPO R9 Plustm A", "OPPO R9 Plusm A", "OPPO R9m", "OPPO R9tm",
                           "OPPO R7sPlus", "UOOGOU", "MEIZU m3 note", "Xiaomi MI 3C", "MEIZU m1 note", "Xiaomi MI4LTE New", "Xiaomi 3", "Xiaomi 4C", "Xiaomi Redmi 3S"]

# Variables For Configurating Webdriver

# Device for testing
deviceInfo = DeviceInfo(
    name = 'Lenovo OnePlus 7 Pro',
    udid = '04a07da9',
    version = '9'
)
# deviceInfo = DeviceInfo(
#     name = 'Lenovo OnePlus 6',
#     udid = '72f2b00a',
#     version = '9'
# )
# deviceInfo = DeviceInfo(
#     name = 'Samsung',
#     udid = '988995373649413853',
#     version = '9'
# )
appium_host = '0.0.0.0'
appium_port = 4723

# WiFi万能钥匙
KeyParams = AppiumParams(
    device = deviceInfo,
    app = '/Users/luoht/Desktop/appium_test/apps/WiFiwannengyaochi_190918.apk',
    package = 'com.snda.wifilocating',
    activity = 'com.lantern.launcher.ui.MainActivity',
)
# WiFi万能钥匙浏览器
BrowserParams = AppiumParams(
    device = deviceInfo,
    app = '/Users/luoht/Desktop/appium_test/apps/WifiKeyBrowser-Guanwang.apk',
    package = 'com.link.browser.app',
    activity = 'com.linksure.browser.activity.SplashActivity',
)

### Locations
sys_username = 'test'
operating_system = platform.system()
if operating_system == "Linux": #Ubuntu
    HOME_DIR = '/home/test'
elif operating_system == "Darwin": #Mac
    HOME_DIR = os.path.expanduser('~')
    sys_username = HOME_DIR[7:-1] # /Users/
elif operating_system == "Windows": #Windows
    HOME_DIR = 'C:/automation'
else:
    HOME_DIR = '/home/test/'

ROOT_FOLDER = os.path.dirname(os.path.dirname(__file__))
if platform.system() == "Linux": # Ubuntu
    ADB_PATH = '/home/test/android-sdk-linux/platform-tools/adb'
elif platform.system() == "Darwin": # Mac
    ADB_PATH = '~/Library/Android/sdk/platform-tools/adb'
else:
    #现在的Server是Ubuntu，如果想要用Windows作为hub，需要单独安装上SSH或者Telnet 服务。所以暂时Windows只会作为调试使用。
    ADB_PATH = 'adb'
SSH_ADB_PATH = '/home/test/android-sdk-linux/platform-tools/adb'

### Commands
cmd_start_appium = ''

### BottomNavigationView
BOTTOM_NAVIGATIONVIEW_TAB_TEXTS = [['连接'], ['小程序'], ['我的', '未登录']]

### My
MY_ICONS_WITHOUT_NETWORK = []
MY_TEXTS_WITHOUT_NETWORK = ['连尚钱包', 'WIFI安全险', '下载管理', '热点分享', '取消热点分享', '帮助与反馈']


MY_ICONS_PATH = os.path.join(ROOT_FOLDER, 'test_my/icon_screenshots')
if not os.path.exists(MY_ICONS_PATH):
    os.makedirs(MY_ICONS_PATH)
MY_TEXTS_WITH_NETWORK = ['有好货商城', '免费流量', 'WiFi安全险', '连尚读书', '连尚钱包', '找工作', '找房子', '星星最新版', \
                         '梦想钥匙', '极速上网', '热点分享', '取消热点分享', '缓存清理', '帮助与反馈']
