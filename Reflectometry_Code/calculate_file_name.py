from height_from_SNR import height_from_SNR
# from height_from_sat import height_from_sat

def calculate_file_name(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots):
    height_array, height, hbar, tot_sats, time = height_from_SNR(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots)

    if height_array is None:  # Check if height_array is None (indicating an error)
        print("Error: Unable to calculate heights.")
        return
    
    if tot_sats != 0:
        percentage_usable_data = round(len(height_array) / tot_sats * 100, 1)
    else: 
        percentage_usable_data = 0
    
    print(f"For the {filename}, the calculated height was {height}, with an hbar of {hbar}, with a total of {len(height_array)} ({percentage_usable_data}%) satellite arcs passing QC.")
    
    time = [int(item) for item in time]
    # Format each component with leading zeros if necessary
    formatted_time = [
        str(component).zfill(2) if index != 0 else str(component)[2:]  # For the year, only take the last two digits
        for index, component in enumerate(time)
    ]
    # Concatenate the formatted components into the desired string format
    stringtime = ''.join(formatted_time)
    return height, stringtime
