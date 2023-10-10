#!/bin/bash
##################################################################
# DISTRIBUTION STATEMENT A. Approved for public release. Distribution is unlimited.

# This material is based upon work supported by the Under Secretary of Defense for 
# Research and Engineering under Air Force Contract No. FA8702-15-D-0001. Any opinions,
# findings, conclusions or recommendations expressed in this material are those 
# of the author(s) and do not necessarily reflect the views of the Under 
# Secretary of Defense for Research and Engineering.

# © 2023 Massachusetts Institute of Technology.

# Subject to FAR52.227-11 Patent Rights - Ownership by the contractor (May 2014)

# The software/firmware is provided to you on an As-Is basis

# Delivered to the U.S. Government with Unlimited Rights, as defined in DFARS Part 
# 252.227-7013 or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. Government rights in this work are defined by DFARS 252.227-7013 or 
# DFARS 252.227-7014 as detailed above. Use of this work other than as specifically
# authorized by the U.S. Government may violate any copyrights that exist in this work.
##################################################################

# Function to source a file containing 'export' statements for environment variables
exportEnvVar() {
  # Check if file exists
  if [ ! -f "$1" ]; then
    echo "File not found: $1"
    return 1
  fi

  source "$1"
}

checkCondaEnv() {
    # Assign arguments to variables
    ENV_NAME=$1
    REQUIREMENTS_FILE=$2
    BASE_ENV="$(getInitName)"

    # Check if the environment already exists
    if conda info --envs | grep -q "^$ENV_NAME "; then
        echo "Environment '$ENV_NAME' already exists."
    else
        echo "Creating a new Anaconda environment named '$ENV_NAME'..."

        local INFO_DIR="InformationFiles"
        local ENV_SET="${INFO_DIR}/environmentVariables.txt"

        # Need to export env variables to create env
        exportEnvVar "$ENV_SET"
        
        conda create -n "$ENV_NAME" python=3.8 -y

        if [ -f "$ENV_SET" ]; then
            setEnvVariables "$ENV_NAME" "$ENV_SET"
        else 
            echo "No additional environment variables provided"
        fi

        if [ "$ENV_NAME" == "$BASE_ENV" ]; then 
            installRequirements "$ENV_NAME" "setup"
            # Using this instead of environment variables because
            # this allows greater ease when replicating the setup env

            local ADDRESS_FILE="${INFO_DIR}/addresses"
            if [[ ! -f $ADDRESS_FILE ]]; then
                echo "The following questions refer to the web server addresses."
                echo "The given design has the worker server address as : http://A_SERVER_NAME:9090,"
                echo "while the interface address is https://A(nother)_SERVER_NAME:7070."

                read -p "What machine is hosting the workers? : " worker_host
                echo "Worker Host: $worker_host" >> $ADDRESS_FILE

                # Ask for the machine hosting the interface and save to the file
                read -p "What is the address of the interface? : " interface_host
                echo "Interface Host: $interface_host" >> $ADDRESS_FILE
            else
                echo "File 'addresses' already exists. Skipping prompts."
            fi

            # Check if gitInfo file exists
            local GIT_INFO_FILE="${INFO_DIR}/gitinfo"
            local GIT_IS_PUBLIC="${INFO_DIR}/gitispublic"

                # If GIT_IS_PUBLIC file does not exist
                if [ ! -f "$GIT_IS_PUBLIC" ]; then
                    # If GIT_INFO_FILE file does not exist
                    if [ ! -f "$GIT_INFO_FILE" ]; then

                        read -p "Are you using GitHub repositories that are private? (yes/no): " response
                        if [[ "$response" =~ ^[Yy][Ee][Ss]|[Yy]$ ]]; then

                            touch "$GIT_INFO_FILE"

                            # Prompt user for GitHub username, if not already stored in environment.
                            # Instead of storing in a file, should consider appedning it to the env file
                            if [ -z "$GITHUB_USERNAME" ]; then
                                read -p "Enter your GitHub username: " GHUB_NAME
                                echo #\n
                                echo "GITHUB_USERNAME=$GHUB_NAME" >> "$GIT_INFO_FILE"
                            fi

                            # Prompt user for Personal Access Token
                            if [ -z "$GITHUB_PERSONAL_ACCESS_TOKEN" ]; then
                                read -sp "Enter your GitHub Personal Access Token : " GHUB_TOKEN
                                echo #\n
                                echo "GITHUB_PERSONAL_ACCESS_TOKEN=$GHUB_TOKEN" >> "$GIT_INFO_FILE"
                            fi
                        else 
                            touch "$GIT_IS_PUBLIC"
                        fi
                fi
                
                if [ -f "$GIT_INFO_FILE" ]; then
                    GITHUB_USERNAME=$(grep "GITHUB_USERNAME=" "$GIT_INFO_FILE" | awk -F'=' '{print $2}')
                    addEnvVariables "$BASE_ENV" GITHUB_USERNAME "$GITHUB_USERNAME"
                    GITHUB_PERSONAL_ACCESS_TOKEN=$(grep "GITHUB_PERSONAL_ACCESS_TOKEN=" "$GIT_INFO_FILE" | awk -F'=' '{print $2}')
                    addEnvVariables "$BASE_ENV" GITHUB_PERSONAL_ACCESS_TOKEN "$GITHUB_PERSONAL_ACCESS_TOKEN"
                fi
            fi

        else
            installRequirements "$ENV_NAME" "../$ENV_NAME/setup"
        fi
        
        (
            cd InformationFiles
            local worker_host_value=$(grep "Worker Host:" addresses | cut -d ' ' -f3-)
            addEnvVariables "$ENV_NAME" "WORKER_ADDRESS" "$worker_host_value"

            local interface_host_value=$(grep "Interface Host:" addresses | cut -d ' ' -f3-)
            addEnvVariables "$ENV_NAME" "INTERFACE_ADDRESS" "$interface_host_value"
        )
    fi
}

