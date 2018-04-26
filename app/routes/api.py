from flask import jsonify, request

from app import app, db
from app.models import State, County, CensusTract
from app.utils import ListConverter, validate_json

import random 

# SETUP
app.url_map.converters['list'] = ListConverter

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def build_response(data, success = True, status = 200, errors = []):
    return jsonify(data = data, success = success, errors = errors), status

@app.route('/api/v1/version')
def version():
    '''Returns the version of the api '''
    data = {
        'version': 1
    }
    return build_response(data)

def serialize_result(serializable):
    dic = serializable.serialize
    dic['value'] = random.randint(10000,500000)
    return dic


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


    if json['detail_level'] == 'state':
        data = {
            'detail_level': json.get('detail_level'),
            'instances': [serialize_result(c) for c in State.query.all()]
        }
        return build_response(data)
    elif json['detail_level'] == 'county':
        data = {
            'detail_level': json.get('detail_level'),
            'instances': [serialize_result(c) for c in County.query.all()]
        }
        return build_response(data)
    # serializing all 1k census tracts takes almost 1 minute. Not feasible for our prototype
    elif json['detail_level'] == 'census':
        data = {
            'detail_level': json.get('detail_level'),
            'instances': [serialize_result(c) for c in CensusTract.query.all()]
        }
        return build_response(data)
    else:
        return build_response(None, 
                    success = False, 
                    status = 501, 
                    errors = [{
                        'field': None,
                        'message': 'detail_level=\'{}\' it not implemented yet.'.format(json['detail_level'] )
                    }]
            )   

    return jsonify(data = data, success=True, error=None)

