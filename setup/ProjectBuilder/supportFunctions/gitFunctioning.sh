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

function createGitLink() {
  # The original Git URL is passed as an argument
  local ORIGINAL_GIT_URL="$1"
  local GITHUB_USERNAME="$2"
  local GITHUB_PERSONAL_ACCESS_TOKEN="$3"
  # Extract the part after 'https://'
  local GIT_PATH=$(echo $ORIGINAL_GIT_URL | sed 's|https://||')

  # Construct the secure Git URL
  local SECURE_GIT_URL="https://${GITHUB_USERNAME}:${GITHUB_PERSONAL_ACCESS_TOKEN}@${GIT_PATH}"
  
  # Return the secure URL, you can use this function output to set a variable
  echo $SECURE_GIT_URL
}

function gitPull() {
  local GIT_URL=$1
  local DIRECTORY_MOVEMENT=$2

  if [ -z "$GIT_URL" ]; then
    echo "Error: GIT_URL is empty"
    return 1
  fi

  if [ -z "$DIRECTORY_MOVEMENT" ]; then
    echo "Error: DIRECTORY_MOVEMENT is empty"
    return 1
  fi

  echo "pulling from $GIT_URL in directory $DIRECTORY_MOVEMENT"

  # Using a subshell to temporarily change directories
  (
      cd "$DIRECTORY_MOVEMENT" || { echo "Error: Could not change to directory $DIRECTORY_MOVEMENT"; return 1; }
      ls
      git pull "$GIT_URL"
  )
}
