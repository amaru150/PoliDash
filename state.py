def unpack_nests(input_container,primarykey,output_container):
    for items in container: #For lists in Dictionary element
        values = {}
        key = ""

        for field in list(items): #For each field in list element
            content = items.get(field)
            key = items.get(primarykey)
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

            values.update(data)
        output_container.update(
        {primarykey: container}
        )
    return output_container

class repsentative:

    def __init__(self,id,chamber,session_year):
        api_key = 'sTeeVu0CD2BFGFOhTOuyBn3OnGH6Wtqq'
        self.id = id
        self.chamber = chamber
        self.session_year = session_year
        politician = {}
        legislation = {}



def parse_nysenate(api,chamber,limit):
        start_year = 2011 if api == 'committees' else 2009
        chamber = '' if api == 'bills' else "/"+chamber
        deytuh = {}

        for year in range (start_year,curent_year):
            resp= requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&limit={limit}&key={api_key}').json()
            
            if (resp['success'] == 1):
                offsetEnd = resp['offsetEnd']
                total_pages = math.ceil(resp['total'] / limit)
                for page in range (1,2):
                    resp= requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&offset={offsetEnd+1}&limit={limit}&key={api_key}').json()
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

print(parse_nysenate('members','senate',3))

def state_import():

    #Request and store as dictionaries data from nysenate Bills, Committee, and Members Api
    api_key = 'sTeeVu0CD2BFGFOhTOuyBn3OnGH6Wtqq'
    session_year = 2019
    politician = {}
    legislation = {}

    #Parse data from nysenate Bills, Committee, and Members Api
    def parse_nysenate(api,chamber,limit):
        start_year = 2011 if api == 'committees' else 2009
        chamber = '' if api == 'bills' else "/"+chamber
        deytuh = {}

        for year in range (start_year,curent_year):
            resp= requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&limit={limit}&key={api_key}').json()
            
            if (resp['success'] == 1):
                offsetEnd = resp['offsetEnd']
                total_pages = math.ceil(resp['total'] / limit)
                for page in range (1,2):
                    resp= requests.get(f'http://legislation.nysenate.gov/api/3/{api}/{year}{chamber}?full=true&offset={offsetEnd+1}&limit={limit}&key={api_key}').json()
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
    
#state_import()