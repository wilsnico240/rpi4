import sys
import openai

openai.api_key="**********"

import requests

def img_gen(query):
    response = openai.Image.create(
        prompt=query,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# main program
query= input("Enter the desired keywords separated by a comma to generate the image:  ")
url = img_gen(query)

exit_conditions = ("exit")
get_conditions = ("get")
print_conditions = ("print")

while True:
    query = input("Type 'get' followed by 'Enter' to download the generated image, 'exit' followed by 'Enter' to exit script, 'print' followed by 'Enter' to see url of image:  ")
    if query in print_conditions:
        print(url)
    if query in exit_conditions:
        break
    if query in get_conditions:
        response = requests.get(url)
        with open('afbeelding.png', 'wb') as f:
            f.write(response.content)
        print("Image downloaded !!!")
    else:
        print(url)
