# Matthew Menendez-Aponte 2/6/2024

# Description:
# Function to format Swarm transmissions

# Inputs:
#   - message: String we desire to transmit via SWARM

# Outputs:
#   - string: Formatted NMEA message to send via serial

# Thoughts:
# No extra formatting of the messages are done (e.g. message id, hold time, etc). We might want to do that in the future.
# We will need to introduce some checking to ensure messages are < 192 bytes. Not sure if we should do that here or
# somewhere else.

from NMEAChecksum import nmeaChecksum

def formatTransmit(message):
    stringSansCheck = ('$TD ' + message)
    checksum = nmeaChecksum(stringSansCheck)
    string = (stringSansCheck + '*' + checksum + "\n")
    return string
