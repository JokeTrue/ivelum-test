FROM python:3

RUN mkdir /ivelum-server
WORKDIR /ivelum-server

ADD . /ivelum-server/
RUN pip install -r requirements.txt

CMD [ "python", "-u", "server.py" ]