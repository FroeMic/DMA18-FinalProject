from flask import jsonify, request

from app import app, db
from app.utils import ListConverter, validate_json

# helpers
app.url_map.converters['list'] = ListConverter

def build_response(data, success = True, status = 200, errors = []):
    return jsonify(data = data, success = success, errors = errors), status

@app.route('/api/v1/version')
def version():
    '''Returns the version of the api '''
    data = {
        'version': 1
    }
    return build_response(data)


@app.route('/api/v1/mapdata', methods=['POST'])
def mapdata():
    json = request.get_json()

    if json is None: 
        return build_response(None, 
                            success = False, 
                            status = 400, 
                            errors = [{
                                'field': None,
                                'message': 'No JSON in request body.'
                            }]
            )

    success, errors = validate_json(json)
    if not success:
        return build_response(None, 
                            success = False, 
                            status = 400, 
                            errors = errors
        )

    return jsonify(data = [], success=True, error=None)

