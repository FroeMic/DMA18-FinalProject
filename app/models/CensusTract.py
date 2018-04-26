from app import db
import json

class CensusTract(db.Model):
    '''A county of an US State.'''

    def __init__(self, census_tract, census_tract_number, county, geojson, avg_loan):
        self.census_tract = census_tract
        self.census_tract_number = census_tract_number
        self.county = county
        self.geojson = geojson
        self.avg_loan = avg_loan

    id = db.Column(db.Integer, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey('county.id'), nullable=False)
    census_tract = db.Column(db.String(128), index=False, nullable=False, unique=False)
    census_tract_number = db.Column(db.String(128), index=False, nullable=False, unique=False)
    avg_loan = db.Column(db.Float, index=False, nullable=True, unique=False)
    
    geojson = db.Column(db.Text, nullable=False, unique=False)

    @property
    def serialize(self):
       return {
           'type': 'census',
           'state': self.county.state.state,
           'state_code': self.county.state.state_code,
           'county': self.county.county,
           'county_code': self.county.county_code,
           'avg_loan': self.avg_loan,
           'census_tract': self.census_tract,
           'census_tract_number': self.census_tract_number,
           'geojson': json.loads(self.geojson)
       }
