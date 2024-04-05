import serial
from gpiozero import CPUTemperature
import time

def CheckTemperature():
    cpu = CPUTemperature()
    temp = cpu.temperature
    return temp

if __name__ == '__main__':
    temp = CheckTemperature()
    print(temp)
