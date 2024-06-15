# syntax=docker/dockerfile:1

FROM python:3.9
WORKDIR /app
COPY ./src/predict_app.py ./src/predict_app.py
COPY ./.env ./.env
COPY ./models/linear_regression_v01.joblib ./models/linear_regression_v01.joblib
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
CMD ["python3", "src/predict_app.py"]
EXPOSE 5000