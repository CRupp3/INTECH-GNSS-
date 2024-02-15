import serial
import time

# Define the UART port and baud rate
uart_port = "/dev/ttyS0"
baud_rate = 115200

# Create a serial connection
ser = serial.Serial(uart_port, baud_rate, timeout=1)

try:
	# Send a message
	message = "$RT 0*16\n"
	ser.write(message.encode('utf-8'))
	print(f"Sent: (message)")
	
finally:
	ser.close()

