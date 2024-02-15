import serial
from time import sleep

# open port with baud rate
ser = serial.Serial('/dev/ttyS0',9600)

while True:
    received_data = ser.read()
    sleep(0.03)
    data_left = ser.inWaiting()  # check for remaining byte
    received_data += ser.read(data_left)
    print(received_data)  # print received data
    ser.write(received_data)
