from flask import Flask, render_template, request
import os
import shutil
from pathlib import Path

app = Flask(__name__)

# This is the logic that moves your files
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Apps": [".dmg", ".pkg"],
    "Zips": [".zip", ".tar"],
    "Music": [".mp3", ".wav",".m4a"],
    "Movies": [".mp4", ".avi", ".mov"]
}

def organize_downloads():
    downloads_path = Path.home() / "Downloads" #path to downloads folder
    moved_files = [] #list to keep track of moved files
    
    for file in downloads_path.iterdir(): #iterate through files in downloads
        if file.is_file(): #check if it's a file
            extension = file.suffix.lower() #get file extension
            for folder_name, extensions in FILE_TYPES.items(): #iterate through file types
                if extension in extensions: #check if file extension matches
                    target = downloads_path / folder_name #set target folder
                    target.mkdir(exist_ok=True) #create folder if it doesn't exist
                    shutil.move(str(file), str(target / file.name)) #move file
                    moved_files.append(file.name) #add name to moved files list
    return moved_files

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/organize', methods=['POST'])
def organize():
    files_list = organize_downloads()
    # We pass the list to a new success page
    return render_template('success.html', files=files_list)

if __name__ == "__main__":
    app.run(debug=True)