from app import db

class CensusTract(db.Model):
    '''A county of an US State.'''
    
    def __init__(self, census_tract, census_tract_number, county, geojson):
        self.census_tract = census_tract
        self.census_tract_number = census_tract_number
        self.county = county
        self.geojson = geojson

    id = db.Column(db.Integer, primary_key=True)
    geojson_id = db.Column(db.Integer, db.ForeignKey('geo_json_feature.id'), nullable=True)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    census_tract = db.Column(db.String(128), index=False, nullable=False, unique=True)
    census_tract_number = db.Column(db.String(128), index=False, nullable=False, unique=True)

    geojson = db.relationship('GeoJsonFeature', uselist=False, backref='census_tract', lazy=False)
 
