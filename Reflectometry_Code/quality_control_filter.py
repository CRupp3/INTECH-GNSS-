import pandas as pd
from read_QC import read_QC

def quality_control_filter(group, QC_filename):
    [emin, emax, ediff, maxHeight, desiredPrecision, frange_0, frange_1, minAmp, minRH, maxArcTime, pknoiseCrit, azmin, azmax] = read_QC(QC_filename)

    # Apply quality control filter
    filtered_group = group[
        (group['elevAng'] >= emin) & (group['elevAng'] <= emax) &
        (group['azAng'] >= azmin) & (group['azAng'] <= azmax)
    ]

    return filtered_group