#!/bin/bash

# Check if no argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <foldername>"
    exit 1
fi

foldername="$1"

# Check if the folder exists
if [ ! -d "$foldername" ]; then
    echo "Folder '$foldername' not found."
    exit 1
fi

subfolders=$(find "$foldername" -mindepth 1 -maxdepth 1 -type d)

# Clear README.md, but keep the beginning
head -n 3 "README.md" > temp.txt && mv temp.txt "README.md"
rm tempt.txt

# Loop through each file in the folder
for scene in $subfolders; do
    scenename=$(basename "$scene")
    echo "Scene: $scenename"
    if [ -d "$scene" ]; then
        echo "Running make_gif.sh for file: $foldername/$scenename"
        ./make_gif.bash "$foldername" "$scenename"
    fi

    # Append the gif to the README.md
    echo "" >> "README.md"
    echo "## $foldername: $scenename" >> "README.md"
    echo "![${foldername}_${scenename}](gifs/${foldername}_${scenename}.gif)" >> "README.md"

done
