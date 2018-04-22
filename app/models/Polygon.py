from app import db

class Polygon(db.Model):
    '''A Polygon composed of multiple coordinates. '''
    
    def __init__(self, coordinates):
        self.type = 'Polygon'
        self.coordinates = coordinates

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), index=False, nullable=False)
    coordinates = db.relationship('Coordinate', backref='polygon', lazy=False)
