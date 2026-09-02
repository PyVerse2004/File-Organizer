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
            "Archives" : [".zip" , ".rar"],
            "Other" : []
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

    def create_folders(self):
        for category, extensions in self.category.items():
            folder = self.f_path / category
            folder.mkdir(exist_ok=True)

    def move_file(self):
        for i in self.f_path.iterdir():
            if i.is_file():

                found = False

                for x, y in self.category.items():
                    if x == "Other":
                        continue

                    if i.suffix in y:
                        dst = self.f_path / x / i.name

                        if dst.exists():
                            counter = 1

                            while True:
                                new_name = f"{i.stem}_{counter}{i.suffix}"
                                new_dst = self.f_path / x / new_name

                                if not new_dst.exists():
                                    dst = new_dst
                                    break

                                counter += 1

                        shutil.move(i, dst)
                        found = True
                        break

                if not found:
                    if i.suffix not in self.category["Other"]:
                        self.category["Other"].append(i.suffix)
                        self.save_file()

                    dst = self.f_path / "Other" / i.name

                    if dst.exists():
                        counter = 1

                        while True:
                            new_name = f"{i.stem}_{counter}{i.suffix}"
                            new_dst = self.f_path / "Other" / new_name

                            if not new_dst.exists():
                                dst = new_dst
                                break

                            counter += 1

                    shutil.move(i, dst)

    def copy_file(self):
        for i in self.f_path.iterdir():
            if i.is_file():

                found = False

                for x, y in self.category.items():
                    if x == "Other":
                        continue

                    if i.suffix in y:
                        dst = self.f_path / x / i.name

                        if dst.exists():
                            counter = 1

                            while True:
                                new_name = f"{i.stem}_{counter}{i.suffix}"
                                new_dst = self.f_path / x / new_name

                                if not new_dst.exists():
                                    dst = new_dst
                                    break

                                counter += 1

                        shutil.copy2(i, dst)
                        found = True
                        break

                if not found:
                    if i.suffix not in self.category["Other"]:
                        self.category["Other"].append(i.suffix)
                        self.save_file()

                    dst = self.f_path / "Other" / i.name

                    if dst.exists():
                        counter = 1

                        while True:
                            new_name = f"{i.stem}_{counter}{i.suffix}"
                            new_dst = self.f_path / "Other" / new_name

                            if not new_dst.exists():
                                dst = new_dst
                                break

                            counter += 1

                    shutil.copy2(i, dst)

acc = FileOrganizer()
acc.folder_path("C:/Users/Sina/Downloads/Documents")
acc.create_folders()
acc.move_file()