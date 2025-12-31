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

def get_total_count():
    """Helper function to read the lifetime log count"""
    try:
        with open("organizer_log.txt", "r") as log:
            return len(log.readlines())
    except FileNotFoundError:
        return 0

@app.route('/')
def index():
    return render_template('index.html', total_count=get_total_count())

@app.route('/organize', methods=['POST'])
def organize():
    chosen_folder = request.form.get('folder_choice', 'Downloads')
    files_list = organize_folder(chosen_folder)
    
    if not files_list:
        # Now we use our new helper here!
        return render_template('index.html', total_count=get_total_count(), message=f"Your {chosen_folder} is already tidy!")
    
    return render_template('success.html', files=files_list)

@app.route('/history')
def show_history():
    history_list = []
    try:
        with open("organizer_log.txt", "r") as log:
            # We reverse the list so the newest files show up at the top!
            history_list = log.readlines()[::-1]
    except FileNotFoundError:
        pass
        
    return render_template('history.html', history=history_list, total_count=len(history_list))

if __name__ == "__main__":
    app.run(debug=True)