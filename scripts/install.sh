mkdir -p HTCondor/log

# Currently it's not possible to install resummino 3.1.1 becuse an older version of boost
# Using instead the version 3.0.0 stored and compiled in backup folder
# source scripts/install_resummino.sh

cp backup/resummino-3.0.0/build/bin/resummino ./