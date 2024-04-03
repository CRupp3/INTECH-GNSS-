import pandas as pd

def get_wavelength(group):
    const = group["constellation"]
    satID = group["satID"]

    if satID.empty:
        #print("Error: satID series is empty.")
        return None, None  

    satFreqType = const.iloc[0]

    # Calculation: C [Mm/s] / F[MHz] = wavelength [m]
    if satFreqType == 1:  # GPS L1
        return 299.792458 / 1575.42, "GPS L1"
    elif satFreqType == 2:  # GLONASS
        return 299.792458 / 1602.5625, "GLONASS"
    elif satFreqType == 3:  # SBAS
        return 0.0951468, "SBAS"  # Default value, should never have this case
    elif satFreqType == 4:  # QZSS L1-C/A
        return 299.792458 / 1575.42, "QZSS L1-C/A"
    elif satFreqType == 5:  # QZSS L1-S
        return 0.0951468, "QZSS L1-S"  # Default value, should never have this case
    elif satFreqType == 6:  # Beidou B1
        return 299.792458 / 1561.098, "Beidou B1"
    elif satFreqType == 7:  # Galileo E1B/C
        return 299.792458 / 1575.42, "Galileo E1B/C"
    elif satFreqType == 8:  # GPS L5
        return 299.792458 / 1176.45, "GPS L5"
    elif satFreqType == 9:  # QZSS L5
        return 299.792458 / 1176.45, "QZSS L5"
    elif satFreqType == 10:  # Beidou B1C
        return 299.792458 / 1575.42, "Beidou B1C"
    elif satFreqType == 11:  # Beidou B2a
        return 299.792458 / 1176.45, "Beidou B2a"
    elif satFreqType == 12:  # Galileo E5a
        return 299.792458 / 1176.45, "Galileo E5a"
    elif satFreqType == 20: #L2 for testing purposes
        return 299.792458 / 1227.6, "Testing - L2"
    else:  # NavIC
        return 299.792458 / 1176.45, "NavIC"