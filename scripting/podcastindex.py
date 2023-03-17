
# setup some basic vars for the search api. 
# for more information, see https://api.podcastindex.org/developer_docs
import calendar
from datetime import date
import hashlib
import json
import sys
import time
import requests

from mysql.connector import connect, Error

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

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

items = []

for idx, val in enumerate(data):
    if(idx < 30):
        id = val["id"]
        url = f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={id}&max=30"
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
            print(f"added {val['title']}")
            items.append(info)

print("item length: ", len(items))

try:
    with connect(
        host="localhost",
        user="root",
        password="Naki1996ihg"
    ) as con:
        with con.cursor() as cursor:
            for item in items:
                item["title"] = item["title"].replace("'", "").replace('"', '')
                item["description"] = item["description"].replace("'", "").replace('"', '')

                insert_podcasts = f'''
                    INSERT INTO podcastpill.podcasts
                    (podcast_id, title, description, image)
                    VALUES (
                        "{item["id"]}", 
                        "{item["title"]}", 
                        "{remove_html_tags(item["description"])}", 
                        "{item["image"]}"
                    );
                '''


                cats = [""] * 4
                for idx, element in enumerate(item["categories"].values()):
                    if idx < 3:
                        cats[idx] = element
                
                insert_categories = f'''
                    INSERT INTO podcastpill.categories
                    (podcast_id, category1, category2, category3, category4)
                    VALUES (
                        "{item["id"]}", 
                        "{cats[0]}", 
                        "{cats[1]}", 
                        "{cats[2]}", 
                        "{cats[3]}"
                    );
                '''

                drops = [0] * 7
                for idx, element in enumerate(item["drops"]):
                    if element is True:
                        drops[idx] = 1

                insert_drops = f'''
                    INSERT INTO `podcastpill`.`drops`
                    (`podcast_id`, `dropsMonday`, `dropsTuesday`,`dropsWednesday`,`dropsThursday`,`dropsFriday`,`dropsSaturday`,`dropsSunday`,`weights`)
                    VALUES (
                        "{item["id"]}", 
                        "{drops[0]}", 
                        "{drops[1]}", 
                        "{drops[2]}", 
                        "{drops[3]}",
                        "{drops[4]}",
                        "{drops[5]}",
                        "{drops[6]}",
                        "{item["frequency"]}"
                    );                
                '''

                cursor.execute(insert_podcasts)
                cursor.execute(insert_categories)
                cursor.execute(insert_drops)
                
                con.commit()
                print(f"pushed {item['title']} to DB")
        
except Error as e:
    print(e)