#!/bin/bash
# Detect Operating System

# Get the absolute directory of this script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

ADDRESS_FILE="${SCRIPT_DIR}/address"  # Define the address file name

# Check if address file exists, if not, check for the INTERFACE_ADDRESS environment variable or ask the user
if [[ ! -f $ADDRESS_FILE ]]; then
    if [[ -n $INTERFACE_ADDRESS ]]; then
        echo "$INTERFACE_ADDRESS" > $ADDRESS_FILE  # Save the INTERFACE_ADDRESS to the file
        interface_host=$INTERFACE_ADDRESS
    else
        read -p "What machine is hosting the interface? : " interface_host
        echo "$interface_host" > $ADDRESS_FILE  # Save the interface_host to the file
    fi
else
    interface_host=$(cat $ADDRESS_FILE)  # Read the interface_host from the file
fi

# Ask for the machine hosting the interface and save to the file
ADDRESS="$interface_host"  # Contents read from the file

OS="Unknown"
if [[ "$(uname)" == "Darwin" ]]; then
    OS="Mac"
    NAME_OF_APP="macSim.app"
    PATH_TO_SIM="${SCRIPT_DIR}/platforms/${NAME_OF_APP}"

    # If the game does not exist as either a file or directory
    if [[ ! -f "$PATH_TO_SIM" && ! -d "$PATH_TO_SIM" ]]; then
        echo "rats $PATH_TO_SIM"
        python "${SCRIPT_DIR}/downloadApp.py" "${ADDRESS}" "${NAME_OF_APP}"
    fi

    open "$PATH_TO_SIM"

elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    OS="Linux"
    MINI_INSTALL_NAME="Miniconda3-latest-Linux-x86_64.sh"

else
    echo "Unknown OS. Exiting."
    exit 1
fi
