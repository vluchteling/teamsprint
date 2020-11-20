import re
import json
import requests
url = 'https://raw.githubusercontent.com/tijmenjoppe/AnalyticalSkills-student/master/project/data/steam.json'
resp = requests.get(url)
resp_parsed = re.sub(r"^jsonp\d+\(|\)\s+$", "", resp.text)
data = json.loads(resp_parsed)
file_name = 'finalAIteam1.txt'
f = open(file_name, 'w')
# open file in append mode
for i in data:
    text = str(i) + "\n"
    f.write(text)
f.close()