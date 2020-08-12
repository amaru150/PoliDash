import requests
import json
import math
import sqlite3
from sqlite3 import Error
from datetime import datetime


#Import NYC Council Persons, Legislation into Database
curent_year = datetime.today().year
delta = curent_year - 2009

#Useful functions

#Unpacks nested containers
def unpack_nests(field,content):
    data = {}
    if isinstance(content,dict): 
        for subfield in content:
            data.update({subfield: content.get(subfield)})
            
    elif isinstance(content,list):
        for items in content:
            for subfield in items:
                data.update({subfield: content.get(subfield)})

    else:
        data.update({field: content}) 
    #print(type(data))
    return data

#API Calls
def state_import():
    
    
    api_key = 'sTeeVu0CD2BFGFOhTOuyBn3OnGH6Wtqq'
    session_year = 2019
    politician = {}
    legislation = {}

 def list_politicians(chamber,delta):
        while delta > 0:
            req = requests.get(f'http://legislation.nysenate.gov/api/3/members/{2009+delta}/{chamber}?full=true&limit=200&key={api_key}')
            resp = req.json()
            delta -= 1
            if (resp['success'] == 1):
                length = resp['offsetEnd']
                count = 0
                while  count < 50: #length
                    memberId = resp['result']['items'][count]['memberId']
                    if memberId not in politician or (politician[memberId] == {}):
                        chamber = resp['result']['items'][count]['chamber']
                        incumbent = resp['result']['items'][count]['incumbent']
                        shortName = resp['result']['items'][count]['shortName']
                        session_years = list(resp['result']['items'][count]['sessionShortNameMap'])

                        personId = resp['result']['items'][count]['person']['personId'] 
                        fullName = resp['result']['items'][count]['person']['fullName'] 
                        firstName = resp['result']['items'][count]['person']['firstName'] 
                        middleName = resp['result']['items'][count]['person']['middleName'] 
                        lastName = resp['result']['items'][count]['person']['lastName']
                        email = resp['result']['items'][count]['person']['email'] 
                        prefix = resp['result']['items'][count]['person']['prefix'] 
                        suffix = resp['result']['items'][count]['person']['suffix'] 
                        verified = resp['result']['items'][count]['person']['verified']
                        districtCode = resp['result']['items'][count]['districtCode']

                        info = {memberId:{
                            'chamber':chamber,
                            'incumbent':incumbent,
                            'shortName':shortName,
                            'session_years':session_years,
                            'personId':personId,
                            'fullName':fullName,
                            'firstName':firstName,
                            'middleName':middleName,
                            'lastName':lastName,
                            'email':email,
                            'prefix':prefix,
                            'suffix':suffix,
                            'verified':verified,
                            'districtCode':districtCode
                            }
                        }
                        politician.update(info)
                    else:
                        pass
                    
                    count += 1
    

    def state_bills(delta,limit):
            for year in range (2009,curent_year):
                print(year)
                req = requests.get(f'http://legislation.nysenate.gov/api/3/bills/{year}?limit={limit}&full=true&key={api_key}')
                resp = req.json()
                offsetEnd = resp['offsetEnd']
                if (resp['success'] == 1):
                    total_pages = math.ceil(resp['total'] / limit)
                    for page in range (1,total_pages):
                        req = requests.get(f'http://legislation.nysenate.gov/api/3/bills/{year}?limit={limit}&offset={offsetEnd+1}full=true&key={api_key}')
                        resp = req.json()
                        for bills in range (1,limit):
                            bill = {}
                            items = resp['result']['items'][i]
                            for field in list(items):
                                content = items.get(field)
                                primarykey = items.get('basePrintNo')
                                data = unpack_nests(field,content)
                                bill.update(data)
                                legislation.update(
                                    {primarykey: bill}
                                )

    state_bills(delta,10)
    print(legislation)

    
state_import()