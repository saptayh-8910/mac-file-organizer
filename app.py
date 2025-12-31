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
    downloads_path = Path.home() / "Downloads"
    moved_files = []
    
    for file in downloads_path.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            for folder_name, extensions in FILE_TYPES.items():
                if extension in extensions:
                    target = downloads_path / folder_name
                    target.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target / file.name))
                    moved_files.append(file.name)
    
    # NEW: Save the history to a 'log.txt' file
    if moved_files:
        with open("organizer_log.txt", "a") as log:
            for name in moved_files:
                log.write(f"{name}\n")
                
    return moved_files

@app.route('/')
def index():
    # We open our log file and count how many lines (files) are in it
    try:
        with open("organizer_log.txt", "r") as log:
            # Each line in the log represents one file organized
            total = len(log.readlines())
    except FileNotFoundError:
        # If the file doesn't exist yet (first time running), set total to 0
        total = 0
        
    # We send that 'total' number to index.html as 'total_count'
    return render_template('index.html', total_count=total)

@app.route('/organize', methods=['POST'])
def organize():
    files_list = organize_downloads()
    # We pass the list to a new success page
    return render_template('success.html', files=files_list)

if __name__ == "__main__":
    app.run(debug=True)