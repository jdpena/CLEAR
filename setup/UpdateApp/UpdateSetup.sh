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

function updateSetup() {
    local SERVICE="$1"

    echo "Using update function"
    local START_REMOTE_REPO_PATH="~/CLEAR_Platform"
    local SERVER=$(getEnvironmentVariable "$SERVICE")
    local USER=$(getEnvironmentVariable "${SERVER}_user")
    # Referencing autoSetup project. This is the path to this setup proj
    local SETUP_REPO_PATH="CLEAR_setup"
    local SETUP_REPO_PATH="$(dirname "${SETUP_REPO_PATH}")"
    local SETUP_REMOTE_PATH="${START_REMOTE_REPO_PATH}/CLEAR_setup"

    # Create remote directory for SETUP if it does not exist
    ssh -v -l ${USER} ${SERVER} "mkdir -p ${SETUP_REMOTE_PATH}"
    
    # Updating the remote systems setup application
    rsync -avz --verbose --delete --exclude '.git/' "${SETUP_REPO_PATH}/" ${USER}@${SERVER}:${SETUP_REMOTE_PATH}/
}
