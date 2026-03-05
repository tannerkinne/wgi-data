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

# This function takes the recap links obtained from the previous function and scrapes the relevant data from each recap page.


    df = pd.DataFrame(columns = ['class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual'])
    for recap_link in recap_links:



        soup = BeautifulSoup(requests.get(recap_link).content, 'html.parser')


        tables = soup.find_all("table")
        for table in tables:

            try:
                rows = table.find_all("tr", class_="header-division-name")

                cls = ''.join(word[0] for word in rows[0].find("td").text.strip().split(' '))

                name_objs = table.select("td.content.topBorder.rightBorderDouble")
                for name_obj in name_objs:
                    name = name_obj.text.strip()
                    if ',' not in name:
                        subs = name_obj.find_next_siblings("td", class_="topBorder rightBorder subcaptionTotal verified")

                        sub_scores = [float(sub.find('td', class_ = 'content score').text.strip()) for sub in subs]

                        overall_score = round(float(name_obj.find_next_sibling("td", class_="topBorder rightBorderDouble").text.strip()), 3)

                        if len(sub_scores) == 4:

                            music_effect = sub_scores[0]
                            visual_effect = sub_scores[1]
                            music = sub_scores[2]
                            visual = sub_scores[3]

                            df.loc[(len(df)), ['class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual']] = [cls, name, overall_score, music_effect, visual_effect, music, visual]


            except AttributeError as e:
                print(e)
            except IndexError:
                continue
    df.to_csv('scores.csv', index=False)


if __name__ == "__main__":
    recap_links = get_recap_links('https://www.wgi.org/scores/percussion-scores/')
    get_recap_data(recap_links)
