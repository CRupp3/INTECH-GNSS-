import numpy as np
import matplotlib.pyplot as plt
import os
from time import strftime
from CheckChargeData import CheckChargeData
from CheckTemperature import CheckTemperature
# one function to rule them all

def CheckHealth(time):
    # Check Charge Data
    (voltage_in_volts, power, yield_today) = CheckChargeData()

    # Check CPU temp
    temperature = CheckTemperature()

    # Get limits from settings
    # Read from settings
    filepath = '/home/intech/INTECH-GNSS-/settings.txt'
    settingsFile = open(filepath, 'r')
    Lines = settingsFile.readlines()

    # Limits
    voltage_limit = float(Lines[5].strip())
    temperature_limit_low = float(Lines[6].strip())
    temperature_limit_high = float(Lines[7].strip())


    # decide if sleep mode is needed
    if voltage_in_volts < voltage_limit or temperature > temperature_limit_high or temperature < temperature_limit_low:
        sleep = 1
    else:
        sleep = 0

    health_string = (f'{voltage_in_volts:.2f}' + '-' + f'{power:.2f}' + '-' + f'{temperature:.2f}' + '-' + f'{sleep:}')


    # Write everything to HealthLog
    file1 = open('Healthlog.txt', 'a')  # open HealthLog.txt
    file1.write(time + '-' + health_string + '\n')
    file1.close()
    return health_string

if __name__ == '__main__':
    string = CheckHealth('time')
    #print(string)