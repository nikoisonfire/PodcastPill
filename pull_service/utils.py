import json
import logging
import re
from typing import List

import numpy


def weigh_drops(drops_list: List[bool], frequency_list: List[float]):
    drops = [0] * 7
    for idx, element in enumerate(drops_list):
        if element is True:
            drops[idx] = 1

    # Multiply with the frequency to get an accurate representation of
    drops = numpy.multiply(drops, frequency_list)
    return drops.tolist()


def remove_html_tags(text: str):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def load_file(filename: str):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        logging.exception("Error loading file")

