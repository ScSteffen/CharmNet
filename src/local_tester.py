from src.config_utils import generate_log_filename, read_config_file, update_parameter, write_config_file,    remove_files

from src.scraping_utils import read_csv_file
from src.simulation_utils  import run_cpp_simulation
import pandas as pd

def main():
    subfolder = "benchmarks/lattice_homogeneous/"
    base_config_file = subfolder + "lattice.cfg"
    parameter_range_abs_blue = [100]#[0, 5, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
    parameter_range_scatter_white = [0, 0.5, 1, 5, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
    output_table_name =  "log_data_combined_" + str(parameter_range_abs_blue[0]) + ".csv"

    for scatter_white_value in parameter_range_scatter_white:
        for absorption_blue_value in parameter_range_abs_blue:
            # Step 1: Read the base config file
            parameters = read_config_file(base_config_file)

            # Step 2: Update parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
            parameters = update_parameter(parameters, key='LATTICE_DSGN_ABSORPTION_BLUE', new_value=absorption_blue_value)
            parameters = update_parameter(parameters, key='LATTICE_DSGN_SCATTER_WHITE', new_value=scatter_white_value)

            # Step 3: Update LOG_FILE to a unique identifier linked to LATTICE_DSGN_ABSORPTION_BLUE
            log_file_cur = f'lattice_abs{absorption_blue_value}_scatter{scatter_white_value}'
            parameters = update_parameter(parameters, key='LOG_FILE', new_value=log_file_cur)
            remove_files(subfolder + parameters['LOG_DIR'] +"/"+ log_file_cur)
            parameters = update_parameter(parameters, key='OUTPUT_FILE', new_value=log_file_cur)
            remove_files(subfolder + parameters['OUTPUT_DIR'] +"/"+ log_file_cur + ".vtk")


            # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
            generated_cfg_file = subfolder + f'lattice_abs{absorption_blue_value}_scatter{scatter_white_value}.cfg'
            write_config_file(parameters=parameters, output_file_path=generated_cfg_file)

            # Step 5: Run the C++ simulation
            print("here")
            run_cpp_simulation(generated_cfg_file)

            # Step 6: Read the log file
            log_filename = generate_log_filename(parameters)
            if log_filename:
                # Step 7: Read and convert the data from the CSV log file to a DataFrame
                log_data = read_csv_file(subfolder + log_filename + ".csv")
                log_data['LATTICE_DSGN_ABSORPTION_BLUE'] = absorption_blue_value
                log_data['LATTICE_DSGN_SCATTER_WHITE'] = scatter_white_value

                # Create or append to the DataFrame
                if 'dataframe' not in locals():
                    dataframe = pd.DataFrame([log_data])
                else:
                    dataframe = pd.concat([dataframe, pd.DataFrame([log_data])], ignore_index=True)
                
                print(dataframe)
                # Step 8: Save the DataFrame to file after each iteration
                dataframe.to_csv(subfolder + output_table_name, index=False)

    print("Log Data for all iterations saved in " + str(output_table_name) )



        
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