import pybaseball as pyb
import pandas as pd
import sys,os

def getPlayerIdLookup(player):
    player = player.split(" ")
    return pyb.playerid_lookup(player[1],player[0])

def displayOptions():
    print("\"[-Player Name]\" -s[-Split Stat] Options for the split stats:\n")
    print("Season Totals\nPlatoon Splits\nHome or Away\nFirst or Second Half\nMonths\nBatting Order Positions\nSwung or Took First Pitch of PA\nCount/Balls-Strikes\nLeading Off Inning\nNumber of Outs in Inning\nBases Occupied\nClutch Stats\nLeverage\nTimes Facing Opponent in Game\nHit Location\nHit Trajectory\nOpponent\nGame Conditions\nBallparks")
    print("\nAdditional Pitcher Options:\n\nGame Outcome for Pitcher\nPitching Role\nRun Support\nOpposition Defensive Position\nPitch Count\nDays of Rest\nBy Umpire")
    print("\nAdditional Batter Options:\n\nGame Outcome for Team\nStarter or Substitute\nDefensive Positions\nvs. Power/Finesse Pitchers\nvs. Ground Ball/Fly Ball Pitchers")


def getPosition(player):
    p = player.split(" ")
    for i,n in enumerate(p):
        p[i] = n.capitalize()
    try:
        df = pyb.pitching_stats(2019,2021)
        g = df.loc[df['Name'] == " ".join(p)]
        if len(g) == 0:
            raise ValueError
        return "P"
    except ValueError:
        df = pyb.batting_stats(2019,2021)
        g = df.loc[df['Name'] == " ".join(p)]
        return "B"

def getStats(player,stat,pos):
    """ Gets the players stats from the two starts dictionary of players that user chooses """
    pid = getPlayerIdLookup(player)
    if pos == "P":
        df,df2 = pyb.get_splits(pid['key_bbref'].iloc[0],year=2021,pitching_splits=True) # Two sets of stats
        df, df2 = df.reset_index(), df2.reset_index()
        split2 = df2["Split Type"] == stat + " -- Game-Level"
        df2 = df2[split2].reset_index()
    elif pos == "B":
        df = pyb.get_splits(pid['key_bbref'].iloc[0],year=2021,pitching_splits=False).reset_index()
        df2 = None
    split = df["Split Type"] == stat # Months -- Game-Level
    df = df[split].reset_index()

    return df,df2

def pitchingSplits(player,stat):
    fin = pd.DataFrame()
    df,df2 = getStats(player,stat,"P")
    if len(df) == 0:
        os.system("python3 main.py -h")
        print("Error with getting stat:",stat)
        sys.exit(1)
    fin["Split"] = df["Split"]
    fin["K%"] = round(df["SO"] / df["PA"],3)
    fin["BB%"] = round(df["BB"] / df["PA"],3)
    fin["HR%"] = round(df["HR"] / df["PA"],3)
    fin["ERA"] = round(df2["ERA"],3)
    fin["AVG"] = round(df["BA"],3)
    fin["BABIP"] = round(df["BAbip"],3)
    fin["OPS"] = round(df["OPS"],3)
    return fin


def battingSplits(player,stat):
    fin = pd.DataFrame()
    df,_ = getStats(player,stat,"B")
    if len(df) == 0:
        os.system("python3 main.py -h")
        print("Error with getting stat:",stat)
        sys.exit(1)
    # HR, K%, BB%, BA, OBP, SLG, OPS, SB SBA ISO
    fin["Split"] = df["Split"]
    fin['HR/AB'] = round(df['HR'] / df['PA'],3)
    fin['K%'] = round(df['SO'] / df['PA'],3)
    fin['BB%'] = round(df['BB'] / df['PA'],3)
    fin['AVG']  = df['BA']
    fin['OBP'] = df['OBP']
    fin['SLG'] = df['SLG']
    fin['OPS'] = df['OPS']
    fin['SBA'] = df['SB'] + df['CS']
    fin['SB%'] = round(df['SB'] / fin['SBA'],3)
    fin['ISO'] = fin['SLG'] - fin['AVG']

    return fin