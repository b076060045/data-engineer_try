import requests

import pandas as pd

import sys

#爬取NBA數據  球隊 常規賽

def parser_team(season = sys.argv[1]):

    season = season
    type = '2'
    url = f'https://china.nba.cn/stats2/league/teamstats.json?conference=All&division=All&locale=zh_CN&season={season}&seasonType={type}'

    stat = requests.get(url)

    name = []
    city = []
    displayConference = []
    division = []
    assistsPg = []
    blocksPg = []
    fgaPg = []
    fgmPg = []
    foulsPg = []
    rebsPg = []
    stealsPg = []
    turnoversPg = []
    assists = []
    blocks = []
    fga = []
    fgm = []
    fouls = []
    rebs = []
    steals = []
    turnovers = []


    for x in stat.json()['payload']['teams']:
        name.append(x['profile']['name'])
        city.append(x['profile']['city'])
        displayConference.append(x['profile']['displayConference'])
        division.append(x['profile']['division'])
        assistsPg.append(x['statAverage']['assistsPg'])
        blocksPg.append(x['statAverage']['blocksPg'])
        fgaPg.append(x['statAverage']['fgaPg'])
        fgmPg.append(x['statAverage']['fgmPg'])
        foulsPg.append(x['statAverage']['foulsPg'])
        rebsPg.append(x['statAverage']['rebsPg'])
        stealsPg.append(x['statAverage']['stealsPg'])
        turnoversPg.append(x['statAverage']['turnoversPg'])
        assists.append(x['statTotal']['assists'])
        blocks.append(x['statTotal']['blocks'])
        fga.append(x['statTotal']['fga'])
        fgm.append(x['statTotal']['fgm'])
        fouls.append(x['statTotal']['fouls'])
        rebs.append(x['statTotal']['rebs'])
        steals.append(x['statTotal']['steals'])
        turnovers.append(x['statTotal']['turnovers'])

    df = pd.DataFrame({'name':name, 
                         'city':city, 
                         'displayConference':displayConference,
                         'division':division,
                         'assistsPg':assistsPg,
                         'blocksPg':blocksPg,
                         'fgaPg':fgaPg,
                         'fgmPg':fgmPg,
                         'foulsPg':foulsPg,
                         'rebsPg':rebsPg,
                         'stealsPg':stealsPg,
                         'turnoversPg':turnoversPg,
                         'assists':assists,
                         'blocks':blocks,
                         'fga':fga,
                         'fgm':fgm,
                         'fouls':fouls,
                         'rebs':rebs,
                         'steals':steals,
                         'turnovers':turnovers})
    return df


if __name__ == '__main__':
    df = parser_team()
    print(df)