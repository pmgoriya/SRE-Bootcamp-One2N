#!/bin/bash
set -e

sudo apt update
echo "Install docker from get.docker.com"
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER 
echo "Docker installed"
rm -rf get-docker.sh
echo " Install docker-compose plugin.."

mkdir -p ~/.docker/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-linux-x86_64 \
    -o ~/.docker/cli-plugins/docker-compose

chmod +x ~/.docker/cli-plugins/docker-compose

echo "DockerCompose installed"

echo "installing make"
sudo apt install -y make
# make install

echo "setup complete"