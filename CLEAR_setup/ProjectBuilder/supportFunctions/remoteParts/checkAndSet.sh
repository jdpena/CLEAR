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

checkIfRemote() {
    # Check if the required parameters are passed
    if [ $# -lt 2 ]; then
        echo "Usage: $0 <setup envir name> <service name>"
        exit 1
    fi

    # Name of the setup environment. 
    BASE_ENV="$1"
    # Assign the second argument to SERVICE
    SERVICE="$2"

    local SETUP_ENV="$(getInitName)"
    read -p "Would you like to setup $SERVICE as a remote instance? (yes/no): " response
    if [[ "$response" =~ ^[Yy][Ee][Ss]|[Yy]$ ]]; then
        read -p "Provide the name of the remote machine, ip, domain name?: " response
        DEVICE_NAME="$response"
        addEnvVariables "$BASE_ENV" "$SERVICE" "$DEVICE_NAME"
        addEnvVariables "$BASE_ENV" "remote_systems" "$SERVICE"

        #If true, means the remote machine has not already been configured.
        #Also adds the value to the remote_systems set
        (
            if ! getEnvironmentVariable "${DEVICE_NAME}_user"; then
                echo "Setting info :"
                read -p "Provide the username of your account within the remote machine : " response
                local USERNAME="$response"
                addEnvVariables "$BASE_ENV" "${DEVICE_NAME}_user" "$USERNAME"

                check_ssh_key "$DEVICE_NAME" "$USERNAME"
            fi
        )
        return 0
    else
        addEnvVariables "$BASE_ENV" "$SERVICE" "local"
        return 1
    fi
}

# Function to check if an SSH key already exists
check_ssh_key() {
    local DEVICE_NAME=$1
    local USERNAME=$2
    
    # Check for the existence of the private key file
    if [ -z "${DEVICE_NAME}_keyed" ]; then 
        echo "SSH key ${DEVICE_NAME} already provided."
    else

        echo "Would you like to create an ssh key for the remote device, $DEVICE_NAME?"
        local prompt="Indicating yes will circumvent repeated inputting of your credentials(yes/no): "
        read -p "$prompt" response

        if [[ "$response" =~ ^[Yy][Ee][Ss]|[Yy]$ ]]; then

            # Check if SSH key already exists
            if [ -f "~/.ssh/id_rsa.pub" ]; then
                echo "SSH key already exists."
            else
                echo "SSH key not found. Generating a new SSH key..."
                ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
            fi
            ssh-copy-id $USERNAME@$DEVICE_NAME 
            addEnvVariables "$BASE_ENV" "${DEVICE_NAME}_keyed" "true"
        fi
    fi
}