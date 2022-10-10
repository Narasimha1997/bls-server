FROM python:3.6.10-buster

# copy the required files
COPY requirements.txt /requirements.txt
COPY setup_everything.sh /setup_everything.sh
COPY proto /proto
COPY server /server

# install the required dependencies
RUN pip3 install -r requirements.txt
RUN sh /setup_everything.sh

WORKDIR /server
ENTRYPOINT ["python3", "main.py"]
