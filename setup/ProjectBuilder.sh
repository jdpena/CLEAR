#!/bin/bash
##################################################################
# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.
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
        exportSecretsFromFile "$BASE_ENV"
        saveSecretsToFile
        if getEnvironmentVariable "$SERVICE"; then
            exportSecretsFromFile "$SERVICE"
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
# setup still must be checked. 
checkCondaEnv "$BASE_ENV"
saveSecretsToFile

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