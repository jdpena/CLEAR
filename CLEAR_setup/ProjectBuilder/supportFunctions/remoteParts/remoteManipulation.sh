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
function sync_and_run() {
    # SSH login information
    # Check if the required parameters are passed

    # if [ $# -lt 1 ]; then
    #     echo "Usage: $0 <SERVICE_NAME> <SERVICE_GIT_URL>"
    #     exit 1
    # fi

    local SERVER=$1
    local SERVICE_NAME=$2
    local SERVICE_GIT_URL=$3

    echo "The server is $SERVER"

    local USER="$(getEnvironmentVariable ${SERVER}_user)"

    echo "The user is $USER"
    
    # Dynamically determine the path of the parent script (the script that called this function)
    local PARENT_SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[1]}")" && pwd)/$(basename "${BASH_SOURCE[1]}")"
    
    # Determine the repository path which houses the parent script
    local PARENT_REPO_PATH="$(dirname "${PARENT_SCRIPT_PATH}")"
    
    # Get the name of the parent repository
    local PARENT_REPO_NAME="$(basename "${PARENT_REPO_PATH}")"
    
    # Specify the remote path where the parent repository should be sent, in this case, 'theRepo'
    local REMOTE_REPO_PATH="~/CLEAR_Platform/${PARENT_REPO_NAME}"
    
    # The script you want to run on the remote server (assumed to be the parent script itself)
    local SCRIPT_NAME="$(basename "${PARENT_SCRIPT_PATH}")"
    # local SCRIPT_NAME="simple.sh"
    
    # SSH into the remote server and create 'theRepo' directory if it does not exist
    ssh -l ${USER} ${SERVER} "mkdir -p ${REMOTE_REPO_PATH}"
    
    # Rsync the parent repository to the new directory under 'theRepo' on the remote server
    # -a: archive mode (preserves permissions, ownership, timestamps, etc.)
    # -v: verbose (provides detailed output)
    # -z: compress file data during the transfer
    # --delete: delete extraneous files from destination dirs (this makes the remote repo exactly match the local repo)
    saveSecretsToFile
    rsync -avz --delete --exclude '.git/' --exclude '*.md' --exclude 'tmp/' --exclude 'clearconda/' "${PARENT_REPO_PATH}/" ${USER}@${SERVER}:${REMOTE_REPO_PATH}
    # rm "InformationFiles/secrets"

    echo "Running script as ${SCRIPT_NAME} ${SERVICE_NAME} ${SERVICE_GIT_URL} yes"

    # SSH into the remote server and run the script
    # export PATH=~/miniconda3/bin:\$PATH && source ~/miniconda3/bin/activate

    ssh -tt -l ${USER} ${SERVER} "bash -s" <<EOF
      cd ${REMOTE_REPO_PATH}
      find $REPO_DIR -type f -name "*.sh" -exec chmod +x {} \;
      conda deactivate
      ./CondaSetup/miniSetup.sh
      source ~/clearconda/bin/activate
      conda info -e
      ./${SCRIPT_NAME} ${SERVICE_NAME} ${SERVICE_GIT_URL} yes
      exit
EOF
}
