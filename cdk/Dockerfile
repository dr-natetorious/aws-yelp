FROM python:3.8

RUN apt-get -y update && apt-get -y install npm zip git
RUN npm install -g aws-cdk

COPY requirements.txt .
RUN pip install -r requirements.txt