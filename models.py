from typing import List
from math import isnan
import datetime



"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation:str, hazardous:bool, name:str=None, 
                diameter:float=float('nan')):
        """Create a new `NearEarthObject`.

        :param designation: A string representing an object's internal database id
        :param name: A string representing the human-readable name. May be None.
        :param diameter: a float representing object diameter(from equivilant sphere).
        NaN if no data is available
        :param hazardous: bool representing wheather it is a PHA
        :approaches: A list of the objects close approaches to earth
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous
        
        self.approaches:List[CloseApproach] = []


    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        rv = self.designation
        if(self.name):
            rv = f"{rv} ({self.name})"
        return rv


    def __str__(self):
        """Return `str(self)`."""
        rv = f"The Near-Earth Object {self.fullname} "
        if not isnan(self.diameter):
            rv += f"has a diameter of {self.diameter:.3f} km and "
        rv+= "is "
        if not self.hazardous:
            rv += "not "
        rv += "potentially hazardous."
        return rv


    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, 'name={self.name!r}', "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation:str, cd_time:str, distance:float, velocity:float):
        """Create a new `CloseApproach`.

        :param designation: String representing .
        """
        self._designation = designation
        self.time = cd_to_datetime(cd_time)
        self.distance = distance
        self.velocity = velocity

        self.neo = None


    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.
        """
        return datetime_to_str(self.time)


    def __str__(self):
        """Return `str(self)`."""

        approach_time = "approached"
        if datetime.datetime.now() < self.time:
            approach_time = "will approach"

        return( f"On {self.time_str}, {self.neo.fullname} {approach_time} earth, "
        f"at a distance of {self.distance:.2f} km and a velocity of {self.velocity:.2f} km/s")


    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")
