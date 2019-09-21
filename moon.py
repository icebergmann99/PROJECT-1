# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json
from pandas.io.json import json_normalize


#date function
from datetime import timedelta, date
dates = []

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

#print("Request Sun and Moon data from usno.navy.mil")
#x = int(input("What year to start? "))
#y = int(input("What is the end year? "))
#LOC = input("What location? (City, ST) ")

start_date = date(2010, 1, 1)
end_date = date(2010, 3, 31)

for single_date in daterange(start_date, end_date):
    #print (single_date.strftime("%d/%m/%Y"))
    dates.append(single_date)
    
dates_df = pd.DataFrame(dates)
dates_df = dates_df.rename(columns={0:"Dates"})

#API Call

moon = pd.DataFrame()
LOC = "Nashville, TN"
miss = ["01/01/2012","02/01/2012", "03/01/2013"]
i = 1

while miss != [] and i<=5:
    #miss = []
    print("Trying pass number: " + str(i))
    z = "."
    for DATE in dates:
        try:
            url = f"https://api.usno.navy.mil/rstt/oneday?date={DATE}&loc={LOC}"
            response = requests.get(url).json()
            #print(json.dumps(response, indent=4, sort_keys=True))
            response_df = json_normalize(response)
            moon = moon.append(response_df)
            z = z + "."
            print(z)
        except ConnectionError:
            miss.append(DATE)
            print("&")
    i += 1
    dates = miss

moon.to_csv(r'Resources/moon.csv')
print(moon.head())
