"""Main module."""
import ujson
import pandas as pd
import random

class ReadFile:
    
    file_dict = {'Technician':'E2_2022.json','General':'E3_2023.json','Extra':'E4_2024.json'}
    
    def readfile():
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
        
    def get_dict_value(data, key):
        return [item.get(key) for item in data]
    
    def get_course():
        for num,key in enumerate(ReadFile.file_dict.keys(),1):
            print(f"{num} - {key}")
        ans = int(input("What course do you want? "))
        UserI.current_course = ans
        UserI.get_pool(course_num.get(ans))
        
    def get_pool(data):
        for num, item in enumerate(data):
            print(f"{num}. {item.get('name')}")
        ans = int(input('What pool would you like? '))
        UserI.current_pool = ans
        UserI.get_section(data,ans)
        
    def get_section(data,sec):
        for num, item in enumerate(tech['pool'][sec]['sections']):
             print(f"{num}. - {item.get('summary')}\n")
        ans = int(input('What section would you like? '))
        UserI.current_section = ans
        UserI.get_random_question(data,sec,ans)
    
    def get_random_question(data,sec,q):
        random_question = random.choice([question for question in data[sec]['sections'][q]['questions']])
        UserI.display_question(random_question)
                
    def display_question(question):
        print(f"\nQuestion id: {question['id']}\n")
        print(f"\n{question['text']}\n")
        for letter, answer in question['answers'].items():
            print(f"{letter} - {answer}")
        ans = input("\nWhat is your selection? ")
        if ans.upper() == question['answer']:
            UserI.answer_correct(question)
        else:
            UserI.answer_missed(question)
    
    def answer_correct(question):
        print("*" * 8, " You got it! ", "*" * 8)
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
        print(f"\n{data[sec]['sections'][q]['questions'][p]['text']}\n")
        for num, answer in tech['pool'][sec]['sections'][q]['questions'][p]['answers'].items():
            print(f"{num} - {answer}")
        ans = input("\nWhat is your selection? ")
        if ans.upper() == data[sec]['sections'][q]['questions'][p]['answer']:
            print('You got it')
        else:
            print('Not it')
            
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

# dict shortcuts
tech_pool = tech['pool']
general_pool = general['pool']
extra_pool = extra['pool']
course_num = {1:tech_pool,2:general_pool,3:extra_pool}
    
tech_sections = "tech['pool'][s]['sections']"

tech_summary = "tech['pool'][s]['sections'][q]['summary']"

#UserI.get_section(tech_sections, 0)
#UserI.get_question(0,0,0)
UserI.get_course()

#UserI.get_pool(tech_pool)

#ShowData.screen(tech_pool_all)
#UserI.get_pool()
#print(UserI.get_section(tech['pool'][0]['sections'], 'summary'))
#print(tech['pool'][0].get('name'))
