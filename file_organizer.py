import os
import json
import shutil
from pathlib import Path


class FileOrganizer:
    def __init__(self):
        self.category = {
            "Images": [".jpg", ".png", ".jpeg"],
            "Documents": [".pdf", ".docx", ".txt"],
            "Music": [".mp3", ".wav"],
            "Videos": [".mp4", ".mkv"],
            "Archives": [".zip", ".rar"],
            "Other": []
        }

        if os.path.exists("Categories.json"):
            self.load_file()
        else:
            self.save_file()

    def save_file(self):
        with open("Categories.json", "w") as file:
            json.dump(self.category, file, indent=4)

    def load_file(self):
        with open("Categories.json", "r") as file:
            self.category = json.load(file)

    def folder_path(self, path):
        self.f_path = Path(path)

    def create_folders(self):
        for category in self.category:
            folder = self.f_path / category
            folder.mkdir(exist_ok=True)

    def get_unique_path(self, folder, file):
        destination = folder / file.name

        if not destination.exists():
            return destination

        counter = 1

        while True:
            new_name = f"{file.stem}_{counter}{file.suffix}"
            destination = folder / new_name

            if not destination.exists():
                return destination

            counter += 1

    def get_category(self, file):
        for category, extensions in self.category.items():
            if category == "Other":
                continue

            if file.suffix.lower() in extensions:
                return category

        return "Other"

    def organize_file(self, file, operation):
        category = self.get_category(file)

        if category == "Other":
            if file.suffix.lower() not in self.category["Other"]:
                self.category["Other"].append(file.suffix.lower())
                self.save_file()

        destination_folder = self.f_path / category
        destination = self.get_unique_path(destination_folder, file)

        if operation == "move":
            shutil.move(file, destination)

        elif operation == "copy":
            shutil.copy2(file, destination)

    def process_files(self, operation):
        processed = 0

        for file in self.f_path.iterdir():
            if file.is_file():
                self.organize_file(file, operation)
                processed += 1

        return processed

    def move_file(self):
        return self.process_files("move")

    def copy_file(self):
        return self.process_files("copy")