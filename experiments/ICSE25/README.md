# Experiment Replication

Hercule achieves a f1-score of 0.949 on a dataset of Python packages comprising subjects
from Backstabber's Knife Collection, MalOSS, MalRegistry. 

In our replication package, we include scripts to reproduce the experiment using Hercule, GuardDog, MalOSS, BanditMal and LastPyMile.
This directory includes scripts and Dockerfile to re-create the experiment setup and reproduce the evaluation results.

Dockerhub Repo: https://hub.docker.com/repository/docker/rshariffdeen/hercule

# Package Structure
This artifact package is organized as following:

    .
    ├── data-set <== contains list of package names for each benchmark
    │   ├── backstabber
    │   ├── latest
    │   ├── maloss
    │   ├── malregistry
    │   ├── popular
    │   └── trusted
    ├── docs <== contains detailed instructions to reproduce experiment results
    │   ├── Macaron.md
    │   ├── RQ1.md
    │   ├── RQ2.md
    │   ├── RQ3.md
    │   └── RQ4.md
    ├── macaron <== necessary configuration files for Macaron
    ├── maloss <== trimmed down version of Maloss for python 
    ├── packages <== compressed archive files containing the packages for each dataset
    ├── scripts <== python/bash scripts to run the experiments and collect results
    ├── README.md
    └── Setup.md <== instructions to setup the environment/docker

# Next Steps
* [Setup Instructions](Setup.md)
* [Replicate RQ1](docs/RQ1.md)
* [Replicate RQ2](docs/RQ2.md)
* [Replicate RQ3](docs/RQ3.md)
* [Replicate RQ4](docs/RQ4.md)
* [Replicate Macaron Improvement](docs/Macaron.md)


