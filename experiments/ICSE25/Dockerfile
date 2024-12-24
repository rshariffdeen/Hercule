FROM rshariffdeen/hercule
LABEL maintainer="Ridwan Shariffdeen <rshariffdeen@gmail.com>"


# install bandit4mal
RUN git clone https://github.com/rshariffdeen/bandit4mal /opt/bandit4mal
RUN cd /opt/bandit4mal && python3 setup.py install
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /opt/bandit4mal/requirements.txt

# install maloss


# install guarddog


# install macaroni


RUN mkdir /experiments
WORKDIR /experiments
