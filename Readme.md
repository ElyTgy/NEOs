# An Application for Finding Out About Near Earth Objects:

NEO is a command line interface for quickly searching for and finding out about 
[near earth objects](https://cneos.jpl.nasa.gov/about/basics.html). Users can search for a 
particular asteroid by name or pdes(their id in the database) or look at certain near earth objects 
based on their [characteristics](https://cneos.jpl.nasa.gov/glossary/PHA.html) and import results to csv or json files.


### Commands:
* Positional arguments:
    * `query`: Shows asteroid that match certain criteria defined by the user such as. The parameters that aren'y defined will be ignored:
        * `--distance-min`: minimum distance between earth and asteroids
        * `--distance-max`:maximum distance between earth and asteroids
        * `velocity_min`: minimum velocity of asteroids
        * `velocity_max`: minimum velocity of asteroids
        * `--date`: date that asteroids pass earth
        * `--start-date`: asteroids that pass earth after this date
        * `--end-date`: asteroids that pass earth before this date
        * `hazardous`: asteroids that are recognized as hazardous
    * `inspect`: Specifically look for an asteroid by looking at its name or database id:
        * `--name`: Find asteroid with the following name.
        * `--pdes`: Find asteroid with the followig `pdes`.
        * `verbose`: Also print all known close approaches of this asteroid
    * `interactive`: Inspect and query objects at the same time. Prevents loading files everytime and speeds up the program.
* optional arguments:
    * `--neofile`: Path to CSV file of near-Earth objects.
    * `--cadfile`: Path to JSON file of close approach data.

    ---

    ### Data:
    The data is divided between two files, both of which are from [nasas Jet Propultion Laboratory](https://www.jpl.nasa.gov/). 
    
    * Data about NEOs:
        * The [neos file](https://github.com/ElyTgy/NEOs/blob/main/data/neos.csv) is a csv file containing information about the near earth objects detected by nasa. It has information about their names, diameter, wheather they are hazardous or not and many other things. Not all the information in the file is used in the application. The data was gathered from [nasas website](https://ssd.jpl.nasa.gov/sbdb_query.cgi).
    * Data about approaches of NEOs:
        * Stored as a [json file](https://github.com/ElyTgy/NEOs/blob/main/data/cad.json), the file contains data about various objects that have approached earth before or will in the future. It contains data like their velocity, the date of their approach, their name, and so on. The data was queried from [nasa SBDB API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html).

---

### Dependencies:
There are no dependencies. Just run the following command with parameters you want.

````python3 main.py````

