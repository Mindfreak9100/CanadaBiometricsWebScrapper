import requests
import re
import smtplib
import json
from bs4 import BeautifulSoup

smtpObj = smtplib.SMTP('smtp-relay.sendinblue.com', 587)
smtpObj.login('dhoom_rik@yahoo.com', 'gPX75Ob038rGfmAc')
bioSites = []
cityDetails = []
count = 0
tableHeaders = [
    "City/port of entry (POE)", "Country/territory", "Website", "Biometrics", "Notes"]
result = requests.get(
    "https://www.cic.gc.ca/english/information/where-to-give-biometrics.asp")
src = result.content

# Parse the reponse from the request
soup = BeautifulSoup(src, 'lxml')

# Find all the data according to cities
city = soup.find_all(
    "td", {"data-search": re.compile("Toronto|Kitchener|Brampton|Mississauga")})

# Filter cities by span tag <SCO>
for i in city:
    if i.find("span").text == "SCO":
        bioSites.append(i.find("span").parent.parent)

# Email to be send
message = """From: WebScrapper Admin <admin@webscrapper.com>
To: Maharsh Patel <maharsh9100@yahoo.com>
MIME-Version: 1.0
Content-type: text/html
Subject: Biometric Status Update

<b>This is an e-mail message to notify to book an appointment for your biometric. Please see the details below:</b>
<table border="1">
<th>City/port of entry (POE)</th><th>Country/territory</th><th>Website</th><th>Biometrics</th><th>Notes</th>
""" + str(bioSites) + """ </table> """

cityDetail = []

for item in bioSites:
    for itemDetails in item.findChildren("td"):
        if count <= 4:
            cityDetail.append(itemDetails.text)
        else: 
            count = 0
    cityDetails.append(cityDetail)
    cityDetail = []

# Validate Appointment availability
for city in cityDetails:
    if city[3] != "Appointments are currently unavailable":
        smtpObj.sendmail('admin@webscrapper.com',['dhoom_rik@yahoo.com','maharsh9100@yahoo.com','komalmgokani@gmail.com', 'shivangibnsl12@gmail.com'], message)
        print("Successfully sent email")
        break
