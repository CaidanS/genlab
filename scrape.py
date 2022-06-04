from bs4 import BeautifulSoup
from itertools import permutations
import pandas as pd
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class Scraper():

    # Subset for testing
    alphabet = 'ab' 
    
    # Full alphabet
    # alphabet = 'abcdefghijklmnopqrstuvwxyz'

    base_url = 'https://search.k-state.edu/?qt={}&curtab=1'
    people_collection = []
    sleeptime = 2

    def __init__(self, path_to_chromdriver):
        self.path_to_chromdriver = path_to_chromdriver

    def scrape(self):
        for two_letter_combo in permutations(self.alphabet, 2):
            url = self.base_url.replace('{}', ''.join(two_letter_combo))
            print(url)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('window-size=1920x1080')
            driver = webdriver.Chrome(self.path_to_chromdriver, options=chrome_options)
            driver.get(url)
            time.sleep(self.sleeptime)
            squadPage=driver.page_source
            soup = BeautifulSoup(squadPage, 'html.parser')

            people = soup.find_all('div', class_="peopleResult")
            # print(people)
            for person in people:
                if person.find('dt', class_="student name"):
                    name = person.find('dt', class_="student name").string
                    name = re.sub(r'\s{2,}', ' ', name)
                    email = person.find('dd', class_="focus").find('a').string
                    discription = person.find('dd', class_="stuPlan").string
                    discription = str(discription).replace('"', '')
                    try:
                        grade = re.search('(.*Masters|PhD|Freshman|Sophomore|Junior|Senior)(.*)', str(discription)).group(1)
                        course = re.search('(.*Masters|PhD|Freshman|Sophomore|Junior|Senior)(.*)', str(discription)).group(2)                        
                        print(grade,course)
                    except AttributeError:
                        grade = 'Not Found'
                        course = str(discription)
                    if course == '' or course == None:
                            course = 'Not Found'
                    eid = person['eid']
                    self.people_collection.append([str(name), str(email), str(eid), str(grade), str(course) ,str(discription)])
    
    def clean_data(self):
        self.df = pd.DataFrame(data=self.people_collection, columns= ['name', 'email', 'eid', 'grade', 'course', 'full discription']) 
        self.df.drop_duplicates(subset=['email'], inplace= True)
    
    def write_data(self, path):
        self.df.to_csv(path)

if __name__ == '__main__':
    # Add the correct path here
    s = Scraper('./chromedriver')
    s.scrape()
    s.clean_data()
    s.write_data('data.csv')