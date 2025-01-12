import os
import subprocess

import keyboard
import time

# Example usage
file_path = "upload_file.py"

subprocess.run(f"Set-Clipboard -Path {os.path.abspath(file_path)}", shell = True)

# Give some time for the clipboard operation to complete
time.sleep(1)
print(os.path.abspath(file_path))
# Now, you can switch to the target application and paste
keyboard.send("alt+tab")
time.sleep(0.1)
keyboard.send("ctrl+v")
time.sleep(1)
keyboard.write("Heyo! Here's the file you requested.")