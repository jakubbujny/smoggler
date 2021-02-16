#!/bin/bash
set -euox pipefail
cd /vagrant

DEV=true bash install.sh

ansible-playbook assertions.yaml
