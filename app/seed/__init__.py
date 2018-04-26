#from app import db
#from app.models import CensusTract, County, State, Coordinate, Polygon, GeoJsonFeature
#import sys
#sys.path.append('/Users/rohankapuria/Downloads/01Spring2018/DMA/FinalProject/DMA18-FinalProject-Server')
import app
from app import db
from app.models import CensusTract, County, State

import json
import simplejson

def seed_database():
    ''' Seeds the database '''
    pass
    filepath = './app/data/2016_California_HDMA.json'
    seed_file = open(filepath).read()
    seed_file = str(seed_file).strip('\n')
    seed_file = str(seed_file).strip(';')
    json_data = json.loads(seed_file)

    create_state(json_data)

def create_state(json_data):
    state = json_data['state']
    stateCode = json_data['state_code']
    avgData = json_data['avg_loan']
    stateGeojson = create_geojsonfeature(json_data['geojson'])
    state = State(state,stateCode,stateGeojson,avgData)
    db.session.add(state)
    db.session.commit()

    create_counties(state, json_data['counties'])


def create_counties(state, json_counties):
    for countyDict in json_counties:
        create_county(state, countyDict)


def create_county(state, countyDict):
    countyName = countyDict['county']
    countyCode = countyDict['county_code']
    avgData = countyDict['avg_loan']
    countyGeojson = create_geojsonfeature(countyDict['geojson'])
    county = County(countyName, countyCode, state, countyGeojson, avgData)
    db.session.add(county)
    db.session.commit()

    create_censustracts(county, countyDict['census_tracts'])


def create_censustracts(county, censusTractList):
    for censusTract in censusTractList:
        create_censustract(county,censusTract)


def create_censustract(county, censusTract):
    censusTractName = censusTract['census_tract']
    censusTractNumber = censusTract['census_tract_number']
    avgData = censusTract['avg_loan']
    censusTractGeojson = create_geojsonfeature(censusTract['geojson'])
    censusTractObj = CensusTract(censusTractName, censusTractNumber, county, censusTractGeojson, avgData)

    db.session.add(censusTractObj)
    db.session.commit()


def create_geojsonfeature(json_geojson):
    return simplejson.dumps(json_geojson, indent=4, sort_keys=False)
 