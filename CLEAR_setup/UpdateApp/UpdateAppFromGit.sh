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

#Updates remote machine setup script along with the target dir
source ./ProjectBuilder/supportFunctions/environmentHandler.sh
source ./LaunchApp/checking.sh
source ./ProjectBuilder/supportFunctions/gitFunctioning.sh
source ./UpdateApp/UpdateSetup.sh


# SETUP_ENV=$(getInitName)
# if ! launchCondaEnv "$SETUP_ENV"; then 
#   exit 1
# fi

SERVICE="$1"

if ! [ -z "$2" ]; then 
    GIT_URL="$2"
else 
    GIT_URL=$(getEnvironmentVariable "${SERVICE}_git_url")
fi
echo "$GIT_URL"

# If the service is a remote system, then launch relative 
# the application where it belongs.
# Starts this process by updating/giving this setup repo, 
# to the target machine
if checkForEnvValue "remote_systems" "$SERVICE"; then
    REMOTE_REPO_PATH="~/CLEAR_Platform/CLEAR_setup"
    SERVER=$(getEnvironmentVariable "$SERVICE")
    USER=$(getEnvironmentVariable "${SERVER}_user")
    updateSetup "$SERVICE"

    THIS_SCRIPT="UpdateApp/UpdateAppFromGit.sh"

    ssh -tt -l ${USER} ${SERVER} "bash -s" <<EOF
    cd ${REMOTE_REPO_PATH}
    find $REPO_DIR -type f -name "*.sh" -exec chmod +x {} \;
    conda deactivate
    source ~/clearconda/bin/activate
    conda activate ${SERVICE}
    ./${THIS_SCRIPT} "${SERVICE}" "${GIT_URL}"
    exit
EOF
    exit 0
fi

FILE_PATH="../${SERVICE}"
gitPull "$GIT_URL" "$FILE_PATH" 

