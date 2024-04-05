import numpy as np
import matplotlib.pyplot as plt
import os
from time import strftime
from CheckChargeData import CheckChargeData
from CheckTemperature import CheckTemperature
# one function to rule them all

def CheckHealth(time):
    # Check Charge Data
    # (voltage_in_volts, power, yield_today) = CheckChargeData()
    voltage_in_volts = 12.34567
    power = 1.23456
    yield_today = 12.34567

    temperature = CheckTemperature()


    # Get limits from settings
    filepath = '/home/mcma/GNSS/INTECH-GNSS-/settings.txt'
    settingsFile = open(filepath, 'r')
    Lines = settingsFile.readlines()

    voltage_limit = float(Lines[11].strip())

    temperature_limit_low = float(Lines[13].strip())
    temperature_limit_high = float(Lines[15].strip())


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
    print(string)