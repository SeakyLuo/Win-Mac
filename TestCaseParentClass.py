import os, sys, unittest
import time, traceback, subprocess, json
import urllib.request
from common import utils, _global
from common import sql_helper as sh
from common.constants import *
from appium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException

# The Parent TestCase Class
class ParentTestCaseClass(unittest.TestCase):
    # The presence of this function is mandatory.
    def setUp(self):
        '''Setup for the test.'''
        self.params = KeyParams
        self.configWebdriver()
        utils.close_dialogs(self.driver)
            
    # The presence of this function is mandatory.
    def tearDown(self):
        '''Tear down the test.'''
        try:
            _global.img_list.clear()
            self.driver.quit()
        except (NoSuchElementException, TimeoutException, WebDriverException) as e:
            print(traceback.format_exc())
        
    def configWebdriver(self, desired_caps: dict = None):
        '''
        Configurate WebDriver.
        If desired_caps is None, a default one will be used.
        '''
        self.failures = [] # Record failed test message
        # Appium Desired Capabilities
        self.desired_caps = desired_caps or self.params.caps
        if not hasattr(self, 'host'): self.host = appium_host
        if not hasattr(self, 'port'): self.port = appium_port
        self.driver_url = f'http://{self.host}:{self.port}/wd/hub' # use individual appium server
        begin = time.time()
        try:
            print("desired_caps=", self.desired_caps)
            self.driver = webdriver.Remote(self.driver_url, self.desired_caps)
            print("appium server 第一次启动成功...")
        except:
            print("!!!第一次启动appium driver失败")
            print(traceback.format_exc())
            print("!!!开始Appium server状态检查...\n")
            appium_status_url = f'http://{self.host}:{self.port}/wd/hub/status'
            try:
                appium_status = json.loads(urllib.request.urlopen(appium_status_url).read().decode('utf-8'))
            except Exception as e:
                print(e)
                appium_status = {'status': -1}

            if appium_status['status'] != 0:
                print(f"appium server 状态异常，将要重启appium server，当前详细appium 状态: {appium_status}")
                self.restart_appium_server()
            else:
                self.driver_url = f'http://127.0.0.1:{self.port}/wd/hub'
            self.driver = webdriver.Remote(self.driver_url, self.desired_caps)
            print("appium server 第二次启动成功...")
        self.duration_startup = time.time() - begin

    def restart_appium_server(self):
        print("准备重启appium进程")
        print(_global.cmd_start_appium)
        if len(_global.cmd_start_appium) < 5:  # 内部调试时，不走run.py，未定义启动appium的命令
            _global.cmd_start_appium = f'{ROOT_FOLDER}/start_appium_by_device.sh --udid {self.udid} --port {self.port} --bp {self.port + 1} --taskid {_global.task_id}'
        appium_status_url = f'http://{self.host}:{self.port}/wd/hub/status'
        print(appium_status_url)
        for i in range(2):
            subprocess.Popen(_global.cmd_start_appium, shell=True, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(2)
            for j in range(_global.MAX_Lanuch_Appium_Time):
                time.sleep(2)
                try:
                    appium_status_res = json.loads(urllib.request.urlopen(appium_status_url).read().decode('utf-8'))
                    appium_status = appium_status_res["status"]
                    print(appium_status_res)
                    if appium_status == 0:
                        return True
                    break
                except:
                    pass
        return False

    def upload_startup_duration(self):
        @sh.execute_sql()
        def execute(conn, cursor):
            sql_update_job = ("UPDATE jobs SET duration_startup=%s WHERE id=%s")
            data_update_job = (self.duration_startup, _global.job_id)
            cursor.execute(sql_update_job, data_update_job)
            sql_str = cursor.statement
            print(sql_str, file=sys.stderr, flush=True)
            conn.commit()
        try:
            execute()
        except Exception:
            pass

    def printf(self):
        '''Print failure messages if any.'''
        if self.failures:
            self.fail('\n'.join(self.failures))

    @property
    def deviceInfo(self):
        return DeviceInfo(self.device, self.udid, self.version)

    @deviceInfo.setter
    def deviceInfo(self, value: DeviceInfo):
        self.device = value.device
        self.udid = value.udid
        self.version = value.version

    @property
    def params(self):
        params = self.__dict__
        for attr in AppiumParams.accepted_params:
            setattr(self.__params, attr, params[attr])
        return self.__params

    @params.setter
    def params(self, value: AppiumParams):
        self.__params = value
        # The commented code simplifies the assignment
        # but IDE will not recognize those properties,
        # Therefore manually assign them.
        # for attr, value in self.__dict__:
        #     setattr(self, attr, value)
        self.deviceInfo = value.deviceInfo
        self.app = value.app
        self.name = value.name
        self.package = value.package
        self.activity = value.activity
        self.browser = value.browser
