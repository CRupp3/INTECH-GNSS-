
# need this code to be written
# check voltage
# check Temperature


#read in settings.txt
# break the file into the variables:
#voltage_cutoff 
#temp_cutoff_low_celcius 
#temp_cutoff_high_celcius 
#sleep_mode_on_bool  
#sleep_time_min  

#if voltage > voltage_cutoff   
    #send message to swarm to wake 

#if || Temperature <= temp_cutoff_low_celcius || Temperature >= temp_cutoff_high_celcius
    #Stop Charging Battery 

#if || Temperature > temp_cutoff_low_celcius && Temperature < temp_cutoff_high_celcius
    #Charge Battery 


###########
#not sure if we should implement sleep mode at this time. I think it may be too complex for our timeline

#check if any of the sleep conditions have been meet:

#if voltage <= voltage_cutoff  
    #sleep_mode_on_bool = 1
    #send message to swarm to send a message that sleep mode it being turned on
    #send message to swarmsleep for sleep_time_min    




