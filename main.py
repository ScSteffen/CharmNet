from src.config_utils import generate_log_filename, read_config_file, update_parameter, write_config_file,    remove_files

from src.scraping_utils import read_csv_file
from src.simulation_utils  import run_cpp_simulation
import pandas as pd

def main():
    subfolder = "benchmarks/lattice_homogeneous/"
    base_config_file = subfolder + "lattice.cfg"
    parameter_range = [1, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

    dataframe_list = []  # List to store DataFrames for each iteration

    for absorption_blue_value in parameter_range:
        # Step 1: Read the base config file
        parameters = read_config_file(base_config_file)

        # Step 2: Update parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
        parameters = update_parameter(parameters, key='LATTICE_DSGN_ABSORPTION_BLUE', new_value=absorption_blue_value)

        # Step 3: Update LOG_FILE to a unique identifier linked to LATTICE_DSGN_ABSORPTION_BLUE
        log_file_cur = f'lattice_{absorption_blue_value}'
        parameters = update_parameter(parameters, key='LOG_FILE', new_value=log_file_cur)
        remove_files(subfolder + parameters['LOG_DIR'] +"/"+ log_file_cur)
        parameters = update_parameter(parameters, key='OUTPUT_FILE', new_value=log_file_cur)
        remove_files(subfolder + parameters['OUTPUT_DIR'] +"/"+ log_file_cur + ".vtk")


        # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
        generated_cfg_file = subfolder + f'lattice_{absorption_blue_value}.cfg'
        write_config_file(parameters=parameters, output_file_path=generated_cfg_file)

        # Step 5: Run the C++ simulation
        run_cpp_simulation(generated_cfg_file)

        # Step 6: Read the log file
        log_filename = generate_log_filename(parameters)
        if log_filename:
            # Step 7: Read and convert the data from the CSV log file to a DataFrame
            log_data = read_csv_file(subfolder + log_filename + ".csv")
            log_data['LATTICE_DSGN_ABSORPTION_BLUE'] = absorption_blue_value

            # Create or append to the DataFrame
            if 'dataframe' not in locals():
                dataframe = pd.DataFrame([log_data])
            else:
                dataframe = pd.concat([dataframe, pd.DataFrame([log_data])], ignore_index=True)
            
            print(dataframe)
            # Step 8: Save the DataFrame to file after each iteration
            dataframe.to_csv(subfolder + "log_data_combined.csv", index=False)

    print("Log Data for all iterations saved in log_data_combined.csv")



        
def main_single_run():
    subfolder = "benchmarks/lattice_baseline/"
    config_file_path =subfolder + "lattice_S3_n10.cfg"

    # Step 1: Read the config file
    parameters = read_config_file(config_file_path)

    # Step 2: Change the design parameters of the test case
    parameters = update_parameter(parameters,key = 'LOG_FILE', new_value= 'test')

    generated_cfg_file = subfolder + 'generated.cfg'
    write_config_file(parameters=parameters,output_file_path=generated_cfg_file)
    # Step 3: Run the C++ simulation
    run_cpp_simulation(generated_cfg_file)

    # Step 4: Read the log file
    log_filename = generate_log_filename(parameters)
    if log_filename:
            # Step 7: Read and append the data from the CSV log file to the DataFrame
            log_data = read_csv_file(subfolder + log_filename + ".csv")

            # Insert a new column with the parameter values
            log_data.insert(0, 'LATTICE_DSGN_ABSORPTION_BLUE', absorption_blue_value)

            # Create or append to the DataFrame
            if 'dataframe' not in locals():
                dataframe = pd.DataFrame(log_data)
            else:
                dataframe = dataframe.append(log_data, ignore_index=True)

            # Step 8: Save the DataFrame to file
            dataframe.to_csv(subfolder + "log_data_combined.csv", index=False)

    print("Log Data for all iterations saved in log_data_combined.csv")


if __name__ == "__main__":
    main()