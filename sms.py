import time
import json
import requests
import urllib3

from tokenize import Name
from unicodedata import name
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome #importing driver

#country = input("Enter Country Code. ID=Indonesia | RU=Russia : ") #get country from user | for future
country = "ID"


path ="C:\\Projects\\chromedriver.exe" #path for the driver
print("Acknowledged path for the driver...")
driver = Chrome(executable_path=path) #chrome acknowledged path for the driver

driver.maximize_window() #maximize browser
############################################################################################################################
#                                                Fetching Number                                                           #
############################################################################################################################
print("Fetching Number...")
driver.get("""\
    https://smspva.com/priemnik.php?\
    metod=get_number
    &country="""+country+
    """&service=opt19
    &apikey=unGlH4wwXmFi6U1aEhf2g9P7JUCjTB""") #get number

driver.implicitly_wait(3) #waiting just in case poor connection
element = driver.find_element(By.TAG_NAME, 'body').text 
data = json.loads(element) #converting into json
Id= str(data['id']) #hardcoded Id position
if (data['number'] is ValueError ):
    print("Number not alloted")

print("Number: " + data['number']) #printing number 
print("Id: " + Id) #printing id 
print("Countrycode: " + data['CountryCode']) #printing countrycode
############################################################################################################################
#                                                Getting Sms                                                               #
############################################################################################################################
print("Fetching sms in 20s...")
time.sleep(20)
driver.implicitly_wait(5) #waiting just in case poor connection
print("Fetching sms...")
driver.get("""\
    https://smspva.com/priemnik.php?\
    metod=get_sms
    &country="""+country+
    """&service=opt19
       &id="""+Id+""" 
    &apikey=unGlH4wwXmFi6U1aEhf2g9P7JUCjTB""") #get sms from site
element2 = driver.find_element(By.TAG_NAME, 'body').text 
data2 = json.loads(element2) #converting into json
sms = str(data2['sms'])
print(sms)

while sms == 'None': 
  #  time.sleep(20) #waiting just in case poor connection
    print("Fetching sms(again)...")
    driver.get("""\
    https://smspva.com/priemnik.php?\
    metod=get_sms
    &country="""+country+
    """&service=opt19
       &id="""+Id+"""
    &apikey=unGlH4wwXmFi6U1aEhf2g9P7JUCjTB""")
    element2 = driver.find_element(By.TAG_NAME, 'body').text
    data2 = json.loads(element2) #converting into json
    try: 
      sms = data2['sms']

    except ValueError: 
        print('Message not yet received retrying in 20s')
        time.sleep(20)
        print("retrying...")
        continue 
    else: 
       print(sms)

time.sleep(10000) #waiting, because laude ka baal band kardeta hai browser ~1000seconds.