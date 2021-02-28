#!/bin/bash
set -euo pipefail

export VERSION=0.0.8

DEV=${DEV:-"false"}

apt-get update
apt-get install -y ansible curl

if [ "$DEV" = "true" ]; then
  ansible-galaxy install geerlingguy.docker
else
  ansible-galaxy install geerlingguy.docker_arm
fi

if [ "$DEV" != "true" ]; then
  cd /tmp
  curl -s https://raw.githubusercontent.com/jakubbujny/smoggler/${VERSION}/install/ansible-local.yaml > ansible-local.yaml
fi

DEV=${DEV} ansible-playbook ansible-local.yaml

cd /opt/smoggler

if [ "$DEV" = "true" ]; then
  echo "DEV=true" > .env
  echo "VERSION=0.0.8
else
  echo "VERSION=0.0.8
fi

if [ "$DEV" = "true" ]; then
  docker load -i /vagrant/image.tgz
else
  docker-compose pull
fi

docker-compose up -d

set +euo

until $(curl --output /dev/null --silent --head --fail http://localhost); do
    echo 'waiting for smoggler to become available'
    sleep 3
done

echo 'All done!'

cd ${OLDPWD}
