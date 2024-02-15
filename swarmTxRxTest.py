# Want to test functionality of sending a command then immediately reading the reply

import serial
from time import sleep
from time import strftime
from FormatPowerStatus import formatPowerStatus


# define the Ras Pi's UART pins and Swarm's baud rate
uart_port = "/dev/ttyS0"
baud_rate = 115200

# open serial port
ser = serial.Serial(uart_port, baud_rate)

# I want a Power Check every 15 seconds
# I want to read for messages every 15?

while True:
    sleep(1*60)  # sleep 1 minute
    if strftime("%s") == ["00", "15", "30", "45"]:  # Every 15 seconds
        # Send a Power Check Request to Swarm
        formatted = formatPowerStatus()

        ser.write(formatted.encode('utf-8'))  # sends command

        # Check for Status
        send_response = ser.read()
        sleep(0.01)
        data_left = ser.in_waiting
        send_response += ser.read(data_left)

        file1 = open('log.txt', 'a')  # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n' + formatted + '|' + 'received things: ' + send_response)
        file1.close()

    else:
        ()
