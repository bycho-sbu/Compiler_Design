# use an Ubuntu base image(for unix base image)
FROM ubuntu:20.04

# set environment variable to avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# update package lists and install Python3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# set the working directory inside the container
WORKDIR /app

# copy all project files into the container
COPY . /app

# default command to run the symbol table manager test driver code
CMD ["python3", "testDriver.py"]

