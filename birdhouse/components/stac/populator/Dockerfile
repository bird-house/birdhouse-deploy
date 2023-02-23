
FROM python:3.8-slim as base

FROM base as builder
# Any python libraries that require system libraries to be installed will likely
# need the following packages in order to build
RUN apt-get update && apt-get install -y build-essential git

ENV CURL_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
ENV PATH=$PATH:/install/bin

ARG install_dev_dependencies=true

RUN git clone https://github.com/cedadev/stac-generator-example.git

COPY ./requirements.txt /

RUN pip install -r requirements.txt

CMD ["ls"]
