#!/bin/bash

echo "Tapez 'open' suivi de ENTER pour afficher l'image dans le navigateur, 'get' suivi de ENTER pour télécharger l'image générée, 'print' suivi de ENTER pour afficher l'URL, 'new' suivi de ENTER pour générer une nouvelle image ou ' exit' suivi de ENTER pour quitter:"
read -r query

while [ "$query" != "exit" ]
do
    url=$(python3 - <<END
import openai
openai.api_key="     "
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


    echo "Tapez 'open' suivi de ENTER pour afficher l'image dans le navigateur, 'get' suivi de ENTER pour télécharger l'image générée, 'print' suivi de ENTER pour afficher l'URL, 'new' suivi de ENTER pour générer une nouvelle image ou ' exit' suivi de ENTER pour quitter :"
    read -r option

    while [ "$option" != "new" ]
    do
        if [ "$option" = "exit" ]
        then
            exit 0
        elif [ "$option" = "get" ]
        then
            random_number=$(shuf -i 0-1000 -n 1)
            filename="picgpt$random_number.png"
            curl -o "$filename" "$url"
            echo "Image téléchargée en tant que $filename"
        elif [ "$option" = "print" ]
        then
            echo "$url"
        elif [ "$option" = "open" ]
        then
            xdg-open "$url"
        else
            echo "Option invalide. Veuillez réessayer."
        fi

    echo " "
    echo " "

        echo "Tapez 'open' suivi de ENTER pour afficher l'image dans le navigateur, 'get' suivi de ENTER pour télécharger l'image générée, 'print' suivi de ENTER pour afficher l'URL, 'new' suivi de ENTER pour générer une nouvelle image ou ' exit' suivi de ENTER pour quitter :"
         read -r option
    done

    echo " "
    echo " "

    echo "Tapez 'open' suivi de ENTER pour afficher l'image dans le navigateur, 'get' suivi de ENTER pour télécharger l'image générée, 'print' suivi de ENTER pour afficher l'URL, 'new' suivi de ENTER pour générer une nouvelle image ou ' exit' suivi de ENTER pour quitter:"
        read -r query
done
