# Fantasy-Baseball-Tools


### Current Tools
- Two start pitchers for the week
- Most added players recently on CBS

##### How To Run
`python3 main.py [-arguments]`

- Current Commands:
    - [-h or -help] displays the help menu and split stats
    - [-d or -display] displays the pitchers with two starts next week and their matchups
        - Optional:
        - ARG = "two starts" shows just two start pitchers
        - ARG = "most added" shows most added players recently on CBS
    - ["Player Name"] [-s of -stats] <"Split Stat">

- Split Stat Options
    - Season Totals
    - Platoon Splits
    - Home or Away
    - First or Second Half
    - Months
    - Batting Order Positions
    - Swung or Took First Pitch of PA
    - Count/Balls-Strikes
    - Leading Off Inning
    - Number of Outs in Inning
    - Bases Occupied
    - Clutch Stats
    - Leverage
    - Times Facing Opponent in Game
    - Hit Location
    - Hit Trajectory
    - Opponent
    - Game Conditions
    - Ballparks

- Additional Pitcher Options:

    - Game Outcome for Pitcher
    - Pitching Role
    - Run Support
    - Opposition Defensive Position
    - Pitch Count
    - Days of Rest
    - By Umpire

- Additional Batter Options:

    - Game Outcome for Team
    - Starter or Substitute
    - Defensive Positions
    - vs. Power/Finesse Pitchers
    - vs. Ground Ball/Fly Ball Pitchers

- Pitching Stats will show:
[K%    BB%    HR%  ERA    AVG  BABIP    OPS]
- Hitting Stats will show:
[HR/AB     K%    BB%    AVG    OBP    SLG    OPS  SBA  SB%    ISO]