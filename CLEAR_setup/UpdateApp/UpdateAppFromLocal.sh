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

# Updates remote machine setup script along with the target dir
source ./ProjectBuilder/supportFunctions/environmentHandler.sh
source ./LaunchApp/checking.sh
source ./ProjectBuilder/supportFunctions/gitFunctioning.sh
source ./UpdateApp/UpdateSetup.sh

SERVICE="$1"

# If the service is a remote system, then launch it on the remote server
# Starts this process by updating/giving this setup repo, 
# to the target machine
if checkForEnvValue "remote_systems" "$SERVICE"; then
    START_REMOTE_REPO_PATH="~/CLEAR_Platform"
    SERVER=$(getEnvironmentVariable "$SERVICE")
    USER=$(getEnvironmentVariable "${SERVER}_user")
    updateSetup "$SERVICE"
    PATH_TO_POPUP_PY="UpdateApp/LocalUpdatePopup.py"
    givePathManually=false 

    # Use Python script to get directory path if a display is available
    TARGET_REPO_PATH=$(python "$PATH_TO_POPUP_PY")
    status=$?  # Save the exit status

    # If status is not equal to 0, then 
    # the user will input the path manually
    if [ $status -ne 0 ]; then
        echo "Please enter the system path to the target project:"
        read -r TARGET_REPO_PATH
        #Yes this is needless, but readability is good
        TARGET_REPO_PATH="$TARGET_REPO_PATH"
    fi

    TARGET_REMOTE_PATH="${START_REMOTE_REPO_PATH}/${SERVICE}" 
    # Create remote directory for TARGET if it does not exist
    ssh -v -l ${USER} ${SERVER} "mkdir -p ${TARGET_REMOTE_PATH}"
    # Updating the remote target project
    rsync -avz --verbose "${TARGET_REPO_PATH}/" ${USER}@${SERVER}:${TARGET_REMOTE_PATH}/
    exit 0
else 
    echo "The service is not remote, update the application on this machine"
    exit 1
fi
