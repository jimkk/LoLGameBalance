import riotAPIHelper
import sys

rankedOnly = False
summonerName = ""

if len(sys.argv) < 2:
    print("Please supply a summoner name.")
    exit()
summonerName = sys.argv[1]
if len(sys.argv) > 2:
    if sys.argv[2] == "ranked":
        rankedOnly = True

riotAPI = riotAPIHelper.APIHelper('na')
id = riotAPI.getSummonerID(summonerName)
rank = riotAPI.getSummonerRank(id)
games = riotAPI.getRecentGames(id)

for game in games:
    if rankedOnly and game['subType'] != "RANKED_SOLO_5x5":
        continue
    teamID = game['teamId']
    championPlayed = riotAPI.getChampionInfo(game['championId'])
    summonerIDs = [[id, teamID]]
    for player in game['fellowPlayers']:
        summonerIDs.append([player['summonerId'], player['teamId']])
    MMBalance = riotAPI.getMMBalance(summonerIDs, default=rank)
    if teamID == 100:
        print("%s\t%s\t%s" % (game['subType'], championPlayed, MMBalance))
    else:
        print("%s\t%s\t%s" % (game['subType'], championPlayed, -MMBalance))
