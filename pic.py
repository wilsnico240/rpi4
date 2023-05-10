import sys
import openai
import webbrowser
import requests

openai.api_key="********************"

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
open_conditions = ("open")

while True:
    query = input("Type 'open' followed by 'Enter' to vieuw image in browser, 'get' followed by 'Enter' to download the generated image, 'exit' followed by 'Enter' to exit script, 'print' followed by 'Enter' to see url of image:  ")
    if query in print_conditions:
        print(url)
    if query in exit_conditions:
        break
    if query in get_conditions:
        response = requests.get(url)
        with open('picgpt.png', 'wb') as f:
            f.write(response.content)
        print("Image 'picgpt.png' downloaded !!!")
    if query in open_conditions:
         webbrowser.open(url)
    else:
        print("    ")
