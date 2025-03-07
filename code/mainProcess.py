import subprocess
import platform

path = None
# Check the platform to determine the correct command
linux_path = '.venv/bin/python'
windows_path = '.venv/Scripts/python'

if platform.system() == "Linux":
    path = linux_path
else:
    path = windows_path


# Start the controllerInput process
controller_process = subprocess.Popen(
    [path, 'controllerInput.py'],  # Replace with 'python3' if necessary
    stdout=subprocess.PIPE,            # Pipe the output
    text=True                          # Treat as text
)

'''reader_process = subprocess.Popen(
    [path, 'canReader.py'],
    stdout=subprocess.PIPE,
    text=True
)'''

# Start the canInterpreter process
interpreter_process = subprocess.Popen(
    [path, 'canInterpreter.py'], 
    stdin=controller_process.stdout,   # Use controller's stdout as input
    text=True                          # Treat as text
)

try:
    # Keep the main script running while the two processes communicate
    controller_process.wait()          # Wait for controllerInput.py to finish (if it ends)
    interpreter_process.wait()         # Wait for canInterpreter.py to finish (if it ends)
except KeyboardInterrupt:
    # Handle Ctrl+C gracefully
    print("Stopping processes...")
    controller_process.terminate()
    interpreter_process.terminate()
