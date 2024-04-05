from height_from_SNR import height_from_SNR
# from height_from_sat import height_from_sat

def calculate_file_name(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots):
    height_array, height, hbar, tot_sats, time = height_from_SNR(filename, QC_filename, dynamic, interpolate, printFailReasons, showAllPlots)
    percentage_usable_data = round(len(height_array) / tot_sats * 100, 1)
    print(f"For the {filename}, the calculated height was {height}, with an hbar of {hbar}, with a total of {len(height_array)} ({percentage_usable_data}%) satellite arcs passing QC.")

    time = [int(item) for item in time]
    stringtime = str(time)
    stringtime = stringtime[1:-1]
    return height, stringtime
