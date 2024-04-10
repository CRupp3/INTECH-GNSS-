# Get IO 
# swarm input
# Checked for messages at 2024-02-29 05:15:25 PM and received $MM ERR,DBX_NOMORE*5c
# IR CODE Inputs: Elevation Angle Mask, Asmuth Mask, QC Variables...?, 
# health code INPUTs: Sleep Mode Voltage Cutoff, Sleep Time, 

# settings.txt will be the global variables file

# function to get the last message
def get_last_MSG(file_path):
    with open(file_path, 'r') as file:
        last_line = file.readlines()[-1]
        error_string = last_line.split('and received ')[-1].strip()
        return error_string
    
# function to handle the message
def msg_handeler(last_MSG):
    # make the newest message equal to the settings file
    with open('settings.txt', 'w') as file: # hardcode file path for settings.txt

        file.write(last_MSG)



#########################################################################
def Message_Parse(last_MSG):
    # file_path = 'SwarmRecievedLog.txt'  # hardcode file path for settings.txt
    # last_MSG = get_last_MSG(file_path)
    # print("MSG:", last_MSG)
    # print("Compare to:$MM ERR,DBX_NOMORE*5c\n")
    # check if not error message
    
    # Split the last message by newline character
    message_lines = last_MSG.strip().split('\n')

    # Check if there are exactly 10 lines
    if len(message_lines) != 10:
        print("Last SWARM message does not contain expected 10 lines of data.")
        return

    # Check if each line is an integer
    for line in message_lines:
        try:
            int(line)
        except ValueError:
            print("Invalid message format. Each line should contain an integer.")
            return

    # If the function reaches this point, the message format is valid
    print("SWARM message format is valid")
    # Now you can handle the message as per your requirement, e.g., update settings file
    msg_handeler(last_MSG)
    print("settings.txt updated based on most recent SWARM message.") 


