import os, sys, traceback, inspect
import random, time, subprocess, platform, json, csv, shutil, re, threading
import mysql.connector
import numpy as np
from PIL import Image, ImageFont, ImageDraw

import smtplib  
from email.header import Header  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
from datetime import datetime

from elasticsearch import Elasticsearch
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from uiautomator import Device, AutomatorServer

from common.constants import *
from common import _global, helper
from common import sql_helper as sh

result_queue = []

#############################################################
######    Find Elements
#############################################################

def find_elements(driver, id_):
    '''
    Only supports id, xpath, class_name and android_uiautomator
    @params:
        driver: a webdriver object
        id_: can be any of the id, xpath, class_name and android_uiautomator
    @returns:
        a list of found elements
    '''
    # __handle_system_dialogs(driver)
    if ':id/' in id_:
        return driver.find_elements_by_id(id_)
    elif id_.startswith('android.widget'):
        return driver.find_elements_by_class_name(id_)
    elif id_.startswith('new '):
        return driver.find_elements_by_android_uiautomator(id_)
    else: # elif id_.startswith('//android.widget') or id_.startswith('//*[contains'):
        return driver.find_elements_by_xpath(id_)

def find_element(driver, id_: str, index: int = 0):
    '''
    This function calls find_elements and returns the indexed element from it.
    @params:
        driver: a webdriver object
        id_ (str): can be any of the id, xpath, class_name and android_uiautomator
        index (int): the index of element found, default is 0
    @returns:
        the indexed element if found, otherwise False
    '''
    elements = find_elements(driver, id_)
    return elements[index] if elements else False

def find_and_do(driver, id_: str, operation, index: int = 0):
    '''
    Find the indexed element and do an operation on it.
    @returns:
        True if element is found otherwise False
    '''
    try:
        elements = find_elements(driver, id_)
        if elements:
            operation(elements[index])
            return True
        return False
    except:
        return False

def click(driver, id_: str, index: int = 0):
    '''Find the indexed element and click it.'''
    return find_and_do(driver, id_, lambda x: x.click(), index)

def set_text(driver, id_: str, text: str, index: int = 0):
    '''Find the indexed element and set its text.'''
    return find_and_do(driver, id_, lambda x: x.set_text(text), index)

def get_text(driver, id_: str, index: int = 0):
    '''
    Find the indexed element and return its text. If not found, return ''.
    '''
    element = find_element(driver, id_, index)
    return element.text if element else ''

def get_attribute(driver, id_: str, attribute: str, index: int = 0):
    '''Find the indexed element and get its attribute.'''
    element = find_element(driver, id_, index)
    return element.get_attribute(attribute) if element else None

def is_selected(driver, id_: str, index: int = 0):
    '''Find if the indexed element has the attribute 'selected' equal to true.'''
    return get_attribute(driver, id_, 'selected', index) == 'true'

def is_checked(driver, id_: str, index: int = 0):
    '''Find if the indexed element has the attribute 'checked' equal to true.'''
    return get_attribute(driver, id_, 'checked', index) == 'true'

#############################################################
######    SWIPE
#############################################################

def __swipe(driver, fromX, fromY, toX, toY):
    size = driver.get_window_size()
    width = size['width']
    height = size['height']
    try:
        driver.swipe(width * fromX, height * fromY, width * toX, height * toY, 600)
    except (NoSuchElementException, TimeoutException, WebDriverException) as e:
        print(traceback.format_exc())

def swipe_left(driver):
    __swipe(driver, 7/8, 1/2, 1/8, 1/2)
    
def swipe_right(driver):
    __swipe(driver, 1/8, 1/2, 7/8, 1/2)
    
def swipe_up(driver):
    __swipe(driver, 1/2, 3/4, 1/2, 2/5)

def swipe_down(driver):
    __swipe(driver, 1/2, 1/4, 1/2, 3/5)

#############################################################
######  WiFiKey Switch tab
#############################################################

def __switch_to_tab(driver, name: str, index: int):
    '''
    @params:
        driver: a webdriver object
        index: the index of tab
        name: the name of the tab
    @returns:
        return True if switch is successful otherwise False
    '''
    driver.implicitly_wait(3)
    tab_image = 'com.snda.wifilocating:id/tab_image'
    for i in range(1, 4):
        if click(driver, tab_image, index):
            if is_selected(driver, tab_image, index):
                break
        else:
            print("未发现底部导航栏")
            driver.launch_app()
            time.sleep(2)
            driver.back()
            driver.back()
            click(driver, 'com.snda.wifilocating:id/button1')
            print(f'切换到{name}tab失败（第{i}次尝试）！！！', file=sys.stderr, flush=True)
    driver.implicitly_wait(3)

