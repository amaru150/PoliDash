

#JSON handling
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