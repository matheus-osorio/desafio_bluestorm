# create args
ARG port
ARG host
ARG debug
ARG reloader

# base image
FROM python:3.8-alpine

# install dependencies
COPY ./ ./
RUN pip install flask

#make tests
RUN python3 -m unittest src/tests/test_simple_app.py
RUN python3 -m unittest src/tests/test_select_app.py
RUN python3 -m unittest src/tests/test_insert_app.py

#run server
CMD ["python3", "app.py"]