import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl.workbook import Workbook


selected_year = input("What Year 1990 - 2022 ")


def data_to_spreadsheet(year):
    url = "https://www.pro-football-reference.com/years/{}/fantasy.htm".format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html)

    headers = [th.getText() for th in soup.findAll('tr')[1].findAll('th')]
    headers = headers[1:]

    rows = soup.findAll('tr', class_ = lambda table_rows: table_rows != 'thead')
    player_stats = [[td.getText() for td in rows[i].findAll('td')] for i in range (len(rows))]
    player_stats = player_stats[2:]

    stats = pd.DataFrame(player_stats, columns = headers)
    stats = stats.replace(r'', 'N/A', regex = True)
    stats = stats.replace(' 0', 'N/A', regex = True)
    stats = stats.drop(columns=["Age"])
    stats = stats.drop(columns=["2PM"])
    stats = stats.drop(columns=["2PP"])
    stats = stats.drop(columns=["FantPt"])
    stats = stats.drop(columns=["DKPt"])
    stats = stats.drop(columns=["FDPt"])
    stats = stats.drop(columns=["VBD"])
    stats = stats.rename(columns={"Y/R": "Yards/Rush"})
    stats = stats.rename(columns={"Y/A": "Yards/Attempt"})
    stats.to_excel('{}FantasyPlayerStats.xlsx'.format(year), index = False)


data_to_spreadsheet(selected_year)


