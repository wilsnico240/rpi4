#!/bin/bash

query=$(zenity --entry --text="Enter the desired keywords separated by a comma to generate the image, or type 'exit' to quit:")

while [ "$query" != "exit" ]
do
     url=$(python3 - <<END
import openai
openai.api_key="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"
def img_gen(query):
     response = openai.Image.create(
         prompt=query,
         n=1,
         size="1024x1024"
     )
     return response['data'][0]['url']
print(img_gen("$query"))
END
)

     option=$(zenity --list --text="Choose an option:" --column=Options "View in browser" "Download" "New" "Exit")

     while [ "$option" != "New" ]
     do
         if [ "$option" = "Exit" ]
         then
             exit 0
         elif [ "$option" = "Download" ]
         then
             random_number=$(shuf -i 0-1000 -n 1)
             filename="picgpt$random_number.png"
             curl -o "$filename" "$url"
             zenity --info --text="Image downloaded as $filename"
         elif [ "$option" = "View in browser" ]
         then
             xdg-open "$url"
         fi

         option=$(zenity --list --text="Choose an option:" --column=Options "View in browser" "Download" "Show URL" "New" "Exit")
     done

     query=$(zenity --entry --text="Enter the desired keywords separated by a comma to generate the image, or type 'exit' to quit:")
done
