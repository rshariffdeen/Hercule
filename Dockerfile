FROM ubuntu:20.04
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

# install experiment dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    bzip2 \
    file \
    git \
    nano \
    python3 \
    python3-pip \
    python3-dev \
    unzip \
    zstd \
    openjdk-17-jdk \
    openjdk-17-jre \
    gradle


# copy src files of the tool
COPY . /opt/hercule/
COPY gumtree-modified /opt/gumtree-modified
COPY pythonparser-modified /opt/pythonparser

# install python packages
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /opt/hercule/requirements.txt


# set git url
WORKDIR /opt/hercule/
RUN git remote rm origin
RUN git remote add origin https://github.com/rshariffdeen/hercule.git

WORKDIR /opt/gumtree-modified/
RUN ./gradlew clean build shadowjar

# set paths
ENV PATH /opt/hercule/bin:${PATH}
ENV PATH /opt/pythonparser:${PATH}
WORKDIR /opt/hercule/

