import numpy as np

def read_QC(filename):
    if filename == "default":
        # Default values 
        emin = 5
        emax = 25
        ediff = 10
        maxHeight = 8
        desiredPrecision = 0.005
        frange_0 = 0 
        frange_1 = 5
        minAmp = 2  # Arbitrary value which should let everything pass through 
        minRH = 0.4  # meters
        maxArcTime = 1  # one hour
        pknoiseCrit = 3.5
        azmin = 0
        azmax = 360
        
    else: 
        try:
            with open(filename, 'r') as file:
                # Set specific values 
                # Read the content of the file
                content = file.read().strip()

                # Split the content into a list of numbers
                numbers = content.split()

                # Check if the number of values matches the expected number of variables
                expected_variable_count = 13  # Expected number of QC variables 
                if len(numbers) != expected_variable_count:
                    raise ValueError(f"Number of values in the file does not match the expected number of variables.")

                # Assign each value to a separate variable
                emin = int(numbers[0])
                emax = int(numbers[1])
                ediff = int(numbers[2])
                maxHeight = int(numbers[3])
                desiredPrecision = float(numbers[4])
                frange_0 = int(numbers[5])
                frange_1 = int(numbers[6])
                minAmp = int(numbers[7])
                minRH = float(numbers[8])
                maxArcTime = int(numbers[9])
                pknoiseCrit = float(numbers[10])
                azmin = int(numbers[11])
                azmax = int(numbers[12])

        except FileNotFoundError:
            print(f"File not found: {filename}")
            return None
        except ValueError as ve:
            print(f"Error: {ve}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    return [emin, emax, ediff, maxHeight, desiredPrecision, frange_0, frange_1, minAmp, minRH, maxArcTime, pknoiseCrit, azmin, azmax]
