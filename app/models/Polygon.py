from app import db

class Polygon(db.Model):
    '''A Polygon composed of multiple coordinates. '''
    
    def __init__(self, coordinates):
        self.coordinates = coordinates

    id = db.Column(db.Integer, primary_key=True)
    geojson_id = db.Column(db.Integer, db.ForeignKey('geo_json_feature.id'), nullable=False)

    @property
    def serialize(self):
       return [c.serialize for c in self.coordinates]

        