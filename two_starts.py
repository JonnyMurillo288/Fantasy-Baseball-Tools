from collections import defaultdict
from collections import defaultdict
import requests
import sys, os
import pybaseball as pyb
import pandas as pd
import sqlite3
from bs4 import BeautifulSoup


def getTwoStarts():
    """ Main funtion that will be called at the start of the program to get all pitchers with two starts 
    and their opponents into a dictionary
     """
    url = "https://www.cbssports.com/fantasy/baseball/two-start-pitchers/"

    r = requests.get(url)
    soup = BeautifulSoup(r.content,"html.parser")

    two_starters = defaultdict(list)
    table = soup.find('table',{"class","TableBase-table"})
    for tr in table.find_all("tr"):
        i = 0 #index of player,
            #EX           i = 0               i = 1               i = 2
            # === Tyler Glassnow === ===== OPPONENT 1 ===== ==== OPPONENT 2 =====
        starter = None
        for a in tr.find_all("span",{"class","CellPlayerName--short"}):
            if i == 0:
                a = str(a)
                try: # jon-lester
                    spl = a.split("/")[5].split("-")
                    if len(spl) > 2:
                        starter = "-".join(spl[:-1]) + " " +spl[-1]
                    else:
                        starter = " ".join(spl)
                except IndexError:
                    break
                i += 1
            else:
                opp = a.find("span",{"class","CellPlayerName-team"})
                if starter != None:
                    two_starters[starter].append(opp.text.replace(" ",'').replace("\n",""))
        if starter == None:
            continue
        if len(two_starters[starter]) == 1:
            for o in tr.find_all("span",{"class","CellPitcherMatchup-opponent"}):
                opp = str(o.find("a")).split("teams/")[1][:3]
                if opp not in two_starters[starter]:
                    two_starters[starter].append(opp)
    return two_starters


def displayMatchups(player_dict):
    """ Displays the matchups for the week of two start pitchers and their opponents """
    for k,v in player_dict.items():
        print("Pitcher:\n" +" ".join([x.capitalize() for x in k.split(" ")]) + ":","\n  Opp 1:",v[0],"\n  Opp 2:",v[1])
        print()



def getStats(player,stat):
    """ Gets the players stats from the two starts dictionary of players that user chooses """
    fin = pd.DataFrame()
    player = player.split(" ")
    pid = pyb.playerid_lookup(player[1],player[0])
    df,df2 = pyb.get_splits(pid['key_bbref'].iloc[0],year=2021,pitching_splits=True) # Two sets of stats
    df, df2 = df.reset_index(), df2.reset_index()
    split = df["Split Type"] == stat # Months -- Game-Level
    df = df[split].reset_index()
    split2 = df2["Split Type"] == stat + " -- Game-Level"
    df2 = df2[split2].reset_index()
    if len(df) == 0:
        os.system("python3","cbsScraper","-h")
        print("Error with getting stat:",stat)
        sys.exit(1)
    # K%, BB%, HR%,, ERA, AVG/Babip, OPS 
    fin["Split"] = df["Split"]
    fin["K%"] = round(df["SO"] / df["PA"],3)
    fin["BB%"] = round(df["BB"] / df["PA"],3)
    fin["HR%"] = round(df["HR"] / df["PA"],3)
    fin["ERA"] = round(df2["ERA"],3)
    fin["AVG"] = round(df["BA"],3)
    fin["BABIP"] = round(df["BAbip"],3)
    fin["OPS"] = round(df["OPS"],3)
    return fin

def displayOptions():
    print("\"[-Pitcher Name]\" -s[-Split Stat] Options for the split stats:\n")
    print("Season Totals\nPlatoon Splits\nHome or Away\nFirst or Second Half\nMonths\nGame Outcome for Pitcher\nPitching Role\nRun Support\nBatting Order Positions\nSwung or Took First Pitch of PA\nCount/Balls-Strikes\nLeading Off Inning\nOpposition Defensive Position\nNumber of Outs in Inning\nBases Occupied\nClutch Stats\nLeverage\nTimes Facing Opponent in Game\nPitch Count\nDays of Rest\nHit Location\nHit Trajectory\nOpponent\nGame Conditions\nBallparks\nBy Umpire")

def main(arg,number=None):
    """ 
    PARAMS: arg- the argument to tell the program what to run
    Optional number- the number that the arg is indexed at in arg

    Tells the program what to run
    -h displays the options
    -d displays the pitchers and their matchups for the week
    -s stat to look at and print the splits for the pitcher for the year
        ARG[0] = cbsScraper
        ARG[1] = pitcher name (make sure to put the whole name in quotes)
        ARG[2] = -s option
        ARG[3] = Split Stat to search for
    """
    ts = getTwoStarts()
    if arg in ['-h','-help']:
        displayOptions()
    if arg in ["-d","-display"]:
        displayMatchups(ts)
    if arg in ["-stat",'-s']:
        
        p = sys.argv[1].lower() # Pitcher name
        if p not in ts:
            print("Pitcher:",p, "not in list")
            print([i for i in ts.keys()])
            sys.exit(1)
        s = sys.argv[number+1] # Split Stats
        print(p,"splits for:",s,"\n", getStats(p,s))


if __name__ == '__main__':
    for i,arg in enumerate(sys.argv):
        main(arg,i)
