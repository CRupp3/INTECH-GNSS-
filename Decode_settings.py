def read_file_and_assign_values(file_path):
    variables = {}
    with open(file_path, 'r') as file:
        current_section = None
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                current_section = line[1:].strip()  # Remove '#' and leading/trailing whitespace
            elif current_section:
                values = line.split()
                variables[current_section] = [int(value) for value in values]  # Assuming values are integers
                current_section = None  # Reset the current section
    return variables

file_path = '/home/mcma/GNSS/INTECH-GNSS-/settings.txt'  # Replace with the path to your file
variables = read_file_and_assign_values(file_path)

# Accessing the variables
emask = variables['emask']
amask = variables['amask']
QC = variables['QC']
sleep = variables['sleep']

print("emask:", emask)
print("amask:", amask)
print("QC:", QC)
print("sleep:", sleep)