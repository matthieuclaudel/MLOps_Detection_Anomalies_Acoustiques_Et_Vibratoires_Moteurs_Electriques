FROM python:3.8-slim

RUN pip install scikit-learn pandas mlflow dagshub
WORKDIR /app
COPY ./load_data.py ./app/load_data.py

CMD ["python", "/app/load_model.py"]