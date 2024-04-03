text = """#emask_min
5
#emas_max
25
#amask_min
10 
#amask_max
120
#e_diff
5 
#volateg_cutoff
11
#temp_cutoff_low_celcius
-20 
#temp_cutoff_high_celcius
30
#sleep_mode_on_bool 
0 
#sleep_time_min
60"""

# Calculate byte size
byte_size = len(text.encode('utf-8'))

print("Byte size:", byte_size)