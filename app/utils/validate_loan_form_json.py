
def validate_loan_form_json(json):
    errors = []

    loan_form = json.get('loan_form')
    if loan_form is None:
        errors.append({
            'field': 'loan_form',
            'message': 'loan_form is required for map_type in [\'predicted\', \'deviation\']'
        })
    else:
        pass 


    return (len(errors) == 0, errors)