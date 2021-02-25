#!/bin/bash

if vagrant up; then
  echo "Tests went fine"
  vagrant destroy -f
else
  echo "failure"
  vagrant destroy -f
  exit 1
fi
