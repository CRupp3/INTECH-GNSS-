import numpy as np

def read_QC(filename):
    # Default values 
    emin = 5
    emax = 25
    ediff = 10
    maxHeight = 6
    desiredPrecision = 0.005
    frange_0 = 0 
    frange_1 = 5
    minAmp = 2  # Arbitrary value which should let everything pass through 
    minRH = 2  # meters
    maxArcTime = 1  # one hour
    pknoiseCrit = 3.5
    azmin = 0
    azmax = 360
    
    try:
        with open(filename, 'r') as file: 
            # Read the content of the file
            content = file.read().strip()

            # Split the content into a list of numbers
            numbers = content.split()

            # Check if the number of values matches the expected number of variables
            expected_variable_count = 10  # Expected number of QC variables
            if len(numbers) != expected_variable_count:
                raise ValueError("Number of values in the file does not match the expected number of variables.")
                
            # If we are reading the file, overwrite these values with what is in the input file
            emin = int(numbers[0])
            emax = int(numbers[1])
            azmin = int(numbers[2])
            azmax = int(numbers[3])
            ediff = int(numbers[4])
                
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}") 
    return [emin, emax, ediff, maxHeight, desiredPrecision, frange_0, frange_1, minAmp, minRH, maxArcTime, pknoiseCrit, azmin, azmax]
