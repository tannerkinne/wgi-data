import time
import csv

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from datetime import date

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from urllib.parse import urlparse


def wgi_recap_links(url):

#This will open a browser window and scrape the recap links from the WGI percussion scores page.
# It uses Selenium to interact with the webpage and extract the necessary links.
    try:
        driver = webdriver.Chrome()

        driver.get(url)

        time.sleep(5)

        recaps = driver.find_elements(By.LINK_TEXT, 'Recap')

        recap_links = [recap.get_attribute('href') for recap in recaps]

        driver.close()

        print(f'Recap links for {url}: {recap_links}')

        return recap_links[::-1]

    except Exception as e:
        print(e)
        return []

def crawler(start_url):
    driver = webdriver.Chrome()

    domain = urlparse(start_url).netloc
    visited = []
    to_visit = [start_url]
    recap_links = []
    unknown_links = []

    links_on_last = False

    while to_visit:
        url = to_visit.pop(0)
        if url not in visited:
            visited.append(url)
            driver.get(url)
            time.sleep(2)
            links_found = False

            if driver.find_elements(By.NAME, "htmlComp-iframe"):
                iframe_recaps = get_iframe_links(url)
                for recap in iframe_recaps:
                    recap_links.append(recap)
                links_on_last = True
                links_found = True
            elif driver.find_elements(By.ID, 'cs-org-scores-area'):
                mouse_needed_recaps = mouse_finder(url)
                for recap in mouse_needed_recaps:
                    recap_links.append(recap)
                links_on_last = True
                links_found = True

            time.sleep(2)

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                href = link.get_attribute('href')
                if not href:
                    continue

                if href not in visited and urlparse(href).netloc == domain and 'score' in href:
                    to_visit.insert(0, link.get_attribute('href'))
                elif href not in visited and urlparse(href).netloc == domain and '.pdf' not in href:
                    to_visit.append(link.get_attribute('href'))
                elif 'recaps.competitionsuite.com' in href:
                    recap_links.append(link.get_attribute('href'))
                    links_on_last = True
                    links_found = True
                elif 'bit.ly' in href:
                    unknown_links.append(link.get_attribute('href'))

            if not links_found and links_on_last:
                break

    for link in unknown_links:
        resolved_link = resolve_url(link)
        if 'recaps.competitionsuite.com' in resolved_link:
            recap_links.append(resolved_link)

    driver.quit()
    return recap_links

def resolve_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return url

def mouse_finder(url):

    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(3)

    actions = ActionChains(driver)


    recap_links = []

    menu_button = driver.find_element(By.ID, 'cs-org-scores-menu-viewEvents')

    actions.move_to_element(menu_button).click().perform()

    time.sleep(1)

    years_area = driver.find_element(By.ID, 'cs-org-scores-area')
    years = years_area.find_elements(By.CLASS_NAME, 'event')

    for year in years:
        actions.click(year).perform()

        event_area = driver.find_element(By.ID, 'cs-org-scores-area')
        events = event_area.find_elements(By.CLASS_NAME, 'event')

        for event in events:
            actions.click(event).perform()

            time.sleep(1)

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                if link.get_attribute('href') and 'recaps.competitionsuite.com' in link.get_attribute('href'):
                    recap_links.append(link.get_attribute('href'))

            actions.click(menu_button).perform()
            time.sleep(1)

        actions.click(menu_button).perform()
        time.sleep(1)

    driver.quit()
    return recap_links



def get_iframe_links(url):

    driver = webdriver.Chrome()
    driver.get(url)

    driver.implicitly_wait(3)
    iframe = driver.find_element(By.NAME, "htmlComp-iframe")
    driver.switch_to.frame(iframe)


    year_scripts = []
    event_scripts = []
    recap_links = []
    time.sleep(3)
    menu_script = driver.find_element(By.ID, 'cs-org-scores-menu-viewEvents').find_element(By.TAG_NAME, 'a').get_attribute('onclick')
    seasons_script = driver.find_element(By.ID, 'cs-org-scores-menu-viewSeasons').find_element(By.TAG_NAME, 'a').get_attribute('onclick')


    driver.execute_script(seasons_script)

    time.sleep(3)

    years_area = driver.find_element(By.ID, 'cs-org-scores-area')
    years = years_area.find_elements(By.CLASS_NAME, 'event')

    for year in years:
        year_scripts.append(year.get_attribute('onclick'))



    for year in year_scripts:
        event_scripts = []

        driver.execute_script(year)
        # print(driver)
        time.sleep(1)
        # print(f'year: {year}')

        event_area = driver.find_element(By.ID, 'cs-org-scores-area')
        events = event_area.find_elements(By.CLASS_NAME, 'event')
        # print(f'event: {events}')

        for event in events:
            event_scripts.append(event.get_attribute('onclick'))

        for script in event_scripts:
            # print(f'script: {script}')
            #event_scripts.append(event.get_attribute('onclick'))
            driver.execute_script(script)

            time.sleep(1)

            links = driver.find_elements(By.TAG_NAME, 'a')
            for link in links:
                if link.get_attribute('href') and 'recaps.competitionsuite.com' in link.get_attribute('href'):
                    recap_links.append(link.get_attribute('href'))
            # recap_links.append([link.get_attribute('href') for link in links if 'recaps.competitionsuite.com' in link.get_attribute('href')])
            # print(f'links: {links}')
            # print(f'recalinks: {recap_links}')

            driver.execute_script(menu_script)
            time.sleep(1)

        driver.execute_script(seasons_script)
        time.sleep(1)



    driver.quit()
    return recap_links



