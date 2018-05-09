#! /bin/bash

sudo docker build -t n1te/conv .
sudo docker stop conv
sudo docker rm conv
sudo docker run -d -i -t \
    --name conv \
    -h conv \
    -p 80:8080 \
    n1te/conv