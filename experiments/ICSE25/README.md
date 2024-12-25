# Experiment Replication

Hercule achieves a f1-score of 0.949 on a dataset of Python packages comprising subjects
from Backstabber's Knife Collection, MalOSS, MalRegistry. 

In our replication package, we include scripts to reproduce the experiment using Hercule, GuardDog, MalOSS, BanditMal and LastPyMile.
This directory includes scripts and Dockerfile to re-create the experiment setup and reproduce the evaluation results.

Dockerhub Repo: https://hub.docker.com/repository/docker/rshariffdeen/hercule


# Getting Started
### Hardware Requirements
All experiments were conducted using Ubuntu 18.04 operating system on a 192-core 2.40GHz 512G RAM Intel Xeon
machine.


### Docker Preliminaries
* Ensure you have `docker` installed.
  See: https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04
* Ensure you have added yourself to the `docker` group: `sudo usermod -a -G
  docker <username>`. You will need to log back in to see the permissions take effect.



## Building the environment
Please note that the environment to run the experiments requires building 2 docker images:
* Docker image for Hercule tool and its dependencies (to build Hercule)
* Docker image for experiment environment and its dependencies to run baseline tools

Setup environment can be built using the Dockerfile provided within, which will encompass the dependencies, configurations
and setup scripts. Use the following command:

```bash
git clone https://github.com/rshariffdeen/Hercule.git

# building docker image for FixMorph
cd Hercule
docker build -t rshariffdeen/hercule:20.04 .

# building docker image for experiments
cd Hercule/experiments/ICSE25
docker build -t rshariffdeen/hercule:icse25 .
```

Note that the build process can be time-consuming, hence you can using the following command to download pre-built Docker image from following repository Dockerhub Repo: https://hub.docker.com/repository/docker/rshariffdeen/hercule
```bash
docker pull rshariffdeen/hercule:icse25
```

Having the image, you can now start a Docker container. 
Note: please make sure to use the correct image which has the dependencies installed for Linux kernel (i.e. rshariffdeen/hercule:icse25)

[comment]: <> (We recommend linking the container to folders in the filesystem,)
[comment]: <> (so that it is possible to check the logs and generated outputs also outside of the Docker container. )

```bash
docker run --name Hercule -it rshariffdeen/hercule:icse25 bash
```

