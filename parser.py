import json
import random
import re
from pprint import pprint
from seleniumwire import webdriver
from fake_useragent import UserAgent
from seleniumwire.utils import decode
import io
from multiprocessing import Pool
import sqlite3
import os
import time

start_time = time.time()
users_urls = []
users_urls2 = []
ids = []
bd_info = []
id_users = []
result_data = []


def get_item():
    useragent = UserAgent()
    # options
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.add_argument("--start-maximized")
    webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True
    rnd_ua = [useragent.google, useragent.chrome, useragent.firefox]
    chrome_options.add_argument(f"user-agent={random.choice(rnd_ua)}")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    proxies = [{"https": f"http://0bq5Ym:PL7wtt@45.153.20.231:10448"},
               {"https": f"http://0bq5Ym:PL7wtt@45.153.20.231:10447"}]
    proxy_options = {
        "proxy": random.choice(proxies)
    }
    hhd = webdriver.Chrome(
        executable_path=r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe",
        seleniumwire_options=proxy_options,
        chrome_options=chrome_options
    )
    with hhd as d_head:
        d_head.get("https://www.vinted.pl/vetements?catalog[]=1904&order=newest_first")
        d_head.get(
            "https://www.vinted.pl/api/v2/catalog/items?catalog_ids=1904&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&page=1&per_page=90")
        for json_url in d_head.requests:
            if json_url.url == 'https://www.vinted.pl/api/v2/catalog/items?catalog_ids=1904&color_ids=&brand_ids=&size_ids=&material_ids=&status_ids=&is_for_swap=0&order=newest_first&page=1&per_page=90':
                body = decode(json_url.response.body, json_url.response.headers.get('Content-Encoding', 'identity'))
                body = body.decode('utf-8')
                body = json.loads(body)
                print("Забрал джейсон")
    with io.open("result.json", "w", encoding="utf-8") as file:
        json.dump(body, file, indent=4, ensure_ascii=False)


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
            user_urls = user_url.get("id_user")
            links = f"https://www.vinted.pl/api/v2/users/{user_urls}?localize=false"
            users_urls.append(links)

        pprint(users_urls)


useragent = UserAgent()
# options
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--start-maximized")
# Ssl
webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

# user-agent
rnd_ua = [useragent.google, useragent.chrome, useragent.firefox]
chrome_options.add_argument(f"user-agent={random.choice(rnd_ua)}")
chrome_options.add_argument("--headless")

proxies = [{"https": f"http://0bq5Ym:PL7wtt@45.153.20.231:10448"},
           {"https": f"http://0bq5Ym:PL7wtt@45.153.20.231:10447"}]

chrome_options.add_argument("--disable-blink-features=AutomationControlled")
proxy_options = {
    "proxy": random.choice(proxies)
}
driver_h = webdriver.Chrome(
    executable_path=r"C:\Users\38095\PycharmProjects\pythonProject1\chromedriver\chromedriver.exe",
    seleniumwire_options=proxy_options,
    chrome_options=chrome_options)

driver_h.get("https://www.vinted.pl/vetements?catalog[]=1904&order=newest_first")


def multi_work(url):
    driver_h.get(url=url)
    id = re.search('/(\d+)', url).group(1)
    print(driver_h.current_url)
    for json_url in driver_h.requests:
        if json_url.url == f"https://www.vinted.pl/api/v2/users/{id}?localize=false":
            body = decode(json_url.response.body, json_url.response.headers.get('Content-Encoding', 'identity'))
            body = body.decode('utf-8')
            body = json.loads(body)
            users = body.get("user")
            Italia = 'Italia'
            France = 'France'
            CZ = 'Česká republika'
            pl = 'Polska'
            prof_url = body.get("user").get('profile_url')
            id_user = body.get("user").get('id')
            country_title_local = body.get("user").get('country_title_local')
            negative_feedback_count = body.get("user").get('negative_feedback_count')
            positive_feedback_count = body.get("user").get('positive_feedback_count')
            neutral_feedback_count = body.get("user").get('neutral_feedback_count')
            meeting_transaction_count = body.get("user").get('meeting_transaction_count')
            print(country_title_local, negative_feedback_count, positive_feedback_count, neutral_feedback_count,
                  meeting_transaction_count)
            connect_sql = sqlite3.connect('vinted_db.db')
            cursor = connect_sql.cursor()
            if id_user not in id_users and country_title_local == pl and positive_feedback_count == 0 and neutral_feedback_count == 0 and meeting_transaction_count == 0 and negative_feedback_count == 0:
                id_users.append(id_user)
                driver_h.get(
                    f"https://www.vinted.pl/api/v2/users/{id}/items?page=1&per_page=20&order=relevance&currency=EUR")
                for url_itim in driver_h.requests:
                    if url_itim.url == f"https://www.vinted.pl/api/v2/users/{id}/items?page=1&per_page=20&order=relevance&currency=EUR":
                        bodys = decode(url_itim.response.body,
                                       url_itim.response.headers.get('Content-Encoding', 'identity'))
                        bodys = bodys.decode('utf-8')
                        bodys = json.loads(bodys)
                        first_items_url = bodys.get("items")[0].get('url')
                        cursor.execute("CREATE TABLE IF NOT EXISTS vinted_page_users("
                                       "id INTEGER PRIMARY KEY,"
                                       "id_user	INTEGER NOT NULL UNIQUE,"
                                       "prof_url TEXT,"
                                       "get_url_chat TEXT)")
                        cursor.execute("""
                            INSERT OR IGNORE INTO vinted_page_users (id_user,prof_url,get_url_chat)
                            VALUES (?, ?, ?)
                            """, (id_user, prof_url, first_items_url))
                        connect_sql.commit()
                        print(country_title_local, negative_feedback_count, positive_feedback_count,
                              neutral_feedback_count,
                              meeting_transaction_count, prof_url, id_user, first_items_url)
        else:
            continue


def main():
    while True:
        get_item()
        os.system("taskkill /im chromedriver.exe /f")
        os.system('taskkill /im chrome.exe /f')
        get_url_json()
        get_url_post()
        n = 90
        p = Pool(processes=1)
        p.map(multi_work, users_urls[:-n - 1:-1])
        print("finish")
        print("--- %s seconds ---" % (time.time() - start_time))
        time.sleep(20)


if __name__ == '__main__':
    main()
