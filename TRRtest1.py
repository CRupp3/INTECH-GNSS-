# Matthew Menendez-Aponte
# Code for TRR System 1 test
import time

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

# Starting from rc.local, called in main


while True:
    # check uptime
    uptime = time.clock_gettime(time.CLOCK_BOOTTIME)  # returns uptime in seconds
    days = 2
    if uptime > 2*24*60*60:  # reboots every 2 days
        os.system('reboot')

    sleep(1*60)  # sleep 1 minute

    if strftime("%M") == "00":  # Top of the hour
        # Check Charge controller - done
        # Check Temperature - missing
        # Check Health - missing
        # Send Swarm Message - done
        # Check for received Swarm messages - done

        # check charge controller
        # format swarm message
        # N001 022824 1949 1.235 2.346 3.457 0
        message = formatFullSwarmMessage()  # includes a CheckChargeData call which writes to log file

        # Send message via Swarm
        swarm = serial.Serial("/dev/ttyS0", 115200)
        formatted = formatTransmit(message)
        swarm.write(formatted.encode('utf-8'))  # sends command

        # Check for Confirmation
        send_response = swarm.read()
        sleep(0.01)
        data_left = swarm.in_waiting()
        send_response += swarm.read(data_left)

        # log everything
        file1 = open('SwarmSendLog.txt', 'a')  # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + ' ' + message + '|' + formatted + 'received things: ' + send_response + '\n')
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
        data_left = swarm.in_waiting()
        send_response += swarm.read(data_left)
        send_response = send_response.decode()  # decode message

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write('Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()

    elif strftime("%M") in ["15", "30", "45"]:  # Not top of hour
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
        data_left = swarm.in_waiting()
        send_response += swarm.read(data_left)
        send_response = send_response.decode()  # decode message

        file2 = open('SwarmRecievedLog.txt', 'a')
        file2.write(
            'Checked for messages at ' + strftime("%Y-%m-%d %I:%M:%S %p") + ' and received ' + send_response + '\n')
        file2.close()

        swarm.close()
    else:
        ()
