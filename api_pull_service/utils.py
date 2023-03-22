import json
import re

import numpy


def weigh_drops(drops_list, frequency_list):
    drops = [0] * 7
    for idx, element in enumerate(drops_list):
        if element is True:
            drops[idx] = 1

    # Multiply with the frequency to get an accurate representation of
    drops = numpy.multiply(drops, frequency_list)
    return drops.tolist()


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def load_file(filename: str):
    with open(filename, "r") as file:
        return json.load(file)
