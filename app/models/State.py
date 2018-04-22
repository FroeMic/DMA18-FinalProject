from app import db

class State(db.Model):
    '''A US State.'''

    def __init__(self, state, state_code, geojson):
        self.state = state
        self.state_code = state_code
        self.geojson = geojson

    id = db.Column(db.Integer, primary_key=True)
    geojson_id = db.Column(db.Integer, db.ForeignKey('geo_json_feature.id'), nullable=True)
    state = db.Column(db.String(128), index=False, nullable=False, unique=True)
    state_code = db.Column(db.String(128), index=False,  nullable=False, unique=True)

    geojson = db.relationship('GeoJsonFeature', uselist=False, backref='state', lazy=False)
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
           'geojson': self.geojson.serialize if self.geojson is not None else None
       }
