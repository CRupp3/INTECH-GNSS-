# Full System Code

# Imports
import time
import serial
import sys
from time import sleep
from time import strftime
import os
from multiprocessing import Process

# Import Utility Functions
from FormatTransmit import formatTransmit
from FormatMessage import formatFullSwarmMessage
from FormatReadNewest import formatReadNewest
from CheckChargeData import CheckChargeData
from Message_Parse import Message_Parse
print('debug -1')

# Import GNSS functions
from Reflectometry_Code.check_append import Watcher
from RawData.parseNMEA import parseNMEA_func

print('debug  0')
w = Watcher()
# start both in parallel
print('debug 1')
p_parseNMEA_func = Process(target=parseNMEA_func())

print('debug 1')
p_Watcher = Process(target=w.run())

print('debug 3')
#p_Watcher.start()
print('debug 4')
#p_parseNMEA_func.start()

print('debug 5')
# Transmit things
while True:
    # check uptime
    uptime = time.clock_gettime(time.CLOCK_MONOTONIC)  # returns uptime in seconds
    days = 30  # reboots every _ days
    if uptime > days*24*60*60:
        os.system('reboot')

    sleep(1)  # sleep 1 minute
    print(strftime("%S")) # debug message


    if strftime("%S") == "00":  # Top of the hour
        # print('Top') #debug message
        # Check Charge controller - done
        # Check Temperature - missing
        # Check Health - missing
        # Send Swarm Message - done
        # Check for received Swarm messages - done

        # check charge controller
        # format swarm message
        # N001 022824 1949 1.235 2.346 3.457 0

        message_file_path = '/home/intech/INTECH-GNSS-/MessageLog.txt'
        message_file = open(message_file_path, 'r')
        lines = message_file.readlines()
        # read last 4 lines
        message = (lines[-1 - 3].strip() + '-' + lines[-1 - 2].strip() + '-' + lines[-1 - 1].strip() + '-' + lines[
            -1].strip())

        # Send message via Swarm
        swarm = serial.Serial("/dev/ttyS0", 115200)
        formatted = formatTransmit(message)
        swarm.write(formatted.encode('utf-8'))  # sends command

        # Check for Confirmation
        send_response = swarm.read()
        sleep(0.01)
        data_left = swarm.in_waiting
        send_response += swarm.read(data_left)
        send_response = send_response.decode()

        # log everything
        file1 = open('SwarmSendLog.txt', 'a')  # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + ' message: ' + message + ' formatted message: ' + formatted + 'received things: ' + send_response + '\n')
        file1.close()

        # close serial connection
        swarm.close()

        # Check for received Swarm messages
        swarm = serial.Serial("/dev/ttyS0", 115200)
        formatted = formatReadNewest()  # format read new messages
        swarm.write(formatted.encode('utf-8'))

        # Check for Response
        send_response = swarm.read()
        sleep(0.01)
        data_left = swarm.in_waiting
        send_response += swarm.read(data_left)
        send_response = send_response.decode()  # decode message

        Message_Parse(send_response)

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write('Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()

    elif strftime("%S") in ["15", "30", "45"]:  # Not top of hour
        # print('Inner') # debug message
        # record charge controller data - done
        # ask swarm for received messages - done

        CheckChargeData()  # writes to log

        # Check swarm messages
        swarm = serial.Serial("/dev/ttyS0", 115200)
        formatted = formatReadNewest()  # format read new messages
        swarm.write(formatted.encode('utf-8'))

        # Read for Response
        send_response = swarm.read()
        sleep(0.01)
        data_left = swarm.in_waiting
        send_response += swarm.read(data_left)
        send_response = send_response.decode()  # decode message

        Message_Parse(send_response)

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write(
            'Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()

