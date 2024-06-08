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


options = webdriver.ChromeOptions()
options.add_argument("--profile-directory=Profile 1")
options.add_argument("--user-data-dir=/Users/joshuakim/Library/Application Support/Google/Chrome")
options.add_argument("disable-infobars")
# options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--start-fullscreen')
ua = UserAgent().random
options.add_argument('user-agent={}'.format(ua))
s=service.Service(r"/Users/joshuakim/Downloads/chromedriver-mac-arm64/chromedriver.exe")
driver = webdriver.Chrome(options=options, service=s)
# driver = webdriver.Chrome(options=options,  executable_path=CM().install())
# driver.set_window_size(1680, 900)

# driver.get('https://www.tiktok.com')
# ActionChains(driver).key_down(Keys.CONTROL).send_keys(
#     '-').key_up(Keys.CONTROL).perform()
# ActionChains(driver).key_down(Keys.CONTROL).send_keys(
#     '-').key_up(Keys.CONTROL).perform()
# print('Waiting 30s for manual login...')
# time.sleep(30)
driver.get('https://www.tiktok.com/creator-center/upload?lang=en')
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

    

    driver.switch_to.frame(0)

    upload_input = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_input.send_keys(video_path)
    time.sleep(60)
    post_button = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//button[@class="css-y1m958"]'))
    )
    post_button.click()
    # post = css-y1m958
    # for div in all_divs:
    #     try:
    #         print(div.get_attribute("class"))
    #     except:
    #         print("not found")
    driver.close()
    # file_uploader = WebDriverWait(driver, 10).until(
    #     # slot="full-post-link"
    #     EC.presence_of_element_located((By.XPATH, "//span[@class='css-1bgawvd']"))
    # )
    # ActionChains(driver).move_to_element(file_uploader).click().perform() 
    # file_uploader.click()


# ================================================================
# Here is the path of the video that you want to upload in tiktok.
# Plese edit the path because this is different to everyone.
upload(r"/Users/joshuakim/Desktop/vid.mp4")
# ================================================================