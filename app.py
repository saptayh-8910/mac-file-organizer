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

def organize_folder(target_folder_name):
    # This now dynamically picks the folder you choose!
    folder_path = Path.home() / target_folder_name
    moved_files = []
    
    if not folder_path.exists():
        return moved_files

    for file in folder_path.iterdir():
        if file.is_file():
            extension = file.suffix.lower()
            for category, extensions in FILE_TYPES.items():
                if extension in extensions:
                    target = folder_path / category
                    target.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target / file.name))
                    moved_files.append(file.name)
    
    # Save to your lifetime log
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
    # 1. Get the folder choice from the HTML radio buttons
    chosen_folder = request.form.get('folder_choice', 'Downloads')
    
    # 2. Run the organization on THAT specific folder
    files_list = organize_folder(chosen_folder)
    
    if not files_list:
        # Re-calculate total for the counter
        total = get_total_count() # You can make a small helper function for this
        return render_template('index.html', total_count=total, message=f"Your {chosen_folder} is already tidy!")
    
    return render_template('success.html', files=files_list)

if __name__ == "__main__":
    app.run(debug=True)