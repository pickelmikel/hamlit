"""Main module."""
import os
import requests
import ujson
import pandas as pd
import random

class GetFiles:
    # JSON file URL's from HamStudy.org
    tech_url = 'https://hamstudy.org/api/pools/E2_2022'
    general_url = 'https://hamstudy.org/api/pools/E3_2023'
    extra_url = 'https://hamstudy.org/api/pools/E4_2024'

    def download_files():
        print("Fetching Exam Questions from HamStudy.org...")
        print('Downloading Technician Exam Questions')
        tech_file = requests.get(GetFiles.tech_url)
        print('Downloading General Exam Questions')
        general_file = requests.get(GetFiles.general_url)
        print('Downloading Extra Exam Questions')
        extra_file = requests.get(GetFiles.extra_url)
        ## Gotta do something different here??
        files = [tech_file,general_file,extra_file]
        for file in files:
            if file.status_code != 200:
                print(f'Check your internet - status code:{file.status_code}')
                quit()
        GetFiles.parse_files(tech_file,general_file,extra_file)
                
                
        """if tech_file.status_code == 200:
            if general_file.status_code == 200:
                if extra_file.status_code == 200:
                    GetFiles.parse_files(tech_file,general_file,extra_file)
        else:
            print(f'Check your internet - status code:{tech_file.status_code}')"""
    
            
    def parse_files(tech_file,general_file,extra_file):
        ## Import and parse downloaded JSON files to pass onto write_files function
        tech = ujson.loads(tech_file.text)
        general = ujson.loads(general_file.text)
        extra = ujson.loads(extra_file.text)
        GetFiles.write_files(tech,general,extra)
        
    def write_files(tech_file,general_file,extra_file):
        ## Saves JSON files downloaded from HamStudy.org to local disk
        print('writing files...')
        with open(ReadFile.file_dict['Technician'], 'w') as json_file:
            ujson.dump(tech_file, json_file, indent=4)
        with open(ReadFile.file_dict['General'], 'w') as json_file:
            ujson.dump(general_file, json_file, indent=4)
        with open(ReadFile.file_dict['Extra'], 'w') as json_file:
            ujson.dump(extra_file, json_file, indent=4)
        print(f'Success! Files Saved in {os.getcwd()}')

class ReadFile:
    
    file_dict = {'Technician':'E2_2022.json','General':'E3_2023.json','Extra':'E4_2024.json'}
    
    def check_file():
        # Checks to see if files are locally stored
        # otherwise attempts to download from HamStudy.org
        print(f"Checking for Exam Question files in {os.getcwd()}")
        for key in ReadFile.file_dict.keys():
            if os.path.exists(ReadFile.file_dict[key]):
                continue
            else:
                GetFiles.download_files()
                
    def read_file():
        # This loads the json files and creates class attributes using file_dict keys:
        # Technician, General, Extra
        for k,v in ReadFile.file_dict.items():
            with open(v, 'r') as file:
                setattr(ReadFile, k, ujson.load(file))
                

class ShowData:
     
    question_correct = None
    question_missed = None
    
    num_correct = []
    num_missed = []
    
    
    def screen(x):
        data = ujson.dumps(x, indent=4)
        print(data)

