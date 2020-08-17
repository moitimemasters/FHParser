from selenium import webdriver
from msedge.selenium_tools import EdgeOptions, Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import TOKEN, ADMIN_ID
import requests
from getpass import getpass
from worker import FLHWorker
from bs4 import BeautifulSoup
from time import sleep
from teleapi import ApiWorker
from pprint import pprint

# options only for EDGE
options = EdgeOptions()
options.use_chromium = True
options.add_argument("headless")
options.add_argument('disable-gpu')
options.add_argument("log_level 3")


telegram = ApiWorker(TOKEN)
url = "https://freelancehunt.com/"


def auth():
    login = input("Введите логин от FreelanceHunt: ")
    password = getpass("Теперь пароль: ")
    return login, password


# only for EDGE
driver = Edge(EdgeChromiumDriverManager().install(),
              options=options)


def get_last_url():
    with open("last_url.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


def set_last_url(new_url):
    with open("last_url.txt", "w", encoding="utf-8") as f:
        return f.write(new_url)


def log_in(login, password, driver):
    driver.get(url)
    keep_btn = driver.find_element_by_xpath(
        "/html/body/div[10]/div/div/form/div[3]/div/a[1]")
    keep_btn.click()

    sleep(2)

    login_btn = driver.find_element_by_xpath(
        "/html/body/div[1]/div/div/div/div[1]/div[2]/a[1]")
    login_btn.click()

    sleep(2)

    input_form = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[3]/div[1]/form/div[1]/div/input")
    input_form.send_keys(login)

    sleep(2)

    password_from = driver.find_element_by_xpath(
        "/html/body/div[1]/div[2]/div/div[3]/div[1]/form/div[2]/div/input")
    password_from.send_keys(password + "\n")
    return driver


def poll(driver):
    while True:
        driver.refresh()
        sleep(5)
        lenta_bnt = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/a/span[1]")
        lenta_bnt.click()
        sleep(5)
        link = driver.find_element_by_xpath(
            "/html/body/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/ul/table/tbody/tr[1]/td[1]/a[2]")
        href = link.get_attribute("href")
        last_link = get_last_url()
        if last_link != href:
            print(link.text)
            link_to_send = "*Найден новый проект: *" + \
                "[%s](%s)" % (link.text, href)
            worker = FLHWorker(href)
            title = "*Описание проекта:*"
            description = worker.get_description()
            status = "*Статус:* _" + worker.get_status() + "_"
            author = "*Автор: *" + worker.get_author()
            bids = "*Кол-во ставок: *_" + str(worker.get_bids_count()) + "_"
            price = "*Цена:* `" + worker.get_price() + "`"
            total_message = "\n".join(
                [link_to_send, author, status, price, bids, title, description])
            pprint(telegram.send_message(ADMIN_ID, total_message))
            set_last_url(href)


if __name__ == "__main__":
    '''
        Все значения sleep были вручную подобраны, можете регулировать их самостоятельно
        или же используйте implicity wait.
    '''
    login, password = auth()
    logged = log_in(login, password, driver)
    poll(logged)
