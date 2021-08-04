 

import requests
import json
import numpy as np
import pandas as pd
import openpyxl
import sched, time
import os
from twisted.internet import task, reactor
import math
import time
import datetime
import random
import string
from datetime import date
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def createAccount(email,Firstname, Surname, phoneNumber, country):
        #create password
    password = generatePassword()
    #attempt to create the account
    url = "https://api.cryptosrvc.com/authentication/user_authentication/signUp"

    payload = '{"username":"'+str(email)+'" ,"password": "'+str(password)+'", "exchange": "BLOCKKOIN","userAttributes": [{"name": "custom:given_name","value": "'+str(Firstname)+'"},{"name": "custom:surname","value": "'+str(Surname)+'"},{"name": "custom:phone_number","value": "'+str(phoneNumber)+'"},{"name": "custom:country","value": "'+str(country)+'"}]}'
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    #check if the account exists or not
    print(response.text)
    accountAlreadyExists = accountExists(response) 

   # path= "C:\\Users\\Admin01\\OneDrive - office 365 Biz 2020\\SignedOnCustomers.xlsx"
   # wb_obj = openpyxl.load_workbook(path)
   # sheet_obj = wb_obj.active;     


    #attribute the password to the appropriate cell
    #storedPosition = len(sheet_obj['F'])
    if(accountAlreadyExists):
        #cool no issue
        #sheet_obj['D'+str(storedPosition)] =""
        print(email)
        print('Account already exists')
    else:
        #store password

        #sheet_obj['D'+str(storedPosition)] = ""+password 
        emailNewUser(email,Firstname, Surname, password)
        recordPassword(email,password)
        print('Account does not exist, \nCreating an account')
    #wb_obj.save(path)

def generatePassword():

    #gets the range of lowercase values
    lower = string.ascii_lowercase

    #gets the range of uppercase values
    upper = string.ascii_uppercase

    #gets the range of integer values
    num = string.digits

    #gets the range of symbols that Blockkoins account allows us to use
    symbols = ['!','@','$','%','^','&','*','<','>','?']

    #randomly samples a set of 3 ascii values of each type
    lowercaseSamples = random.sample(lower,3)
    uppercaseSamples = random.sample(upper,3)
    numberSamples = random.sample(num,3)
    symbolsSamples = random.sample(symbols,3)

    password = []
    passwordString = ""
    for i in range(3):
        password.append(str(lowercaseSamples[i])+str(uppercaseSamples[i])+str(numberSamples[i])+str(symbolsSamples[i]))

    passwordString = "".join(map(str,password))
    return passwordString


def getAccountDetails():
    global firstname
    global surname
    global email
    global path
    global wb_obj
    global sheet_obj
    global storedPosition
    path= "C:\\Users\\Admin01\\OneDrive - office 365 Biz 2020\\SignedOnCustomers.xlsx"
    wb_obj = openpyxl.load_workbook(path, data_only = True)
    sheet_obj = wb_obj.active  

    storedPosition = len(sheet_obj['C'])+1
    for i in range(1,storedPosition):
        print(i)
        firstname = sheet_obj['A'+str(i)].value
        surname = sheet_obj['B'+str(i)].value
        email = sheet_obj['C'+str(i)].value
    # = sheet_obj['D1'].value need to set this value
        orderNumber = sheet_obj['E'+str(i)].value
        phoneNumber = sheet_obj['G'+str(i)].value
        country = sheet_obj['H'+str(i)].value
    #now that we have the account details we create the account
        createAccount(email,firstname,surname, phoneNumber, country)
    time.sleep(4)






def accountExists(response):
    responseJSON = response.json()
    exists = responseJSON['result']
    exists = not exists
    return exists

def printError(e):
    with open('Error.txt', 'a') as f:
        #getting current time for logging the error
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        f.write('\n Account Creation Error at'+' '+str(d1)+' '+str(current_time)+' '+'\nError:'+ str(e) + str(e.args)) 
        print('error file updated')
        
def recordPassword(email, password):
    with open('Credentials.txt', 'a') as f:
        #getting current time for logging the error
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        f.write('\n Account Creation email:'+' '+str(email)+' '+str(current_time)+' '+'  Password:'+ str(password)) 
        print('credential file updated')

def emailNewUser(email,firstname, surname, passwordEmail):
    sender_email = "exchange@blockkoin.io"
    receiver_email = email
    password = "BK@Exchangeyr2021"
    host = "smtp.ionos.co.uk"
    port = 465
    message = MIMEMultipart("alternative")
    message["Subject"] = "Blockkoin Account"
    message["From"] = sender_email
    message["To"] = receiver_email
    text = 'Hi there {0} {1} \n\nWe noticed that you purchased some BK-Koin and we have taken the liberty of creating an account for you.\n\nYour temporary account password is {2} \n\nWe also sent you your verification code in a separate email, please note that this expires within 24 hours.\n\n You can log into your account at https://exchange.blockkoin.io/login\n\nHappy Trading!\nThe Blockkoin Team.'.format(firstname,surname,passwordEmail)
    message.attach(MIMEText(text, "plain"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )   

while True:
    try: 
        getAccountDetails()
    except Exception as e:
        printError(e)
        continue