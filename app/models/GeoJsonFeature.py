from app import db

class GeoJsonFeature(db.Model):
    '''A GeoJson feature composed of a polygon of points '''
    
    def __init__(self, dict, geometry):
        self.type = "Feature"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), index=False, nullable=False)

    geometry = db.relationship('Polygon', backref='feature', lazy=False)
