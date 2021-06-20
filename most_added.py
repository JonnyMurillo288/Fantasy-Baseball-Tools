import requests
import pandas as pd
import pybaseball as pyb
from bs4 import BeautifulSoup
import sys
from utils import *


def getMostAdded(lim=80):
    """ Main function that can get the most added players on CBS Fantasy """
    url = "https://www.cbssports.com/fantasy/baseball/trends/added/all/"

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    most_added = []
    table = soup.find('table',{"class":"TableBase-table"})
    for tr in table.find_all('tr'):
        name = tr.find('span',{"class":"CellPlayerName--long"})
        try:
            if int(tr.find_all('td')[2].text.strip('\n ')) < lim:
                most_added.append(name.a.text)
        except:
            pass
    return most_added

def displayMostAdded(lim=80):
    i = 0
    print("The most added players recently is:")
    for p in getMostAdded(lim):
        i+=1
        if i % 3 == 0:
            print(str(i)+".",p)
            print()
        else:
            print(str(i)+".",p,end=" ")


def splitStats(player,stat,lim=5):
    """ Get the stats for the players """
    if getPosition(player) == "P":
        return pitchingSplits(player,stat)
    elif getPosition(player) == "B":
        return battingSplits(player,stat)
    else:
        raise AttributeError ("Unable to get postiion for %s",player)

