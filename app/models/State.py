from app import db
import json

class State(db.Model):
    '''A US State.'''

    def __init__(self, state, state_code, geojson, avg_loan):
        self.state = state
        self.state_code = state_code
        self.geojson = geojson
        self.avg_loan = avg_loan

    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(128), index=False, nullable=False, unique=True)
    state_code = db.Column(db.String(128), index=False,  nullable=False, unique=True)
    avg_loan = db.Column(db.Float, index=False, nullable=True, unique=False)
    geojson = db.Column(db.Text, nullable=False, unique=False)

    counties = db.relationship('County', backref='state', lazy=True)

    @property
    def serialize(self):
       return {
           '_id': self.generated_id,
           'type': 'state',
           'state': self.state,
           'state_code': self.state_code,
           'county': None,
           'county_code': None,
           'avg_loan': float('{:10.2f}'.format(self.avg_loan * 1000)),
           'census_tract': None,
           'census_tract_number': None,
           'geojson': json.loads(self.geojson)
       }

    @property
    def generated_id (self):
        stateCode = int(self.state_code) if self.state_code else 0
        countyCode = 0
        censusTractName = 0
        censusTractNumber = 0.0

        return '-'.join([
            '{:02d}'.format(stateCode),
            '{:03d}'.format(countyCode),
            '{:06d}'.format(censusTractName),
            '{:04.2f}'.format(censusTractNumber)
        ])