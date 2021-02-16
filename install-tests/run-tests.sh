#!/bin/bash
set -euox pipefail

TEST=${TEST:-}

cp ../config.yaml ../install/config.yaml

cd ..

docker build -t jakubbujny/smoggler:latest .

docker save -o install/image.tgz jakubbujny/smoggler:latest

cd install-tests
if [ ! -z "${TEST}" ]; then
  cd ${TEST}
  bash entrypoint.sh
  cd ..
else
  for d in */ ; do
      cd $d
      bash entrypoint.sh
      cd ..
  done
fi
