FROM rshariffdeen/hercule:22.04
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"


# install bandit4mal
RUN git clone https://github.com/rshariffdeen/bandit4mal /opt/bandit4mal
RUN cd /opt/bandit4mal && python3 setup.py install
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /opt/bandit4mal/requirements.txt

# install maloss


# install guarddog
RUN pip3 install guarddog


# install macaron
RUN mkdir /opt/macaron
WORKDIR /opt/macaron
RUN apt install -y curl docker.io
ENV MACARON_VERSION=main
RUN curl -O https://raw.githubusercontent.com/oracle/macaron/$MACARON_VERSION/scripts/release_scripts/run_macaron.sh
RUN chmod +x run_macaron.sh


# setup packages
RUN mkdir /data
ADD packages/popular.tar.gz /data

COPY . /experiments
WORKDIR /experiments