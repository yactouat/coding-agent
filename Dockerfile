FROM python:3.10.12

WORKDIR /workspace

COPY requirements.txt /workspace/requirements.txt
RUN pip install -r requirements.txt

COPY vertexai-sa.json /workspace/vertexai-sa.json
COPY .env /workspace/.env

COPY ./src /workspace
