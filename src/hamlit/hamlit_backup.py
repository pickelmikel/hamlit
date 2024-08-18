"""Main module."""
import ujson
import pandas as pd

class ReadFile:
    
    file_dict = {'Technician':'E2_2022.json','General':'E3_2023.json','Extra':'E4_2024.json'}
    
    def readfile():
        # This loads the json files and creates class attributes using file_dict keys:
        # Technician, General, Extra
        for k,v in ReadFile.file_dict.items():
            with open(v, 'r') as file:
                setattr(ReadFile, k, ujson.load(file))
                

class ShowData:
    
    def screen(x):
        data = ujson.dumps(x, indent=4)
        print(data)

class DData:
    
    def to_dataframe(x):
        DData.df = pd.DataFrame(x)
        return DData.df
    
    def to_dict(x):
        DData.tech = dict(x)
        return DData.tech

### RUN CODE ###

# Create class attributes to ReadFile
# Technician, General, Extra 
ReadFile.readfile()

# Convert each json to a dict
tech = DData.to_dict(ReadFile.Technician)
general = DData.to_dict(ReadFile.General)
extra = DData.to_dict(ReadFile.Extra)

tech_pool = tech['pool'][0]['sections'][3]['questions']
general_pool = general['pool'][0]['sections'][3]['questions']
extra_pool = extra['pool'][0]['sections'][3]['questions']

tech_pool_test = tech['pool']

def find_all_keys(d, parent_key=''):
    keys = []
    if isinstance(d, dict):
        for k, v in d.items():
            full_key = f"{parent_key}.{k}" if parent_key else k
            keys.append(full_key)
            if isinstance(v, dict) or isinstance(v, list):
                keys.extend(find_all_keys(v, full_key))
    elif isinstance(d, list):
        for i, item in enumerate(d):
            full_key = f"{parent_key}[{i}]"
            keys.append(full_key)
            if isinstance(item, dict) or isinstance(item, list):
                keys.extend(find_all_keys(item, full_key))
    return keys


def pn(d, indent=0):
    for k,v in d.items():
        print(" " * indent + str(k))
        if isinstance(v, dict):
            pn(v, indent + 4)
        

#all_keys = find_all_keys(tech)
#ShowData.screen(all_keys)
t0 = tech['pool'][9]
#ShowData.screen(t0)
print(t0.get('id'))

