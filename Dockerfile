FROM nvidia/cuda:10.2-cudnn8-runtime-ubuntu18.04

WORKDIR /home/usr/

RUN apt-get update -y \
    && apt-get install -y wget \
    && apt-get -y install curl \
    && apt-get -y install sudo \
    && apt-get install -y libhdf5-dev libxml2-dev libxslt1-dev zlib1g-dev \
    && apt-get install -y unzip  

# Install Chrome
#RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
#RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
#RUN apt-get update && apt-get install -y google-chrome-stable  
    
# Install Docker
RUN  curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.03.1-ce.tgz \
    && tar --strip-components=1 -xvzf docker-17.03.1-ce.tgz -C /usr/local/bin 

COPY requirements.txt /home/usr/requirements.txt
COPY . /home/usr/

ADD . /home/usr/

CMD /bin/bash 

# docker run -v /var/run/docker.sock:/var/run/docker.sock -ti docker
# docker build . -t lid-ds
# docker run -t -i -v /var/run/docker.sock:/var/run/docker.sock lid-ds_docker_sock bash

# Error pytables
# apt-get build-dep python-tables
# HDF5_DIR=/usr/lib/x86_64-linux-gnu/hdf5/serial/ && pip install tables
