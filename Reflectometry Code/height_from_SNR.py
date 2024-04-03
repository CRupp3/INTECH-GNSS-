import pandas as pd
from read_QC import read_QC
from quality_control_filter import quality_control_filter
from get_wavelength import get_wavelength
from peak2noise import peak2noise
from lomb import lomb
from get_ofac_hifac import get_ofac_hifac
from height_from_sat import height_from_sat
import numpy as np

def height_from_SNR(file, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots):
    custom_row_names = ["constellation", "satID", "elevAng", "azAng", "SNR_data", "year", "month", "day", "hour", "min", "sec"]
    df = pd.read_csv(file, sep='\s+', header=None, names=custom_row_names)
    
    # Convert the time columns to seconds, and save year and day of year 
    df['gpsTime'] = df['hour'] * 3600 + df['min'] * 60 + df['sec']
    year = df['year'].iloc[0]
    doy = df['day'].iloc[0]

    # Create a new DataFrame with the desired columns
    df_time_correct = df[['constellation', 'satID', 'elevAng', 'azAng', 'SNR_data', 'year', 'month', 'day', 'gpsTime']]  # Adjust column names here
    
    # Sort based on Constellation, Satellite, and time
    df = df_time_correct.sort_values(by=["constellation", "satID", "gpsTime"])
    
    # Group by Constellation and Satellite
    grouped_df = df.groupby(['constellation', 'satID'])
    
    calced_Heights = []  # Empty array to save calculated water heights hbar value for dynamic  
    tan_elevAngles = [] # Empty array to save the tan(elev(t))
    edots = [] # Empty array to save the edot(t)
    
    total_height_calls = 0

    if dynamic:  # Check if dynamic is enabled before the loop
        maxRH_list = []
        tan_elevAngles_over_edots_list = []

    for (constellation, satID), group_df in grouped_df:  # Loop through every individual satellite in snr file
        # Check for time difference greater than 20 minutes
        time_diff = group_df['gpsTime'].diff().shift(-1).fillna(0) # Calculate time difference between consecutive rows
        group_df['group'] = (time_diff > 30 * 60).cumsum()  # Create a new group whenever time difference is greater than 30 minutes

        # Exclude the first row of each group
        group_df = group_df.groupby(['constellation', 'satID', 'group']).apply(lambda x: x.iloc[1:]).reset_index(drop=True)

        # Group by both 'constellation', 'satID', and the new 'group'
        grouped_by_time = group_df.groupby(['constellation', 'satID', 'group'])
        
        for _, time_group_df in grouped_by_time:
            # Call height_from_sat function for every satellite present
            result = height_from_sat(time_group_df, QC_filename, dynamic, year, doy, interpolate, printFailReasons, showAllPlots)
            total_height_calls += 1
            
            if result is not None:
                maxRH, tan_elevAngle_at_avg_time, edot_at_avg_time = result

                # Append the results to respective lists
                if maxRH is not None:
                    calced_Heights.append(maxRH)
                if dynamic:
                    if tan_elevAngle_at_avg_time is not None:
                        tan_elevAngles.append(tan_elevAngle_at_avg_time)
                    if edot_at_avg_time is not None:
                        edots.append(edot_at_avg_time)

                    # Append values for constructing matrices
                    if maxRH is not None:
                        maxRH_list.append(maxRH)
                    if tan_elevAngle_at_avg_time is not None and edot_at_avg_time is not None:
                        tan_elevAngles_over_edots_list.append(tan_elevAngle_at_avg_time / edot_at_avg_time)

    if dynamic: 
        if len(maxRH_list) > 0:
            # Convert lists to numpy arrays
            L = np.array(maxRH_list).reshape(-1, 1)
            A = np.column_stack((np.ones(len(maxRH_list)), np.array(tan_elevAngles_over_edots_list)))

            # Calculate transpose of A
            A_transpose = np.transpose(A)

            # Calculate A^T A
            ATA = np.dot(A_transpose, A)

            # Calculate A^T L
            ATL = np.dot(A_transpose, L)

            # Calculate the inverse of ATA
            ATA_inv = np.linalg.inv(ATA)

            # Calculate x
            x = np.dot(np.dot(ATA_inv, A_transpose), L)

            # Extract calculated_h and calculated_hbar from x
            calculated_h = x[0][0]
            calculated_hbar = x[1][0]
        else:
            calculated_h = None
            calculated_hbar = None
    else: 
        if len(calced_Heights) > 0:
            calculated_h = np.mean(calced_Heights)
        else:
            calculated_h = None
        calculated_hbar = None
    
    height_array = calced_Heights
    
    return height_array, calculated_h, calculated_hbar, total_height_calls 