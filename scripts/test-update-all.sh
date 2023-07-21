#!/bin/bash
# basic reference for writing script for travis

# Define the array of versions
versions=(3.2 3.3 3.4 4.0 4.1 4.2 4.3 4.4 5.0 5.1 6.0)

# Loop through the array and execute the test.sh script for each version
for version in "${versions[@]}"
do
    ./scripts/test.sh "$version" --snapshot-update
done
