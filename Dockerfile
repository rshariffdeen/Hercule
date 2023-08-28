FROM ubuntu:22.04
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

# install experiment dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    bzip2 \
    git \
    nano \
    python3 \
    python3-pip \
    python3-dev \
    unzip

# install python packages
RUN pip3 --disable-pip-version-check --no-cache-dir install \
    rich \
    bandit \
    slack_sdk  \
    discord \
    jsonschema

# copy src files of the tool
COPY . /opt/spade/

# set git url
WORKDIR /opt/spade/
RUN git remote rm origin
RUN git remote add origin https://github.com/rshariffdeen/spade.git


# set paths
ENV PATH /opt/spade/bin:${PATH}





