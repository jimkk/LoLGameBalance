import requests
import time


class APIHelper:
    region = "na"
    api_url = "https://" + region + ".api.pvp.net"
    api_key = ""
    cdn = ""
    cdn_versions = {}
    champions = {}

    def __init__(self, region , api_key=""):
        if api_key == "":
            self.api_key = raw_input("Enter the API Key: ")
        else:
            self.api_key = api_key
        self.region = region

    def getCDN(self):
        url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/realm"
        params = {'api_key': self.api_key}
        r = requests.get(url, params=params)
        data = r.json()
        self.cdn = data['cdn']
        self.cdn_versions = data['n']

    def getChampions(self):
        champion_url = self.api_url + "/api/lol/static-data/" + \
            self.region + "/v1.2/champion"
        params = {'api_key': self.api_key}
        r = requests.get(champion_url, params=params)
        self.champions = r.json()['data']

    def getChampionInfo(self, id):
        if len(self.champions) == 0:
            self.getChampions()
        for champion in self.champions:
            if self.champions[champion]['id'] == id:
                return self.champions[champion]['name']
        return ""

    def getChampionFromSkinName(self, skin):
        skin_words = skin.split(' ')
        champion = skin_words[len(skin_words) - 1]
        if champion in self.champions:
            return champion
        else:
            return "Unknown"

    def getSkinNumber(self, champion, skin_name):
        champion_num = str(self.champions[champion]['id'])
        url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champion_num
        params = {'api_key': self.api_key, 'champData': 'skins'}
        r = requests.get(url, params=params)
        data = r.json()['skins']
        for skin in data:
            if skin['name'] == skin_name:
                return skin['num']
        return None

    def getChampionImages(self, champion_name="", skin=""):
        skin_num = 0
        if skin != "":
            if champion_name == "":
                champion_name = self.getChampionFromSkinName(skin)
            skin_num = self.getSkinNumber(champion_name, skin)
            if skin_num == None:
                return None
        url = self.cdn + "/img/champion/loading/" + champion_name + "_" + str(skin_num) + ".jpg"
        return url

    def getSummonerID(self, name):
        url = self.api_url + "/api/lol/" + self.region + "/v1.4/summoner/by-name/" + name
        params = {'api_key': self.api_key}
        r = requests.get(url, params=params)
        data = r.json()
        return data[name.lower()]['id']

    def getSummonerRank(self, id):
        url = self.api_url + "/api/lol/" + self.region + "/v2.5/league/by-summoner/" + str(id) + "/entry"
        params = {'api_key': self.api_key}
        r = requests.get(url, params=params)
        if r.status_code == 404:
            return -1
        if r.status_code == 429:
            time.sleep(3)
            r = requests.get(url, params=params)
        data = r.json()
        try:
            if data['status']['status_code'] == 429:
                time.sleep(5)
                r = requests.get(url, params=params)
                data = r.json()
        except:
            pass
        rank = 0
        for entries in data[str(id)]:
            if(entries['queue'] == "RANKED_SOLO_5x5"):
                tier = entries['tier']
                if tier == "BRONZE" :
                    pass
                elif tier == "SILVER":
                    rank = 5
                elif tier == "GOLD":
                    rank = 10
                elif tier == "PLATINUM":
                    rank = 15
                elif tier == "DIAMOND":
                    rank = 20
                elif tier == "MASTER":
                    rank = 25
                else:
                    rank = 26
                if rank < 25:
                    division = entries['entries'][0]['division']
                    if division == "V":
                        pass
                    elif division == "IV":
                        rank += 1
                    elif division == "III":
                        rank += 2
                    elif division == "II":
                        rank += 3
                    elif division == "I":
                        rank += 4
        return rank


        return

    def getRecentGames(self, id):
        url = self.api_url + "/api/lol/" + self.region + "/v1.3/game/by-summoner/" + str(id) + "/recent"
        params = {'api_key': self.api_key}
        r = requests.get(url, params=params)
        data = r.json()['games']
        return data

    def getMMBalance(self, summoners, default=0):
        balance = 0
        for summoner in summoners:
            rank = self.getSummonerRank(summoner[0])
            if rank == -1:
                rank = default
            if summoner[1] == 100:
                balance += rank
            else:
                balance -= rank
        return balance
