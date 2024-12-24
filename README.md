# Hercule
AST based differential tool to determine the faithfulness of a build-artifact compared to the source, which can be used to detect supply chain attacks


Hercule is a behavior analysis tool for Python packages that can detect supply chain attacks. Hercule is:

* Accurate: Achieves a f1-score of 0.95 scanning nearly 5000 packages
* Extensible: Hercule is designed so that it can be easily extended to support advanced behavior analysis using CodeQL queries
* Scalable: Hercule can analyze large Python packages including but not limited to scipy, numpy, pandas etc


Note: See the [Experiment Guide](experiments/ICSE25/README.md) to replicate the experiments for ICSE'25. 


## Dependencies
* Python - 3.11+
* Docker - 20.10.1+
* CodeQL - 17.0.3+
* TreeSitter - 
* GumTree - 17.0.3+


## Build using Dockerfile

Building Hercule is easy with the provided Dockerfile, which has all the build dependencies and libraries required. We provide two Dockerfiles

* Dockerfile: This will build the environment necessary to run the stand-alone tool
* experiments/ICSE25/Dockerfile: This environment includes all necessary dependencies to reproduce the experiments

You can use the following command to build hercule image:

```bash
cd Hercule
docker build -t rshariffdeen/hercule .
# start docker
docker run -it rshariffdeen/hercule /bin/bash              
```

The experiments/ICSE25/Dockerfile depends on the hercule base image. The instructions to build and execute experiments/ICSE25/Dockerfile can be found [here](./experiments/ICSE25).


# Example Usage
TODO

# Limitations #
* Current implementation is based on CodeQL, and thus inherits the limitations of that framework. Please note that CodeQL license is limited to academic research purpose only.
* Hercule does not perform dynamic analysis


## Bugs ##
Hercule should be considered alpha-quality software. Bugs can be reported here:

    https://github.com/rshariffdeen/Hercule/issues

## Documentation ##

* [Getting Started](docs/GetStarted.md)
* [Example Usage](docs/Examples.md)
* [ICSE'25 Experiment Replication](experiments/ICSE25/README.md)  
* [Manual](docs/Manual.md)

# Contributions 
We welcome contributions to improve this work, see [details](docs/Contributing.md)

## Developers ##
* Ridwan Shariffdeen
* Martin Mirchev
* Ali El Husseini


## Publication ##
**Detecting Python Malware in the Software Supply Chain with Program Analysis** <br>
Ridwan Shariffdeen, Behnaz Hassanshahi, Martin Mirchev, Ali El Husseini, Abhik Roychoudhury <br>
47th International Conference on Software Engineering (ICSE), Software Engineering in Practice track (SEIP)

## Acknowledgements ##
This research was supported by the National Research Foundation, Singapore, and Cyber Security Agency of Singapore under its National Cybersecurity R&D Programme (Fuzz Testing NRF-NCR25-Fuzz-0001). Any opinions, findings and conclusions, or recommendations expressed in this material are those of the author(s) and do not reflect the views of National Research Foundation, Singapore, and Cyber Security Agency of Singapore.

# License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Citation

If you use Hercule in your research work, we would highly appreciate it if you
cited the [following paper](https://rshariffdeen.com/paper/ICSE25-SEIP.pdf):

```
@inproceedings{hercule,
author = {Shariffdeen, Ridwan and Hassanshahi, Behnaz and Mirchev, Martin  and Husseini, Ali El and Roychoudhury, Abhik},
title = {Detecting Python Malware in the Software Supply Chain with Program Analysis},
year = {2025},
doi = {},
booktitle = {2025 IEEE/ACM 47th International Conference on Software Engineering: Companion Proceedings (ICSE-Companion)},
pages = {},
numpages = {},
keywords = {Supply Chain Protection, Program Analysis, Malware Detection},
location = {Ottawa, Canada},
series = {ICSE SEIP 2025}
}
```
