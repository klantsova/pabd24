"""House price prediction service"""
from dotenv import dotenv_values
from flask import Flask, request
from flask_cors import CORS
from joblib import load
from flask_httpauth import HTTPTokenAuth

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
    total_meters = float(in_data['total_meters'])
    floor = int(in_data['floor'])
    floors_count = int(in_data['floors_count'])
    first_floor = (floor == 1)
    last_floor = (floor == floors_count)
    rooms_count = int(in_data['rooms_count'])
    price = model.predict([[floor,
                            floors_count,
                            rooms_count,
                            total_meters,
                            first_floor,
                            last_floor]])
    return int(price)


@app.route("/")
def home():
    return """
    <h1>Housing price service.</h1> Use /predict endpoint
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
