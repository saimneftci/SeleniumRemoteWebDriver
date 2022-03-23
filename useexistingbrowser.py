from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SessionRemote(webdriver.Remote):
    def start_session(self, desired_capabilities, browser_profile=None):
        # Skip the NEW_SESSION command issued by the original driver
        # and set only some required attributes
        self.w3c = True

class WebDriver(object):
    """selenium web driver constructor
    :
    """
    def __init__(self, name=None):
        self.name = name
        #check if file exist
        try:
            file = open(name+".session","r")
            session_id = file.readline().replace("\n","")
            executor_url = file.readline()
            print("session_id=" + session_id)
            print("session_url=" + executor_url)
            file.close()
        except:
            print("Page not ready to read")
            self.create_new_browser()
            return

        #try to connect existing browser

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        self.driver = SessionRemote(command_executor=executor_url, desired_capabilities=firefox_capabilities)
        self.driver.session_id = session_id
        try:
            self.driver.page_source
            return
        except Exception as e:
            print("Page not ready to read",e)
            self.create_new_browser()

    def create_new_browser(self):
        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        options = webdriver.FirefoxOptions()
        # options.add_argument("-headless")
        self.driver = webdriver.Firefox(
            options=options,
            executable_path="/usr/local/bin/geckodriver",
            desired_capabilities=firefox_capabilities)
        print("Firefox Headless Browser Invoked")
        # write session id and url to reattach it
        file = open(self.name + ".session", "w")
        file.write(self.driver.session_id + "\n" + self.driver.command_executor._url)
        file.close()

    def check_alive(self):

        firefox_capabilities = DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        self.driver = SessionRemote(command_executor=self.executor_url, desired_capabilities=firefox_capabilities)

        self.driver.session_id = self.session_id

        try:
            self.driver.page_source
            return True
        except Exception as e:
            options = webdriver.FirefoxOptions()
            # options.add_argument("-headless")
            self.driver = webdriver.Firefox(firefox_options=options, executable_path="/usr/local/bin/geckodriver")
            print("Firefox Headless Browser RE-Invoked")
            # write session id and url to reattach it
            file = open(self.name + ".session", "w")
            file.write(self.driver.session_id + "\n" + self.driver.command_executor._url)
            file.close()
            return True
        return False

if __name__ == "__main__":
    wd = WebDriver("google")
    wd.driver.get("https://www.google.com")
