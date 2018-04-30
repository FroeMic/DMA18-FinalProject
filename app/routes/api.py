from flask import jsonify, request

from app import app, db
from app.models import State, County, CensusTract
from app.utils import ListConverter, validate_json, validate_loan_form_json

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

@app.route('/api/v1/revision')
def revision():
    detail_level = request.args.get('detail_level')
    revision = None
    if detail_level == 'state':
        revision = 1
    elif detail_level == 'county':
        revision = 1
    elif detail_level == 'census':
        revision = 1

    if revision is None:
        return build_response(None, 
                    success = False, 
                    status = 400, 
                    errors = [{
                        'field': 'detail_level',
                        'message': 'The url parameter \'detail_level\' must be set and withing [\'state\', \'county\', \'census\']' 
                    }]
            )   

    data = {
        'revision': revision
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

    if json['detail_level'] == 'state':
        data = {
            'detail_level': json.get('detail_level'),
            'revision': 1,
            'instances': [c.serialize for c in State.query.all()]
        }
        return build_response(data)
    elif json['detail_level'] == 'county':
        data = {
            'detail_level': json.get('detail_level'),
            'revision': 1,
            'instances': [c.serialize for c in County.query.all()]
        }
        return build_response(data)
    # serializing all 1k census tracts takes almost 1 minute. Not feasible for our prototype
    elif json['detail_level'] == 'census':
        data = {
            'detail_level': json.get('detail_level'),
            'revision': 1,
            'instances': [c.serialize for c in CensusTract.query.all()]
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


def predict_for_state(state, data):
    return (state.generated_id, random.randint(10000,500000))
    
def predict_for_county(county, data):
    return (county.generated_id, random.randint(10000,500000))
    
def predict_for_census(census, data):
    return (census.generated_id, random.randint(10000,500000))

@app.route('/api/v1/predict', methods=['POST'])
def predict():
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

    success_1, errors_1 = validate_json(json)
    success_2, errors_2 = validate_loan_form_json(json)
    success = success_1 and success_2
    errors = errors_1 + errors_2
    if not success:
        return build_response(None, 
                            success = False, 
                            status = 400, 
                            errors = errors
        )

    loan_form = json.get('loan_form')
    if json['detail_level'] == 'state':
        data = {}
        for state in State.query.all():
            (_id, predicted_value) = predict_for_state(state, loan_form)
            data[_id] = predicted_value
        return build_response(data)
    elif json['detail_level'] == 'county':
        data = {}
        for county in County.query.all():
            (_id, predicted_value) = predict_for_county(county, loan_form)
            data[_id] = predicted_value
        return build_response(data)
    elif json['detail_level'] == 'census':
        data = {}
        for census in CensusTract.query.all():
            (_id, predicted_value) = predict_for_census(census, loan_form)
            data[_id] = predicted_value
        return build_response(data)
    else:
        return build_response(None, 
                    success = False, 
                    status = 501, 
                    errors = [{
                        'field': None,
                        'message': 'Predicition for detail_level=\'{}\' it not implemented yet.'.format(json['detail_level'] )
                    }]
            )   