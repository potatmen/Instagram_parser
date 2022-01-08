from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from data import username, password
import time
import random
import requests


class InstagramBot():
    def __init__(self):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome('chromedriver.exe')

    def close_browser(self):
        self.browser.close()
        self.browser.quit()

    def login(self):
        browser = self.browser

        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element_by_name('username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(1)

        password_input = browser.find_element_by_name('password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)

        time.sleep(2)

    def element_exists(self, url):
        browser = self.browser
        try:
            browser.find_element_by_xpath(url)
            return True
        except Exception:
            return False

    def put_exact_like(self, url):
        browser = self.browser
        browser.get(url)
        time.sleep(1)
        wrong_path = '/html/body/div[1]/section/main/div/div/h2'
        if self.element_exists(wrong_path):
            print('There is not post with this URL')
            self.close_browser()
        else:
            browser.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
            print(f'Post {url} is liked!')
            time.sleep(1)
            self.close_browser()

    def get_all_post_urls(self, userurl):
        browser = self.browser
        browser.get(userurl)
        time.sleep(1)
        wrong_path = '/html/body/div[1]/section/main/div/div/h2'
        if self.element_exists(wrong_path):
            print('There is no user with this URL')
            self.close_browser()
        else:
            print('User is found!')
            posts_urls = set()
            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span").text)
            loops_count = posts_count // 12 + int(posts_count % 12 != 0)
            for _ in range(1, loops_count + 1):
                hrefs = browser.find_elements_by_tag_name('a')
                hrefs = [items.get_attribute(
                    'href') for items in hrefs if '/p/' in items.get_attribute('href')]
                for href in hrefs:
                    posts_urls.add(href)
                browser.execute_script(
                    'window.scrollTo(0,document.body.scrollHeight);')
                time.sleep(random.randrange(1, 3))
            file_name = userurl.split('/')[-2]
            with open(f'{file_name}.txt', 'w') as file:
                for href in posts_urls:
                    file.write(href + '\n')

    def likes_for_all_posts(self, userurl):
        browser = self.browser
        self.get_all_post_urls(userurl)
        time.sleep(1)
        file_name = userurl.split('/')[-2]
        with open(f'{file_name}.txt') as file:
            content = file.readlines()
            for url in content:
                try:
                    browser.get(url[:-1:1])
                    time.sleep(1)
                    like_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button'
                    browser.find_element_by_xpath(like_button).click()
                    time.sleep(1)
                    print(f'Post {url[:-1:1]} is liked!')
                except Exception as ex:
                    print(ex)
                    self.close_browser()
                time.sleep(random.randrange(80,100))
        self.close_browser()

    def download_content_from_user(self, userurl):
        browser = self.browser
        self.get_all_post_urls(userurl)
        time.sleep(3)
        file_name = userurl.split('/')[-2]
        photos = set()
        with open(f'{file_name}.txt') as file:
            try:
                content = file.readlines()
                for url in content:
                    browser.get(url[:-1])
                    time.sleep(1)
                    next_image_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div[1]/div[2]/div/button'
                    other_imgage_button = '/html/body/div[1]/section/main/div/div[1]/article/div/div[1]/div/div[1]/div[2]/div/button[2]'
                    if not self.element_exists(next_image_button):
                        with open('photos_xpath.txt') as file:
                            xpaths = file.read().split('\n')
                            for xpath in xpaths:
                                if self.element_exists(xpath):
                                    with open('images_urls.txt', 'a') as img_file:
                                        element = browser.find_element_by_xpath(
                                            xpath).get_attribute('src') + '\n'
                                        if element in photos:
                                            continue
                                        img_file.write(element)
                                        photos.add(element)
                                    break

                    else:
                        with open('photos_xpath.txt') as file:
                            xpaths = file.read().split('\n')
                            for xpath in xpaths:
                                if self.element_exists(xpath):
                                    with open('images_urls.txt', 'a') as imgaes_file:
                                        element = browser.find_element_by_xpath(
                                            xpath).get_attribute('src') + '\n'
                                        if element in photos:
                                            continue
                                        imgaes_file.write(element)
                                        photos.add(element)
                                    break
                        browser.find_element_by_xpath(
                            next_image_button).click()
                        flag = True
                        while flag:
                            time.sleep(0.5)
                            flag = self.element_exists(
                                other_imgage_button)
                            with open('photos_xpath.txt') as file:
                                xpaths = file.read().split('\n')
                                for xpath in xpaths:
                                    if self.element_exists(xpath):
                                        with open('images_urls.txt', 'a') as imgaes_file:
                                            element = browser.find_element_by_xpath(
                                                xpath).get_attribute('src') + '\n'
                                            if element in photos:
                                                continue
                                            imgaes_file.write(element)
                                            photos.add(element)
                                        break
                            if flag:
                                browser.find_element_by_xpath(
                                    other_imgage_button).click()

            except Exception as ex:
                print(ex)
                self.close_browser()
            cnt = 1
            with open('images_urls.txt', 'r') as file:
                content = file.readlines()
                for cur in content:
                    url = cur[:-2]
                    with open(f'Files/{cnt}_img.jpg', 'wb') as image_file:
                        image_file.write(requests.get(url).content)
                        cnt += 1
            self.close_browser()
