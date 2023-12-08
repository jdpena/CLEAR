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

source ./CondaSetup/informUser.sh

if [ ! -n "$BASH_VERSION" ]; then
    echo "The script is not running in Bash. Restarting with Bash..."
    # Rerunning the script in bash, and ending current run
    exec bash "$0" "$@"
    exit 1
fi

# Checking the user
userAcceptance

# Check for conda installation
if ! conda --version &> /dev/null;then
    echo "installing miniconda"
    # Not sourcing because source belowd
    source ./CondaSetup/miniSetup.sh
    source ~/clearconda/bin/activate
fi

python main.py