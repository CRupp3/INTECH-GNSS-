# Matthew Menendez-Aponte 2/21/2024

# Description:
#   Format message to be sent via swarm containing:
#       - Node: NXXX
#       - Date: MMDDYY
#       - UTC Time: HH:MM
#       - Battery Capacity Remaining: XXX.X
#       - PV yield previous 24 Hrs: XX.XX
#       - Sleep Mode On/Off: B

from datetime import datetime, timezone
from time import strftime

from CheckChargeData import CheckChargeData
from FormatTransmit import formatTransmit


def formatFullSwarmMessage():
    time = datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%m%d%y %H%M')
    #(voltage_in_volts, power, yield_today) = CheckChargeData()
    voltage_in_volts = 1.23456
    power = 2.34567
    yield_today = 3.45678

    message = 'N001 '+ time + f' {voltage_in_volts:.3f}' + f' {power:.3f}' f' {yield_today:.3f}' + ' 0'

    return(message)



# testing
if __name__ == '__main__':
    message = formatFullSwarmMessage()
    print(message)
    formatted = formatTransmit(message)
    print(formatted)
