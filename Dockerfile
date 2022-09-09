FROM ubuntu:20.04


WORKDIR /home/root/

RUN apt-get update  \
    && apt-get upgrade -y \
    && apt-get install -y \
    && apt-get -y install curl \
    && curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.03.1-ce.tgz \
    && tar --strip-components=1 -xvzf docker-17.03.1-ce.tgz -C /usr/local/bin \
    && apt-get -y install gcc mono-mcs\
    && apt-get -y install sudo \
    && apt-get -y install software-properties-common  \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get -y install python3.7 \
    && apt-get -y install python3-pip python3 python3-setuptools \
    && apt-get -y install libpython3.7-dev \
    && apt-get -y install python3.7-distutils \
    && apt-get -y install python3-apt \
    && apt-get -y install python3-pip \
    && apt-get -y install unzip 
    # 

RUN useradd -m dev && echo "dev:dev" | chpasswd && adduser dev sudo


COPY requirements.txt /home/root/requirements.txt
COPY . /home/root/

ADD . /home/root/

RUN python3.7 -m pip install -r requirements.txt
RUN python3.7 -m pip install -e .


USER dev
CMD /bin/bash

# docker run -v /var/run/docker.sock:/var/run/docker.sock -ti docker
# docker build . -t lid-ds
# docker run -t -i --rm -v /var/run/docker.sock:/var/run/docker.sock lid-ds bash