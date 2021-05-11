import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import random

class InstaMacGyver:
    def __init__(self, target_hashtag, max_hashtags):
        self.target_hashtag = target_hashtag
        self.max_hashtags = max_hashtags
        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def wait_for(self, locator):
        return WebDriverWait(self.browser, 20).until(ec.presence_of_element_located((By.CLASS_NAME, f'{locator}')))

    def log_in(self):
        self.browser.get(f'https://www.instagram.com/accounts/login/')

        to_login = WebDriverWait(self.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "pexuQ")))
        to_login[0].send_keys("""ID""")
        to_login[1].send_keys("""PASSWORD""")


        time.sleep(1)
        # password 에 input 을 이용해 개인정보를 공개하지 않고 비밀번호를 넣는 방법이 있음.
        # XPath 혹은 link text 를 이용해서도 element 를 찾을 수 있음.
        log_in_button = self.browser.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/div[1]/div/form/div/div[3]/button')
        # to_login[1].send_keys(Keys.ENTER)
        log_in_button.click()

    def get_related_hashtag_links(self, target_hashtag):
        links = []

        search_bar = self.wait_for('x3qfX')
        search_bar.send_keys(f'#{target_hashtag}')
        hashtag_box = self.wait_for('fuqBx')
        hashtags = WebDriverWait(self.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "-qQT3")))

        for hashtag in hashtags[:self.max_hashtags]:
            link = hashtag.get_attribute('href')
            links.append(link)

        return links

    def open_links(self, links):
        for link in links:
            self.browser.execute_script(f"window.open('{link}')")  # js 를 이용해 얻은 url 새 탭에서 열기
            time.sleep(0.7)

        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def extract_data(self):
        hashtag_name = self.wait_for('fKFbl').text[1:]
        post_count = self.browser.find_element_by_class_name('g47SY').text
        post_count = int(post_count.replace(",", ""))

        return hashtag_name, post_count

    def get_hashtag_info(self):
        collected_hashtags = []
        for window in self.browser.window_handles:  # 열려있는 tab 관리
            try:
                collected_hashtags.append(self.extract_data())
            except Exception:
                pass

            time.sleep(1)
            self.browser.switch_to.window(window)

        return collected_hashtags

    def start_mining(self):
        self.log_in()
        links = self.get_related_hashtag_links(self.target_hashtag)
        self.open_links(links)
        return self.get_hashtag_info()

    ######

    def open_each_post(self):
        anchors = []
        posts = WebDriverWait(self.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'weEfm')))

        for post in posts[:5]:
            anchors += post.find_elements_by_tag_name('a')

        for anchor in anchors:
            link = anchor.get_attribute("href")
            self.browser.execute_script(f"window.open('{link}')")
            time.sleep(1)

        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[-1])

    def follow_like_submit_comment(self, comment_list):
        for window in self.browser.window_handles:
            try:
                follow_and_submit_buttons = WebDriverWait(self.browser, 20).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, 'y3zKF')))
                follow_and_submit_buttons[0].click()
                textarea = self.browser.find_element_by_tag_name('textarea')
                textarea.click()
                textarea = self.browser.find_element_by_tag_name('textarea')
                textarea.send_keys(f'{comment_list[random.randint(0, len(comment_list) - 1)]}')
                follow_and_submit_buttons = WebDriverWait(self.browser, 20).until(
                    ec.presence_of_all_elements_located((By.CLASS_NAME, 'y3zKF')))
                follow_and_submit_buttons[1].click()
                like_button = self.browser.find_element_by_xpath(
                    '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button'
                )
                like_button.click()
                time.sleep(7)


            except Exception:
                pass

            time.sleep(3)

            if len(self.browser.window_handles) > 1:
                self.browser.close()
                self.browser.switch_to.window(window)

    def start_FLC_bot(self, comment_list):  # Follow, Like, Comment
        self.log_in()
        links = self.get_related_hashtag_links(self.target_hashtag)
        for link in links:
            self.browser.get(link)
            self.open_each_post()
            self.follow_like_submit_comment(comment_list)

    def finish(self):
        self.browser.quit()


insta_macgyver = InstaMacGyver('porshce', 10)
comment_list = ['hello', 'iloveit', 'SOCOOL', ]
insta_macgyver.start_FLC_bot(comment_list)


#####
# insta_macgyver.log_in()
#
# profile_button = WebDriverWait(insta_macgyver.browser, 20).until(ec.presence_of_element_located((By.CLASS_NAME, 'qNELH')))
# profile_button.click()
# time.sleep(0.5)
# profile_button = insta_macgyver.browser.find_element_by_class_name('-qQT3')
# profile_button.click()
#
# my_infos = WebDriverWait(insta_macgyver.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, '-nal3')))
# my_infos[1].click()
#
# followers_box = insta_macgyver.browser.find_element_by_class_name('isgrP')
# followers = WebDriverWait(insta_macgyver.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'notranslate')))
#
# followers_list = []
#
# for follower in followers:
#     followers_list.append(follower.text)
# print(followers_list)
#
# exit_button = insta_macgyver.browser.find_elements_by_class_name('wpO6b')
# exit_button[-1].click()
#
# time.sleep(1)
# my_infos = WebDriverWait(insta_macgyver.browser, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, '-nal3')))
# my_infos[2].click()
# following_box = insta_macgyver.browser.find_element_by_class_name('isgrP')
# followings = WebDriverWait(insta_macgyver.browser, 20).until(ec.presence_of_all_elements_located((By.TAG_NAME, 'li')))
# for following in followings:
#     print(following.text)
