import time
import random
import requests
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome import service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

# insta: <input accept="image/jpeg,image/png,image/heic,image/heif,video/mp4,video/quicktime" class="_ac69" multiple="" type="file">

options = webdriver.ChromeOptions()
options.add_argument("--profile-directory=Profile 1")
options.add_argument("--user-data-dir=/Users/joshuakim/Library/Application Support/Google/Chrome")
options.add_argument("disable-infobars")
options.add_argument('--start-fullscreen')
ua = UserAgent().random
options.add_argument('user-agent={}'.format(ua))
s=service.Service(r"/Users/joshuakim/Downloads/chromedriver-mac-arm64/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=s)

# time.sleep(30)
driver.get('https://www.instagram.com/')
# time.sleep(20)


def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True


def upload(video_path):
    # while True:
    time.sleep(5)
    # upload = driver.find_element(By.XPATH, '//span[@class="css-1bgawvd"]')
    # ac = ActionChains(driver)
    # ac.move_to_element(upload).move_by_offset(500, 0).click().perform()

    new_post = driver.find_element(By.XPATH, '//*[name()="svg" and @aria-label="New post"]')
    new_post.click()

    # specify file
    upload_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
    )
    upload_input.send_keys(video_path)
    
    # go to next page
    next_button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37"]'))
    )
    time.sleep(3)
    next_button.send_keys('\n')

    # go to next page
    next_button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37"]'))
    )
    time.sleep(2)
    next_button.send_keys('\n')

    # post reel
    next_button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="x1i10hfl xjqpnuy xa49m3k xqeqjp1 x2hbi6w xdl72j9 x2lah0s xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x2lwn1j xeuugli x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1q0g3np x1lku1pv x1a2a7pz x6s0dn4 xjyslct x1ejq31n xd10rxx x1sy0etr x17r0tee x9f619 x1ypdohk x1f6kntn xwhw2v2 xl56j7k x17ydfre x2b8uid xlyipyv x87ps6o x14atkfc xcdnw81 x1i0vuye xjbqb8w xm3z3ea x1x8b98j x131883w x16mih1h x972fbf xcfux6l x1qhh985 xm0m39n xt0psk2 xt7dq6l xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x1n5bzlp x173jzuc x1yc6y37"]'))
    )
    time.sleep(1)
    next_button.send_keys('\n')
    # next_button.click()
    # post_button = WebDriverWait(driver, 60).until(
    #     EC.presence_of_element_located((By.XPATH, '//button[@class="css-y1m958"]'))
    # )
    # post_button.click()
    # post = css-y1m958

    
    # time.sleep(10)
    # file_uploader = WebDriverWait(driver, 10).until(
    #     # slot="full-post-link"
    #     EC.presence_of_element_located((By.XPATH, "//span[@class='css-1bgawvd']"))
    # )
    # ActionChains(driver).move_to_element(file_uploader).click().perform() 
    # file_uploader.click()


# ================================================================
# Here is the path of the video that you want to upload to insta.
# Plese edit the path because this is different to everyone.
# upload(r"/Users/joshuakim/Desktop/newvid.mp4")
driver.close()
# ================================================================