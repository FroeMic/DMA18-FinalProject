from app import db
import json

class State(db.Model):
    '''A US State.'''

    def __init__(self, state, state_code, geojson):
        self.state = state
        self.state_code = state_code
        self.geojson = geojson

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(128), index=False, nullable=False, unique=True)
    state_code = db.Column(db.String(128), index=False,  nullable=False, unique=True)
    geojson = db.Column(db.Text, nullable=False, unique=False)

    counties = db.relationship('County', backref='state', lazy=True)

    @property
    def serialize(self):
       return {
           'type': 'state',
           'state': self.state,
           'state_code': self.state_code,
           'county': None,
           'county_code': None,
           'census_tract': None,
           'census_tract_number': None,
           'geojson': json.loads(self.geojson)
       }
