from flask import jsonify

from app import app, db
from app.utils import ListConverter

# helpers
app.url_map.converters['list'] = ListConverter

@app.route('/api/v1/version')
def version():
    '''Returns the version of the api '''
    data = {
        'version': 1
    }
    return jsonify(data = data, success=True, error=None)
