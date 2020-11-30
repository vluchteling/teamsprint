import urllib.request
import json
with urllib.request.urlopen("https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json") as url:
    data = json.loads(url.read().decode())
file_name = 'finalAIteam1.txt'
f = open(file_name, 'w')
# open file in write mode
json.dump(data, f)
f.close()
