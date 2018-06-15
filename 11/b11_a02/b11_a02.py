#!/usr/bin/python

from flask import Flask
from flask_restful import Resource, Api
import re

app = Flask(__name__)
api = Api(app)


def f_to_c(fahrenheit):
    return ((fahrenheit - 32) / 1.8)

def c_to_f(celsius):
    return (celsius * 1.8 + 32)

def convert(value, target_unit):
    """
    takes an value and a target unit. Validates input and returns converted
    temperature or error message, if no number given
    """
    try:
        temperature = value.strip()
    	pattern = "^-?[0-9]+([,\.][0-9]+)?$"
    	matches = re.match(pattern, temperature)
    	if matches:
            temperature = float(temperature)
            if target_unit == 'C':
                return {'celsius': f_to_c(temperature)}
            else:
                return {'fahrenheit': c_to_f(temperature)}
        else:
            return {'error': 'Seriously! Numbers only'}
    except ValueError:
        return {'error': 'Seriously! Numbers only'}



class C_to_F(Resource):
    def get(self, celsius):
        return convert(celsius, 'F')

class F_to_C(Resource):
    def get(self, fahrenheit):
        return convert(fahrenheit, 'C')

api.add_resource(C_to_F, '/ctof/<celsius>')
api.add_resource(F_to_C, '/ftoc/<fahrenheit>')




if __name__ == '__main__':
    app.run(debug=False)
