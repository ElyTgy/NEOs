import datetime
from helpers import cd_to_datetime, bt_floats, lt_floats
from typing import Union
from extract import *



class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        
        des_to_neo = {}
        for neo in neos:
            des_to_neo[neo.designation] = neo
        
        for close_approach in approaches:
            try:
                curr_des = des_to_neo[close_approach._designation]
                close_approach.neo = curr_des
                curr_des.approaches.append(close_approach)
            except KeyError:
                #designation doesnt exist
                print("skipped an approach")
                continue
        
        #TODO: Use sets
        self._neos = des_to_neo.values()
        self._approaches = approaches
            

    def get_neo_by_designation(self, designation:str) -> Union[None, NearEarthObject]:
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.
        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        for neo in self._neos:
            if neo.designation == designation:
                return neo            
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.
        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        for neo in self._neos:
            if neo.name == name:
                return neo            
        return None

    @property
    def max_time(self):
        """find the time of the asteroid furthest in the future in nasas database"""
        max_date = self._approaches[0].time
        for approach in self._approaches:
            if approach.time > max_date:
                max_date = approach.time 
        return max_date

    @property
    def min_time(self):
        """find the time of the earliest recorded asteroid in nasas database"""
        min_date = self._approaches[0].time
        for approach in self._approaches:
            if approach.time < min_date:
                min_date = approach.time 
        return min_date

    def query(self, args):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        #handle None values that havent been entered
        for key, val in args.items():
            if key[-3:] == 'min':
                if val == None:
                    args[key] = float('-inf')
            elif key[-3:] == 'max':
                if val == None:
                    args[key] = float('inf')
            elif key[:5] == 'start':
                if val == None:
                    args[key] = self.min_time.date()
            elif key[:3] == 'end':
                if val == None:
                    args[key] = self.max_time.date()


        #TODO: Save str fields of args somewhere as well (in a tuple of strings) as well as query keyword
        for approach in self._approaches:
            
            if not (bt_floats(approach.distance, float(args["distance_min"])) and 
            lt_floats(approach.distance, float(args["distance_max"]))):
                continue

            if not (bt_floats(approach.neo.diameter, float(args["diameter_min"])) and 
            lt_floats(approach.neo.diameter, float(args["diameter_max"]))):
                continue

            if not (bt_floats(approach.velocity, float(args["velocity_min"])) and 
            lt_floats(approach.velocity, float(args["velocity_max"]))):
                continue

            if args["date"] != None:
                if approach.time.date() != args["date"]:
                    continue
            
            if not (approach.time.date() > args["start_date"] and 
                approach.time.date() <  args["end_date"]):
                    continue

            if args["hazardous"] != None and approach.neo.hazardous != args["hazardous"]:
                continue
     
            yield approach


if __name__ == "__main__":
    db = NEODatabase(load_neos(getcwd() + "\\data\\neos.csv"), load_approaches(getcwd() + "\\data\\cad.json"))
    print(db.max_time)