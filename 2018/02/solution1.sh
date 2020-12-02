#!/usr/local/bin/bash

# Pure Bash, no calls to other executables
# Requires Bash 4+

twos=0
threes=0
while read code; do
  gotthree=0
  gottwo=0
  unset seen
  declare -A seen
  for (( i=0; i<${#code}; i++ )); do
    c="${code:$i:1}"
    if [ ! -z ${seen[$c]} ]; then
      seen[$c]=$(( ${seen[$c]}+1 ))
    else
      seen[$c]="1"
    fi
  done
  for c in "${!seen[@]}"; do
    if [ "${seen[$c]}" -eq "2" -a $gottwo -eq "0" ]; then
      twos=$(( $twos+1 ))
      gottwo=1
    elif [ "${seen[$c]}" -eq "3" -a $gotthree -eq "0" ]; then
      threes=$(( $threes+1 ))
      gotthree=1
    fi
    [ $gottwo -eq "1" -a $gotthree -eq "1" ] && break
  done
done <input.txt
echo $(( $twos*$threes ))