from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import csv

CONFIG = {
    "waitingTime": 1, # waiting time for page loading in seconds
    "links": {
        "loginPage": "https://linkedin.com/uas/login",
        "aboutPage": "https://www.linkedin.com/company/COMPANY/about"
    },
    "auth": {
        "email": "EMAIL",
        "password": "PASSWORD"
    },
    "selectors": {
        "login": {
            "username": "username",
            "password": "password",
            "loginBtn": "//button[@type='submit']"
        },
        "about": {
            "name": ".t-24.t-black.t-bold.full-width > span",
            "website": ".link-without-visited-state > span",
            "number_of_employees": ".artdeco-card.p5.mb4 > .overflow-hidden > .text-body-small.t-black--light.mb1",
            "HQ": ".org-location-card.pv2 > p"
        }
    },
    "companies": ['oxus-ai', 'linkedin', 'google', 'facebook', 'twitter', 'amazon', 'microsoft']
}


def login(driver):  
    # Open login page 
    driver.get(CONFIG['links']['loginPage'])
    
    # give page time to load
    time.sleep(CONFIG['waitingTime'])

    # entering email
    email = driver.find_element_by_id(CONFIG['selectors']['login']['username'])
    email.send_keys(CONFIG['auth']['email'])  
    
    # entering password
    password = driver.find_element_by_id(CONFIG['selectors']['login']['password'])
    password.send_keys(CONFIG['auth']['password'])        
    
    # clicking login
    driver.find_element_by_xpath(CONFIG['selectors']['login']['loginBtn']).click()




def getCompanyData(driver, company):
        
    #navigate to company's profile
    driver.get(CONFIG['links']['aboutPage'].replace('COMPANY', company))

    # waiting for the profile to load
    time.sleep(CONFIG['waitingTime'])

    # scrape the html and pass it to bs
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    
    # The following getting the desired data and strip it and make sure to give None to it if it's not exist
    
    name = soup.select(CONFIG['selectors']['about']['name'])
    if(len(name) > 0) :
        name = name[0].text.strip()
    else:
        name = None
    
    website = soup.select(CONFIG['selectors']['about']['website'])
    if(len(website) > 0) :
        website = website[0].text.strip()
    else:
        website = None
    
    numberOfEmployees = soup.select(CONFIG['selectors']['about']['number_of_employees'])
    if(len(numberOfEmployees) > 0) :
        numberOfEmployees = numberOfEmployees[0].text.strip().split(' ')[0]
    else:
        numberOfEmployees = None
    
    HQ = soup.select(CONFIG['selectors']['about']['HQ'])
    if(len(HQ) > 0) :
        HQ = HQ[0].text.strip()
    else:
        HQ = None
        
    return [name, website, numberOfEmployees, HQ]



    

def main():
    # Creating webdriver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    # login with email and password
    login(driver)

    # scrape data and save it to csv
    header = ['Name', 'Website', 'Number of employees', 'HQ']
    with open('companies.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)
        for company in CONFIG['companies']:
            # write the data
            writer.writerow(getCompanyData(driver, company))


main()
