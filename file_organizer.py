import os
import json
import shutil
from pathlib import Path


class FileOrganizer:
    def __init__(self):
        self.category = {
            "Images" : [".jpg" , ".png" , ".jpeg"] ,
            "Documents" : [".pdf" , ".docx" , ".txt"] , 
            "Music" : [".mp3" , ".wav"] ,
            "Videos" : [".mp4" , ".mkv"] ,
            "Archives" : [".zip" , ".rar"]
        }
        
        if os.path.exists("Categories.json"):
            self.load_file()
        else:
            self.save_file()

    def save_file(self):
        with open("Categories.json" , "w") as file:
            json.dump(self.category , file , indent=4)

    def load_file(self):
        with open("Categories.json" , "r") as file:
            self.category = json.load(file)

    def folder_path(self , path):
        self.f_path = Path(path)
        
        for i in self.f_path.iterdir():
            if i.is_file():
                for x , y in self.category.items():
                    if i.suffix in y:
                        print(x)
                    else:
                        self.category["Other"].append(i.suffix)
                self.save_file()

    def create_folders(self):
        for category, extensions in self.category.items():
            folder = self.f_path / category
            folder.mkdir(exist_ok=True)

    def move_file(self):
        for i in self.f_path.iterdir():
            if i.is_file():
                for x , y in self.category.items():
                    if i.suffix in y:
                        dst = self.f_path / x
                        shutil.move(i , dst)
                    # else:
                    #     dst = self.f_path / "Other"
                    #     shutil.move(i , dst)
        

acc = FileOrganizer()
acc.folder_path("C:/Users/Sina/Downloads/Documents")
acc.create_folders()
acc.move_file()