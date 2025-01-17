FROM python:3.8-slim

RUN pip install scikit-learn pandas mlflow dagshub
WORKDIR /app
COPY ./train_model.py ./app/train_model.py

CMD ["python", "/app/train_model.py"]