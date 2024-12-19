import os

throttleL = 0
throttleR = 0
rudderAngle = 0
backwards = False

def process_data(read_pipe):
    """Reads data from the pipe and processes it."""
    buffer = b""
    while True:
        chunk = os.read(read_pipe, 1024)  # Read up to 1024 bytes at a time
        if not chunk:
            break
        buffer += chunk

        # Process complete lines in the buffer
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            process_line(line.decode())

    os.close(read_pipe)  # Close the read pipe when done

def process_line(line):
    """Processes a single line of input."""
    key, value = line.split(": ")
    match key:
        case "throttleL":
            global throttleL
            throttleL = int(value)
        case "throttleR":
            global throttleR
            throttleR = int(value)
        case "rudderAngle":
            global rudderAngle
            rudderAngle = int(value)
        case "backwards":
            global backwards
            backwards = value == "True"



if __name__ == "__main__":
    read_pipe = int(input("READ_PIPE: "))  # Pipe ID passed by the parent
    process_data(read_pipe)

while True:
    print(f"throttleL: {throttleL},\nthrottleR: {throttleR},\n rudderAngle: {rudderAngle},\n backwards: {backwards}")
    sleep(1)  # Sleep to avoid high CPU usage