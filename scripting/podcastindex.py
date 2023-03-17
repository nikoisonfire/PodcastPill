from dotenv import dotenv_values
import hashlib
import json
import time
from datetime import date

import numpy
import requests
from mysql.connector import connect, Error

config = dotenv_values("../.env")


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


api_key = config["PCI_API_KEY"]
api_secret = config["PCI_API_SECRET"]

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
    if idx < 5:
        pod_id = val["id"]
        url = f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={pod_id}&max=30"
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
                "frequency": [x / sum(weekdays) for x in weekdays]
            }
            print(f"added {val['title']}")
            items.append(info)

print("item length: ", len(items))

try:
    with connect(
            host=config["MYSQL_HOST"],
            user=config["MYSQL_USER"],
            password=config["MYSQL_PW"]
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

                cursor.execute(insert_podcasts)

                cats = item["categories"].values()
                params = [(x,) for x in cats]

                insert_categories = f'''
                    INSERT INTO podcastpill.categories
                    (podcast_id, category)
                    VALUES (
                        "{item["id"]}", 
                        %s
                    );
                '''

                cursor.executemany(insert_categories, params)

                drops = [0] * 7
                for idx, element in enumerate(item["drops"]):
                    if element is True:
                        drops[idx] = 1

                # Multiply with the frequency to get an accurate representation of
                drops = numpy.multiply(drops, item["frequency"])
                drops = drops.tolist()

                insert_drops = f'''
                    INSERT INTO `podcastpill`.`drops`
                    (`podcast_id`, `dropsMonday`, `dropsTuesday`,`dropsWednesday`,`dropsThursday`,`dropsFriday`,`dropsSaturday`,`dropsSunday`)
                    VALUES (
                        "{item["id"]}", 
                        "{drops[0]}", 
                        "{drops[1]}", 
                        "{drops[2]}", 
                        "{drops[3]}",
                        "{drops[4]}",
                        "{drops[5]}",
                        "{drops[6]}"
                    );                
                '''

                cursor.execute(insert_drops)

                con.commit()
                print(f"pushed {item['title']} to DB")

except Error as e:
    print(e)
