class DeviceInfo:
    def __init__(self, name: str = '', udid: str = '', version: str = ''):
        '''
        Corresponding capability names:
        name     deviceName (mandatory)
        udid     udid
        version  platformVersion (9.0.0)
        '''
        self.device = name
        self.udid = udid
        self.version = version

    def copy(self):
        obj = DeviceInfo()
        for attr, value in self.__dict__.items():
            setattr(obj, attr, value)
        return obj

class AppiumParams:
    accepted_params = ('device', 'name', 'app', 'package', 'activity', 'browser')
    def __init__(self, **kwargs):
        '''
        Accepted params, data types, corresponding capability names:

        device   DeviceInfo (See DeviceInfo)
        name     str        applicationName (WiFi万能钥匙)
        app      str        app (apk file path)
        package  str        appPackage (com.snda.wifilocating)
        activity str        appActivity (com.lantern.launcher.ui.MainActivity)
        browser  str        browserName (Chrome)
        '''
        device = kwargs['device']
        self.deviceInfo = device
        self.device = device.device
        self.udid = device.udid
        self.version = device.version
        
        self.app = kwargs.get('app', '')
        self.name = kwargs.get('name', '')
        self.package = kwargs.get('package', '')
        self.activity = kwargs.get('activity', '')
        self.browser = kwargs.get('browser', '')

    def copy(self):
        obj = AppiumParams(device = self.deviceInfo.copy())
        for attr, value in self.__dict__.items():
            setattr(obj, attr, value)
        return obj

    @property
    def caps(self):
        caps = {
            "automationName": "uiautomator2",
            "platformName": "ANDROID",
            # Don’t reset app state between sessions
            # IOS: don’t delete app plist files;
            # Android: don’t uninstall app before new session
            "noReset": True,
            # Enable Unicode input
            "unicodeKeyboard": True,
            # Reset keyboard to its original state, after running Unicode tests with unicodeKeyboard capability
            "resetKeyboard": True,
            "deviceName": self.device,
            "newCommandTimeout": 300
        }
        if self.udid:
            caps['udid'] = self.udid
        if self.version:
            caps['platformVersion'] = self.version
        if self.activity and self.package:
            caps.update({
                "appPackage": self.package,  # "com.snda.wifilocating"
                "appActivity": self.activity,
            })
            if self.app:
                caps["app"] = self.app
                # Check if apk exists
                import os
                assert os.path.exists(self.app), "apk NOT FOUND."
            if 'oppo' in self.device.lower():
                del caps["unicodeKeyboard"], caps["resetKeyboard"]
        elif self.browser:
            caps["browserName"] = self.browser
        return caps