import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.workbook import Workbook

## Take user input for valid years
valid = False

while not valid:
    selected_year = input("What Year 1990 - 2022 ")
    if int(selected_year) > 1990 and int(selected_year) < 2023:
        valid = True


def data_to_spreadsheet(year):
    url = "https://www.pro-football-reference.com/years/{}/fantasy.htm".format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html)

    ##Skip first header due to irrelevant data
    headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
    headers = headers[1:]

    ## Finding all data rows and parsing them, skipping the first couple due to them not containing relevant info
    rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != 'thead')
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range (len(rows))]
    player_stats = player_stats[2:]

    ## Creating DataFrame and removing all blank data entries
    stats = pd.DataFrame(player_stats, columns = headers)
    stats = stats.replace(r'', 'N/A', regex = True)


    ## Removing irrelevant data points
    stats = stats.drop(columns=["Age"])
    stats = stats.drop(columns=["2PM"])
    stats = stats.drop(columns=["2PP"])
    stats = stats.drop(columns=["FantPt"])
    stats = stats.drop(columns=["DKPt"])
    stats = stats.drop(columns=["FDPt"])
    stats = stats.drop(columns=["VBD"])

    ## Changing data point names to make them more readable
    stats = stats.rename(columns={"Y/R": "Yards/Rush"})
    stats = stats.rename(columns={"Y/A": "Yards/Attempt"})

    ## Creating spreadsheet
    stats.to_excel('{}FantasyPlayerStats.xlsx'.format(year), index = False)


data_to_spreadsheet(selected_year)


