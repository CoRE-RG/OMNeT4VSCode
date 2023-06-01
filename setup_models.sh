#! /bin/bash
# This script will setup the models for the project

set -e # Exit on error

echo "INFO: Make sure you have setup ssh access to git.inet.haw-hamburg.de"

# Download core simulation models from INET GIT
INET_GIT_USER="git"
INET_GIT_URL="git.inet.haw-hamburg.de"
REPO_SIM_PREFIX="/core/source/simulation/"
CORE4INET="CoRE4INET"
FICO4OMNET="FiCo4OMNeT"
OPENFLOW="OpenFlow"
SDN4CORE="SDN4CoRE"
SIGNALSANDGATEWAYS="SignalsAndGateways"
SOA4CORE="SOA4CoRE"

echo "Downloading CoRE Sim Models from INET GIT"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$CORE4INET"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$FICO4OMNET"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$OPENFLOW"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$SDN4CORE"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$SIGNALSANDGATEWAYS"
git clone "$INET_GIT_USER@$INET_GIT_URL:$REPO_SIM_PREFIX$SOA4CORE"

# Download the inet framework from GITHUB
echo "Downloading INET Framework from GITHUB"
git clone git@github.com:inet-framework/inet.git

# Checkout the correct versions and branches
CORE_BRANCH="integration"
INET_VERSION="v3.6.6"

echo "Checking out CoRE Sim Models on $CORE_BRANCH branches"
cd "$CORE4INET"
git checkout "$CORE_BRANCH"
cd "../$FICO4OMNET"
git checkout "$CORE_BRANCH"
cd "../$OPENFLOW"
git checkout "$CORE_BRANCH"
cd "../$SDN4CORE"
git checkout "$CORE_BRANCH"
cd "../$SIGNALSANDGATEWAYS"
git checkout "$CORE_BRANCH"
cd "../$SOA4CORE"
git checkout "$CORE_BRANCH"

echo "Checking out inet $INET_VERSION"
cd "../inet"
git -c advice.detachedHead=false checkout "$INET_VERSION"
echo "Getting inet submodules"
git submodule update --init --recursive

echo "Done, you should be good to go!"
