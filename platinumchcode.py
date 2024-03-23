import re, sqlite3
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: 'API untuk Analisis Sentimen'),
        'version' : LazyString(lambda: '1.0.0'),
        'description' : LazyString(lambda: 'Membuat API untuk Analisis Sentimen')
    },
    host = LazyString(lambda: request.host),
)

swagger_config = {
    'headers' : [],
    'specs' : [
        {
            "endpoint" : "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path" : "/flasgger_static",
    "swagger_ui": True,
    "specs_route" : "/docs/",
}
swagger = Swagger(app, template = swagger_template, config = swagger_config)

# Endpoint testing dengan hello world
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        '3. status_code': 200,
        '1. description' : "Please visit: ",
        '2. data' : "http://127.0.0.1:5000/docs/",
    }
    response_data = jsonify(json_response)
    return response_data

# Endpoint 1 untuk Neural Network menerima teks

# Endpoint 2 untuk Neural Network menerima file

# Endpoint 3 untuk LSTM menerima teks

# Endpoint 4 untuk LSTM menerima file

if __name__ == '__main__':
    app.run()