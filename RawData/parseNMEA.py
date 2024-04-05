import serial
import serial.tools.list_ports
import time
from datetime import datetime, timezone

def parseZDA(line, header, GNSSid, SENTid):

    # Initialize ZDA
    ZDA = {
        'hour': 0,
        'min': 0,
        'sec': 0,
        'day': 0,
        'month': 0,
        'year': 0,
        'checksum': 0
    }

    # Initialize Index Vector
    Ind = [0] * 7

    # Count Indexes
    i = len(header) + len(GNSSid) + len(SENTid) + 1
    arg = 0
    while i <= len(line):
        if line[i-1] == ',' or line[i-1] == '*':
            arg += 1
            i += 1
            continue
        else:
            Ind[arg-1] += 1
            i += 1

    # Parse ZDA Message
    i = len(header) + len(GNSSid) + len(SENTid) + 2
    arg = 1
    while i <= len(line):
        if arg == 1 and Ind[arg-1] != 0:
            # print(line[i-1:i+1])
            ZDA['hour'] = int(line[i-1:i+1])
            # print(line[i+1:i+3])
            ZDA['min'] = int(line[i+1:i+3])
            # print(round(float(line[i+3:i+8])))
            ZDA['sec'] = round(float(line[i+3:i+8]))
            i += Ind[arg-1] + 1
            arg += 1
        elif arg in [2, 3, 4] and Ind[arg-1] != 0:
            value = int(line[i-1:i-1+Ind[arg-1]])
            if arg == 2:
                ZDA['day'] = value
            elif arg == 3:
                ZDA['month'] = value
            elif arg == 4:
                ZDA['year'] = value
            i += Ind[arg-1] + 1
            arg += 1
        elif arg == 7 and Ind[arg-1] != 0:
            ZDA['checksum'] = int(line[i-1:i-1+Ind[arg-1]],16)
            i += Ind[arg-1] + 1
            arg += 1
        else:
            arg += 1
            i += 1

    return ZDA

def parseGSV(line, header, GNSSid, SENTid):
    # Initialize GSV Struct
    GSV = {
        'totS': 0, 'sentN': 0, 'totSat': 0,
        'satid1': 0, 'elev1': 0, 'azim1': 0, 'snr1': 0,
        'satid2': 0, 'elev2': 0, 'azim2': 0, 'snr2': 0,
        'satid3': 0, 'elev3': 0, 'azim3': 0, 'snr3': 0,
        'satid4': 0, 'elev4': 0, 'azim4': 0, 'snr4': 0,
        'sigid': 0, 'checksum': 0
    }

    # Initialize valid satellites
    sat1, sat2, sat3, sat4 = 0, 0, 0, 0
    
    # Initialize Index Vector
    Ind = [0] * 21
    
    # Count Indexes
    i = len(header) + len(GNSSid) + len(SENTid) + 1
    arg = 0
    while i <= len(line):
        if line[i-1] == ',' or line[i-1] == '*':
            arg += 1
            i += 1
            continue
        else:
            Ind[arg-1] += 1
            i += 1

    # Parse ZDA Message
    i = len(header) + len(GNSSid) + len(SENTid) + 2
    arg = 1

    while i <= len(line):
        if arg in range(1,21) and Ind[arg-1] != 0:
            segment = line[i-1:i-1+Ind[arg-1]]
            # value = int(segment.strip())
            try:
                value = int(segment.strip())
            except ValueError:
                print(f"Error converting to int. Segment: '{segment}', Type: {type(segment)} at arg {arg}, full line: '{line}'")
            if arg == 1:
                GSV['totS'] = value
            elif arg == 2:
                GSV['sentN'] = value
            elif arg == 3:
                GSV['totSat'] = value
            elif arg == 4:
                GSV['satid1'] = value
            elif arg == 5:
                GSV['elev1'] = value
            elif arg == 6:
                GSV['azim1'] = value
            elif arg == 7:
                GSV['snr1'] = value
            elif arg == 8:
                GSV['satid2'] = value
            elif arg == 9:
                GSV['elev2'] = value
            elif arg == 10:
                GSV['azim2'] = value
            elif arg == 11:
                GSV['snr2'] = value
            elif arg == 12:
                GSV['satid3'] = value
            elif arg == 13:
                GSV['elev3'] = value
            elif arg == 14:
                GSV['azim3'] = value
            elif arg == 15:
                GSV['snr3'] = value
            elif arg == 16:
                GSV['satid4'] = value
            elif arg == 17:
                GSV['elev4'] = value
            elif arg == 18:
                GSV['azim4'] = value
            elif arg == 19:
                GSV['snr4'] = value
            elif arg == 20:
                GSV['sigid'] = value
            i += Ind[arg-1] + 1
            arg += 1
        elif arg == 21 and Ind[arg-1] != 0:
            checkVal = line[i-1:i-1+Ind[arg-1]]
            GSV['checksum'] = checkVal.strip()
            i += Ind[arg-1] + 1
            arg += 1
        else:
            arg += 1
            i += 1
        
    # Check if each satellite has valid values
    sat1 = 1 if GSV['satid1'] != 0 and GSV['snr1'] != 0 and GSV['elev1'] != 0 and GSV['azim1'] != 0 else 0
    sat2 = 2 if GSV['satid2'] != 0 and GSV['snr2'] != 0 and GSV['elev2'] != 0 and GSV['azim2'] != 0 else 0
    sat3 = 3 if GSV['satid3'] != 0 and GSV['snr3'] != 0 and GSV['elev3'] != 0 and GSV['azim3'] != 0 else 0
    sat4 = 4 if GSV['satid4'] != 0 and GSV['snr4'] != 0 and GSV['elev4'] != 0 and GSV['azim4'] != 0 else 0
    
    return GSV,sat1,sat2,sat3,sat4

