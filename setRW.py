#Write and Read Json files
import json

def read_json():
    with open('settings.json') as f:
        return json.load(f)


def write_json(data):
    with open('settings.json', 'w') as f:
        f.write(data)

def check(id:str):
    data = read_json()
    for i in data['setting']:
        if i['user_id'] == id:
            return 

    with open('defult.json') as f :
        defult = json.load(f)
    
    defult['defult']['user_id'] = id
    data['setting'].append(defult['defult'])
    write_json(json.dumps(data, indent=2))
    return 




#class for modifying the settings.json file settings
class setting_data:
    #find the specific setting by user_id and return the option 
    def find(id:int, option:str):
        id = str(id)
        check(id)
        data = read_json()
        if option == 'all':
            for i in data['setting']:
                if i['user_id'] == id:
                    result = json.dumps(i, indent=2)
        else:
            for i in data['setting']:
                if i['user_id'] == id:
                    result = i[option]
        return result 


    #refresh to the new data 
    def replace(id:int, option:str, content:str):#content 是字串比較方便，這樣就不用辨識後再存取。
        if option == 'user_id':
            return 'Error : cant change user_id, Its from Discord'
        #check if string is number not containing(- and .)
        if option == 'delete_time' and not content.isnumeric():
            return 'Error : please enter numbers only'
        id = str(id)
        check(id)
        data = read_json()
        #return if the option isnt in the setitng.json settings
        if option not in data['setting'][0]:
            return f'Error : Cant find [ \'{option}\' ] in setting'
        for i in data['setting']:
            if i['user_id'] == id:
                i[option] = content
        data = json.dumps(data, indent=2)
        write_json(data)
        return 'Done'