#!/bin/bash
##################################################################
# DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

# This material is based upon work supported by the Under Secretary of Defense for 
# Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
# findings, conclusions or recommendations expressed in this material are those 
# of the author(s) and do not necessarily reflect the views of the Under 
# Secretary of Defense for Research and Engineering.

# © 2023 Massachusetts Institute of Technology.

# Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

# The software/firmware is provided to you on an As-Is basis

# Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
# 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
# DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
# authorized by the U.S. Government may violate any copyrights that exist in this work.
##################################################################

source ./ProjectBuilder/supportFunctions/environmentHandler.sh
source ./ProjectBuilder/supportFunctions/remoteParts/checkAndSet.sh
source ./ProjectBuilder/supportFunctions/remoteParts/remoteManipulation.sh
source ./ProjectBuilder/supportFunctions/remoteParts/remoteManipulation.sh
source ./ProjectBuilder/supportFunctions/gitFunctioning.sh

# Check if the required parameters are passed
if [ $# -lt 2 ]; then
    echo "Usage: $0 <SERVICE_NAME> <SERVICE_GIT_URL>"
    exit 1
fi

SERVICE="$1"
SERVICE_GIT_URL="$2"

# The third argument is passed for launching script
# on remote machines. This conditional asks if there exists 
# a non null 3rd arg value 
if ! [ -z "$3" ]; then 
    echo "I am Remote $3"
    export I_AM_REMOTE="true"
fi

BASE_ENV=$(getInitName)

checkIfBaseEnv
RELAUNCH=$?

# If I am not remote, and am using a base 
# conda environment, check if the setup env exists.
# If it does not, it will be created. Setup will then be
# Activated and the python main script will restart.  
if [ -z "$I_AM_REMOTE" ]; then 
    if [ $RELAUNCH -eq 0 ]; then
        # checkCondaEnv "$BASE_ENV"
        if launchCondaEnv "$BASE_ENV"; then
            echo "starting python script"
            python main.py
            echo "ended python script"
            exit 6
        fi
    fi
fi

if 
(  
    if launchCondaEnv "$BASE_ENV"; then
        if getEnvironmentVariable "$SERVICE"; then
            echo "The service, ${SERVICE}, already exists"
            exit 0
        fi
    fi
    exit 1
); 
then 
    exit 0
fi

# In case the script is remote, 
# setup still must be checked. Also,
# having it here means it checking if apps 
# exist is faster. If a project exists, 
# this will not run.
checkCondaEnv "$BASE_ENV"

# If not remote, the link will be formatted as 
if [ -z "$I_AM_REMOTE" ]; then 
    # If any git repo is private
    if [ ! -f "$GIT_IS_PUBLIC" ]; then
        SERVICE_GIT_URL=$(createGitLink \
        "$SERVICE_GIT_URL" \
        $(getEnvironmentVariable "GITHUB_USERNAME") \
        $(getEnvironmentVariable "GITHUB_PERSONAL_ACCESS_TOKEN"))
    fi

    dynamic_var_name="${SERVICE}_git_url"
    addEnvVariables "$BASE_ENV" "$dynamic_var_name" "$SERVICE_GIT_URL"

    if checkIfRemote "$BASE_ENV" "$SERVICE"; then 
        launchCondaEnv "$BASE_ENV"
        sync_and_run "$(getEnvironmentVariable $SERVICE)" "$SERVICE" "$SERVICE_GIT_URL"
        exit 1
    fi
    launchCondaEnv "$BASE_ENV"
fi

# Check if the repo $SERVICE does not exist in $PARENT_DIR
if [ ! -d "../$SERVICE" ]; then
    # Download $SERVICE from GitHub
    git clone "$SERVICE_GIT_URL" "../$SERVICE"
else
    echo "app exists"
fi

# Update the project to the most current 
gitPull "$SERVICE_GIT_URL" "../$SERVICE"
# Create environment for $SERVICE
checkCondaEnv "$SERVICE"

exit 0