def formatSNR(GNSSid, GSV, ZDA, satnum):
    # Initialize SNR
    SNR = {
        'gnssid': '00',
        'satid': 0,
        'elev': 0,
        'azim': 0,
        'snr': 0,
        'year': ZDA['year'],
        'month': ZDA['month'],
        'day': ZDA['day'],
        'hour': ZDA['hour'],
        'min': ZDA['min'],
        'sec': ZDA['sec']
    }

    # Determine GNSS index based on GNSS ID and signal ID
    SIGid = GSV['sigid']
    GNSSindex = '00'
    if GNSSid == "GP":
        if SIGid == 1:
            GNSSindex = '01'  # GPS L1
        elif SIGid == 7:
            GNSSindex = '08'  # GPS L5
    elif GNSSid == "GL":
        GNSSindex = '02'  # GLONASS
    elif GNSSid == "GQ":
        if SIGid == 1:
            GNSSindex = '04'  # QZSS L1-C/A
        elif SIGid == 7:
            GNSSindex = '09'  # QZSS L5
    elif GNSSid == "GB":
        if SIGid == 1:
            GNSSindex = '06'  # Beidou B1l
        elif SIGid == 3:
            GNSSindex = '10'  # Beidou B1C
        elif SIGid == 5:
            GNSSindex = '11'  # Beidou B2a
    elif GNSSid == "GA":
        if SIGid == 7:
            GNSSindex = '07'  # Galileo E1B/C
        elif SIGid == 1:
            GNSSindex = '12'  # Galileo E5a
    elif GNSSid == "GI":
        GNSSindex = '13'  # NavIC
    else:
        print('Error Finding GNSS ID')

    # Satellite information
    sat_key = f'satid{satnum}'
    if sat_key in GSV:
        SNR['gnssid'] = GNSSindex
        SNR['satid'] = f"{GSV[f'satid{satnum}']:02d}"
        SNR['elev'] = f"{GSV[f'elev{satnum}']:02d}"
        SNR['azim'] = f"{GSV[f'azim{satnum}']:03d}"
        SNR['snr'] = f"{GSV[f'snr{satnum}']:02d}"

    return SNR

