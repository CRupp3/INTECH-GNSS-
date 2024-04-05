import serial
from gpiozero import CPUTemperature
import time

def CheckTemperature():
    ser = serial
    temperature = CPUTemperature()
    return temperature

if __name__ == '__main__':
    temp = CheckTemperature()
    print(temp)