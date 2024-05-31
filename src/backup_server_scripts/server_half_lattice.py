import umbridge


from src.config_utils import (
    generate_log_filename,
    read_config_file,
    update_parameter,
    write_config_file,
    remove_files,
    update_half_lattice_mesh_file,
    write_slurm_file,
)
from src.scraping_utils import read_csv_file
from src.simulation_utils import run_cpp_simulation_containerized
from src.general_utils import replace_next_line


class KiTRTModelHalfLattice(umbridge.Model):

    def __init__(self):
        super().__init__("forward")

    def get_input_sizes(self, config):
        return [5]

    def get_output_sizes(self, config):
        return [7]

    def __call__(self, parameters, config):
        """
        A function that performs a series of steps including reading a base config file,
        updating parameters based on input values, running a C++ simulation, and processing
        the output data. It takes in parameters and a config dictionary, and returns a list
        of quantities of interest calculated during the simulation.
        """

        scatter_white_value = parameters[0][0]
        absorption_blue_value = parameters[0][1]

        n_cells = parameters[0][2]
        quad_order = int(parameters[0][3])

        hpc_operation = parameters[0][4]

        subfolder = "benchmarks/half_lattice/"
        base_config_file = subfolder + "half_lattice.cfg"

        # Step 1: Read the base config file
        kitrt_parameters = read_config_file(base_config_file)
        lattice_file_new = update_half_lattice_mesh_file(n_cells, subfolder + "mesh/")

        # Step 2: Update kitrt_parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
        kitrt_parameters = update_parameter(
            kitrt_parameters,
            key="LATTICE_DSGN_ABSORPTION_BLUE",
            new_value=absorption_blue_value,
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters,
            key="LATTICE_DSGN_SCATTER_WHITE",
            new_value=scatter_white_value,
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="QUAD_ORDER", new_value=quad_order
        )
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="MESH_FILE", new_value="mesh/" + lattice_file_new
        )

        # Step 3: Update LOG_FILE to a unique identifier linked to LATTICE_DSGN_ABSORPTION_BLUE
        unique_name = f"half_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_p{n_cells}_q{quad_order}"

        kitrt_parameters = update_parameter(
            kitrt_parameters, key="LOG_FILE", new_value=unique_name
        )
        remove_files(subfolder + kitrt_parameters["LOG_DIR"] + "/" + unique_name)
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="OUTPUT_FILE", new_value=unique_name
        )
        remove_files(
            subfolder + kitrt_parameters["OUTPUT_DIR"] + "/" + unique_name + ".vtk"
        )

        # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
        generated_cfg_file = subfolder + unique_name + ".cfg"
        write_config_file(
            parameters=kitrt_parameters, output_file_path=generated_cfg_file
        )

        # Step 5: Run the C++ simulation
        # command = "../../build/KiT-RT " + f'half_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_p{n_cells}_q{quad_order}.cfg'
        # slurm_file = "slurm_" + f'half_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_p{n_cells}_q{quad_order}.sh'
        # replace_next_line("slurm_scripts/slurm_script.txt", command, slurm_file)

        if hpc_operation == 0:
            # Step 5: Run the C++ simulation
            run_cpp_simulation_containerized(generated_cfg_file)
        elif hpc_operation == 1:
            # Write slurm file
            write_slurm_file(
                "benchmarks/half_lattice/slurm_scripts/", unique_name, subfolder
            )
        # Step 6: Read the log file
        if hpc_operation == 0 or hpc_operation == 2:
            log_filename = generate_log_filename(kitrt_parameters)

            if log_filename:
                # Step 7: Read and convert the data from the CSV log file to a DataFrame
                log_data = read_csv_file(subfolder + log_filename + ".csv")
                log_data["LATTICE_DSGN_ABSORPTION_BLUE"] = absorption_blue_value
                log_data["LATTICE_DSGN_SCATTER_WHITE"] = scatter_white_value
                quantities_of_interest = [
                    float(log_data["Cur_outflow"]),
                    float(log_data["Total_outflow"]),
                    float(log_data["Max_outflow"]),
                    float(log_data["Cur_absorption"]),
                    float(log_data["Total_absorption"]),
                    float(log_data["Max_absorption"]),
                    float(log_data["Wall_time_[s]"]),
                ]
        else:
            quantities_of_interest = [0] * 7

        return [quantities_of_interest]

    def supports_evaluate(self):
        return True

    def gradient(self, out_wrt, in_wrt, kitrt_parameters, sens, config):
        return 0

    def supports_gradient(self):
        return True


kitrtmodel = KiTRTModelHalfLattice()

umbridge.serve_models([kitrtmodel], 4243)
