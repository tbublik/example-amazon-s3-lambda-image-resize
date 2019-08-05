#!/usr/bin/env bash

docker run --rm -it -v $(pwd):/tmp/packages python:3.7 pip install Pillow -t /tmp/packages