setEnvVariables() {
    # Check for correct number of arguments
    if [ $# -ne 2 ]; then
        echo "Usage: create_conda_env <env_name> <path_to_export_file>"
        return 1
    fi

    # Assign arguments to variables
    ENV_NAME=$1
    EXPORT_FILE=$2

    # Create the conda environment (modify the Python version as necessary)
    # Note: You may need to uncomment and modify the line below as needed
    # conda create -n $ENV_NAME python=3.8

    # Directory path for activate script
    ACTIVATE_DIR=$(conda info --base)/envs/$ENV_NAME/etc/conda/activate.d

    # Create the activate script directory
    mkdir -p $ACTIVATE_DIR

    # Path to the activate script
    ENV_VARS_SCRIPT=$ACTIVATE_DIR/env_vars.sh

    # Create the activate script from the export file
    cp $EXPORT_FILE $ENV_VARS_SCRIPT

    # Make the activate script executable
    chmod +x $ENV_VARS_SCRIPT

    echo "Conda environment '$ENV_NAME' has been created and configured with the specified environment variables."
}

addEnvVariables() {
    if [ $# -lt 3 ]; then
        echo "Usage: addEnvVariables <env_name> <var_name> <var_value> [change]"
        return 1
    fi
    ENV_NAME=$1
    VAR_NAME=$(echo $2 | tr '-' '_')
    VAR_VALUE=$3
    CHANGE_MODE=$4  # Optional argument for "change"
    ACTIVATE_DIR=$(conda info --base)/envs/$ENV_NAME/etc/conda/activate.d
    mkdir -p $ACTIVATE_DIR
    ENV_VARS_SCRIPT=$ACTIVATE_DIR/env_vars.sh

    if [ ! -f $ENV_VARS_SCRIPT ]; then
        touch $ENV_VARS_SCRIPT
        chmod +x $ENV_VARS_SCRIPT
        echo "#!/bin/bash" > $ENV_VARS_SCRIPT
        echo "echo 'Activating environment $ENV_NAME with custom variables'" >> $ENV_VARS_SCRIPT
    fi

    if [ "$CHANGE_MODE" == "change" ]; then
        echo "export $VAR_NAME=\"$VAR_VALUE\"" >> $ENV_VARS_SCRIPT
    else
        echo "if [ -z \"\${$VAR_NAME}\" ]; then" >> $ENV_VARS_SCRIPT
        echo "    export $VAR_NAME=\"$VAR_VALUE\"" >> $ENV_VARS_SCRIPT
        echo "else" >> $ENV_VARS_SCRIPT
        echo "    if ! echo \",\${$VAR_NAME},\" | grep -q \",${VAR_VALUE},\"; then" >> $ENV_VARS_SCRIPT
        echo "        export $VAR_NAME=\"\${$VAR_NAME},$VAR_VALUE\"" >> $ENV_VARS_SCRIPT
        echo "    fi" >> $ENV_VARS_SCRIPT
        echo "fi" >> $ENV_VARS_SCRIPT
    fi

    echo "Environment variable has been added to the Conda environment '$ENV_NAME'."
}

installRequirements() {
    # Check for correct number of arguments
    if [ $# -ne 2 ]; then
        echo "Usage: setup_conda_env <env_name> <path_to_requirements_directory>"
        return 1
    fi

    # Assign arguments to variables
    ENV_NAME=$1
    REQUIREMENTS_DIR=$2

    # Check if the given path is actually a directory
    if [ ! -d "$REQUIREMENTS_DIR" ]; then
        echo "The provided path is not a directory: $REQUIREMENTS_DIR"
        return 1
    fi

    # Check if conda activation was successful
    conda info

    if source activate $ENV_NAME || conda activate $ENV_NAME; then
        if [ $? -eq 0 ]; then
            OUTPUT=$(conda info)
            echo -e "$OUTPUT \n\n $(printenv)"
            
            # Path to the new single requirements file
            REQUIREMENTS_FILE="$REQUIREMENTS_DIR/requirements.txt"

            # Check if the requirements file exists
            if [ -f "$REQUIREMENTS_FILE" ]; then
                # Read the requirements file line by line
                while read -r line; do
                    # Skip empty lines or lines starting with a comment (#)
                    [[ "$line" =~ ^\#.*$ || "$line" == "" ]] && continue

                    # Execute the command
                    echo "Executing: $line"
                    eval "$line"
                    
                    # Check for errors
                    if [ $? -ne 0 ]; then
                        echo "Failed to execute: $line"
                        return 1
                    fi
                done < "$REQUIREMENTS_FILE"
            else
                echo "Requirements file '$REQUIREMENTS_FILE' does not exist."
                return 1
            fi
        else
            echo "Failed to activate conda environment: $ENV_NAME"
            return 1
        fi

        echo "Packages installed successfully in '$ENV_NAME' environment."
        return 0
    else 
        echo "error, could not activate the '$ENV_NAME' environment."
        exit 1
    fi
}

launchCondaEnv() {
    # Define the path to your conda's activate script
    CONDA_PATH=$(conda info --base)

        # Source the conda.sh script
    source $CONDA_PATH/etc/profile.d/conda.sh

    # Now use the conda command directly in your script
    # Check for environment name argument
    if [ "$#" -ne 1 ]; then
        echo "Usage: $0 <env_name>"
        return 1 
    fi

    # Activate the Conda environment
    conda activate $1

    # Check the activation status
    if [ $? -eq 0 ]; then
        echo "Successfully activated the Conda environment: $1"
        return 0
    else
        echo "Failed to activate the Conda environment: $1"
        return 1
    fi
}

getEnvironmentVariable() {
    # The value provided as command line argument
    VALUE=$1

    # Compose the environment variable name
    VAR_NAME="$VALUE" 

    # Replace hyphens with underscores in VAR_NAME
    VAR_NAME=$(echo $VAR_NAME | tr '-' '_')

    # Try to get the value of the environment variable
    VAR_VALUE=${!VAR_NAME}

    # Check if the environment variable exists
    if [ -z "$VAR_VALUE" ]; then
        echo "Environment variable $VAR_NAME not found."
        return 2
    fi

    # Output the value of the environment variable
    echo $VAR_VALUE
    return 0
}

# Function to check if the active environment is 'base'
checkIfBaseEnv() {
    # Get the currently active conda environment
    local active_env=$(conda info --envs | grep '*' | awk '{print $1}')
    
    if [ "$active_env" == "base" ]; then
        return 0
    else
        return 1
    fi
}

getInitName() {
    local INFO_DIR="InformationFiles"
    local NAME_FILE="${INFO_DIR}/initName"
    
    # Make the directory if it does not already exist
    if [[ ! -d "$INFO_DIR" ]]; then 
        mkdir "$INFO_DIR"
    fi

    #Create file if it does not already exist
    if [[ ! -f "$NAME_FILE" ]]; then
        read -p "Provide a name for the configurement environment? : " name
        echo "$name" >> "$NAME_FILE"
    fi

    if [[ -f "$NAME_FILE" ]]; then
        # Read the content of the file into a variable
        local name=$(<"$NAME_FILE")
        
        # Alternatively, if you want to return the value so you can use it in other functions
        # uncomment the following line
        echo "$name"
    else
        echo "Name file does not exist."
    fi
}
