from app import db

class GeoJsonFeature(db.Model):
    '''A GeoJson feature composed of a polygon of points '''
    
    def __init__(self, geometry_type, polygons):
        self.type = "Feature"
        self.geometry_type = geometry_type
        self.polygons = polygons

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(128), index=False, nullable=False)
    geometry_type = db.Column(db.String(128), index=False, nullable=False)

    polygons = db.relationship('Polygon', backref='feature', lazy=False)

    @property
    def serialize(self):
       return {
           'type': self.type,
           'geometry': {
               'type': self.geometry_type,
               'coordinates': [polygon.serialize for polygon in self.polygons]
           }
       }


