FROM python:3.9.0-alpine

RUN apk add --no-cache --update \
    python3 python3-dev gcc \
    gfortran musl-dev g++ \
    libffi-dev openssl-dev \
    libxml2 libxml2-dev \
    libxslt libxslt-dev \
    libjpeg-turbo-dev zlib-dev

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-numpy py3-pandas@testing

WORKDIR /service
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3", "server.py"]