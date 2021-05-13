import json
import csv
from models import NearEarthObject, CloseApproach
import typing
from math import isnan

#TODO: Refactor code in this file

#class loader. Attributes: tuple of headers, load_csv, load_json static functions
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
        
            #TODO: Change with a call to load_approaches
            curr_neo_params['approaches'] = []

            if line['name'] != '':
                curr_neo_params['name'] = line['name']

            if line['diameter'] != '':
                curr_neo_params['diameter'] = float(line['diameter'])

            neos.append(NearEarthObject(**curr_neo_params))

    return neos


def load_approaches(cad_json_path) -> typing.List[CloseApproach]:
    #TODO: Update for the new __init__ method of CloseApproach
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
        print(field_to_index)

        for obj_index in range(int(reader['count'])):
            close_approaches.append(CloseApproach(designation=reader['data'][obj_index][field_to_index['des']],
                                    cd_time=reader['data'][obj_index][field_to_index['cd']],
                                    distance=float(reader['data'][obj_index][field_to_index['dist']]),
                                    velocity=float(reader['data'][obj_index][field_to_index['v_rel']]))) 

    return close_approaches


if __name__ == "__main__":
    load_approaches('I:\\NEOs\\data\\cad.json')