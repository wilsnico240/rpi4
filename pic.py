import sys
import openai

openai.api_key=""

import requests

def img_gen(query):
    response = openai.Image.create(
        prompt=query,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# main program
query= input("Entrez les mots clés souhaités séparés par une virgule pour générer l'image:  ")
url = img_gen(query)

exit_conditions = ("exit")
get_conditions = ("get")
print_conditions = ("print")

while True:
    query = input("Tapez 'get' suivi parla touche 'Entrée' pour télécharger l'image générée:  ")
    if query in print_conditions:
        print(url)
    if query in exit_conditions:
        break
    if query in get_conditions:
        response = requests.get(url)
        with open('afbeelding.png', 'wb') as f:
            f.write(response.content)
        print("Afbeelding gedownload.")
    else:
        print(url)
