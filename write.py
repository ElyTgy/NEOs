"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 
    'name', 'diameter_km', 'potentially_hazardous')
    
    rows = []
    for close_approach in results:
        name = close_approach.neo.name
        if close_approach.neo.name == None:
            name = ''

        name = close_approach.neo.name
        if close_approach.neo.name == None:
            name = ''
        
        curr_row = [
            str(close_approach.time),
            str(close_approach.distance),
            str(close_approach.velocity),
            str(close_approach._designation),
            name,
            str(close_approach.neo.diameter),
            str(close_approach.neo.hazardous).capitalize()]
        rows.append(curr_row)

    with open(f"{filename}.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for row in rows:
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.


if __name__ == '__main__':
    var = str(float('nan'))
    print("False".capitalize())