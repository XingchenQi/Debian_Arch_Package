#!/bin/bash

echo "Please enter the architecture name to view the top 10 packages:"
read -p ":" arch
echo "Please wait for the file to download and calculate related packages for $arch"
output=$(python3 package_statistics.py $arch)
echo "$output"