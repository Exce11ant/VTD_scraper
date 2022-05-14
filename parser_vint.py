import json
import random
import re
import multiprocessing
import requests
from pprint import pprint
from seleniumwire import webdriver
from fake_useragent import UserAgent
import time
from seleniumwire.utils import decode
import io
from multiprocessing import Pool
from bs4 import BeautifulSoup
import sqlite3
import os
import schedule
from random import choice

useragent = UserAgent()
# options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

# Ssl
webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# user-agent
rnd_ua = [useragent.google, useragent.chrome, useragent.firefox]
chrome_options.add_argument(f"user-agent={random.choice(rnd_ua)}")
chrome_options.add_argument("--headless")

# proxy
# proxies = [{"https": f"http://4LxXc4:r3QCsC@45.133.210.115:8000"},
#            {"https": f"http://wmvMte:TFKRow@196.18.166.179:8000"}]
proxies = [{"https": f"http://B0MJDf:8K3R3d@85.195.81.158:14269"},
           {"https": f"http://fAqy4h:rfugG2@45.91.209.148:13841"},
           {"https": f"http://f8FLkF:6gJyfh@45.153.20.225:11426"},
           {"https": f"http://ZM5Ppd:ThFgWM@85.195.81.158:14270"},
           {"https": f"http://4LxXc4:r3QCsC@45.133.210.115:8000"},
           {"https": f"http://wmvMte:TFKRow@196.18.166.179:8000"}]

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
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

users_urls = []
users_urls2 = []
ids = []
bd_info = []
id_users = []


def get_item():
    hhd = webdriver.Chrome(
        executable_path=r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe",
        seleniumwire_options=proxy_options,
        chrome_options=chrome_options
    )
    with hhd as d_head:
        d_head.get("https://www.vinted.it/vetements?catalog[]=1904&order=newest_first")
        d_head.get(
            "https://www.vinted.it/api/v2/catalog/items?catalog_ids=1904&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&page=1&per_page=60")
        for json_url in d_head.requests:
            if json_url.url == 'https://www.vinted.it/api/v2/catalog/items?catalog_ids=1904&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&page=1&per_page=60':
                body = decode(json_url.response.body, json_url.response.headers.get('Content-Encoding', 'identity'))
                body = body.decode('utf-8')
                body = json.loads(body)
                print("Забрал джейсон")

    with io.open("result.json", "w", encoding="utf-8") as file:
        json.dump(body, file, indent=4, ensure_ascii=False)

        # os.system("taskkill /im chromedriver.exe /f")
        # hhd.close()
        # os.system("taskkill /im chromedriver.exe /f")


def get_url_json():
    with open("result.json", "r", encoding="utf-8") as json_file:
        date = json.load(json_file)

    result_data = []
    for data in date["items"]:
        id = data["id"]
        title = data["title"]
        price = data["price"]
        id_user = data["user"]["id"]
        pr_url = data["user"]["profile_url"]
        url_post = data["url"]

        result_data.append(
            {
                "id": id,
                "title": title,
                "price": price,
                "id_user": id_user,
                "pr_url": pr_url,
                "url_post": url_post
            }
        )
    with open("result_2.json", "w", encoding="utf-8") as file:
        json.dump(result_data, file, indent=2, ensure_ascii=False)

    print("Сохранил всю дату")


def get_url_post():
    with open("result_2.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for user_url in data:
            user_urls = user_url.get("pr_url")
            users_urls.append(user_urls)

        pprint(users_urls)


def multi_work(url):
    # Если захочешь скрыть хром, будут траблы с читаемостью !
    ddh = webdriver.Chrome(
        executable_path=r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe",
        seleniumwire_options=proxy_options,
        chrome_options=chrome_options)
    with ddh as driver_h:
        connect_sql = sqlite3.connect('vinted_db.db')
        cursor = connect_sql.cursor()
        # for x in users_urls:
        driver_h.get(url=url)
        # time.sleep(0.5)
        time.sleep(1)
        id = re.search('/(\d+)-', driver_h.current_url).group(1)
        # for i in ids:
        driver_h.get(f"https://www.vinted.it/api/v2/users/{id}?localize=false")
        time.sleep(1)
        print(driver_h.current_url)
        for json_url in driver_h.requests:
            if json_url.url == f"https://www.vinted.it/api/v2/users/{id}?localize=false":
                body = decode(json_url.response.body, json_url.response.headers.get('Content-Encoding', 'identity'))
                body = body.decode('utf-8')
                body = json.loads(body)
                users = body.get("user")
                Italia = 'Italia'
                France = 'France'
                prof_url = body.get("user").get('profile_url')
                id_user = body.get("user").get('id')
                country_title_local = body.get("user").get('country_title_local')
                negative_feedback_count = body.get("user").get('negative_feedback_count')
                positive_feedback_count = body.get("user").get('positive_feedback_count')
                neutral_feedback_count = body.get("user").get('neutral_feedback_count')
                meeting_transaction_count = body.get("user").get('meeting_transaction_count')
                if id_user not in id_users and country_title_local == Italia and positive_feedback_count == 0 and neutral_feedback_count == 0 and meeting_transaction_count == 0 and negative_feedback_count == 0:
                    id_users.append(id_user)
                    cursor.execute("""
                    INSERT OR IGNORE INTO vinted_page_users (id_user,prof_url)
                    VALUES (?, ?)
                    """, (id_user, prof_url))
                    connect_sql.commit()
                print(country_title_local, negative_feedback_count, positive_feedback_count, neutral_feedback_count,
                      meeting_transaction_count, prof_url, id_user)
            else:
                continue


        # driver_h.close()
        # else:
        # with open("bd_info.json", "w", encoding='utf-8') as file:
        #     json.dump(bd_info, file, indent=4, ensure_ascii=False)


def main():
    while True:
        # process_count = int(input("Enter the num of processes: "))
        # os.remove(r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\result.json")
        # os.remove(r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\result_2.json")
        get_item()
        time.sleep(1)
        os.system("taskkill /im chromedriver.exe /f")
        time.sleep(1)
        os.system('taskkill /im chrome.exe /f')
        time.sleep(1)
        get_url_json()
        get_url_post()
        n = 60
        p = Pool(processes=5)
        p.map(multi_work, users_urls[:-n - 1:-1])
        # with multiprocessing.Pool(processes=4) as p:
        #     p.map(multi_work, users_urls)
        # p.close()
        # p.join()
        # p.terminate()
        # os.system("taskkill /im chromedriver.exe /f")
        # os.system('taskkill /pid chrome.exe /f')
        print("finish")
        time.sleep(60)
        # os.system('taskkill /PID chromedriver.exe/T')
        # os.system('taskkill /PID chrome.exe/T')
        # driver_head.close()


if __name__ == '__main__':
    main()
