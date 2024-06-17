# syntax=docker/dockerfile:1

FROM python:3.9
WORKDIR /app
COPY ./src/predict_app.py ./src/predict_app.py
COPY ./.env ./.env
COPY ./models/model_rf_BEST.joblib ./models/model_rf_BEST.joblib
COPY ./requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt
RUN pip install gunicorn
CMD ["gunicorn"  , "-b", "0.0.0.0", "-w", "3", "src.predict_app:app"]
#CMD ["python3", "src/predict_app.py"]
EXPOSE 8000
