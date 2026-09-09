import os
import time
import subprocess
import shutil

INCOMMING_DIR = './incoming_cargo'
ARCHIVE_DIR = './archive_cargo'

os.makedirs(INCOMMING_DIR, exist_ok=True)
os.makedirs(ARCHIVE_DIR, exist_ok=True)

print("Watchdog Bot started. Monitoring for new cargo manifests...")

while True:
    for filename in os.listdir(INCOMMING_DIR):
        
        if filename.endswith('.csv'):
            file_path = os.path.join(INCOMMING_DIR, filename)
            print(f"New file detected: {filename}. Processing...")
            
            try:
                result = subprocess.run(['python', 'aws_load.py',file_path],
                                                    check = True,
                                                    capture_output = True,
                                                    text = True)
                print("aws_load.py output:\n", result.stdout)
                            
                archive_path = os.path.join(ARCHIVE_DIR, filename)
                            
                shutil.move(file_path, archive_path)
                print(f"file {file_path} moved to archive {archive_path}")
                
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while processing {filename}: {e.stderr}")
            except Exception as e:
                print(f"Unexpected error occurred while processing {filename}: {str(e)}")
    time.sleep(5)
                            
            