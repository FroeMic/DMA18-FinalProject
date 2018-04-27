from app import db
import json

class County(db.Model):
    '''A county of an US State.'''
    
    def __init__(self, county, county_code, state, geojson, avg_loan):
        self.county = county
        self.county_code = county_code
        self.state = state
        self.geojson = geojson
        self.avg_loan = avg_loan

    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    county = db.Column(db.String(128), index=False, nullable=False, unique=True)
    county_code = db.Column(db.String(128), index=False, nullable=False, unique=True)
    avg_loan = db.Column(db.Float, index=False, nullable=True, unique=False)
    geojson = db.Column(db.Text, nullable=False, unique=False)

    census_tracts = db.relationship('CensusTract', backref='county', lazy=True)

    @property
    def serialize(self):
       return {
           'type': 'county',
           'state': self.state.state,
           'state_code': self.state.state_code,
           'county': self.county,
           'county_code': self.county_code,
           'avg_loan': float('{:10.2f}'.format(self.avg_loan * 1000)),
           'census_tract': None,
           'census_tract_number': None,
           'geojson': json.loads(self.geojson)
       }