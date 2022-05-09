# Remove negative.txt and positive.dat if they exist
rm -f -- negative.txt positive.dat

# Loop through all images in the negative directory
for file in negative/*.png; do
  # Append file name to negative.txt
  echo "$file" >> negative.txt
done

# TODO: Generate positive dataset using python script

# TODO: Generate cascaded file using negative.txt and positive.dat

# Print success message
echo 'Finished!'