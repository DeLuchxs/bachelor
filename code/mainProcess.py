import os
import subprocess

def main():
    # Create a pipe
    read_fd, write_fd = os.pipe()

    try:
        # Launch controllerInput.py
        controller_process = subprocess.Popen(
            ['python', 'controllerInput.py'],  # Adjust for your environment (e.g., 'python3')
            pass_fds=(write_fd,),              # Pass the write end of the pipe
            env={**os.environ, 'WRITE_PIPE': str(write_fd)}  # Pass pipe ID via environment
        )

        # Launch canInterpreter.py
        interpreter_process = subprocess.Popen(
            ['python', 'canInterpreter.py'], 
            pass_fds=(read_fd,),               # Pass the read end of the pipe
            env={**os.environ, 'READ_PIPE': str(read_fd)}    # Pass pipe ID via environment
        )

        # Close the pipe ends in the parent process
        os.close(read_fd)
        os.close(write_fd)

        # Wait for both processes to complete
        controller_process.wait()
        interpreter_process.wait()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            os.close(read_fd)
        except OSError:
            pass
        try:
            os.close(write_fd)
        except OSError:
            pass

if __name__ == "__main__":
    main()
