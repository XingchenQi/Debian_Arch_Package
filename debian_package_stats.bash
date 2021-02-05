#!/bin/bash

echo "enter architectire you wish to view stats on: "
read -p ":" arch
echo "wait one moment will we pull the stats for $arch"
va=$(python3 debian_package_stats.py $arch)
echo "$va"

