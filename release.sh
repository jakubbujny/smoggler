#!/usr/bin/env bash

echo "Version? like 0.0.0"
read version

sed "s/version:.*/version: ${version}/g" -i config.yaml

sed "s/VERSION=.*/VERSION=${version}/g" -i install/install.sh

git add -A
git commit -m "release ${version}"
git push
git tag ${version}
git push --tags

export VERSION=${version}

./docker-release.sh
