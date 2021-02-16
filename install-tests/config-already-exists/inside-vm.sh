#!/bin/bash
set -euox pipefail
mkdir -p /opt/smoggler

cd /opt/smoggler
cat > config.yaml <<- EOM
version: 0.0.0
prod:
  queueSize: 1
EOM

cd /vagrant
DEV=true bash install.sh

ansible-playbook assertions.yaml
