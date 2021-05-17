import json
import csv
from models import NearEarthObject, CloseApproach
import typing
from math import isnan
from os import getcwd



def load_neos(neo_csv_path) -> typing.List[NearEarthObject]:
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos = []
    
    with open(neo_csv_path) as file:
        reader = csv.DictReader(file)
        for line in reader:
            curr_neo_params = {}

            curr_neo_params['designation'] = line['pdes']
            
            if line['pha'] == 'Y':
                curr_neo_params['hazardous'] = True
            else:
                curr_neo_params['hazardous'] = False

            if line['name'] != '':
                curr_neo_params['name'] = line['name']

            if line['diameter'] != '':
                curr_neo_params['diameter'] = float(line['diameter'])

            neos.append(NearEarthObject(**curr_neo_params))

    return neos


def load_approaches(cad_json_path) -> typing.List[CloseApproach]:
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    close_approaches = []
    
    with open(cad_json_path) as file:
        reader = json.load(file)
        field_to_index = {}
        for i in range(len(reader['fields'])):
            field_to_index[reader['fields'][i]] = i

        for obj_index in range(int(reader['count'])):
            curr_query = reader['data'][obj_index]
            close_approaches.append(CloseApproach(
                                    designation=  curr_query[field_to_index['des']],
                                    cd_time=      curr_query[field_to_index['cd']],
                                    distance=float(curr_query[field_to_index['dist']]),
                                    velocity=float(curr_query[field_to_index['v_rel']]))) 

    return close_approaches

def approaches_count(cad_json_path) -> int:
    """Number of close_approched listed in the json file

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: Number of close approaches.
    """
    
    with open(cad_json_path) as file:
        reader = json.load(file)
        return int(reader['count'])


if __name__ == "__main__":
    n = approaches_count(getcwd()+'\\data\\cad.json')
    print(n)