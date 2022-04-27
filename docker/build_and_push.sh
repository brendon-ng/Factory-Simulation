#!/bin/bash
docker build --no-cache --ssh default -t brendonng/createmesimulation:simulation-app .
docker push brendonng/createmesimulation:simulation-app
