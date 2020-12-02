#!/usr/local/bin/bash

# Pure Bash, no calls to other executables
# Requires Bash 4+

declare -A map
while read code; do
  for (( i=0; i<${#code}; i++ )); do
    key="${code:0:$i}${i}${code:$(( i + 1 )):${#code}}"
    if [ ! -z ${map[$key]} ]; then
      echo "${code:0:$i}${code:$(( i + 1 )):${#code}}"
      exit
    else
      map[$key]="1"
    fi
  done
done <input.txt