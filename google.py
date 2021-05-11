from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class GoogleKeywordScreenshooter:

    """ 구글 검색결과 자동 스크린샷 """

    index = 0

    def __init__(self, keyword):
        options = Options()
        # options.add_argument("--headless")  # 윈도우가 열리지 않고 작업 수행
        # self.browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.keyword = keyword
        self.links = self.get_links()

    def get_links(self):
        self.browser.get('https://google.com')

        search_bar = self.browser.find_element_by_class_name('gLFyf')
        search_bar.send_keys(self.keyword)
        search_bar.send_keys(Keys.ENTER)

        self.shot()
        pages = self.browser.find_elements_by_tag_name("tbody")[-1].find_elements_by_tag_name('td')
        links = []

        for page in pages[:-1]:
            try:
                link = page.find_element_by_tag_name("a").get_attribute("href")
                # 마지막 페이지를 얻어와 url 에 대입할수도 있지만 최대 10페이지만 하기로 함.
            except Exception:
                pass
            else:
                links.append(link)
        return links

    def shot(self):
        try:
            shitty_element = WebDriverWait(self.browser, 3).until(ec.presence_of_element_located((By.CLASS_NAME, "g-blk")))
            # shitty_element 가 나타날때까지 대기
        except Exception:
            pass
        else:
            self.browser.execute_script("""
            const shitty = arguments[0]
            shitty.parentElement.removeChild(shitty)
            """, shitty_element)  # execute_script 를 이용해서 js 명령문을 실행시킬 수 있음.

        search_results = self.browser.find_element_by_id('rso').find_elements_by_class_name('g')

        for search_result in search_results:

            class_name = search_result.get_attribute("class")
            if class_name != 'kno-kp mnr-c g-blk':
                search_result.screenshot(f"screenshots/{self.keyword}x{self.index}.png")
                self.index += 1

    def start(self):
        for link in self.links:
            self.browser.get(link)
            self.shot()

    def finish(self):
        self.browser.quit()


domain_competitors = GoogleKeywordScreenshooter("개발자")


domain_competitors.start()
domain_competitors.finish()
