import urllib.request
import json

text = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=420AB17541C350F11D8B840D85F9E1B6&steamid=76561197995118880&format=json&include_appinfo=true"
with urllib.request.urlopen(text) as url:
    data = json.loads(url.read().decode())
file_name = 'finalAIteam1.txt'
f = open(file_name, 'w')
# open file in write mode
json.dump(data, f)
f.close()
