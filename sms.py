import time
import json
import requests
import urllib3
import cv2
import re
import time

from tokenize import Name
from unicodedata import name
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome #importing driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver

#country = input("Enter Country Code. ID=Indonesia | RU=Russia : ") #get country from user | for future
country = "ID"

path ="C:\\Projects\\chromedriver.exe" #path for the driver

print("Acknowledged path for the driver...")
driver = Chrome(executable_path=path) #chrome acknowledged path for the driver

print("(Buff) Path okay!...")
driver2 = Chrome(executable_path=path) #path works

driver.maximize_window() #maximize browser
############################################################################################################################
#                                       Fetching Number & Entering Number on buff                                          #
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
Id= str(data['id']) #get ID
if (data['number'] is ValueError ):
    print("Number not alloted")
number = data['number']
print("Number: " + data['number']) #printing number 
print("Id: " + Id) #printing id 
print("Countrycode: " + data['CountryCode']) #printing countrycode

driver2.get("https://buff.163.com/") #open buff
print("(Buff) Site opened!...")
driver2.maximize_window() #maximize browser
wait = driver2.implicitly_wait(10)
element = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[onclick*='loginModule.showLogin()']"))))
ActionChains(driver2).move_to_element(element).perform()
element.click() #clicking on login/register
print("(Buff) Login clicked!...")

if driver2.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[2]/div[2]/span/i'):
    print("(Buff) Found Agree button") #searching agreement button
driver2.implicitly_wait(5)
driver2.find_element(By.XPATH, '/html/body/div[9]/div[2]/div/div[2]/div[2]/span/i').click()
print("(Buff) Agree button clicked") #sucessfully clicked agreement button

WebDriverWait(driver2, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '/html/body/div[9]/div[2]/div/div[1]/iframe')))
print("(Buff) Login box found") #switching to login document

time.sleep(2) #delay because site ki mkc

gotya = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/div[1]'))))
ActionChains(driver2).click(gotya).perform()
print("(Buff) clicked countrycode")

Indonesia = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/div[2]/a[206]'))))
ActionChains(driver2).click(Indonesia).perform()
print("(Buff) clicked Indonesia")

Inputnumber = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[2]/div[1]/input'))))
ActionChains(driver2).click(Inputnumber).perform()
ActionChains(driver2).send_keys_to_element(Inputnumber, number).perform()
print("(Buff) Number Entered")

############################################################################################################################
######################################           CAPTCHA                   ################################################
############################################################################################################################
'''
bgimg = cv2.imread(WebDriverWait(driver2, 20).until(EC.element_to_be_selected((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div/div/div[1]/div/div[1]/img[1]')))) #background of captcha
puzzleimg = cv2.imread(WebDriverWait(driver2, 20).until(EC.element_located_to_be_selected((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[3]/div/div/div[1]/div/div[1]/img[2]')))) #puzzle peice of captcha

# Identify the edge of the image
bg_edge = cv2.Canny(bgimg, 320, 160) #constant dimensions of the puzzle captcha
tp_edge = cv2.Canny(puzzleimg, 320, 160)

bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

# Gap matching
res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res) # Looking for the best match

X = max_loc[0] # location of the gap

# Draw a box
th, tw = tp_pic.shape[:2]
tl = max_loc # The coordinates of the upper left corner
br = (tl[0]+tw,tl[1]+th) # The coordinates of the lower right corner
cv2.rectangle(bgimg, tl, br, (0, 0, 255), 2) # Draw a rectangle
cv2.imwrite('out.jpg', bgimg) # Keep it locally
'''
#gand marao, khud karo
############################################################################################################################
#                                                Getting Sms                                                               #
############################################################################################################################
print("Solve the Captcha...")
time.sleep(1)
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
sms = re.findall(r'\d+',str(data2['sms']))
convert = list(map(int, sms))
otp = ([int(x) for x in convert])
print("otp:" + str(convert))
print (type(convert))

loop_end = time.time() + 60 * 12

while time.time() < loop_end:
  #  time.sleep(20) #waiting just in case poor connection
    #print("Fetching sms(again)...")
    driver.get("""\
    https://smspva.com/priemnik.php?\
    metod=get_sms
    &country="""+country+
    """&service=opt19
       &id="""+Id+"""
    &apikey=unGlH4wwXmFi6U1aEhf2g9P7JUCjTB""")
    element2 = driver.find_element(By.TAG_NAME, 'body').text
    data2 = json.loads(element2) #converting into json
    sms = re.findall(r'\d+',str(data2['sms']))
    otp = list(map(int, sms))
    matches = [x for x in otp if x > 0 (x)]
    if (matches):
         print(sms)
         print(otp)
         Inputotp = (WebDriverWait(driver2, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[2]/form/div/div[4]/div/div[1]/div[1]/input'))))
         ActionChains(driver2).click(Inputotp).perform()
         ActionChains(driver2).send_keys_to_element(Inputotp, otp).perform()
         print("(Buff) OTP Entered")
    else:
        print('Message not yet received retrying in 20s')
        time.sleep(20)
        print("retrying...")
        continue 
print ("720s Expired. Restart.")

time.sleep(10000) #waiting, because laude ka baal band kardeta hai browser ~1000seconds.
#"\u3010NETEASE\u3011Verification code: 217475_"    test otp
