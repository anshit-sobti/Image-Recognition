import configparser
import os
import uuid

config = configparser.ConfigParser()
config.read("config.ini")

config_dic = {}

for option in config['DEFAULT']:
    config_dic[option] = config.get('DEFAULT', option, raw=True)

def store_file(file,location=config_dic.get("upload_path")):
    name = uuid.uuid4().hex
    print(name)
    print(location)
    file.save(os.path.join(location, name))
    return location+name