def __switch_to_tab_backup(driver, name: str):
    driver.implicitly_wait(5)
    xpath = _global.ELEMENT[name]
    for i in range(1, 4):
        try:
            # 有时会跳到feed页某tab上或某条新闻里，检查是否有tab，没有就back一下
            if not find_element(driver, xpath):
                driver.back()
                driver.back()
                click(driver, 'com.snda.wifilocating:id/button2')
                click(driver, xpath)
                time.sleep(2)
            if is_selected(driver, xpath) or click(driver, xpath) and is_selected(driver, xpath):
                break
            print(f'切换到{name}tab失败（第{i}次尝试）！！！', file=sys.stderr, flush=True)
        except (NoSuchElementException, TimeoutException, WebDriverException):
            print(traceback.format_exc())
            print(f'{name}tab没有找到（第{i}次尝试）！！！', file=sys.stderr, flush=True)

def switch_to_connect_tab(driver):
    __switch_to_tab(driver, '连接', 0)

def switch_to_connect_tab_backup(driver):
    __switch_to_tab_backup(driver, '连接')

def switch_to_applets_tab(driver):
    __switch_to_tab(driver, '小程序', 1)

def switch_to_applets_tab_backup(driver):
    __switch_to_tab_backup(driver, '小程序')

def switch_to_my_tab(driver):
    __switch_to_tab(driver, '我的', 2) or \
    click(driver, "//android.widget.TextView[contains(@text,'未登录')]") or \
    click(driver, "//android.widget.TextView[contains(@text,'我的')]")

def switch_to_my_tab_backup(driver):
    __switch_to_tab_backup(driver, '我的')

#############################################################
######    General methods
#############################################################

#根据设备配置文件, 获得adb路径
def get_adb_path(info = deviceInfo):
    if platform.system() == "Linux": # Ubuntu
        adb_path = f"/home/test/android-sdk-linux/platform-tools/adb -s {info.udid}"
    else: # Mac
        adb_path = f"~/Library/Android/sdk/platform-tools/adb -s {info.udid}"
    return adb_path

def close_dialogs(driver):
    '''
    Close any dialogs when WiFiKey is launching.
    '''
    time.sleep(6)  # 开屏页5秒
    if click(driver, 'com.snda.wifilocating:id/btn_startuse'): # 立即体验
        click(driver, 'com.snda.wifilocating:id/button1') # 同意并继续
    time.sleep(0.5)
    if click(driver, 'com.snda.wifilocating:id/tv_perm_add'): # 我知道了
        for _ in range(3): # 点击三次权限授予
            if not click(driver, 'com.android.packageinstaller:id/permission_allow_button'): # 始终允许
                break
    # 关闭弹窗广告
    time.sleep(1)
    close_button_id = 'com.snda.wifilocating:id/pop_count_layout'
    if find_element(driver, close_button_id):
        while True:
            click(driver, close_button_id)
            time.sleep(1)
            if not find_element(driver, close_button_id):
                break

#对于特殊的设备,开启安装的进程后,再开启监控进程
def install_apk(apk_path: str, info: DeviceInfo):
    try:
        if info.device in INSTALL_SPECIAL_DEVICES or "vivo" in info.device:
            #后续可以考虑在device.json中添加字段, 区别安装过程中需要系统提示的设备
            for i in range(1, 4):
                print(f"第{i}次尝试安装", file=sys.stderr, flush=True)
                threads = [
                    threading.Thread(target=install_apk_override, args=(apk_path, info)),
                    threading.Thread(target=install_monitor, args=(apk_path, info, 60))
                ]
                for t in threads:
                    t.setDaemon(True)
                    t.start()
                t.join()
                
                copy = result_queue[:]
                result_queue.clear()
                if any(res[0] == SUCCESS for res in copy):
                    print(f"第{i}次尝试安装成功", file=sys.stderr, flush=True)
                    return SUCCESS
                time.sleep(10)
            return FAIL
        else:
            return install_apk_override(apk_path, info)
    except:
        print(traceback.format_exc())

