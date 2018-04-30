from flask import jsonify, request

from app import app, db
from app.models import State, County, CensusTract
from app.utils import ListConverter, validate_json, validate_loan_form_json
import pickle
import random
import numpy as np
import os

# SETUP
app.url_map.converters['list'] = ListConverter

# Setup for model
propery_type_mapping = {'Manufactured housing': 2, 'Multifamily dwelling': 3,
                       'One-to-four family dwelling (other than manufactured housing)': 4}

preapproval_mapping = {'Not applicable': 5, 'Preapproval was not requested': 6,
                       'Preapproval was requested': 7}

purpose_mapping = {'Home improvement': 8, 'Home purchase': 9, 'Refinancing': 10}

hoepa_mapping = {'HOEPA loan': 11, 'Not a HOEPA loan': 12}

coapp_sex = {'Female': 13, 'Information not provided by applicant in mail, Internet, or telephone application': 14,
            'Male': 15, 'No co-applicant': 16, 'Not applicable': 17}

coapp_race = {'American Indian or Alaska Native': 18, 'Asian': 19, 'Black or African American': 20,
             'Information not provided by applicant in mail, Internet, or telephone application': 21,
              'Native Hawaiian or Other Pacific Islander': 22, 'No co-applicant': 23, 'Not applicable':24,
             'White': 25}

app_sex = {'Female': 26, 'Information not provided by applicant in mail, Internet, or telephone application': 27,
           'Male': 28, 'Not applicable': 29}

app_race = {'American Indian or Alaska Native': 30, 'Asian': 31, 'Black or African American': 32,
           'Information not provided by applicant in mail, Internet, or telephone application': 33,
           'Native Hawaiian or Other Pacific Islander': 34, 'Not applicable': 35, 'White': 36}


pickle_file_path = os.path.abspath('Lasso.sav')
with open(pickle_file_path, 'rb') as pickle_file:
    loaded_model = pickle.load(pickle_file)

pickle_file_path = os.path.abspath('county_mapping.pickle')
with open(pickle_file_path, 'rb') as pickle_file:
    county_map = pickle.load(pickle_file)

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
    array = np.full((1, 95), 0.0)

    array[0][0] = np.log(int(data['medianFamilyIncome']))
    array[0][1] = np.log(int(data['medianPersonalIncome']))
    array[0][propery_type_mapping[data['propertyTypeName']]] = 1
    array[0][preapproval_mapping[data['preApprovalName']]] = 1
    array[0][purpose_mapping[data['loanPurposeName']]] = 1
    array[0][hoepa_mapping[data['hopeaStatus']]] = 1
    array[0][coapp_sex[data['coApplicantSex']]] = 1
    array[0][coapp_race[data['coApplicantRace']]] = 1
    array[0][app_sex[data['applicantSex']]] = 1
    array[0][app_race[data['applicantRace']]] = 1
    array[0][county_map[county.county]] = 1

    prediction = np.exp(loaded_model.predict(array)[0]) * 1000
    return (county.generated_id, prediction)
    #return (county.generated_id, random.randint(10000,500000))
    
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