def get_recap_data(recap_links):

# This function takes the recap links obtained from the previous function and scrapes the relevant data from each recap page.
    year_tracker = 0
    start = []

    df = pd.DataFrame(columns = ['year', 'month', 'day', 'class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual'])
    for recap_link in recap_links:

        soup = BeautifulSoup(requests.get(recap_link).content, 'html.parser')

        date_table = soup.find("table")

        try:
            date_w_year = date_table.find_all("td")[1].find_all("div")[2].text.strip().replace(',', '').split(' ')[1:4]
            if not date_w_year:
                date_w_year = date_table.find_all("td")[1].find_all("div")[1].text.strip().replace(',', '').split(' ')[1:4]
            day = date_w_year[1]
            month = date_w_year[0]
            year = date_w_year[2]

            print(f'Processing date {month} {day}, {year}')
        except IndexError:
            print(f'Error with date for {recap_link}')
            continue
        except AttributeError:
            continue


        #
        # try:
        #     date_w_year = date_table.find_all("td")[1].find_all("div")[2].text.strip().replace(',', '').split(' ')[1:4]
        #     if not date_w_year:
        #         date_w_year = date_table.find_all("td")[1].find_all("div")[1].text.strip().replace(',', '').split(' ')[1:4]
        #     # date = date_w_year[0:2]
        #     print(date_w_year)
        #     year = date_w_year[2]
        #
        # except IndexError:
        #     print(f'Error with date for {recap_link}')
        #     continue
        # except AttributeError:
        #     continue
        # if(year != year_tracker):
        #     week = get_week(date_w_year, date_w_year)
        #     start = date_w_year
        #     year_tracker = year
        # else:
        #     week = get_week(date_w_year, start)


        tables = soup.find_all("table")
        for table in tables:

            try:
                rows = table.find_all("tr", class_="header-division-name")

                if not rows:
                    rows = table.find_all('td')
                    if rows[0].text:
                        cls = ''.join(word[0] for word in rows[0].text.strip().split(' '))
                    else:
                        continue
                else:
                    cls = ''.join(word[0] for word in rows[0].find("td").text.strip().split(' '))


                # cls = ''.join(word[0] for word in rows[0].find("td").text.strip().split(' '))

                name_objs = table.select("td.content.topBorder.rightBorderDouble")
                for name_obj in name_objs:
                    name = name_obj.text.strip()
                    if ',' not in name:
                        subs = name_obj.find_next_siblings("td", class_="topBorder rightBorder subcaptionTotal verified")
                        if not subs:
                            subs = name_obj.find_next_siblings("td", class_="topBorder rightBorder subcaptionTotal")



                        sub_scores = [float(sub.find('td', class_ = 'content score').text.strip()) for sub in subs]


                        overall_score = round(float(name_obj.find_next_sibling("td", class_="topBorder rightBorderDouble").text.strip()), 3)

                        if(len(sub_scores) != 4 and len(sub_scores) != 8):
                            sub_scores = sub_scores[:(len(sub_scores)-1)]

                        if len(sub_scores) == 4:

                            music_effect = sub_scores[0]
                            visual_effect = sub_scores[1]
                            music = sub_scores[2]
                            visual = sub_scores[3]

                            df.loc[(len(df)), ['year', 'month', 'day', 'class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual']] = [year, month, day, cls, name, overall_score, music_effect, visual_effect, music, visual]
                        elif len(sub_scores) == 8:
                            music_effect = round((sub_scores[0] + sub_scores[1]) / 2, 3)
                            visual_effect = round((sub_scores[2] + sub_scores[3]) / 2, 3)
                            music = round((sub_scores[4] + sub_scores[5]) / 2, 3)
                            visual = round((sub_scores[6] + sub_scores[7]) / 2, 3)

                            df.loc[(len(df)), ['year', 'month', 'day', 'class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual']] = [year, month, day, cls, name, overall_score, music_effect, visual_effect, music, visual]


            except AttributeError as e:
                print(e)
                continue
            except IndexError as e:
                continue
            except ValueError:
                continue


    df.to_csv('scores.csv', index=False)

    weeks_df = get_week(df)

    weeks_df.to_csv('scores_with_weeks.csv', index=False)





