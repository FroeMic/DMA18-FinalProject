from app import db
from app.models import CensusTract, County, State, Coordinate, Polygon, GeoJsonFeature

import json

def seed_database():
    ''' Seeds the database '''
    pass

    filepath = './app//data/2016_California_HDMA.json'
        
    seed_file = open(filepath).read()
    seed_file = str(seed_file).strip('\n')
    seed_file = str(seed_file).strip(';')
        
    json_data = json.loads(seed_file)

    # !Create a new State object
    print(json_data['state'])
