import itertools
from models import CloseApproach
from helpers import bt_floats, lt_floats
from datetime import date



"""The arguments used by ArgumentParser and for filtering NEOs/closeapproaches"""
DISTANCE_MIN = "distance_min"
DISTANCE_MAX = "distance_max"
DIAMETER_MIN = "diameter_min"
DIAMETER_MAX = "diameter_max"
VELOCITY_MIN = "velocity_min"
VELOCITY_MAX = "velocity_max"
DATE = "date"
START_DATE = "start_date"
END_DATE = "end_date"
HAZARDOUS = "hazardous"


def clean_args_dict(args:dict, minimum_valid_date:date, maximum_valid_date:date) -> dict:
    """Clean a dictionary of arguments taken from user input by setting any `None` item
    that has a key with `min` or `start` in it to the lowest value possible and any key with
    `end` or max` to the highest value possible. Other values will be left unchanged"""
    
    args = dict(args) #copy so that we wont modify the actual dictionary
    for key, val in args.items():
        if 'min' in key:
            if val == None:
                #all keys with min are floats
                args[key] = float('-inf')
        elif 'max' in key:
            if val == None:
                #all keys with max are floats
                args[key] = float('inf')
        elif 'start' in key:
            if val == None:
                #all keys with start are dates
                args[key] = minimum_valid_date
        elif 'end' in key:
            if val == None:
                #all keys with end are dates
                args[key] = maximum_valid_date
    return args


def is_valid_close_approach(approach:CloseApproach, restrictions:dict) -> bool:
    """Check if the close approach object is valid based on the restriction in the dictionary.
    
    :param approach: a close approach instance object
    :param clean_restrictions: a dictionary of the values the user entered in the query command
    in their 'clean' form; Meaning that minimum and maximum values are set to the minimum and
    maximum values accessible and none of them can be `None` except for filters that don't
    represent a maxmium or minimum(like hazardous and date)
    :return: a boolean represnting if `approach` is valid"""

    if not (bt_floats(approach.distance, float(restrictions[DISTANCE_MIN])) and 
            lt_floats(approach.distance, float(restrictions[DISTANCE_MAX]))):
        return False

    if not (bt_floats(approach.neo.diameter, float(restrictions[DIAMETER_MIN])) and 
            lt_floats(approach.neo.diameter, float(restrictions[DIAMETER_MAX]))):
        return False

    if not (bt_floats(approach.velocity, float(restrictions[VELOCITY_MIN])) and 
            lt_floats(approach.velocity, float(restrictions[VELOCITY_MAX]))):
        return False

    if restrictions["date"] != None and approach.time.date() != restrictions[DATE]:
        return False

    if not (approach.time.date() > restrictions[START_DATE] and 
            approach.time.date() < restrictions[END_DATE]):
        return False

    if restrictions[HAZARDOUS] != None and approach.neo.hazardous != restrictions[HAZARDOUS]:
        return False

    return True


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    if n == 0 or n == None:
        return iterator
    return itertools.islice(iterator, n)
