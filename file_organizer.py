import os
import json
from pathlib import Path

if not os.path.exists("Categories.json"):
    with open("Categories.json" , "w") as file:
        json.dump({} , file)

class FileOrganizer:
    pass