def parseNMEA_func():
    # Get a list of available serial ports
    ports = serial.tools.list_ports.comports()
    print(ports[0])

    # Check if there are any available ports
    if ports:
        port = ports[0].device  # Assume you want to connect to the first available port

        try:
            # Create a serial connection
            s = serial.Serial(port, 115200, timeout=1)
            s.write_timeout = 1
            # Set the line terminator. CR = '\r', LF = '\n'. CR/LF = '\r\n'
            s.newline = '\r\n'
            print("Connected to Serial Port")
        except serial.SerialException as e:
            print(f"Error opening the serial port: {e}")
    else:
        print("No serial ports found.")

    # Creating Commands
    # End of command
    CFLF = b'\x0D\x0A'  # Equivalent to hex2dec(["0D", "0A"])

    # Serial Port Startup
    # @GGNS: Acquire the positioning-use satellite setting
    GGNS = b'@GGNS' + CFLF
    # @VER: Firmware revision number acquisition
    VER = b'@VER' + CFLF

    # Inject Current UTC Time
    # @GTIM: Time setting
    utcTime = datetime.now(timezone.utc)
    GTIM = f'@GTIM {utcTime.year} {utcTime.month} {utcTime.day} {utcTime.hour} {utcTime.minute} {utcTime.second}'.encode() + CFLF

    # Save Backup Data For Hot Start
    # @BUP: Backup data saving
    BUP = b'@BUP' + CFLF

    # 1 Pulse Per Second Output Enable
    # @GPPS: 1PPS output setting
    GPPS = b'@GPPS 1' + CFLF

    # Idle Mode
    # @GSTP: Positioning stop
    GSTP = b'@GSTP' + CFLF

    # Cold Start
    GCD = b'@GCD' + CFLF

    # Hot Start
    # @GSR: Hot start
    GSR = b'@GSR' + CFLF

    # Set Which Satellites will be tracked (for now all of them)
    # @GNS: Positioning-use satellite setting
    GNS = f'@GNS 0x{16383:X}'.encode() + CFLF # All satellites
    # GNS = f'@GNS 0x{257:X}'.encode() + CFLF  # GPS L1L5 -> GP
    # GNS = f'@GNS 0x{552:X}'.encode() + CFLF  # QZSS L1-C L1-S L5 -> GQ
    # GNS = f'@GNS 0x{3136:X}'.encode() + CFLF  # Beidou B1 B1C B2A -> GB
    # GNS = f'@GNS 0x{4224:X}'.encode() + CFLF  # Galileo E1B E5A -> GA
    # GNS = f'@GNS 0x{1:X}'.encode() + CFLF  # GPS L1 -> GP -> SigID: 1
    # GNS = f'@GNS 0x{2:X}'.encode() + CFLF  # GLONASS -> GL -> SigID: 1
    # GNS = f'@GNS 0x{4:X}'.encode() + CFLF  # SBAS -> ? -> SigID: ?
    # GNS = f'@GNS 0x{8:X}'.encode() + CFLF  # QZSS L1-C/A -> GQ -> SigID: 1
    # GNS = f'@GNS 0x{32:X}'.encode() + CFLF  # QZSS L1-S -> GQ -> SigID: ?
    # GNS = f'@GNS 0x{64:X}'.encode() + CFLF  # Beidou B1l -> GB -> SigID: 1
    # GNS = f'@GNS 0x{128:X}'.encode() + CFLF  # Galileo E1B/C -> GA -> SigID: 7
    # GNS = f'@GNS 0x{256:X}'.encode() + CFLF  # GPS L5 -> GP -> SigID: 7
    # GNS = f'@GNS 0x{512:X}'.encode() + CFLF  # QZSS L5 -> GQ -> SigID: 7
    # GNS = f'@GNS 0x{1024:X}'.encode() + CFLF  # Beidou B1C -> GB -> SigID: 3
    # GNS = f'@GNS 0x{2048:X}'.encode() + CFLF  # Beidou B2a -> GB -> SigID: 5
    # GNS = f'@GNS 0x{4096:X}'.encode() + CFLF  # Galileo E5a -> GA -> SigID: 1
    # GNS = f'@GNS 0x{8192:X}'.encode() + CFLF  # NavIC -> GI -> SigID: 1

    # Set which messages to output
    # @BSSL: Output sentence select
    BSSL = f'@BSSL 0x{136:X}'.encode() + CFLF  # ZDA and GSV
    # BSSL = f'@BSSL 0x{8:X}'.encode() + CFLF  # GSV

    # Execute Commands
    s.write(GSTP)
    s.write(GTIM)
    s.write(GNS)
    s.write(BSSL)
    s.write(GSR)

    time.sleep(5)

    # Initialize Counters
    ZDAcount = 0
    GSVcount = 0
    GPScount = 0
    GLOcount = 0
    GALcount = 0
    BDScount = 0
    QZScount = 0
    NAVICcount = 0
    SNRcount = 0

    # Initiate Minute Counter
    current_min = None
    prev_min = None

    # Initialize Data Storage
    ZDA = []
    GSV = []
    SNR = []

    print('Start')

    try:
        # print('Listening for serial data...')
        while True:
            line = s.readline().decode('utf-8').strip()  # Read a line from the serial port and decode it
            # Assuming you want to do something with 'line' here. For example, print it:
            # print(line)
            # Make sure to include some condition to break out of the loop, or it will run forever.
            if line:
                if line.startswith('$'):
                    GNSSid = line[1:3]
                    SENTid = line[3:6]
                    if SENTid == "ZDA":  # ZDA Message
                        ZDAcount += 1
                        parsed_data = parseZDA(line, '$', GNSSid, SENTid)
                        ZDA.append(parsed_data)
                        # print(f"ZDA Data: {parsed_data}")  # Print parsed ZDA data for debugging
                        current_min = parsed_data['min']
                        if prev_min is None or (current_min in [0, 15, 30, 45] and current_min != prev_min):  # Check for 5 minutes difference, considering hour change
                            prev_min = current_min
                            # Use datetime to format filename with date and time for uniqueness
                            filename = f"{parsed_data['year']} {parsed_data['month']:02d} {parsed_data['day']:02d}_{parsed_data['hour']:02d} {parsed_data['min']:02d}.txt"
                    elif SENTid == "GSV": # GSV Message
                        GSVcount += 1
                        parsed_data,sat1,sat2,sat3,sat4 = parseGSV(line, '$', GNSSid, SENTid)
                        GSV.append(parsed_data)
                        if ZDAcount > 0:
                            with open(filename, 'a') as fid:
                                # Process each satellite if it has valid data
                                for sat in [sat1, sat2, sat3, sat4]:
                                    if sat in [1, 2, 3, 4]:  # Check if satellite number is valid
                                        SNRcount += 1
                                        # Assume SNR is a list to store formatted SNR data for each satellite
                                        SNR.append(formatSNR(GNSSid, GSV[GSVcount-1], ZDA[ZDAcount-1], sat))
                                        # print(SNR[SNRcount-1])
                                        # Fetch the latest SNR entry
                                        snr_data = SNR[SNRcount-1]
                                        # Prepare data string to write to file
                                        data_str = f"{snr_data['gnssid']} {snr_data['satid']} {snr_data['elev']} {snr_data['azim']} {snr_data['snr']} {snr_data['year']} {snr_data['month']} {snr_data['day']} {snr_data['hour']} {snr_data['min']} {snr_data['sec']}\r\n"
                                        # Write the SNR data string to file
                                        fid.write(data_str)

    except KeyboardInterrupt:
        # Graceful exit on keyboard interrupt (Ctrl+C)
        print("\nExiting...")
        print(f"Total ZDA messages: {ZDAcount}")
        print(f"Total GSV messages: {GSVcount}")
    finally:
        # Make sure to close the serial port when done
        s.close()
        fid.close()


if __name__ == "__main__":
    parseNMEA_func()