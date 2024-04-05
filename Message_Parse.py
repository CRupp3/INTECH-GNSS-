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
    with open('settings_overwrite.txt', 'w') as file: # hardcode file path for settings.txt

        file.write(last_MSG)



#########################################################################
def Message_Parse(last_MSG):
    # file_path = 'SwarmRecievedLog.txt'  # hardcode file path for settings.txt
    # last_MSG = get_last_MSG(file_path)
    # print("MSG:", last_MSG)

    # check if not error message
    if last_MSG != "$MM ERR,DBX_NOMORE*5c":
        msg_handeler(last_MSG)


