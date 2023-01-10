FROM python:3.10
WORKDIR /code
RUN apt-get update && apt-get install -y python3-dev &&\
    pip3 install -U setuptools pip wheel cython
RUN wget -nc https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get update
RUN apt-get install -y -f ./google-chrome-stable_current_amd64.deb
COPY ./requirements requirements
RUN pip3 install selenium webdriver-manager
RUN pip3 install -r requirements/dev.txt
ADD . /code
RUN pip3 install .
CMD bash