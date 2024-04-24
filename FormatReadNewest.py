from NMEAChecksum import nmeaChecksum
import serial
from time import sleep

def formatReadNewest():
	stringSansCheck = ('$MM R=N')
	checksum = nmeaChecksum(stringSansCheck)
	string = (stringSansCheck + '*' + checksum + "\n")
	return string

if __name__ == '__main__':
	swarm = serial.Serial("/dev/ttyS0", 115200)
	formatted = formatReadNewest()  # format read new messages
	swarm.write(formatted.encode('utf-8'))

	send_response = swarm.read()
	sleep(0.01)
	data_left = swarm.in_waiting
	send_response += swarm.read(data_left)
	send_response = send_response.decode()
	swarm.close()

	print('sent: ', formatted)
	print('and got: ', send_response)
	
