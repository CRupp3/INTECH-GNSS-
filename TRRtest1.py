# Matthew Menendez-Aponte
# Code for TRR System 1 test

# Goals:
#   - Transmit a swarm message containing battery info every 2 hours at the top of the hour.
#   - Record the swarm's responses in a text file
#   - Listen for swarm messages received
#   - Save any messages received


# Import things
import serial
from time import sleep
from time import strftime
from FormatTransmit import formatTransmit

# define the Ras Pi's UART pins and Swarm's baud rate
uart_port = "/dev/ttyS0"
baud_rate = 115200

# open serial port
ser = serial.Serial(uart_port, baud_rate)

# Format message send
# Queued at 2/5/2024 18:08
# message = 'Queued at ' + strftime("%Y-%m-%d %I:%M %p")
# print(message)

# I want a message sent every hour
# I want to read for messages every 15? minutes

while True:
    sleep(1*60) # sleep 1 minute
    if strftime("%M") == "00": # Top of the hour
        # Send a Message via Swarm
        message = 'Queued at ' + strftime("%Y-%m-%d %I:%M %p")
        formatted = formatTransmit(message)

        ser.write(formatted.encode('utf-8'))  # sends command

        # Check for Status
        send_response = ser.read()
        sleep(0.01)
        data_left = ser.in_waiting()
        send_response += ser.read(data_left)

        # Ask modem for received messages


        file1 = open('log.txt', 'a') # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n' + message + '|' + formatted + 'received things: ' + send_response)
        file1.close()

    elif strftime("%M") in ["15","30","45"]:  # Not top of hour
        #received_data = ser.read()
        #sleep(0.03)
        #data_left = ser.inWaiting()  # check for remaining byte
        #received_data += ser.read(data_left)
        #print(received_data)  # print received data
        print("looking for reception")
    else:
        ()
