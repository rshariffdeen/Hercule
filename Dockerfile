FROM ubuntu:20.04
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"

RUN apt-get update && apt-get upgrade -y && apt-get autoremove -y

# install experiment dependencies
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    bzip2 \
    file \
    git \
    jq \
    nano \
    python3 \
    python3-pip \
    python3-dev \
    unzip \
    zstd \
    openjdk-17-jdk \
    openjdk-17-jre \
    gradle \
    wget


# copy src files of the tool
COPY . /opt/hercule/
COPY gumtree-modified /opt/gumtree-modified
COPY pythonparser-modified /opt/pythonparser

# install python packages
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /opt/hercule/requirements.txt

# install bandit4mal
RUN git clone https://github.com/rshariffdeen/bandit4mal /opt/bandit4mal
RUN cd /opt/bandit4mal && python3 setup.py install
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /opt/bandit4mal/requirements.txt

# set git url
WORKDIR /opt/hercule/
RUN git remote rm origin
RUN git remote add origin https://github.com/rshariffdeen/hercule.git

WORKDIR /opt/gumtree-modified/
RUN ./gradlew clean build shadowjar

# install cloc for loc computation
RUN git clone https://github.com/AlDanial/cloc /opt/cloc

# Download codeql v2.12.2
WORKDIR /opt
RUN wget https://github.com/github/codeql-cli-binaries/releases/download/v2.15.0/codeql-linux64.zip
RUN unzip codeql-linux64.zip
ENV PATH="${PATH}:/opt/codeql/"

# set paths
ENV PATH /opt/hercule/bin:/opt/cloc:${PATH}
ENV PATH /opt/pythonparser:${PATH}
WORKDIR /opt/hercule/

WORKDIR /opt/hercule/codeql
RUN codeql pack install

WORKDIR /opt/hercule/
