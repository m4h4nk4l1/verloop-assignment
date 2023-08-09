"""
Weather API Using Flask

This module defines a Flask-based API that retrieves current weather data based on
a provided city name and output format. It supports both JSON and XML responses.
"""

import os
import xml.etree.ElementTree as ET
import requests
from flask import Flask, request, jsonify, Response
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')
WEATHER_API_URL = "https://weatherapi-com.p.rapidapi.com/current.json"

@app.route('/weather', methods=['POST'])
def get_weather_data():
    """
    Fetches weather data based on the provided city name and output format.
    Returns the weather data in JSON or XML format.
    """
    try:
        data = request.get_json()

        if not data or 'city' not in data or 'output_format' not in data:
            return jsonify({'error': 'Invalid request data'}), 400

        city = data['city']
        output_format = data['output_format']

        querystring = {"q": city}

        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

        response = requests.get(WEATHER_API_URL, headers=headers, params=querystring, timeout=5)
        weather_data = response.json()

        if output_format == 'json':
            return jsonify(weather_data), 200
        elif output_format == 'xml':
            xml_response = convert_to_xml(weather_data)
            return Response(xml_response, content_type='application/xml'), 200
        else:
            return jsonify({'error': 'Invalid output_format'}), 400

    except requests.exceptions.RequestException as error:
        return jsonify({'error': f'Request Exception: {str(error)}'}), 500
    except ValueError as error:
        return jsonify({'error': f'Value Error: {str(error)}'}), 400
    except Exception as error:
        return jsonify({'error': f'An unexpected error occurred: {str(error)}'}), 500

def convert_to_xml(data):
    """
    Converts a dictionary to an XML representation.
    """
    root = ET.Element('weather')
    for key, value in data.items():
        element = ET.SubElement(root, key)
        element.text = str(value)
    xml_string = ET.tostring(root, encoding='utf-8', method='xml')
    return xml_string

if __name__ == '__main__':
    app.run(debug=True)
