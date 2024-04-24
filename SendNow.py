import serial
from FormatTransmit import formatTransmit
from time import sleep
from time import strftime

def sendNow():
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

    print('Swarm got: ', formatted)


    # Check for Confirmation
    send_response = swarm.read()
    sleep(0.01)
    data_left = swarm.in_waiting
    send_response += swarm.read(data_left)
    send_response = send_response.decode()

    print('The Modem Responded: ', send_response)

    # log everything
    file1 = open('SwarmSendLog.txt', 'a')  # open log.txt
    file1.write('Manual Transmission - Communication that occured at' + strftime("%Y-%m-%d %I:%M:%S %p") + ' message: ' + message + ' formatted message: ' + formatted + 'received things: ' + send_response + '\n')
    file1.close()

if __name__ == '__main__':
    sendNow()
