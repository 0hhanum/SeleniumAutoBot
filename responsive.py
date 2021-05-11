import time
from math import ceil
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os

"""
웹사이트의 화면을 가로 사이즈 별로 스크롤하며 모두 스크린샷 하는 코드
"""


class ResponsiveTester:
    def __init__(self, urls):
        self.urls = urls
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.browser.maximize_window()
        self.sizes = [480, 960, 1920]  # 주로 디스플레이되는 화면 사이즈

    def screenshot(self, url):
        BROWSER_HEIGHT = 801
        self.browser.get(url)
        name = url.replace("https://", "").replace(".com", "")
        os.mkdir(f'screenshots/{name}')
        for size in self.sizes:
            self.browser.set_window_size(size, BROWSER_HEIGHT)  # 현재 내 디스플레이 height 801
            self.browser.execute_script("window.scrollTo(0,0)")
            time.sleep(2)
            scroll_size = self.browser.execute_script("return document.body.scrollHeight")
            total_sections = ceil(scroll_size / BROWSER_HEIGHT)
            for section in range(total_sections):
                self.browser.execute_script(f"window.scrollTo(0, {section * BROWSER_HEIGHT})")
                self.browser.save_screenshot(f'screenshots/{name}/{size}x{section + 1}.png')
                time.sleep(1)

    def start(self):
        for url in self.urls:
            self.screenshot(url)

    def finish(self):
        self.browser.quit()


test = ResponsiveTester(["https://naver.com"])
test.start()
test.finish()
