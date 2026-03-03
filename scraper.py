import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
from collections import defaultdict

def get_recap_links(url):

#This will open a browser window and scrape the recap links from the WGI percussion scores page.
# It uses Selenium to interact with the webpage and extract the necessary links.

    from selenium import webdriver
    from selenium.webdriver.common.by import By

    driver = webdriver.Chrome()

    driver.get('https://www.wgi.org/scores/percussion-scores/')

    recaps = driver.find_elements(By.LINK_TEXT, 'Recap')

    recap_links = [recap.get_attribute('href') for recap in recaps]

    driver.close()

    return recap_links

def get_recap_data(recap_links):

# This function takes the recap links obtained from the previous function and scrapes
# the scores for each performance. It uses BeautifulSoup to parse the HTML content of
# each recap page and extract the relevant data. The scores are stored in a dictionary
# where the keys are the names of the performers and the values are their overall scores.

    scores = defaultdict(lambda: {
        "overall": None
    })

    for recap_link in recap_links:

        soup = BeautifulSoup(requests.get(recap_link).content, 'html.parser')

        cells = soup.select("td.content.topBorder.rightBorderDouble")

        for c in cells:
            name = c.text.strip()
            score = c.find_next_sibling("td", class_="topBorder rightBorderDouble").text.strip()
            if ',' not in name and float(score) > (scores[name]["overall"] or 0):
                scores[name]["overall"] = round(float(score), 3)

    return scores

if __name__ == "__main__":
    recap_links = get_recap_links('https://www.wgi.org/scores/percussion-scores/')
    recap_data = get_recap_data(recap_links)
    for key, value in sorted(recap_data.items()):
        print(f"{key}: {value['overall']}")
