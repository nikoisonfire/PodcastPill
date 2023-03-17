
# setup some basic vars for the search api. 
# for more information, see https://api.podcastindex.org/developer_docs
import calendar
from datetime import date
import hashlib
import json
import time
import requests


api_key = 'WXRKPNKDNC3FKJNWLZYV'
api_secret = 'MRZucBTzP9SJ3RWNuxGFcx^V4xYCwdh5ZFsku2EY'


# we'll need the unix time
epoch_time = int(time.time())

# our hash here is the api key + secret + time 
data_to_hash = api_key + api_secret + str(epoch_time)
# which is then sha-1'd
sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

headers = {
    'X-Auth-Date': str(epoch_time),
    'X-Auth-Key': api_key,
    'Authorization': sha_1,
    'User-Agent': 'podtester-v1'
}

with open("podcast_data.json", "r") as file:
    data = json.load(file)


"""
    ideal data format:
    {
        "id": ...
        "title": ...
        "description": ...
        "image": ...
        "categories": {...}
        
        // To categorize on which weekdays an episode of the pod drops
        "drops": [True, False, True, ...]

        // Some podcasts drop infrequently on certain days, so use weights 
        // to roll more certain predictions which podcasts are going to reliably drop
        "frequency": [x/sum(last40) for x in last40]
    }
"""

for idx, val in enumerate(data):
    if(idx < 10):
        id = val["id"]
        url = f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={id}&max=40"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            episodes = json.loads(r.text)
            weekdays = [0, 0, 0, 0, 0, 0, 0]
            for y in episodes["items"]:
                dt = date.fromtimestamp(y["datePublished"])
                weekdays[dt.weekday()] += 1
            info = {
                "id": val["id"],
                "title": val["title"],
                "description": val["description"],
                "image": val["image"],
                "categories": val["categories"],
                "drops": [x > 0 for x in weekdays],
                "frequency": [x/sum(weekdays) for x in weekdays]
            }
            print(json.dumps(info, indent=2))