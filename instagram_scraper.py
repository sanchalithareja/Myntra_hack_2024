from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime
import pandas as pd
from dateutil import tz
import re

class InstagramBot():
    def __init__(self, email, password):
        options = webdriver.ChromeOptions()
        options.binary_location = r"chromedriver.exe"
        self.browser = webdriver.Chrome(options=options)
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        print(self.browser.title)
        time.sleep(1)
        emailInput = self.browser.find_element(By.XPATH, "//input[@name='username']")
        passwordInput = self.browser.find_element(By.XPATH, "//input[@name='password']")

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

def is_fashion_post(post):
    fashion_keywords = ['#fashion', '#style', '#ootd', '#fashionblogger', '#fashionista', 'fashion', 'style']
    try:
        caption_element = post.find_element(By.CLASS_NAME, 'C4VMK')
        caption_text = caption_element.text
        for keyword in fashion_keywords:
            if re.search(keyword, caption_text, re.IGNORECASE):
                return True
    except NoSuchElementException:
        return False
    return False

bot = InstagramBot('ctrldefeat', 'myntrahack2024')
wait = WebDriverWait(bot.browser, 10)
bot.signIn()
time.sleep(3)
okay = bot.browser.find_element(By.CLASS_NAME, "sqdOP.yWX7d.y3zKF")
okay.send_keys(Keys.RETURN)
time.sleep(2)
notnow = bot.browser.find_element(By.CLASS_NAME, "aOOlW.HoLwm")
notnow.send_keys(Keys.RETURN)
time.sleep(1)

names = []
profiles = []
datetimelist = []
SCROLL_PAUSE_TIME = 1.6

last_height = bot.browser.execute_script("return document.body.scrollHeight")
for i in range(5):
    posts = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'v1Nh3.kIKUG._bz0w')))
    for post in posts:
        if is_fashion_post(post):
            try:
                name1 = post.find_element(By.CLASS_NAME, "sqdOP.yWX7d._8A5w5.ZIAjV")
                date1 = post.find_element(By.CLASS_NAME, "_1o9PC.Nzb55")
                profile = name1.get_attribute("text")
                date = date1.get_attribute("datetime")
                profiles.append(profile)
                datetimelist.append(date)
            except NoSuchElementException:
                continue
    bot.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = bot.browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

new_profile = []
for profile in profiles:
    profile = profile.replace("See All", "")
    if profile != "":
        new_profile.append(profile)
df1 = pd.DataFrame(list(zip(new_profile)), columns=['profile_name'])
df1.to_csv('profiles.csv')

new_date = []
for date in datetimelist:
    date = date.replace("T", " ")[:-5]
    utc = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Kolkata')
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    new_date.append(central)

df = pd.DataFrame(list(zip(new_date)), columns=['datetimelist'])
df.to_csv('datetime.csv')

with open('profile.txt', 'w') as filehandle:
    for profile in new_profile:
        filehandle.write('%s,' % profile)