def get_week(df):

    # This function takes a date in the format of [month, day] and calculates
    # the corresponding week number based on a fixed starting point (February 1st).
    # It uses a base dictionary to determine the cumulative number of days up to
    # the given month and then calculates the week number accordingly.

    new_df = pd.DataFrame(columns = ['year', 'week', 'class', 'name', 'overall score', 'music effect', 'visual effect', 'music', 'visual'])

    base = {"January": 1, "February": 2, "March": 3, "April": 4}

    # Map month names to numbers in a new column, then sort by it
    df['month_num'] = df['month'].map(base)
    df.sort_values(by=['year', 'month_num', 'day'], inplace=True)
    df.drop(columns=['month_num'], inplace=True)

    start_year = 0


    for idx, row in df.iterrows():
        if row['year'] != start_year:
            start_year = row['year']
            start_date = [row['month'], row['day'], row['year']]


        new_date = [row['month'], row['day'], row['year']]


        try:
            d = date(int(new_date[2]), base[new_date[0]], int(new_date[1])).isocalendar().week
            start = date(int(start_date[2]), base[start_date[0]], int(start_date[1])).isocalendar().week
            week = d - start
            new_df.loc[len(new_df)] = [row['year'], week, row['class'], row['name'], row['overall score'], row['music effect'], row['visual effect'], row['music'], row['visual']]
        except KeyError:
            print(f"Error with date for {row['name']} on {row['month']} {row['day']}, {row['year']}")


    return new_df



    # base = {"January": 1, "February": 2, "March": 3, "April": 4}
    #
    # d = date(int(new_date[2]), base[new_date[0]], int(new_date[1])).isocalendar().week
    # start = date(int(start_date[2]), base[start_date[0]], int(start_date[1])).isocalendar().week
    # return d - start


    # day = base[date[0]] + int(date[1])
    #
    # day_rounded = round(day / 7) * 7
    #
    # week = day_rounded // 7 - 6
    #
    # return week


if __name__ == "__main__":
    wgi_links = [
        "https://wgi.org/percussion/perc-scores-2022/?_gl=1*1ktv0zs*_gcl_au*MTExNDUwMTgyNy4xNzcyMjQ0ODEw*_ga*OTIzMTMxNjc3LjE3NzIyNDQ4MTA.*_ga_7BC7XFTSPV*czE3NzI3NDIzMzckbzQkZzEkdDE3NzI3NDM0ODEkajUwJGwwJGgw",
        'https://wgi.org/percussion/perc-scores-2023/?_gl=1*1ktv0zs*_gcl_au*MTExNDUwMTgyNy4xNzcyMjQ0ODEw*_ga*OTIzMTMxNjc3LjE3NzIyNDQ4MTA.*_ga_7BC7XFTSPV*czE3NzI3NDIzMzckbzQkZzEkdDE3NzI3NDM0ODEkajUwJGwwJGgw',
        'https://www.wgi.org/historical_score_per/2024/',
        'https://www.wgi.org/historical_score_per/2025/',
        'https://www.wgi.org/scores/percussion-scores/',
        #Beginning wayback machine links
        'https://web.archive.org/web/20180418041418/http://www.wgi.org:80/2017-percussion-scores/',
        'https://web.archive.org/web/20221004225547/https://www.wgi.org/2018-percussion-scores/',
        'https://web.archive.org/web/20190414064010/https://www.wgi.org/percussion/2019-perc-scores/'
    ]


    recap_links_grouped = []

    #Adding some myself
    recap_links = []

    local_links = [ #'https://www.nyspercussion.org/',
                    # 'https://www.mapsdrumlines.org/',
                    # 'https://www.armarchingarts.org/',
                    # 'https://cweaindoor.org/',
                    # 'https://www.cs-pa.org/',
                    # 'https://www.cvgpa.org/',
                    # 'https://www.etpaa.org/',
                    # 'http://gipacircuit.com/',
                    # 'https://gcgpc.org/',
                    # 'https://www.hwaa.org/',
                    'https://indianapercussion.org/',
                    # 'https://www.im-pa.org/',
                    # 'https://www.kida.org/',
                    # 'https://www.magnoliaarts.org/',
                    # 'https://www.performmapa.org/',
                    # 'https://mepa-circuit.org/',
                    # #'https://mpacircuit.org/index.php',
                    # 'https://www.ohiocircuit.org/',
                    # 'https://www.pacificperformingarts.org/',
                    # 'https://www.svwaa.com/',
                    # 'https://scpa.live/',
                    # 'https://tristatemarchingarts.org/'
                    ]

    recap_links = pd.read_csv('recap_links.csv')['links'].tolist()
    for link in local_links:
        recap_links_grouped.append(crawler(link))
    #
    # #recap_links.append(get_iframe_links('https://www.mapsdrumlines.org/scores'))
    #
    #

    # for link in wgi_links:
    #     recap_links_grouped.append(wgi_recap_links(link))

    for i in range(len(recap_links_grouped)):
        for link in recap_links_grouped[i]:
            recap_links.append(link)
    recap_links = np.unique(recap_links).tolist()
    print(recap_links)
    #
    # links_df = pd.DataFrame(recap_links, columns=['links'])
    # links_df.to_csv('recap_links.csv', index=False)

    #for when not testing or adding to scraping functions, just want to run the data collection and cleaning


    get_recap_data(recap_links)
