from height_from_SNR import height_from_SNR
from height_from_sat import height_from_sat

def calculate_file_name(filename, dynamic, interpolate, printFailReasons, showAllPlots):
    height_array, height, hbar, tot_sats = height_from_SNR(filename, "default", dynamic, interpolate, printFailReasons, showAllPlots)
    percentage_usable_data = round(len(height_array) / tot_sats * 100, 1)
    print(f"For the {filename}, the calculated height was {height}, with an hbar of {hbar}, with a total of {len(height_array)} ({percentage_usable_data}%) satellite arcs passing QC.")

#Load in SNR Files
filename = "02_28_24_QUEC.txt" #Data we collected 
better_file = "Larson_data.txt" #24 hours of data collected from Professor Larson 
#Load QC file
QC_filename = "QC_test_file.txt"
#Specify calculation methods 
dynamic = True #Turns on dynamic height correction
interpolate = True #Turns on interpolation *necessary for our antenna 
#Specify  output parameters 
printFailReasons = False #Prints reasons why satellites fail QC parameters to screen
showAllPlots = False #Shows quadchart for every satellite arc and prints to screen all availible information 


calculate_file_name(filename, dynamic, interpolate, printFailReasons, showAllPlots)