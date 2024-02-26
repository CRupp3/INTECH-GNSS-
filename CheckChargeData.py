import serial
import time
from time import strftime


# Copying from Dev's code
# Add return values for:

# Outputs: (voltage,
#   - voltage: Battery voltage (V)
#   - PVPower: Average PV Input Power
#   - Internal Temperature

def CheckChargeData():
    # Setup serial port
    mppt = serial.Serial('/dev/ttyUSB0', 19200, timeout=2)  # Adjust '/dev/ttyUSB0' as per the Raspberry Pi's serial port

    # Command for Get Status
    command = bytes([7])  # Command code for Get

    # Write command to serial port
    mppt.write(command)
    time.sleep(1)  # Pause for a second to wait for response

    # Read and process response
    bytes_to_read = mppt.in_waiting
    if bytes_to_read > 0:
        response_data = mppt.read(bytes_to_read)

        # Attempt to decode with 'ignore' to bypass invalid byte errors
        char_data_str = response_data.decode('utf-8', 'ignore').replace('\r\n', '|')
        data_lines = char_data_str.split('|')

        # Process each line
        for line in data_lines:
            if len(line) > 0:
                parts = line.split('\t')  # Tab character as separator
                if len(parts) == 2:
                    label, value = parts
                    # Display label and value
                    #print(f'{label}: {value}')

                    # Extract the values we want
                    if label == 'V':  # Battery Voltage
                        voltage_in_millivolts = float(value)
                        voltage_in_volts = voltage_in_millivolts / 1000
                        #print(f'Battery Voltage: {voltage_in_volts:.3f} V')

                    if label == 'PPV': # PV Power
                        power = float(value) # W
                        #print(f'Panel Power right now: {power:.3f} W')

                    if label == 'H20':  # PV yield today
                        yield_today = float(value) # kWh
                        #print(f'Panel Yield Today: {yield_today:.3f} kWh')

        # Write values to a data file
        file1 = open('ChargeLogVerbose.txt', 'a')  # open log.txt
        file1.write('Time: ' + strftime("%Y-%m-%d %I:%M:%S %p ") + f'Voltage: {voltage_in_volts:.3f}' + f' Panel Power: {power:.3f}' + f' Yield: {yield_today: .3f}')
        file1.close()
        file2 = open('ChargeLog.txt', 'a')
        file2.write(strftime("%Y-%m-%d %I:%M:%S %p ") + f',{voltage_in_volts:.3f}' + f',{power:.3f}' f',{yield_today:.3f}')
        file2.close()

        return(voltage_in_volts, power, yield_today)

    else:
        return(0.0, 0.0)

    # Clean up by closing the serial port
    mppt.close()

if __name__ == '__main__':
    (voltage_in_volts, power, yield_today) = CheckChargeData()
    print('Voltage in V: ', voltage_in_volts)
    print('Yield today: ', yield_today)