#覆盖安装apk
#appium调用install_app时会先uninstall，导致万能钥匙app退出登录。所以只能直接用 adb install -r -d 来覆盖安装
def install_apk_override(apk_path: str, info: DeviceInfo):
    cmd = f'{get_adb_path(info)} install -r -d {apk_path}'
    print("##### adb install -r -d #####")
    print(cmd, file=sys.stderr, flush=True)
    
    # sleep randomly to avoid failure of installing apk to lots of devices at the same time
    # time.sleep(random.randint(1, 15))
    install_result = ""
    try:
        p = subprocess.Popen(cmd, shell=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        response_out = []
        while True:
            line = p.stdout.readline().strip()
            if line:
                line = line.decode('utf-8')
                print(line)
                response_out.append(line)
            elif p.poll() != None:
                break
        install_result = response_out[-1]
        print(f"install_result={install_result}")
    except subprocess.CalledProcessError as ex: # error code != 0 
        print("--------error------")
        print(ex.cmd)
        print(ex.returncode)
        print(ex.output) # contains stdout and stderr
    finally:
        result = install_result or '-'
        if info.device in INSTALL_SPECIAL_DEVICES or "vivo" in info.device:
            result_queue.append((result, sys._getframe().f_code.co_name))
        else:
            return result

#监控安装过程中的系统弹框
def install_monitor(apk_path, info: DeviceInfo, nub):
    print("Start install monitor", file=sys.stderr, flush=True)
    time.sleep(5)

    for _ in range(nub):
        d = Device(info.udid)
        el1 = d(text="安装")
        el2 = d(text="确定")
        el3 = d(text="继续安装")
        el4 = d(text="替换")
        el5 = d(text="安装失败")
        el6 = d(resourceId="com.oppo.market:id/fn") # 部分OPPO手机获取不到text"安装",使用ID
        el7 = d(text="安装完成") # 部分OPPO手机安装完成后,会有"安装完成"的提示
        el8 = d(resourceId="android:id/button1") # Vivo 手机对第三方应用有额外的安全警告, 10秒内默认取消
        el9 = d(text="继续安装")
        el10 = d(resourceId="com.android.packageinstaller:id/password") # OPPO R7s Plus 需要OPPO帐号密码
        el12 = d(text="继续安装旧版本")
        el13 = d(text="允许")
        if el1.exists:
            el1.click() 
        if el2.exists:
            el2.click()
        if el3.exists:
            el3.click()
        if el4.exists:
            el4.click()
        if el5.exists: #OPPO 手机有时候adb install安装会失败,使用adb shell pm install
            try:
                print("Trying pm install", file=sys.stdout, flush=True)
                adb_path = get_adb_path()
                subprocess.Popen(f"{adb_path} push {apk_path} /sdcard/Download", stdout=subprocess.PIPE, shell=True)
                print("Copied apk to sdcard/Download")
                print("Installing via pm", file=sys.stdout, flush=True)
                cmd = f"{adb_path} shell pm install -r -d /sdcard/Download/{os.path.basename(apk_path)}"
                pm_install = subprocess.Popen(cmd)
                data = pm_install.stdout.read()
                print(str(data))
            except:
                print(traceback.format_exc())
        if el6.exists:
            el6.click()
        if el7.exists:
            print("Install finished", file=sys.stdout, flush=True)
            result_queue.append((SUCCESS, sys._getframe().f_code.co_name))
            break
        if el8.exists:
            el8.click()
        if el9.exists:
            el9.click()
        if el10.exists:
            el10.set_text('15961898630')
            time.sleep(2)
            el11 = d(text="确定安装")
            if el11.exists:
                el11.click()
        if el12.exists:
            el12.click()
        if el13.exists:
            el13.click()
        time.sleep(1)
        #ds.stop()

    cmd_getpid = f"ps -ef | grep {info.udid} | grep uiautomator | " + "awk '{print $2}'"
    p = subprocess.Popen(cmd_getpid, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    out, err = p.communicate()
    uiautomator_script_pid = out.strip().decode('utf-8')
    list_uiautomator_pid = uiautomator_script_pid.split('\n')
    cmd_kill = "kill -9 " + ' '.join(list_uiautomator_pid)
      
    print(cmd_kill, file=sys.stderr, flush=True)
    subprocess.Popen(cmd_kill, shell=True)
    
    print("Install monitor finished", file=sys.stdout, flush=True)
    
def unlock_device():
    adb = get_adb_path()
    cmd_unlock = adb + " shell am start -n io.appium.unlock/.Unlock && sleep 3"
    subprocess.Popen(cmd_unlock, shell=True)

    cmd_input = adb + " shell input keyevent 3 && sleep 3"
    subprocess.Popen(cmd_input, shell=True)