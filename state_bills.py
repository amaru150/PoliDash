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