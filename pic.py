import sys
import openai
import webbrowser
import requests

openai.api_key="     "

def img_gen(query):
    response = openai.Image.create(
        prompt=query,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# main program
exit_conditions = ("exit")
get_conditions = ("get")
print_conditions = ("print")
open_conditions = ("open")
new_conditions = ("new")

while True:
     query= input("Enter the desired keywords separated by a comma to generate the image, or type 'exit' followed by ENTER to quit: ")
     if query in exit_conditions:
         sys.exit()

     url = img_gen(query)

     while True:
         query = input("Type 'open' followed by ENTER to view the image in browser, 'get' followed by ENTER to download the generated image, 'print' followed by ENTER to show the URL, 'new' followed by ENTER to generate a new image or 'exit' followed by ENTER to quit: ")
         if query in exit_conditions:
             sys.exit()
         if query in get_conditions:
             response = requests.get(url)
             with open('picgpt.png', 'wb') as f:
                 f.write(response.content)
             print("The image 'picgpt' is downloaded in png format on your computer !!!")
         if query in print_conditions:
             print(url)
         if query in open_conditions:
             webbrowser.open(url)
         if query in new_conditions:
             break
         else:
             print("    ")
