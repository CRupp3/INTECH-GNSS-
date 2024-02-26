# Matthew Menendez-Aponte
# Code for TRR System 1 test

# Goals:
#   - Record and save health data every 15 minutes
#       - battery voltage
#       - panel instant power
#       - panel production over the last day
#       -
#   - Transmit a swarm message containing battery info every 2 hours at the top of the hour.
#   - Record the swarm's responses in a text file
#   - Listen for swarm messages received
#   - Save any messages received
#   -


# Import things
import serial
from time import sleep
from time import strftime
from FormatTransmit import formatTransmit

# Format message send
# Queued at 2/5/2024 18:08
# message = 'Queued at ' + strftime("%Y-%m-%d %I:%M %p")
# print(message)

while True:
    sleep(1*60) # sleep 1 minute
    if strftime("%M") == "00":  # Top of the hour
        # Send a Message via Swarm
        # Message contains queue time, health data

        swarm = serial.Serial("/dev/ttyS0", 115200)
        message = 'Queued at ' + strftime("%Y-%m-%d %I:%M %p")
        formatted = formatTransmit(message)

        swarm.write(formatted.encode('utf-8'))  # sends command

        # Check for Status
        send_response = swarm.read()
        sleep(0.01)
        data_left = swarm.in_waiting()
        send_response += swarm.read(data_left)

        # Ask modem for received messages


        file1 = open('log.txt', 'a') # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n' + message + '|' + formatted + 'received things: ' + send_response)
        file1.close()

    elif strftime("%M") in ["15","30","45"]:  # Not top of hour
        #received_data = swarm.read()
        #sleep(0.03)
        #data_left = swarm.inWaiting()  # check for remaining byte
        #received_data += swarm.read(data_left)
        #print(received_data)  # print received data
        print("looking for reception")
    else:
        ()
