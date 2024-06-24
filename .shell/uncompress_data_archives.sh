#!/bin/sh

mkdir -p data/raw
tar -xJf data/original.tar.xz -C data/raw --strip-components=1
