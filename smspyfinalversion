from itertools import dropwhile
from os import system
import time
import json
import requests
import urllib3
import os
import re
from tokenize import Name
from unicodedata import name
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome #importing driver
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

querystringnumber = {"metod":"get_number","country":"ID","service":"opt19","apikey":"unGlH4wwXmFi6U1aEhf2g9P7JUCjTB"}
headers = {"Content-Type": "application/json"}
url = "https://smspva.com/priemnik.php"
path ="C:\\Projects\\chromedriver.exe" #path for the driver
driver2 = Chrome(executable_path=path) #chrome acknowledged path for the driver
os.system('cls||clear')
outputfile = open("output.txt","w")
with open("accnt.txt","r") as fp:
    x = len(fp.readlines())
    print ("Number of accounts: " + str(x))
for line in open("accnt.txt","r").readlines():
    login_info = line.split()
    username = login_info[0] 
    password = login_info[1]   
    print(username + " " + password)
    print("-------------------------------------------------------------------------")
    response = requests.request("GET", url, headers=headers, params=querystringnumber)
    data = response.json()
    id = data['id']
    number = data['number']
    countrycode = data['CountryCode']
    lifespan = data['lifeSpan']
    sms = data['sms']
    responsesmspva = data['response']
    print( str(responsesmspva) + str(lifespan ))
    if responsesmspva == "2":
        print("Number not alloted. Retrying in a minute")
        time.sleep(10)
        continue
    elif responsesmspva == "1":
        querystringdeny = {"metod":"denial","country":"ID", "service":"opt19", "id": id, "apikey":"unGlH4wwXmFi6U1aEhf2g9P7JUCjTB"}
        querystringsms = {"metod":"get_sms","country":"ID","service":"opt19","id": id, "apikey":"unGlH4wwXmFi6U1aEhf2g9P7JUCjTB"}
        print("[SMSPVA] Response: " +responsesmspva)
        print("[SMSPVA] Number: " + str(number)) #printing number 
        print("[SMSPVA] Id: " + str(id)) #printing id 
        print("[SMSPVA] Countrycode: " + countrycode) #printing countrycode
        print("[SMSPVA] sms: " + str(sms))
        driver2.maximize_window() #maximize browser
        driver2.get("https://buff.163.com/") #open buff
        print("[BUFF] Site opened!...")
        driver2.maximize_window() #maximize browser
        wait = driver2.implicitly_wait(10)
        element = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='loginModule.showLogin()']"))))
        ActionChains(driver2).move_to_element(element).perform()
        element.click() #clicking on login/register
        print("[BUFF] Login clicked!...")
        time.sleep(5) #delay because site ki mkc
        if driver2.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[2]/div[2]/span/i'):
            print("[BUFF] Found Agree button") #searching agreement button
        driver2.implicitly_wait(7)
        driver2.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[2]/div[2]/span/i').click()
        print("[BUFF] Agree button clicked") #sucessfully clicked agreement button
        WebDriverWait(driver2, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[9]/div[2]/div/div[1]/iframe')))
        print("[BUFF] Login box found") #switching to login document
        time.sleep(7) #delay because site ki mkc
        gotya = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/div[1]'))))
        ActionChains(driver2).click(gotya).perform()
        print("[BUFF] clicked countrycode")
        Indonesia = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/div[2]/a[206]'))))
        ActionChains(driver2).click(Indonesia).perform()
        print("[BUFF] clicked Indonesia")
        Inputnumber = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/input'))))
        ActionChains(driver2).click(Inputnumber).perform()
        ActionChains(driver2).send_keys_to_element(Inputnumber, number).perform()
        print("[BUFF] Number Entered")
        print("Solve the Captcha...")
        time.sleep(7)
        print("[SMSPVA] Fetching sms...")
        response2 = requests.request("GET", url, headers=headers, params=querystringsms)
        data2 = response2.json()
        sms = data2['sms']
        responsesmspva2 = data2['response']
        print(sms)
        loop_end = time.time() + 60 * 10 # loop 10 minutes
        while time.time > loop_end:
            response2 = requests.request("GET", url, headers=headers, params=querystringsms)
            print(response2)
            data2 = response2.json()
            sms = data2['sms']
            responsesmspva2 = data2['response']
            print(sms)
            if (responsesmspva2 == 1):
                sms = re.findall(r'\d+',str(data2['sms']))
                otp = list(map(int, sms))
                Inputotp = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div/div[1]/div[1]/input'))))
                ActionChains(driver2).click(Inputotp).perform()
                ActionChains(driver2).send_keys_to_element(Inputotp, otp).perform()
                print("[BUFF] OTP Entered")
            else:
                    print('Message not yet received retrying in 20s')
                    time.sleep(20)
                    print("retrying...")
                    continue 
        print ("[SMSPVA] 10mins Expired. Denying Number")    
        requests.request("GET", url, headers=headers, params=querystringdeny)
        print("[SMSPVA] Number Refused ") #printing countrycode
        driver2.execute_script("window.open('');")
        driver2.implicitly_wait(10)
        driver2.switch_to.window(driver2.window_handles[1])
        driver2.get("https://store.steampowered.com/login/")
        driver2.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[5]/div/div[1]/div/div/div/div[2]/div/form/div[3]/div[1]').click()
        driver2.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[5]/div/div[1]/div/div/div/div[2]/div/form/div[1]/input').send_keys(username)
        print("enterd username...")
        driver2.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[5]/div/div[1]/div/div/div/div[2]/div/form/div[2]/input').send_keys(password)
        print("enterd password...")
        driver2.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[5]/div/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()
        driver2.switch_to.window(driver2.window_handles[0])
        print("Itna tej hua sab kuch, bhaisaab bhagwaan. ")
        outputfile.writelines( "ID" + countrycode + " " + number + " " + username + " " + password + " " + "Otp: " + str(otp))
        outputfile.close()
        print ("[Script] Saved Details in output.txt") 
print("Finished all the accounts...Exiting in 10 seconds.")
time.sleep(10)
