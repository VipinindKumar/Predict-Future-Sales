# syntax=docker/dockerfile:1

FROM python:3.10.5-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# because of error while importing xgboost, libgomp1 is missing
RUN apt-get update && \

     apt-get -y --no-install-recommends install \

     libgomp1

# open port and makes it public to the host
# EXPOSE 5000

COPY . .

CMD ["python3", "app.py"]