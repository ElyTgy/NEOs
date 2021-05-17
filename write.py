import csv
import json
from helpers import datetime_to_str



FIELD_NAMES = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 
    'name', 'diameter_km', 'potentially_hazardous')

def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    
    rows = []
    for close_approach in results:
        name = close_approach.neo.name
        if close_approach.neo.name == None:
            name = ''

        name = close_approach.neo.name
        if close_approach.neo.name == None:
            name = ''
        
        curr_row = [
            datetime_to_str(close_approach.time),
            str(close_approach.distance),
            str(close_approach.velocity),
            str(close_approach._designation),
            name,
            str(close_approach.neo.diameter),
            str(close_approach.neo.hazardous).capitalize()]
        rows.append(curr_row)

    with open(f"{filename}.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(FIELD_NAMES)
        for row in rows:
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    objs = []
    for result in results:
        obj = {}
        name = str(result.neo.name)
        if name == None:
            name = ''

        obj[FIELD_NAMES[0]] = datetime_to_str(result.time)
        obj[FIELD_NAMES[1]] = result.distance
        obj[FIELD_NAMES[2]] = result.velocity
        obj['neo'] = {}
        obj['neo'][FIELD_NAMES[3]] = str(result.neo.designation)
        obj['neo'][FIELD_NAMES[4]] = name
        obj['neo'][FIELD_NAMES[5]] = str(result.neo.diameter)
        obj['neo'][FIELD_NAMES[6]] = result.neo.hazardous
        objs.append(obj)

    with open(f"{filename}.json", 'w') as file:
        json.dump(objs, fp=file)
