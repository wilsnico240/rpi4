#!/bin/bash

interval=300 # 5 * 60

url="https://api.sat24.com/animated/EU/infraPolair/3/Romance%20Standard%20Time/9407075"

while true
do
    response=$(curl -o wallpaper.gif -w '%{http_code}' "$url")
    if [ "$response" -eq 200 ]
    then
        echo "Image download @:" $(date +"%Y-%m-%d %H:%M:%S")
    else
        echo "Error download image."
    fi

    sleep "$interval"
done
