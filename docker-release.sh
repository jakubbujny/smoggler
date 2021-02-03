#!/bin/bash

docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t jakubbujny/smoggler:0.0.5 -t jakubbujny/smoggler:latest --push .
