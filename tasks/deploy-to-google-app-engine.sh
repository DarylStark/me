#!/bin/bash
#---------------------------------------------------------------------------------------------------
# Script to deploy the 'Me' application to Google App Engine. The syntax for the script is:
#
# deploy-to-google-app-engine.sh <service> <version> <project>
#---------------------------------------------------------------------------------------------------
# Verify given command line arguments
#---------------------------------------------------------------------------------------------------
if [ -z "$1" ]; then
    echo "ERROR: Service not set"
    exit
else
    cmd_service=$1
fi
if [ -z "$2" ]; then
    echo "ERROR: Version not set"
    exit
else
    cmd_version=$2
fi
if [ -z "$3" ]; then
    echo "ERROR: Project not set."
    exit
else
    cmd_project=$3
fi
#---------------------------------------------------------------------------------------------------
# Set the project in the gcloud config
#---------------------------------------------------------------------------------------------------
echo "--> Setting project"
echo -n "--> "
gcloud config set project $cmd_project

# Go to the correct directory
echo "--> Moving to correct directory"
cd $(dirname $0)
if [ "$cmd_service" == "rest-api-v1" ]; then
    cd ../src/google-app-engine/rest-api-v1
elif [ "$cmd_service" == "web-gui-v1" ]; then
    cd ../src/google-app-engine/web-gui-v1
elif [ "$cmd_service" == "web-gui-v1" ]; then
    cd ../src/google-app-engine/web-gui-v1
else
    echo "ERROR: Service doesn't exist"
    exit
fi

# Add the quiet flag
cmd="gcloud app deploy ./service.yaml --version $cmd_version --quiet"

# Run the command
echo "--> Executing command: $cmd"

$cmd
#---------------------------------------------------------------------------------------------------
