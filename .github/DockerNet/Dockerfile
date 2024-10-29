FROM python:3.12
WORKDIR /usr/local/flask-serv
EXPOSE 5000

# copy server files
COPY . /usr/local/flask-serv/

# Install flask
RUN pip install flask

CMD python webknd.py