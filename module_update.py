import requests

def update(module=""):
    """Fetch modules from Github and write them to folder"""
    nba = requests.get("https://raw.githubusercontent.com/Yoonsen/Modules/master/{module}.py".format(module=module))
    
    if nba.status_code == 200:
        nba = nba.text
        with open('{m}.py'.format(m=module),'w', encoding='UTF-8') as pyfile:
            pyfile.write(nba)
        print("Updated file {module}.py".format(module=module))
    else:
        print("Det oppstod en feil med ", module, nba.status_code)
    return

update("nbtext")
update("nbpictures")