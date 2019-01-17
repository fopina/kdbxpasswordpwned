#!/bin/sh

cd $(dirname $0)

docker build -t fopina/kdbxpasswordpwned .
docker push fopina/kdbxpasswordpwned:latest
