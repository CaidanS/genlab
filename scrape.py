from bs4 import BeautifulSoup
from itertools import permutations
import pandas as pd

from selenium import webdriver
from bs4 import BeautifulSoup
import time


alphabet = 'abcdefghijklmnopqrstuvwxyz'
alphabet = 'ab'
base_url = 'https://search.k-state.edu/?qt={}&curtab=1'
people_collection = [['name', 'email', 'eid','discription']]
sleeptime = 1

for two_letter_combo in permutations(alphabet, 2):
    url = base_url.replace('{}', ''.join(two_letter_combo))
    print(url)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('window-size=1920x1080');
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)
    driver.get(url)
    time.sleep(sleeptime)
    squadPage=driver.page_source
    soup = BeautifulSoup(squadPage, 'html.parser')

    people = soup.find_all('div', class_="peopleResult")
    print(people)
    for person in people:
        if person.find('dt', class_="student name"):
            name = person.find('dt', class_="student name").string
            email = person.find('dd', class_="focus").find('a').string
            eid = person['eid']
            discription = person.find('dd', class_="stuPlan").string
            people_collection.append([name, email, eid, discription])
            # print(people_collection)
print(people_collection)