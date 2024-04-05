# Matthew Menendez-Aponte
# Code for TRR System 2 test

# Adding a bunch of stuff, including
#   Full Health Reporting
#       temperature from CPU temp
#
#   Water Level Computation
#       record raw NMEA messages
#       save NMEA messages in an organized way
#       process NMEA messages into height with an associated time
#
#   Start from reboot functionality

import time
from multiprocessing import Process


# import parseNMEA and check_append
from Reflectometry_Code.check_append import Watcher
from RawData.parseNMEA import parseNMEA_func

import sys
# caution: path[0] is reserved for script path (or '' in REPL)
sys.path.insert(1, '/home/mcma/GNSS/INTECH-GNSS-/Reflectometry_Code')
sys.path.insert(1, '/home/mcma/GNSS/INTECH-GNSS-/RawData')

w = Watcher()
# start both in parallel
p_parseNMEA_func = Process(target=parseNMEA_func())
p_Watcher = Process(target=w.run())

p_Watcher.start()
p_parseNMEA_func.start()


# Goals:
#   - Record and save health data every 15 minutes
#       - battery voltage
#       - panel instant power
#       - panel production over the last day
#       -
#   - Transmit a swarm message containing battery info every hour at the top of the hour.
#   - Record the swarm's responses in a text file
#   - Listen for swarm messages received
#   - Save any messages received

# Import things
import serial
from time import sleep
from time import strftime
from FormatTransmit import formatTransmit
from FormatMessage import formatFullSwarmMessage
from FormatReadNewest import formatReadNewest
from CheckChargeData import CheckChargeData
import os




while True:
    # check uptime
    uptime = time.clock_gettime(time.CLOCK_MONOTONIC)  # returns uptime in seconds
    days = 30  # reboots every _ days
    if uptime > days*24*60*60:
        os.system('reboot')

    sleep(1*60)  # sleep 1 minute
    # print(strftime("%S")) # debug message


    if strftime("%M") == "00":  # Top of the hour
        # print('Top') #debug message
        # Check Charge controller - done
        # Check Temperature - missing
        # Check Health - missing
        # Send Swarm Message - done
        # Check for received Swarm messages - done

        # check charge controller
        # format swarm message
        # N001 022824 1949 1.235 2.346 3.457 0

        message_file_path = '/home/mcma/GNSS/INTECH-GNSS-/MessageLog.txt'
        message_file = open(message_file_path, 'r')
        lines = message_file.readlines()
        # read last 4 lines

        message = formatFullSwarmMessage()  # read from MessageLog.txt

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

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write('Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()

    elif strftime("%M") in ["15", "30", "45"]:  # Not top of hour
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

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write(
            'Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()

