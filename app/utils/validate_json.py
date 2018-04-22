from flask import jsonify, request


def validate_json(json):
    errors = []

    detail_level = json.get('detail_level')
    if detail_level is None or detail_level not in ['state', 'county', 'census']:
        errors.append({
            'field': 'detail_level',
            'message': 'detail_level must be set and in [\'state\', \'county\', \'census\']'
        })

    if detail_level:
        state_code = json.get('state_code')
        if state_code is None:
            errors.append({
                'field': 'state_code',
                'message': 'state_code is required.'
            })   

    # if detail_level and detail_level in ['county', 'census']:
    #     county_code = json.get('county_code')
    #     if county_code is None:
    #         errors.append({
    #             'field': 'county_code',
    #             'message': 'county_code is required for detail_level in [\'county\', \'census\']'
    #         })     

    # if detail_level and detail_level in ['census']:
    #     census_tract_number = json.get('census_tract_number')
    #     if census_tract_number is None:
    #         errors.append({
    #             'field': 'census_tract_number',
    #             'message': 'census_tract_number is required for detail_level in [\'census\']'
    #         })     

    map_type = json.get('map_type')
    if map_type is None or map_type not in ['average', 'predicted', 'deviation']:
        errors.append({
            'field': 'map_type',
            'message': 'map_type must be set and in [\'average\', \'predicted\', \'deviation\']'
        })

    if map_type and map_type in ['predicted', 'deviation']:
        loan_form = json.get('loan_form')
        if loan_form is None:
            errors.append({
                'field': 'loan_form',
                'message': 'loan_form is required for map_type in [\'predicted\', \'deviation\']'
            })
        else:
            loan_success, loan_errors = validate_loan_json(loan_form)
            errors + loan_errors

    return (len(errors) == 0, errors)


def validate_loan_form_json(json):
    errors = []

    return (len(errors) == 0, errors)