#!/bin/bash
sudo apt-get update
sudo apt-get install openjdk-21-jdk -y

#ngrok setup & install
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
tar -xf ngrok-v3-stable-linux-amd64.tgz

#installing required modules
pip install mega.py
pip install requests
#pip install --upgrade tenacity

clear