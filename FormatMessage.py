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
from CheckChargeData import CheckChargeData


def formatFullSwarmMessage():
    time = datetime.utcnow().replace(tzinfo=timezone.utc).strftime('%m%d%y%H%M')
    (voltage_in_volts, yield_today) = CheckChargeData()

    message = 'N001 ' + time + voltage_in_volts + yield_today, '0'
    return(message)
