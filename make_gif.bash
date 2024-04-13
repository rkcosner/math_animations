#!/bin/bash

# Check if no argument is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <foldername>"
    exit 1
fi

foldername="$1"

scenename="$2"

# Check if the folder exists
if [ ! -d "$foldername" ]; then
    echo "Folder '$foldername' not found."
    exit 1
fi

# Check if the scene exists
if [ ! -d "$foldername/$scenename" ]; then
    echo "Scene '$scenename' not found."
    exit 1
fi

# Get full path extension
first_mp4_file=$(find "${foldername}/${scenename}/media/videos/scene/480p15/" -maxdepth 1 -type f -name "*.mp4" | head -n 1)

# Create gif from video 
ffmpeg -i "$first_mp4_file" -vf "fps=10,scale=320:-1:flags=lanczos" -c:v pam -f image2pipe - | convert -delay 10 - -loop 0 -layers optimize "gifs/${foldername}_${scenename}.gif"