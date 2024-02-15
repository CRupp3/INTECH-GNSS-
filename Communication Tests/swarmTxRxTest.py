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
print('opened serial')

# I want a Power Check every 15 seconds
# I want to read for messages every 15?
i = 0

while True:
    sleep(0.5)  # sleep 1 second
    i += 1

    print(strftime("%S"))
    
    if strftime("%S") in {"00", "15", "30", "45"}:  # Every 15 seconds
        # Send a Power Check Request to Swarm
        print('Sending Power Request')
        formatted = formatPowerStatus()
        print('here1')

        ser.write(formatted.encode('utf-8'))  # sends command
        send_response = ser.read()
        sleep(0.02)
        data_left = ser.in_waiting
        send_response += ser.read(data_left)
        print(send_response)


        print('here2')

        # Check for Status
        print('here3')
        
        
        # Decode Message
        print(send_response)
        print('trying to decode')
        send_response = send_response.decode()

        print(strftime("%Y-%m-%d %I:%M:%S %p"))
        print('message sent: ', formatted)
        print('recieved: ', send_response)
        
        
        file1 = open('log.txt', 'a')  # open log.txt
        file1.write('Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + '\n' + formatted + '|' + 'received things: ' + send_response)
        file1.close()

    else:
        ()
