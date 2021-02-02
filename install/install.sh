#!/bin/bash

apt-get install -y ansible

ansible-galaxy install geerlingguy.docker_arm

cd /tmp

curl -s https://raw.githubusercontent.com/jakubbujny/smoggler/main/install/ansible-local.yaml > ansible-local.yaml

ansible-playbook ansible-local.yaml

cd /opt/smoggler

docker-compose up -d

