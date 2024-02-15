# Matthew Menendez-Aponte
# Making a script for a longer Swarm and Charge Controller test
# Goals:
#	- Record Battery voltage every 15(ish) minutes
#   	- Transmit a swarm message every hour at the top of the hour.
#		- message will contain battery voltage and time queued
#  	- Record the swarm's responses in a text file
#   	- Listen for swarm messages received
#   	- Save any messages received


# Import things
import serial
from time import sleep
from time import strftime
from time import struct_time
from pprint import pprint
from FormatTransmit import formatTransmit
from FormatPowerStatus import formatPowerStatus
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
        sleep(0.02)
        data_left = ser.in_waiting()
        send_response += ser.read(data_left)
        send_response = send_response.decode()

        
        # Record communication
        file1 = open('Sendlog.txt', 'a') # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n' + message + '|' + formatted + 'received things: ' + send_response)
        file1.close()
        
        # Ask modem for received messages
        formatted_check = formatReadNewest()
        
        ser.write(formatted_check.encode('utf-8'))  # sends command
        received_response = ser.read()
        sleep(0.02)
        data_left = ser.in_waiting()
        received_response += ser.read(data_left)
        
        received_response = received_response.decode()
        
        file2 = open('Receivelog.txt', 'a') # open log.txt
        file2.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n 'command sent' + formatted_check + 'received things: ' + received_response)
        file2.close()


    elif strftime("%M") in ["15","30","45"]:  # Not top of hour
        # Ask modem for received messages
        formatted_check = formatReadNewest()
        
        ser.write(formatted_check.encode('utf-8'))  # sends command
        received_response = ser.read()
        sleep(0.02)
        data_left = ser.in_waiting()
        received_response += ser.read(data_left)
        
        received_response = received_response.decode()
        
        file2 = open('Receivelog.txt', 'a') # open log.txt
        file2.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n 'command sent' + formatted_check + 'received things: ' + received_response)
        file2.close()
    else:
        ()
