import requests
import json
import math
import sqlite3
from sqlite3 import Error
from datetime import datetime


#Import NYC Council Persons, Legislation into Database
curent_year = datetime.today().year

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
def ny_import():
    
    
    api_key = 'sTeeVu0CD2BFGFOhTOuyBn3OnGH6Wtqq'
    session_year = 2019

    #Parse data from nysenate Bills, Committee, and Members Api
    def parse_nysenate(api,chamber,limit):
        start_year = 2011 if api == 'committees' else 2009
        chamber = '' if api == 'bills' else "/"+chamber
        deytuh = {}

        for year in range (start_year,curent_year):
            req = requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&limit={limit}&key={api_key}')
            resp = req.json()
            
            if (resp['success'] == 1):
                offsetEnd = resp['offsetEnd']
                total_pages = math.ceil(resp['total'] / limit)
                for page in range (1,2):
                    req = requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&offset={offsetEnd+1}&limit={limit}&key={api_key}')
                    resp = req.json()
                    if resp['responseType'] != 'empty list':
                        for i in range(0,limit):
                            container = {}
                            items = resp['result']['items'][i]
                            print(i)
                            for field in list(items):
                                content = items.get(field)
                                primarykey = items.get('memberId')
                                data = unpack_nests(field,content)
                                container.update(data)
                        deytuh.update(
                            {primarykey: container}
                        )
        return deytuh

    #Loops and stores data from all apis and chambers
    def grab_nysenate():
        api = ['members','committees','bills']
        chamber = ['senate','assembly']
        limit = 3
        container = {}

        for apis in api:
            for chambers in chamber:
                container.update(
                        {apis: parse_nysenate(apis,chambers,limit)}
                    )
        print(container)
    grab_nysenate()
    
def propub_import():
    api_key = 'a819EVguXs3g0g2reDwgWy1hd5RWY6QOH6ubf82t'

    def parse_pro(congress,chamber):
        header = {'X-API-Key': api_key}
        resp = requests.get(f'https://api.propublica.org/congress/v1/{congress}/{chamber}/members.json',headers=header).json()
        print(resp)

    parse_pro(116,'house')

propub_import()