FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

# Space-separated version string without leading 'v' (e.g. "0.4.21 0.4.22") 
ARG SOLC

RUN apt-get update \
  && apt-get install -y \
     libsqlite3-0 \
     libsqlite3-dev \
  && apt-get install -y \
     apt-utils \
     build-essential \
     locales \
     python-pip-whl \
     python3-pip \
     libleveldb-dev \
     python3-setuptools \
     software-properties-common \
  && add-apt-repository -y ppa:ethereum/ethereum \
  && apt-get update \
  && apt-get install -y \
     solc \
     libssl-dev \
     python3-dev \
     pandoc \
     git \
     wget \
  && ln -s /usr/bin/python3 /usr/local/bin/python

RUN pip3 install solc-select
RUN solc-select install all
RUN export PATH=/usr/local/bin:$PATH
COPY ./requirements.txt /opt/batin/requirements.txt

RUN cd /opt/batin \
  && pip3 install -r requirements.txt

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.en
ENV LC_ALL en_US.UTF-8

COPY . /opt/batin
RUN cd /opt/batin \
  && python setup.py install

WORKDIR /home/batin

RUN ( [ ! -z "${SOLC}" ] && set -e && for ver in $SOLC; do python -m solc.install v${ver}; done ) || true

COPY ./batin/support/assets/signatures.db /home/batin/.batin/signatures.db

ENTRYPOINT ["/usr/local/bin/map"]
