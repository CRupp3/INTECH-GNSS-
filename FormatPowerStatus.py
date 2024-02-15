# Matthew Menendez-Aponte 2/6/2024

# Description:
# Function to format Swarm Power Status Command

# Inputs:
#   -

# Outputs:
#   - string: Formatted NMEA message to send via serial

# Thoughts:
#

from NMEAChecksum import nmeaChecksum

def formatPowerStatus():
    stringSansCheck = ('$PW ' + '?')
    checksum = nmeaChecksum(stringSansCheck)
    string = (stringSansCheck + '*' + checksum + "\n")
    return string
