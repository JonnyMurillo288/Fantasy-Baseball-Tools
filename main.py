import sys
from most_added import *
from two_starts import *
from utils import *

def main(arg,number=None):
    """ 
    PARAMS: arg- the argument to tell the program what to run
    Optional number- the number that the arg is indexed at in arg

    Tells the program what to run
    -h displays the options
    -d displays the pitchers and their matchups for the week
        ARG = "two starts" shows just two start pitchers
        ARG = "most added" shows most added players recently on CBS
    -s stat to look at and print the splits for the pitcher for the year
        ARG[0] = main.py
        ARG[1] = player name (make sure to put the whole name in quotes)
        ARG[2] = -flag option
        ARG[3] = Split Stat to search for
    """
    if arg in ['-d','-display']:
        if sys.argv[-1] not in ['-d','-display'] and sys.argv[-1] in ['two starts','most added']:
            if sys.argv[-1] == 'two starts':
                displayMatchups()
            elif sys.argv[-1] == 'most added':
                displayMostAdded()
        else:
            displayMostAdded()
            displayMatchups()
    if arg in ['-s','-stats']:
        player = sys.argv[number-1]
        print(player,"stats are:\n",splitStats(player,sys.argv[number+1]))
    if arg in ['-h','-help']:
        displayOptions()


if __name__ == '__main__':
    for i,arg in enumerate(sys.argv):
        main(arg,i)
