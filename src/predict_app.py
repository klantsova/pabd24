"""House price prediction service"""
import os
from dotenv import dotenv_values
from flask import Flask, request
from flask_cors import CORS
from joblib import load
from flask_httpauth import HTTPTokenAuth
from flask import send_from_directory

MODEL_SAVE_PATH = 'models/model_rf_BEST.joblib'

app = Flask(__name__)
CORS(app)

config = dotenv_values(".env")
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    config['APP_TOKEN']: "user23",
}

model = load(MODEL_SAVE_PATH)


@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]


def predict(in_data: dict) -> int:
    """ Predict house price from input data parameters.
    :param in_data: house parameters.
    :raise Error: If something goes wrong.
    :return: House price, RUB.
    :rtype: int
    """
    in_data = request.get_json()
    floor = int(in_data['floor'])
    floors_count = int(in_data['floors_count'])
    rooms_count = int(in_data['rooms_count'])
    total_meters = float(in_data['total_meters'])
    price = predict([[floor,
                      floors_count,
                      rooms_count,
                      total_meters]])
    return int(price)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/")
def home():
    return """
    <html>
    <head>
    <link rel="shortcut icon" href="/favicon.ico">
    </head>
    <body>
    <h1>Housing price service.</h1> Use /predict endpoint
    </body>
    </html>
    """


@app.route("/predict", methods=['POST'])
@auth.login_required
def predict_web_serve():
    """Dummy service"""
    in_data = request.get_json()
    price = predict(in_data)
    return {'price': price}


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
