from app import db

class Coordinate(db.Model):
    '''A coordinate represented by longitude at latitude.'''
    
    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    id = db.Column(db.Integer, primary_key=True)
    lng = db.Column(db.Float, index=False,  nullable=False)
    lat = db.Column(db.Float, index=False,  nullable=False)
    polygon_id = db.Column(db.Integer, db.ForeignKey('polygon.id'), nullable=False)

    @property
    def serialize(self):
       return [ self.lng, self.lat ]