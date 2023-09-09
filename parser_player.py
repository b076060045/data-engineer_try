import requests

import pandas as pd

import sys

def parser_player(year = sys.argv[1]):
    name = []
    country = []
    pointsPg = []
    assistsPg = []
    blocksPg = []
    efficiency = []
    rebsPg = []
    stealsPg = []
    turnoversPg = []
    assists = []
    blocks = []
    rebs = []
    steals = []
    turnovers = []
    for x in range(20):
        page = x
        url = f"https://china.nba.cn/stats2/league/playerstats.json?conference=All&country=All&individual=All&locale=zh_CN&pageIndex={page}&position=All&qualified=false&season={year}&seasonType=2&split=All+Team&statType=rebounds&team=All&total=perGame"
        req = requests.get(url)
        if req.json()['payload']['players']:
            for y in req.json()['payload']['players']:
                name.append(y['playerProfile']['code'])
                country.append(y['playerProfile']['countryEn'])
                pointsPg.append(y['statAverage']['pointsPg'])
                assistsPg.append(y['statAverage']['assistsPg'])
                blocksPg.append(y['statAverage']['blocksPg'])
                efficiency.append(y['statAverage']['efficiency'])
                rebsPg.append(y['statAverage']['rebsPg'])
                stealsPg.append(y['statAverage']['stealsPg'])
                turnoversPg.append(y['statAverage']['turnoversPg'])
                assists.append(y['statTotal']['assists'])
                blocks.append(y['statTotal']['blocks'])
                rebs.append(y['statTotal']['rebs'])
                steals.append(y['statTotal']['steals'])
                turnovers.append(y['statTotal']['turnovers'])
        else:
            break

    df = pd.DataFrame({'name':name, 
                       'country':country, 
                       'pointsPg':pointsPg, 
                       'assistsPg':assistsPg, 
                       'blocksPg':blocksPg, 
                       'efficiency':efficiency, 
                       'rebsPg':rebsPg, 
                       'stealsPg':stealsPg, 
                       'turnoversPg':turnoversPg,
                       'assists':assists,
                       'blocks':blocks,
                       'rebs':rebs,
                       'steals':steals,
                       'turnovers':turnovers})
    return df

if __name__ == '__main__':
    df = parser_player()
    print(df)