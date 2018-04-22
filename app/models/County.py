from app import db

class County(db.Model):
    '''A county of an US State.'''
    
    def __init__(self, county, county_code, state, geojson):
        self.county = county
        self.county_code = county_code
        self.state = state
        self.geojson = geojson

    id = db.Column(db.Integer, primary_key=True)
    geojson_id = db.Column(db.Integer, db.ForeignKey('geo_json_feature.id'), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id'), nullable=False)
    county = db.Column(db.String(128), index=False, nullable=False, unique=True)
    county_code = db.Column(db.String(128), index=False, nullable=False, unique=True)

    geojson = db.relationship('GeoJsonFeature', uselist=False, backref='county', lazy=False)
    census_tracts = db.relationship('CensusTract', backref='county', lazy=True)


    @property
    def serialize(self):
       return {
           'type': 'county',
           'state': self.state.state,
           'state_code': self.state.state_code,
           'county': self.county,
           'county_code': self.county_code,
           'census_tract': None,
           'census_tract_number': None,
           'geojson': self.geojson.serialize if self.geojson is not None else None
       }