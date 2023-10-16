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
if [ $# -lt 1 ]; then
    echo "Usage: $0 <SERVICE_NAME> [<COORDINATOR_CLASS>] [<ROBOT_RUN_INSTRUCTIONS>] [<SERVICE_GIT_URL>]"
    exit 1
fi

SERVICE="$1"
COORDINATOR_CLASS="$2"
ROBOT_RUN_INSTRUCTIONS="$3"
SERVICE_GIT_URL="$4"
BASE_ENV=$(getInitName)

COORDINATOR_CLASS_VARIABLE_NAME="${SERVICE}_COORDINATOR_CLASS"
ROBOT_VARIABLE_NAME="robot"
CHANGE_FLAG="change"
ROBOT_VAR_ADDRESS_NAME="${SERVICE}_raw_git"
ROBOT_VAR_INSTRUCTIONS_NAME="${SERVICE}_RUN_INSTRUCTIONS"

# Set Robot Var to point to specific robot platform
addEnvVariables "$BASE_ENV" "$ROBOT_VARIABLE_NAME" "$SERVICE" "$CHANGE_FLAG"

# Set parameters for the coordinator class that relate to the robot
if [ ! -z "$COORDINATOR_CLASS" ]; then
    addEnvVariables "$BASE_ENV" "$COORDINATOR_CLASS_VARIABLE_NAME" "$COORDINATOR_CLASS" "$CHANGE_FLAG"
fi

# The instructions on how to run the application from the root directory. 
# example : command <dir>/<sub-dir>/<script> or python launch/platform/main.py
if [ ! -z "$ROBOT_RUN_INSTRUCTIONS" ]; then
    addEnvVariables "$BASE_ENV" "$ROBOT_VAR_INSTRUCTIONS_NAME" "$ROBOT_RUN_INSTRUCTIONS" "$CHANGE_FLAG"
fi

# Sets the git url for the robot application
if [ ! -z "$SERVICE_GIT_URL" ]; then
    addEnvVariables "$BASE_ENV" "$ROBOT_VAR_ADDRESS_NAME" "$SERVICE_GIT_URL" "$CHANGE_FLAG"
fi  

(
    launchCondaEnv "$BASE_ENV"
    python main.py
    exit 0
)