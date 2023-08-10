FROM python:3.7-slim-buster
ARG MLFLOW_USER_DATA_DIR
# Install python packages 
RUN pip install mlflow

# To make sure sqlite file is found
WORKDIR ${MLFLOW_USER_DATA_DIR}/mlflow