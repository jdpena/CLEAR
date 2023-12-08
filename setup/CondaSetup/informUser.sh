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

# Checking the user
userAcceptance() {
    # Check if the user has already agreed
    script_dir=$(dirname "$0")
    file_path="${script_dir}/CondaSetup/.userAgreed"

    if [ -f "$file_path" ]; then
        echo "The file .userAgreed already exists."
        return 0
    fi

    echo "This script will install Miniconda on this system if no Anaconda distribution is currently in use."
    echo "Additionally, this application in pursuit of configuring your CLEAR project, has the ability to instruct"
    echo "machines detailed by this current user to also install Miniconda. The terms and conditions of Anaconda are detailed in:"
    echo "https://legal.anaconda.com/policies/en/?name=anaconda-org-terms-and-conditions."
    echo "However, use of the CLEAR Platform does NOT require use of this specific service nor Miniconda;"
    echo "CLEAR setup exists just for your convenience in managing your CLEAR project."
    echo ""

    read -p "Do you accept the terms and conditions of Anaconda? (yes/no): " response
    if [[ "$response" =~ ^[Yy][Ee][Ss]|[Yy]$ ]]; then
        read -p "Do you wish to proceed with the CLEAR setup? (yes/no): " response
        if [[ "$response" =~ ^[Yy][Ee][Ss]|[Yy]$ ]]; then
            touch "$file_path"
            return 0
        fi
    fi
    exit 1
}