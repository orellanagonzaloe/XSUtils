#!/usr/bin/bash

echo "Setting up ATLAS..."
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -- # the 2 dashes are to avoid problems with negative mu
source $AtlasSetup/scripts/asetup.sh 21.2,AthAnalysis,latest -- 

source run_resummino.sh $1 $2 $3 outputHT