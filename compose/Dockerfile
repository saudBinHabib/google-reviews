FROM python:3.10
WORKDIR /code

RUN apt-get update && apt-get install -y python3-dev &&\
    pip3 install -U setuptools pip wheel cython

COPY ./requirements requirements
RUN pip3 install -r requirements/dev.txt
ADD . /code
RUN pip3 install .
CMD bash