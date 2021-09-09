from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import os

class RPA:

    by = By
    el = None
    driver = None

    def __init__(self, driver_path):
        here = os.getcwd()
        options = Options()
        # options.add_argument("--headless")
        prefs = { "download.default_directory" : here }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=driver_path, options=options)

    # open site
    def open(self, url):
        self.driver.get(url)
        return self

    # execute javascript
    def script(self, script):
        self.driver.execute_script(script)
        return self

    # select element
    def elem(self, xpath, by=By.CSS_SELECTOR):
        self.el = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, xpath)))
        return self

    # input value to element
    def input(self, value):
        self.el.send_keys(value)
        return self

    # click on element
    def click(self):
        self.el.click()
        return self

    # clear input text field
    def clear(self):
        self.el.clear()
        return self

    # get downloaded file from downloads tab
    def file(self, timeout=120):

        def download(drv):

            if not "chrome://downloads" in drv.current_url:

                drv.execute_script("window.open('');")
                drv.switch_to.window(drv.window_handles[1])
                drv.get("chrome://downloads/")

            return drv.execute_script("""
                return document.querySelector('downloads-manager')
                .shadowRoot.querySelector('#downloadsList')
                .items.filter(e => e.state === 'COMPLETE')
                .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url);
                """)

        files = WebDriverWait(self.driver, timeout, 1).until(download)
        if "chrome://downloads" in self.driver.current_url:
            self.driver.close()

        self.driver.switch_to.window(self.driver.window_handles[0])
        return files[0] if len(files) > 0 else None

    # close window
    def close(self):
        self.driver.close()