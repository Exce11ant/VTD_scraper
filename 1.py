import json
import multiprocessing
import random
import re
import threading
import requests
from pprint import pprint
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
import time
from seleniumwire.utils import decode
import io
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sqlite3
import os

useragent = UserAgent()
# options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Ssl
webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# user-agent
chrome_options.add_argument(f"user-agent={useragent.chrome}")
# chrome_options.add_argument("--headless")
# proxy
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
proxies = [{"https": f"http://4LxXc4:r3QCsC@45.133.210.115:8000"},
           {"https": f"http://Yoej0t:p1d1sf@45.153.20.230:10465"},
           {"https": f"http://YUzdZ2:ELudWQ@45.153.20.230:10462"},
           {"https": f"http://QfWD4d:msYKd2@45.153.20.217:13391"}]
proxy_options = {
    "proxy": random.choice(proxies)
}
# proxy_options = {
#     "proxy": {
#         "https": f"http://4LxXc4:r3QCsC@45.133.210.115:8000"
#
#     }
# }
driver_head = webdriver.Chrome(
    executable_path=r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe",
    seleniumwire_options=proxy_options,
    chrome_options=chrome_options
)

# users_urls = ["https://www.reg.ru/web-tools/myip",
#               "https://hidemy.name/ru/what-is-my-ip/",
#               "https://proxy6.net/myip",
#               "https://proxyline.net/ip-moego-servera/"]
users_urls = ['https://www.vinted.it/member/89520838-ellahalifax',
              'https://www.vinted.it/member/63257650-maeriix',
              'https://www.vinted.it/member/89043366-pao533',
              'https://www.vinted.it/member/54468112-saandre',
              'https://www.vinted.it/member/65345629-ilag2409',
              'https://www.vinted.it/member/89408211-lally88',
              'https://www.vinted.it/member/89048485-samotracia59',
              'https://www.vinted.it/member/89524318-antonella899',
              'https://www.vinted.it/member/89822076-j3820261',
              'https://www.vinted.it/member/50272721-lucia1021978']
bd_info = []
id_users = []


def multi_work(url):
    connect_sql = sqlite3.connect('vinted_db.db')
    cursor = connect_sql.cursor()
    # for x in users_urls:
    driver_head.get(url=url)
    time.sleep(0.5)
    id = re.search('/(\d+)-', driver_head.current_url).group(1)
    # driver_head.get(f"https://www.vinted.it/api/v2/users/{id}?localize=false")
    # driver_head.get(f"https://whoer.net/ru")
    # print(driver_head.current_url)
    # for json_url in driver_head.requests:
    #     if json_url.url == f"https://www.vinted.it/api/v2/users/{id}?localize=false":
    #         body = decode(json_url.response.body, json_url.response.headers.get('Content-Encoding', 'identity'))
    #         body = body.decode('utf-8')
    #         body = json.loads(body)
    #         users = body.get("user")
    #         # print(users)
    #         Italia = 'Italia'
    #         France = 'France'
    #         # for stat in users:
    #         prof_url = body.get("user").get('profile_url')
    #         id_user = body.get("user").get('id')
    #         country_title_local = body.get("user").get('country_title_local')
    #         negative_feedback_count = body.get("user").get('negative_feedback_count')
    #         positive_feedback_count = body.get("user").get('positive_feedback_count')
    #         neutral_feedback_count = body.get("user").get('neutral_feedback_count')
    #         meeting_transaction_count = body.get("user").get('meeting_transaction_count')
    #         if id_user not in id_users and country_title_local == Italia and positive_feedback_count == 0 and neutral_feedback_count == 0 and meeting_transaction_count == 0 and negative_feedback_count == 0:
    #             id_users.append(id_user)
    #             cursor.execute("""
    #             INSERT OR IGNORE INTO vinted_page_users (id_user,prof_url)
    #             VALUES (?, ?)
    #             """, (id_user, prof_url))
    #             connect_sql.commit()
    #         # print(country_title_local, negative_feedback_count, positive_feedback_count, neutral_feedback_count,
    #         #       meeting_transaction_count, prof_url, id_user)
    #


def main():
    # while True:
    p = Pool(processes=3)
    p.map(multi_work, users_urls)
    # multi_work()


if __name__ == '__main__':
    main()
