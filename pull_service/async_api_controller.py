import asyncio
import hashlib
import json
import logging
import time
from datetime import date

import aiohttp
from dotenv import dotenv_values

from db_service.db_controller import write_to_db
from pull_service.Podcast import Podcast
from pull_service.utils import load_file, remove_html_tags, weigh_drops


def calculate_auth_headers(environment):
    if "PCI_API_KEY" not in environment:
        return
    if "PCI_API_SECRET" not in environment:
        return

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


async def get(url, session):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(e)


async def main(env_config, pod_data, start_idx=0, iterations=20):
    items = []
    length = slice(start_idx, start_idx + iterations)
    headers = calculate_auth_headers(env_config)
    api_url = "https://api.podcastindex.org/api/1.0/episodes/byfeedid?id="
    max_episodes = "30"

    connector = aiohttp.TCPConnector(limit=50)
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        responses = await asyncio.gather(
            *[get(f"{api_url}{item['id']}&max={max_episodes}", session) for item in pod_data[length]]
        )
        for idx, response in enumerate(responses):
            if idx % 100 == 0:
                logging.info(f"Processing batch {idx + start_idx}")
                # await asyncio.sleep(1)

            try:
                episodes = json.loads(response)
            except json.decoder.JSONDecodeError:
                continue

            weekdays = [0] * 7

            pod = pod_data[idx + start_idx]

            for episode in episodes["items"]:
                dt = date.fromtimestamp(episode["datePublished"])
                weekdays[dt.weekday()] += 1

            drops = [x > 0 for x in weekdays]
            frequency = [x / sum(weekdays) for x in weekdays]
            weighted = weigh_drops(drops, frequency)

            title = pod["title"].replace("'", "").replace('"', '')
            description = pod["description"].replace("'", "").replace('"', '')
            description = remove_html_tags(description)

            podcast = Podcast(
                id=pod["id"],
                title=title,
                description=description,
                image=pod["image"],
                categories=pod["categories"].values(),
                weightedDrops=weighted
            )
            items.append(podcast)
    return items


if __name__ == "__main__":
    config = dotenv_values("../.env")
    data = load_file("podcast_data.json")

    t1 = time.perf_counter()

    items = asyncio.run(main(env_config=config, pod_data=data, start_idx=800, iterations=200))

    write_to_db(items, config["DB_PATH"])

    t2 = time.perf_counter()

    print(f"Finished all batches in {t2 - t1} seconds")
