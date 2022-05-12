#!/bin/bash

# Remove negative.txt and positive.dat if they exist
rm -f -- negative.txt positive.dat

# Check if negative and positive directory exists
if [ ! -d "negative" ] || [ ! -d "positive" ]; then
    echo "Couldn't find training data"
    exit 1
fi

# Loop through all images in the negative directory
for file in negative/*.jpg; do
  # Append file name to negative.txt
  echo "$file" >> negative.txt
done

# Generate positive dataset using python script
# Exit if it failed
if ! python extract.py; then
  echo "Failed to extract positive images"
  exit 2
fi

# TODO: Generate cascade file with opencv_traincascade using negative.txt and positive.dat

# Print success message
echo 'Finished!'