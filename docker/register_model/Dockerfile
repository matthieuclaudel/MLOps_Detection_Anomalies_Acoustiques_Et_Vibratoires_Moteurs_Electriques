FROM python:3.8-slim

RUN pip install scikit-learn pandas mlflow dagshub
WORKDIR /app
COPY ./register_model.py ./app/register_model.py

CMD ["python", "/app/register_model.py"]