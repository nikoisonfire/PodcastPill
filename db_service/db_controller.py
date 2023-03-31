import logging
import sqlite3
from typing import List

from pull_service.Podcast import Podcast


def write_to_db(podcast_list: List[Podcast], path_to_db_file: str):
    try:
        with sqlite3.connect(path_to_db_file) as con:
            cur = con.cursor()
            for podcast in podcast_list:
                insert_podcasts = """
                    INSERT INTO podcasts
                    (podcast_id, title, description, image)
                    VALUES (
                        '{id}', 
                        '{title}', 
                        '{description}', 
                        '{image}'
                    );
                """.format(id=podcast.id, title=podcast.title, description=podcast.description, image=podcast.image)

                cur.execute(insert_podcasts)

                cats = podcast.categories
                params = [(x,) for x in cats]

                insert_categories = """
                    INSERT INTO categories
                    (podcast_id, category)
                    VALUES (
                        '{id}', 
                        ?
                    );
                """.format(id=podcast.id)

                cur.executemany(insert_categories, params)

                insert_drops = """
                    INSERT INTO drops
                    (`podcast_id`, `dropsMonday`, `dropsTuesday`,`dropsWednesday`,`dropsThursday`,`dropsFriday`,`dropsSaturday`,`dropsSunday`)
                    VALUES (
                        '{id}', 
                        '{0}', 
                        '{1}', 
                        '{2}', 
                        '{3}',
                        '{4}',
                        '{5}',
                        '{6}'
                    );                
                """.format(id=podcast.id, *podcast.weightedDrops)

                cur.execute(insert_drops)

                con.commit()
                logging.info(f"Write {podcast.id} to DB done.")

    except sqlite3.Error as e:
        logging.exception("Error using MySQL")


def get_pod_ids_from_db(path_to_db_file: str) -> List[int]:
    try:
        with sqlite3.connect(path_to_db_file) as con:
            cur = con.cursor()
            cur.execute("SELECT podcast_id FROM podcasts")
            return cur.fetchall()
    except sqlite3.Error as e:
        logging.exception("Error using MySQL")
