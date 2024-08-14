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

ReadFile.readfile()

ShowData.screen(ReadFile.Technician)
ShowData.screen(ReadFile.General)
ShowData.screen(ReadFile.Extra)
