import re
import os

def read_config_file(config_file):
    # Dictionary to store parameter names and values
    parameters = {}

    with open(config_file, 'r') as file:
        # Read lines from the file
        lines = file.readlines()

        # Define a regular expression pattern to match parameter lines
        pattern = re.compile(r'\s*([^#%]+)\s*=\s*([^#%]+)\s*')

        # Iterate through lines and extract parameters
        for line in lines:
            # Remove content after '%' symbol
            line = line.split('%')[0].strip()

            # Skip lines starting with '%'
            if line.startswith('%'):
                continue

            match = pattern.match(line)
            if match:
                parameter_name = match.group(1).strip()
                parameter_value = match.group(2).strip()
                parameters[parameter_name] = parameter_value

    return parameters



def generate_log_filename(parameters):
    log_dir = parameters.get('LOG_DIR', '')
    log_file = parameters.get('LOG_FILE', '')

    # Concatenate log_dir and log_file to form the resulting filename
    if log_dir and log_file:
        log_filename = f"{log_dir}/{log_file}"
        return log_filename
    else:
        print("Error: LOG_DIR or LOG_FILE not found in the parameters.")
        return None


def update_parameter(parameters, key, new_value):
    # Create a new dictionary to avoid modifying the original parameters
    updated_parameters = parameters.copy()

    # Update the specified key with the new value
    updated_parameters[key] = new_value

    return updated_parameters

def write_config_file(parameters, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
        file.write("%  Auto-generated Config File           %\n")
        file.write("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n")

        for key, value in parameters.items():
            file.write(f"{key} = {value}\n")


def remove_files(filename):
    # Construct file paths for the log file and CSV file
    log_file_path = filename
    csv_file_path = filename + ".csv"

    # Remove the log file if it exists
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
        print(f"Removed {log_file_path}")

    # Remove the CSV file if it exists
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)
        print(f"Removed {csv_file_path}")

def update_lattice(n_cell, filepath):
    filename_geo = filepath + 'lattice.geo'
    filename_su2 = filepath + f'lattice_n{n_cell}.su2'
    filename_con = filepath + f'lattice_n{n_cell}.con'

    if not os.path.exists(filename_su2):
        with open(filename_geo, 'r') as file:
            lines = file.readlines()

        with open(filename_geo, 'w') as file:
            for line in lines:
                if line.startswith('n_recombine'):
                    line = f'n_recombine = {n_cell};\n'
                file.write(line)

        # Remove the .con file
        if os.path.exists(filename_con):
            os.remove(filename_con)

        os.system(f'gmsh {filename_geo} -2 -format su2 -save_all -o {filename_su2}')

    return f'lattice_n{n_cell}.su2'