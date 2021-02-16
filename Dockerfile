FROM python:3.7.9-alpine

RUN pip3 install --no-cache-dir -U pip pipenv

ADD . /opt/workdir

WORKDIR /opt/workdir

RUN pipenv install --system --deploy --ignore-pipfile

CMD python3 main.py
