#!/bin/bash

echo "########## aws cli v2 install"
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install


echo "########## create a named profile (name it default as shown below)"
aws configure --profile default


echo "########## install nodejs and npm v16+"
curl -fsSL https://deb.nodesource.com/setup_21.x | sudo -E bash - 
sudo apt-get install -y nodejs


echo "########## install cdk"
sudo npm install -g npm@latest
sudo npm install -g aws-cdk
cdk --version
