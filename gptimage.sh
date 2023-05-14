#!/bin/bash

echo "Enter the desired keywords separated by a comma to generate the image, or type 'exit' followed by ENTER to quit:"
read -r query

while [ "$query" != "exit" ]
do
    url=$(python3 - <<END
import openai
openai.api_key="  "
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

    echo "Type 'open' followed by ENTER to view the image in browser, 'get' followed by ENTER to download the generated image, 'print' followed by ENTER to show the URL, 'new' followed by ENTER to generate a new image, or 'exit' followed by ENTER to quit:"
    read -r option

    while [ "$option" != "new" ]
    do
        if [ "$option" = "exit" ]
        then
            exit 0
        elif [ "$option" = "get" ]
        then
            random_number=$(shuf -i 0-1000 -n 1)
            filename="gptimage$random_number.png"
            curl -o "$filename" "$url"
            echo "Image downloaded as $filename"
        elif [ "$option" = "print" ]
        then
            echo "$url"
        elif [ "$option" = "open" ]
        then
            xdg-open "$url"
        else
            echo "Invalid option. Please try again."
        fi

    echo " "

        echo "Type 'open' followed by ENTER to view the image in browser, 'get' followed by ENTER to download the generated image, 'print' followed by ENTER to show the URL, 'new' followed by ENTER to generate a new image, or 'exit' followed by ENTER to quit:"
        read -r option
    done

    echo " "

    echo "Enter the desired keywords separated by a comma to generate the image, or type 'exit' followed by ENTER to quit:"
    read -r query
done
