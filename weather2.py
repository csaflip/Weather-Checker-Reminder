from bs4 import BeautifulSoup
import ssl
import time
import smtplib
from datetime import date
import requests
import json

with open('config.json') as infile:
    data = json.load(infile) #FIXTHIS
    users = data['users'][0]
    email = data['email']
    password = data['pass']
    port = data['port']
    url_1 = data['url_1']
    url_2 = data['url_2']

page = requests.get(url_1)
soup = BeautifulSoup(page.content, 'html.parser')
today = soup.find(id="seven-day-forecast")
fore = today.find_all(class_="tombstone-container")
rtoday = fore[0]
img = rtoday.find("img")
desc = img['title']

page = requests.get(url_2)
soup = BeautifulSoup(page.content, 'html.parser')
precips = soup.findAll(color='#996633')
umbrella = False
first_rain = 7
for x in range(1, 12):
    print(precips[x].text)
for x in range(1, 12): #only precips for the current day
    if int(precips[x].text) >= 25:
        first_rain += x
        umbrella = True
        break

if first_rain > 12:
    first_rain = first_rain - 12
    first_rain = str(first_rain) + ':00 p.m'
elif first_rain == 12:
    first_rain = str(first_rain) + ':00 p.m'
else:
    first_rain = str(first_rain) + ':00 a.m'


if umbrella:
    desc = "\nBRING AN UMBRELLA!!\nFirst rain chance @" + first_rain + "\nToday is " + str(date.today()) + "\n" + desc
else:
    desc = "\nToday is " + str(date.today()) + "\n" + desc
print(desc)





context = ssl.create_default_context()
msg = desc

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as loggerserver:
    loggerserver.login(email, password)

    for user, phone in users.items():
        loggerserver.sendmail(email, phone, msg)
        time.sleep(1)