class UserI:
    current_course = None
    current_pool = None
    current_section = None
    quit_list = ['q','Q','73',73,'quit','QUIT']
    
    def input_to_int(prompt):
        while True:
            user_input = input(prompt)
            try:
                if user_input in UserI.quit_list:
                    quit()
                return int(user_input)
            except ValueError:
                print(f"Try another selection")
            
    
    def get_dict_value(data, key):
        return [item.get(key) for item in data]
    
    def get_course():
        for num,key in enumerate(ReadFile.file_dict.keys(),1):
            print(f"{num} - {key}")
        print('73 - Quit Program')
        ans = UserI.input_to_int("What course do you want? ")
        #ans = input("What course do you want? ")
        UserI.current_course = ans
        UserI.get_pool(course_num.get(ans))
        
        
    def get_pool(data):
        for num, item in enumerate(data):
            print(f"{num}. {item.get('name')}")
        print('73 - Quit Program')
        ans = UserI.input_to_int('What pool would you like? ')
        UserI.current_pool = ans
        UserI.get_section(data,ans)
        
    def get_section(data,sec):
        for num, item in enumerate(tech['pool'][sec]['sections']):
             print(f"{num}. - {item.get('summary')}\n")
        print('73 - Quit Program')
        ans = UserI.input_to_int('What section would you like? ')
        UserI.current_section = ans
        UserI.get_random_question(data,sec,ans)
    
    def get_random_question(data,sec,q):
        random_question = random.choice([question for question in data[sec]['sections'][q]['questions']])
        UserI.display_question(random_question)
                
    def display_question(question):
        answers = ['A','B','C','D']
        print(f"\nQuestion id: {question['id']}")
        print(f"\n{question['text']}\n")
        for letter, answer in question['answers'].items():
            print(f"{letter} - {answer}")
        print('\n73 - Quit Program')
        ans = input("\nWhat is your selection? ")        
        if ans.upper() in answers:
            if ans.upper() == question['answer']:
                UserI.answer_correct(question)
            else:
                UserI.answer_missed(question)
        elif ans in UserI.quit_list:
            ExitCode.qcount()
        else:
            print('Try something else')
            UserI.display_question(question)
        
    
    def answer_correct(question):
        print("*" * 30, " You got it! ", "*" * 30)
        if ShowData.question_correct == None:
            ShowData.question_correct = set()
            ShowData.question_correct.add(question['id'])
        else:
            ShowData.question_correct.add(question['id'])
        print(f"Correct Questions - {ShowData.question_correct}")
        if ShowData.question_missed != None:
            print(f"Missed Questions - {ShowData.question_missed}")
        UserI.get_random_question(course_num[UserI.current_course],UserI.current_pool,UserI.current_section)
    
    def answer_missed(question):
        print("Not it, try again")
        if ShowData.question_missed == None:
            ShowData.question_missed = set()
            ShowData.question_missed.add(question['id'])
        else:
            ShowData.question_missed.add(question['id'])
        UserI.display_question(question)
    
    
    def get_question(data,sec,q,p):
        ## Get a specific question: data=dict(source dictionary), sec=int(section),
        ## q=int(sub section),p=int(actual question)
        print(f"\n{data[sec]['sections'][q]['questions'][p]['text']}\n")
        for num, answer in tech['pool'][sec]['sections'][q]['questions'][p]['answers'].items():
            print(f"{num} - {answer}")
        ans = input("\nWhat is your selection? ")
        if ans.upper() == data[sec]['sections'][q]['questions'][p]['answer']:
            print('You got it')
        elif ans in UserI.quit_list:
            quit()
        else:
            print('Not it')
            
class DData:
    
    def to_dataframe(x):
        DData.df = pd.DataFrame(x)
        return DData.df
    
    def to_dict(x):
        DData.tech = dict(x)
        return DData.tech

class ExitCode:
    
    def qcount():
        if ShowData.question_correct != None:
            ccount = len(ShowData.question_correct)
            print(f"\nNumber Correct: {ccount}")
        if ShowData.question_missed != None:
            mcount = len(ShowData.question_missed)
            print(f"Number Missed: {mcount}")
        """if ccount in :
            print("You got 100% Correct!")
        elif mcount in locals():
            print("You got 0% Correct.")
        else:
            tcount = ccount + mcount
            print(f"You got {(ccount/tcount)*100}% Correct!")
        """
    
    
class TestingCode:
    #UserI.get_section(tech_sections, 0)
    #UserI.get_question(0,0,0)
    #UserI.get_pool(tech_pool)
    #ShowData.screen(tech_pool_all)
    #UserI.get_pool()
    #print(UserI.get_section(tech['pool'][0]['sections'], 'summary'))
    #print(tech['pool'][0].get('name'))
    pass

### RUN CODE ###
### RUN CODE ###
# Create class attributes to ReadFile
# Technician, General, Extra 
ReadFile.check_file()
ReadFile.read_file()

# Convert each json to a dict
tech = DData.to_dict(ReadFile.Technician)
general = DData.to_dict(ReadFile.General)
extra = DData.to_dict(ReadFile.Extra)

# dict shortcuts
tech_pool = tech['pool']
general_pool = general['pool']
extra_pool = extra['pool']
course_num = {1:tech_pool,2:general_pool,3:extra_pool}

## User Interface run code ##
UserI.get_course()

    

