import logging

from api_pull_service.Podcast import Podcast
from typing import List
from mysql.connector import connect, Error


def write_to_db(podcast_list: List[Podcast], environment):
    try:
        with connect(
                host=environment["MYSQL_HOST"],
                user=environment["MYSQL_USER"],
                password=environment["MYSQL_PW"]
        ) as con:
            with con.cursor() as cursor:
                for podcast in podcast_list:
                    insert_podcasts = """
                        INSERT INTO podcastpill.podcasts
                        (podcast_id, title, description, image)
                        VALUES (
                            '{id}', 
                            '{title}', 
                            '{description}', 
                            '{image}'
                        );
                    """.format(id=podcast.id, title=podcast.title, description=podcast.description, image=podcast.image)

                    cursor.execute(insert_podcasts)

                    cats = podcast.categories
                    params = [(x,) for x in cats]

                    insert_categories = """
                        INSERT INTO podcastpill.categories
                        (podcast_id, category)
                        VALUES (
                            '{id}', 
                            %s
                        );
                    """.format(id=podcast.id)

                    cursor.executemany(insert_categories, params)

                    insert_drops = """
                        INSERT INTO `podcastpill`.`drops`
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

                    cursor.execute(insert_drops)

                    con.commit()
                    logging.info(f"Write {podcast.id} to DB done.")

    except Error as e:
        logging.exception("Error using MySQL")
