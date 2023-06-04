import requests
import time

interval = 5 * 60
url = "https://www.meteobelgium.net/belgium/sat/last_sat.gif"

while True:
    response = requests.get(url)
    if response.status_code == 200:
        with open('background.gif', 'wb') as f:
            f.write(response.content)
            print("Image download @:", time.strftime("%Y-%m-%d %H:%M:%S"))
    else:
        print("Error download image !!!")
   
    time.sleep(interval)
