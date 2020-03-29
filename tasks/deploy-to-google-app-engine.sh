#!/bin/bash
#---------------------------------------------------------------------------------------------------
# Script to deploy the 'Me' application to Google App Engine. The first argument of the script
# should be the project to which the application is pushed, the second should be the version of the
# services to be pushed. If the second one isn't set, we assume no version
#---------------------------------------------------------------------------------------------------
if [ -z "$1" ]; then
    echo "ERROR: Project not set. Set project first"
else
    if [ -z "$2" ]; then
        echo "WARNING: Using default version"
    else
        echo "Using version $2"
        cmd_version=" --version $2"
    fi

    # Set the project in the gcloud config
    gcloud config set project $1

    # Create the basic command
    cmd="gcloud app deploy"

    # Add all the service files
    for service in $(find -name service.yaml); do
        cmd="$cmd $service"
    done

    # Add all cron files
    for service in $(find -name cron.yaml); do
        cmd="$cmd $service"
    done

    # Add all dispatch files
    for service in $(find -name dispatch.yaml); do
        cmd="$cmd $service"
    done

    # Add the version, if given
    if [ "$cmd_version" != "" ]; then
        cmd="$cmd $cmd_version"
    fi

    # Add the quiet flag
    cmd="$cmd --quiet"

    # Run the command
    $cmd
fi
