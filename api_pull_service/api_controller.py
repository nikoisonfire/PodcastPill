import hashlib
import json
import time
from datetime import date

import requests

from api_pull_service.Podcast import Podcast
from api_pull_service.utils import weigh_drops, remove_html_tags


def calculate_auth_headers(environment):
    api_key = environment["PCI_API_KEY"]
    api_secret = environment["PCI_API_SECRET"]

    # we'll need the unix time
    epoch_time = int(time.time())

    # our hash here is the api key + secret + time
    data_to_hash = api_key + api_secret + str(epoch_time)
    # which is then sha-1'd
    sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

    return {
        'X-Auth-Date': str(epoch_time),
        'X-Auth-Key': api_key,
        'Authorization': sha_1,
        'User-Agent': 'podtester-v1'
    }
def pull_frequency_data(data, headers, numberOfPods):
    items = []

    for idx, val in enumerate(data):
        if idx < numberOfPods:
            pod_id = val["id"]
            url = f"https://api.podcastindex.org/api/1.0/episodes/byfeedid?id={pod_id}&max=30"
            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                episodes = json.loads(r.text)
                weekdays = [0] * 7
                for y in episodes["items"]:
                    dt = date.fromtimestamp(y["datePublished"])
                    weekdays[dt.weekday()] += 1

                drops = [x > 0 for x in weekdays]
                frequency = [x / sum(weekdays) for x in weekdays]
                weighted = weigh_drops(drops, frequency)

                title = val["title"].replace("'", "").replace('"', '')
                description = val["description"].replace("'", "").replace('"', '')
                description = remove_html_tags(description)

                podcast = Podcast(
                    id=pod_id,
                    title=title,
                    description=description,
                    image=val["image"],
                    categories=val["categories"].values(),
                    weightedDrops=weighted
                )
                items.append(podcast)