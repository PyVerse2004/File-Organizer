# 📁 File Organizer

A desktop file organization tool built with Python and Tkinter that automatically organizes files into categorized folders based on their file extensions.

The application supports both **Move** and **Copy** operations and automatically handles duplicate filenames.

---

## ✨ Features

- 📂 Select any folder using a graphical interface
- 🖼️ Automatically categorize image files
- 📄 Automatically categorize document files
- 🎵 Automatically categorize music files
- 🎬 Automatically categorize video files
- 📦 Automatically categorize archive files
- 📁 Move files into categorized folders
- 📋 Copy files without removing the original
- ❓ Automatically detect unknown file extensions
- 🔄 Handle duplicate filenames automatically
- ⚙️ Store categories and extensions in a JSON configuration file
- 📊 Display operation progress with a progress bar
- 🧵 Run file operations in a background thread to keep the GUI responsive
- ⚠️ Handle errors and invalid operations with GUI messages

---

## 🛠️ Technologies

- Python 3
- Tkinter
- pathlib
- shutil
- JSON
- threading
- Object-Oriented Programming (OOP)

---

## 📂 Project Structure

```text
File-Organizer/
│
├── file_organizer.py
├── gui.py
├── Categories.json
├── README.md
└── .gitignore
