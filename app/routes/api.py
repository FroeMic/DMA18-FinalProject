from flask import jsonify, request

from app import app, db
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


    # TODO: Replace Dummy Data

    data = {
        'detail_level': json.get('detail_level'),
        'instances': [
            {
                "type": "county",
                "state": "California",
                "state_code": "06",
                "county": "Alameda County",
                "county_code": 1,
                "value": 2134567,
                "geojson": {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [
                                    -122.333711,
                                    37.809797
                                ],
                                [
                                    -122.323567,
                                    37.823214
                                ],
                                [
                                    -122.317676,
                                    37.826814
                                ],
                                [
                                    -122.306222,
                                    37.827469
                                ],
                                [
                                    -122.303931,
                                    37.830087
                                ],
                                [
                                    -122.301313,
                                    37.847758
                                ],
                                [
                                    -122.310477,
                                    37.873938
                                ],
                                [
                                    -122.309986,
                                    37.892755
                                ],
                                [
                                    -122.313258,
                                    37.89701
                                ],
                                [
                                    -122.313495917826,
                                    37.897210726126204
                                ],
                                [
                                    -122.27108,
                                    37.905824
                                ],
                                [
                                    -122.248914,
                                    37.886867
                                ],
                                [
                                    -122.223878,
                                    37.878326
                                ],
                                [
                                    -122.221488,
                                    37.865026
                                ],
                                [
                                    -122.184179,
                                    37.833922
                                ],
                                [
                                    -122.185977,
                                    37.820726
                                ],
                                [
                                    -122.157392,
                                    37.817952
                                ],
                                [
                                    -122.14026,
                                    37.804562
                                ],
                                [
                                    -122.045473,
                                    37.798126
                                ],
                                [
                                    -122.004809,
                                    37.770571
                                ],
                                [
                                    -121.997771,
                                    37.763227
                                ],
                                [
                                    -122.011771,
                                    37.747428
                                ],
                                [
                                    -121.989971,
                                    37.733628
                                ],
                                [
                                    -121.97247,
                                    37.728528
                                ],
                                [
                                    -121.96077,
                                    37.718629
                                ],
                                [
                                    -121.873542,
                                    37.739317
                                ],
                                [
                                    -121.666262,
                                    37.790427
                                ],
                                [
                                    -121.624161,
                                    37.799127
                                ],
                                [
                                    -121.58056,
                                    37.812467
                                ],
                                [
                                    -121.560855,
                                    37.818414
                                ],
                                [
                                    -121.556936,
                                    37.817218
                                ],
                                [
                                    -121.556959,
                                    37.743051
                                ],
                                [
                                    -121.556655,
                                    37.542732
                                ],
                                [
                                    -121.541833,
                                    37.530215
                                ],
                                [
                                    -121.50442,
                                    37.525863
                                ],
                                [
                                    -121.493183,
                                    37.502421
                                ],
                                [
                                    -121.469275,
                                    37.489688
                                ],
                                [
                                    -121.471925,
                                    37.481783
                                ],
                                [
                                    -121.472648,
                                    37.48217
                                ],
                                [
                                    -121.855762,
                                    37.484537
                                ],
                                [
                                    -121.925041,
                                    37.454186
                                ],
                                [
                                    -121.947087,
                                    37.467424
                                ],
                                [
                                    -121.975071,
                                    37.460639
                                ],
                                [
                                    -121.996671,
                                    37.467239
                                ],
                                [
                                    -122.046554266444,
                                    37.4595373585317
                                ],
                                [
                                    -122.059031,
                                    37.475548
                                ],
                                [
                                    -122.068539,
                                    37.491202
                                ],
                                [
                                    -122.092442,
                                    37.499489
                                ],
                                [
                                    -122.111344,
                                    37.50758
                                ],
                                [
                                    -122.11144457163401,
                                    37.5108510385602
                                ],
                                [
                                    -122.111998,
                                    37.528851
                                ],
                                [
                                    -122.128688,
                                    37.560594
                                ],
                                [
                                    -122.133924,
                                    37.562885
                                ],
                                [
                                    -122.137524,
                                    37.567467
                                ],
                                [
                                    -122.144396,
                                    37.581866
                                ],
                                [
                                    -122.147014,
                                    37.588411
                                ],
                                [
                                    -122.145378,
                                    37.600846
                                ],
                                [
                                    -122.14636,
                                    37.607391
                                ],
                                [
                                    -122.152905,
                                    37.640771
                                ],
                                [
                                    -122.162802519462,
                                    37.6672730133697
                                ],
                                [
                                    -122.163049,
                                    37.667933
                                ],
                                [
                                    -122.170904,
                                    37.676114
                                ],
                                [
                                    -122.179085,
                                    37.680041
                                ],
                                [
                                    -122.197411,
                                    37.692804
                                ],
                                [
                                    -122.203971,
                                    37.697769
                                ],
                                [
                                    -122.213774,
                                    37.698695
                                ],
                                [
                                    -122.221628,
                                    37.705567
                                ],
                                [
                                    -122.246826,
                                    37.72193
                                ],
                                [
                                    -122.255989,
                                    37.735674
                                ],
                                [
                                    -122.257953,
                                    37.739601
                                ],
                                [
                                    -122.257134,
                                    37.745001
                                ],
                                [
                                    -122.252226,
                                    37.747619
                                ],
                                [
                                    -122.244938,
                                    37.750294
                                ],
                                [
                                    -122.242638,
                                    37.753744
                                ],
                                [
                                    -122.253753,
                                    37.761218
                                ],
                                [
                                    -122.264101,
                                    37.764667
                                ],
                                [
                                    -122.275408,
                                    37.76735
                                ],
                                [
                                    -122.286139,
                                    37.769458
                                ],
                                [
                                    -122.293996,
                                    37.770416
                                ],
                                [
                                    -122.304345,
                                    37.774632
                                ],
                                [
                                    -122.318909,
                                    37.77904
                                ],
                                [
                                    -122.33079,
                                    37.78383
                                ],
                                [
                                    -122.331748,
                                    37.796052
                                ],
                                [
                                    -122.335675,
                                    37.799652
                                ],
                                [
                                    -122.333711,
                                    37.809797
                                ]
                            ]
                        ]
                    }
                },
            },
            {
                "type": "county",
                "state": "California",
                "state_code": "06",
                "county": "Alpine County",
                "county_code": 3,
                "value": 232542,
                "geojson": {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [
                                    -120.072484,
                                    38.509869
                                ],
                                [
                                    -120.072392,
                                    38.702767
                                ],
                                [
                                    -119.964948,
                                    38.775986
                                ],
                                [
                                    -119.947927,
                                    38.781642
                                ],
                                [
                                    -119.942108,
                                    38.80311
                                ],
                                [
                                    -119.92186,
                                    38.820962
                                ],
                                [
                                    -119.92271,
                                    38.829955
                                ],
                                [
                                    -119.908493,
                                    38.834346
                                ],
                                [
                                    -119.906779,
                                    38.854664
                                ],
                                [
                                    -119.891909,
                                    38.857344
                                ],
                                [
                                    -119.877287,
                                    38.870193
                                ],
                                [
                                    -119.888444,
                                    38.879301
                                ],
                                [
                                    -119.879516,
                                    38.887021
                                ],
                                [
                                    -119.887643,
                                    38.918295
                                ],
                                [
                                    -119.904315,
                                    38.933324
                                ],
                                [
                                    -119.587679,
                                    38.714734
                                ],
                                [
                                    -119.587066,
                                    38.714345
                                ],
                                [
                                    -119.585437,
                                    38.713212
                                ],
                                [
                                    -119.579518,
                                    38.705609
                                ],
                                [
                                    -119.598647,
                                    38.670942
                                ],
                                [
                                    -119.614658,
                                    38.665879
                                ],
                                [
                                    -119.619237,
                                    38.604501
                                ],
                                [
                                    -119.599815,
                                    38.593348
                                ],
                                [
                                    -119.587367,
                                    38.558354
                                ],
                                [
                                    -119.568055,
                                    38.537707
                                ],
                                [
                                    -119.556217,
                                    38.516621
                                ],
                                [
                                    -119.556616,
                                    38.501702
                                ],
                                [
                                    -119.542862,
                                    38.499694
                                ],
                                [
                                    -119.542367,
                                    38.481657
                                ],
                                [
                                    -119.555863,
                                    38.470242
                                ],
                                [
                                    -119.556426,
                                    38.447465
                                ],
                                [
                                    -119.570009,
                                    38.43486
                                ],
                                [
                                    -119.561995,
                                    38.410734
                                ],
                                [
                                    -119.592409,
                                    38.398877
                                ],
                                [
                                    -119.601212,
                                    38.405354
                                ],
                                [
                                    -119.622093,
                                    38.393875
                                ],
                                [
                                    -119.607395,
                                    38.366458
                                ],
                                [
                                    -119.635575,
                                    38.353908
                                ],
                                [
                                    -119.628295,
                                    38.349733
                                ],
                                [
                                    -119.639205,
                                    38.32688
                                ],
                                [
                                    -119.669524,
                                    38.348288
                                ],
                                [
                                    -119.700029,
                                    38.365215
                                ],
                                [
                                    -119.693622,
                                    38.378899
                                ],
                                [
                                    -119.698671,
                                    38.409838
                                ],
                                [
                                    -119.705385,
                                    38.416102
                                ],
                                [
                                    -119.753481,
                                    38.416759
                                ],
                                [
                                    -119.770553,
                                    38.406663
                                ],
                                [
                                    -119.801737,
                                    38.401321
                                ],
                                [
                                    -119.814691,
                                    38.387516
                                ],
                                [
                                    -119.837551,
                                    38.382411
                                ],
                                [
                                    -119.869667,
                                    38.367597
                                ],
                                [
                                    -119.884749,
                                    38.356185
                                ],
                                [
                                    -120.019951,
                                    38.433521
                                ],
                                [
                                    -120.05365,
                                    38.455607
                                ],
                                [
                                    -120.072566,
                                    38.447081
                                ],
                                [
                                    -120.072484,
                                    38.509869
                                ]
                            ]
                        ]
                    }
                },
            }
        ]
    }

    return jsonify(data = data, success=True, error=None)

