#from app import db
#from app.models import CensusTract, County, State, Coordinate, Polygon, GeoJsonFeature
#import sys
#sys.path.append('/Users/rohankapuria/Downloads/01Spring2018/DMA/FinalProject/DMA18-FinalProject-Server')
import app
from app import db
from app.models import CensusTract, County, State, Coordinate, Polygon, GeoJsonFeature

import json

def seed_database():
    ''' Seeds the database '''
    pass
    filepath = './app/data/2016_California_HDMA.json'
    seed_file = open(filepath).read()
    seed_file = str(seed_file).strip('\n')
    seed_file = str(seed_file).strip(';')
    json_data = json.loads(seed_file)
    #create_geojsonfeature(json_data['geojson'])

    create_state(json_data)

def create_state(json_data):
    state = json_data['state']
    stateCode = json_data['state_code']
    stateGeojson = create_geojsonfeature(json_data['geojson'])
    state = State(state,stateCode,stateGeojson)
    db.session.add(state)
    db.session.commit()

    create_counties(state, json_data['counties'])


def create_counties(state, json_counties):
    for countyDict in json_counties:
        create_county(state, countyDict)



def create_county(state, countyDict):
    countyName = countyDict['county']
    countyCode = countyDict['county_code']
    countyGeojson = create_geojsonfeature(countyDict['geojson'])
    county = County(countyName, countyCode, state, countyGeojson)
    db.session.add(county)
    db.session.commit()
    create_censustracts(county, countyDict['census_tracts'])


def create_censustracts(county, censusTractList):
    for censusTract in censusTractList:
        create_censustract(county,censusTract)


def create_censustract(county, censusTract):
    censusTractName = censusTract['census_tract']
    censusTractNumber = censusTract['census_tract_number']
    censusTractGeojson = create_geojsonfeature(censusTract['geojson'])
    censusTractObj = CensusTract(censusTractName, censusTractNumber, county, censusTractGeojson)

    db.session.add(censusTractObj)
    db.session.commit()


def create_geojsonfeature(json_geojson):
    '''
      "geojson": {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -123.233256,
                        42.006186
                    ],
                    ...
                ],
                ...
            ]
        }
    }
    '''
    #print('json_geojson', json_geojson)
    coordinates_lists = json_geojson['geometry']['coordinates']
    coordinates_lists = coordinates_lists if coordinates_lists is not None else []
    polygons = []
    for coordinates_list in coordinates_lists:
        polygons.append(create_polygon(coordinates_list))

    geojsonfeature = GeoJsonFeature(polygons)
    db.session.add(geojsonfeature)
    db.session.commit()
    return geojsonfeature


def create_polygon(json_polygon):
    ''' json_polygon is e.g.  [ [2134324.323, 2121.4343] ]'''
    #print('json_polygon', json_polygon)
    coordinates = []
    for json_coordinate in json_polygon:
        coordinates.append(create_coordinate(json_coordinate))

    polygon = Polygon(coordinates)
    db.session.add(polygon)
    db.session.commit()

    for coordinate in coordinates:
        coordinate.polygon_id = polygon.id
    db.session.commit()

    return polygon

def create_coordinate(json_coordinate):
    ''' json_coordinates is e.g. [2134324.323, 2121.4343]'''
    #print('json_coordinate', json_coordinate)
    lng = json_coordinate[0]
    lat = json_coordinate[1]
    lng = type(lng) is list if lng[0] else lng
    lat = type(lat) is list if lat[0] else lat
    coordinate = Coordinate(json_coordinate[0], json_coordinate[1])
    db.session.add(coordinate)
    db.session.commit()
    return coordinate


# seed_database()
