import os
import json
from pathlib import Path

if not os.path.exists("Categories.json"):
    with open("Categories.json" , "w") as file:
        json.dump({} , file)

class FileOrganizer:
    def __init__(self):
        self.category = {
            "Images" : [".jpg" , ".png" , ".jpeg"] ,
            "Documents" : [".pdf" , ".docx" , ".txt"] , 
            "Music" : [".mp3" , ".mav"] ,
            "Videos" : [".mp4" , ".mkv"] ,
            "Archives" : [".zip" , ".rar"]
        }

        self.save_file()

    def save_file(self):
        with open("Categories.json" , "w") as file:
            json.dump(self.category , file , indent=4)




acc = FileOrganizer()

print(acc)