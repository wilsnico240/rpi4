#!/bin/bash

query=$(zenity --entry --text="Entrez les mots clés souhaités séparés par une virgule pour générer l'image, ou tapez 'Quitter' suivi de ENTER pour quitter:")

while [ "$query" != "Quitter" ]
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

     option=$(zenity --list --text="Choisis une option:" --column=Options "Afficher l'image dans le navigateur" "Télécharger l'image" "Générer une nouvelle image" "Quitter")

     while [ "$option" != "Générer une nouvelle image" ]
     do
         if [ "$option" = "Quitter" ]
         then
             exit 0
         elif [ "$option" = "Télécharger l'image" ]
         then
             random_number=$(shuf -i 0-1000 -n 1)
             filename="picgpt$random_number.png"
             curl -o "$filename" "$url"
             zenity --info --text="Image téléchargée en tant que $filename"
         elif [ "$option" = "Afficher l'image dans le navigateur" ]
         then
             xdg-open "$url"
         fi

         option=$(zenity --list --text="Choisis une option:" --column=Options "Afficher l'image dans le navigateur" "Télécharger l'image" "Générer une nouvelle image" "Quitter")
     done

     query=$(zenity --entry --text="Entrez les mots clés souhaités séparés par une virgule pour générer l'image, ou tapez 'Quitter' suivi de ENTER pour quitter:")
done
