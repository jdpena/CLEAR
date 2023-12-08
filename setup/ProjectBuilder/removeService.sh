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

# String to look for and remove
target_string="$1"
# Conda environment name
env_name="$2"

# Directory where the environment variables for the Conda environment are stored
activate_dir=$(conda info --base)/envs/$env_name/etc/conda/activate.d
env_vars_script=$activate_dir/env_vars.sh

# Function to remove the target string from a given value
remove_target() {
    NEW_VALUES=()
    IFS=',' read -ra ADDR <<< "$1"
    for i in "${ADDR[@]}"; do
        trimmed=$(echo "$i" | xargs)
        if [[ "$trimmed" != "$target_string" ]]; then
            NEW_VALUES+=("$trimmed")
        fi
    done
    new_string=$(IFS=,; echo "${NEW_VALUES[*]}")
    echo "$new_string"
}

# Check if the target string is empty
if [[ -z "$target_string" ]]; then
    echo "Usage: source ./removeService.sh <target_string> <conda_environment_name>"
    return 1
fi

# Check if the env_vars_script exists
if [ ! -f "$env_vars_script" ]; then
    echo "No env_vars.sh script found for the Conda environment '$env_name'."
    return 1
fi

# Make a backup of the original env_vars_script
cp "$env_vars_script" "${env_vars_script}.bak"

# Modify the env_vars_script to reflect these changes permanently
awk -v target="$target_string" -F '=' '
BEGIN {OFS="="; IGNORECASE=1}
{
    if ($1 ~ "export " target) {
        # Skip lines that export the target variable
        next
    } else if (match($2, target)) {
        # Modify lines that include the target string in the value
        gsub(target ",", "", $2);
        gsub("," target, "", $2);
        gsub(target, "", $2); # for single value match
        if ($2 != "") {
            print $0
        }
        next
    }
    print $0
}
' "$env_vars_script" > "${env_vars_script}.tmp"

# Replace the original env_vars_script with the modified one
mv "${env_vars_script}.tmp" "$env_vars_script"

echo "Environment variables have been permanently removed or modified in the Conda environment '$env_name'."
