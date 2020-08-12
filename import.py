import requests
import json
import math
import sqlite3
from sqlite3 import Error
from datetime import datetime

#Database Handling
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, sql):
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)


#Import NYC Council Persons, Legislation into Database

#Global Variables
curent_year = datetime.today().year
delta = curent_year - 2009

#Useful Functions
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
    def create_tables():
        database = r"data.db"
        sql_create_reps_table = """ CREATE TABLE IF NOT EXISTS ny_state_reps (
                                        id INTEGER PRIMARY KEY,
                                        memberID INTEGER,
                                        sessionMemberID INTEGER,
                                        shortName TEXT,
                                        sessionYear TEXT,
                                        chamber TEXT,
                                        districtCode INTEGER,
                                        fullName TEXT,
                                        incumbant TEXT,
                                        prefix TEXT,
                                        firstname TEXT,
                                        lastname TEXT,
                                        email TEXT,
                                        phone TEXT,
                                        address TEXT,
                                        city TEXT,
                                        state TEXT,
                                        alternate TEXT,
                                        ); """
                                        

        sql_create_bills_table = """CREATE TABLE IF NOT EXISTS ny_state_bills (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        priority integer,
                                        status_id integer NOT NULL,
                                        project_id integer NOT NULL,
                                        begin_date text NOT NULL,
                                        end_date text NOT NULL,
                                        FOREIGN KEY (project_id) REFERENCES projects (id)
                                    );"""

        conn = create_connection(database)

        # create tables
        if conn is not None:
            # create projects table
            create_table(conn, sql_create_reps_table)

            # create tasks table
            create_table(conn, sql_create_bills_table)
        else:
            print("Error! cannot create the database connection.")

    api_key = 'sTeeVu0CD2BFGFOhTOuyBn3OnGH6Wtqq'
    session_year = 2019
    politician = {}
    legislation = {}

    def list_politicians(chamber,delta,limit):
        for year in range (2009,curent_year):
            req = requests.get(f'http://legislation.nysenate.gov/api/3/members/{year}/{chamber}?full=true&limit={limit}&key={api_key}')
            resp = req.json()
            offsetEnd = resp['offsetEnd']
            if (resp['success'] == 1):
                total_pages = math.ceil(resp['total'] / limit)
                for page in range (1,2):
                    req = requests.get(f'http://legislation.nysenate.gov/api/3/members/{year}/{chamber}?full=true&offset={offsetEnd+1}full=true&key={api_key}')
                    resp = req.json()
                    for members_ct in range(1,limit):
                        member = {}
                        items = resp['result']['items'][members_ct]
                        for field in list(items):
                            content = items.get(field)
                            primarykey = items.get('memberId')
                            data = unpack_nests(field,content)
                            member.update(data)
                            politician.update(
                                {primarykey: member}
                            )
   
    list_politicians('senate')
    print(politician)
    print(list(politician[384]))

    def add_politicians():
        list_politicians('assembly',delta)
        list_politicians('senate',delta)
        create_connection('db')



   def state_bills(delta,limit):
        for year in range (2009,curent_year):
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

state_import()

    #Persons
    
    #Legislation

#Import State Congressional Persons, Legislation into Database

    #API Calls
   # def state_import():
    #Persons
    
    #Legislation

#Import Federal congressional Persons, Legislation into Database
    #API Calls

    #Persons
    
    #Legislation