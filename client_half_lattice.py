# import umbridge
import numpy as np
import os

from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_lattice_samples_from_param_range,
    load_lattice_samples_from_npz,
    delete_slurm_scripts,
)
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


# url = "http://localhost:4243"
# model = umbridge.HTTPModel(url, "forward")


def main():
    hpc_operation = False  # Flag when using HPC cluster
    load_from_npz = False

    # Define parameter ranges
    # characteristic length of the cells
    parameter_range_n_cell = [
        0.02, 0.01, 0.005, 0.0025, 0.001,
    ]
    #    0.0075,
    #    0.005,
    #    0.0025,
    #    0.001,
    # ]
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)

    parameter_range_quad_order = [
        10, 20, 30, 40, 50
    ]
    #    20,
    #    30,
    #    40,
    #    50,
    #    60,
    # ]  # GAUSS LEGENDRE 2D quadrature

    parameter_range_abs_blue = [
        10
    ]  # [0, 5, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
    parameter_range_scatter_white = [
        1
    ]  # [0, 0.5, 1, 5, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

    if load_from_npz:  # TODO
        design_params, design_param_names = load_lattice_samples_from_npz(
            "sampling/pilot-study-samples-hohlraum-05-29-24.npz"
        )
    else:
        design_params, design_param_names = create_lattice_samples_from_param_range(
            parameter_range_n_cell,
            parameter_range_quad_order,
            parameter_range_abs_blue,
            parameter_range_scatter_white,
        )

    if hpc_operation:
        print("==== Execute HPC version ====")
        directory = "./benchmarks/half_lattice/slurm_scripts/"

        delete_slurm_scripts(directory)  # delete existing slurm files for hohlraum
        call_models(design_params, hpc_operation_count=1)

        user = read_username_from_config("./slurm_config.txt")
        if user:
            print("Executing slurm scripts with user " + user)
            execute_slurm_scripts(directory, user)
            wait_for_slurm_jobs(user=user, sleep_interval=10)
        else:
            print("Username could not be read from config file.")

        qois = call_models(design_params, hpc_operation_count=2)
    else:
        qois = call_models(design_params, hpc_operation_count=0)

    print(
        "design parameter matrix: [grid_param, quad_order, scatter value white, absorption value blue]"
    )
    print("design parameter matrix")
    print(design_params)
    print(
        "quantities of interest: [Cur_outflow, Total_outflow, Max_outflow, Cur_absorption, Total_absorption, Max_absorption, Wall_time_[s]]"
    )
    print(qois)
    np.savez("benchmarks/half_lattice/sn_study_half_lattice_qois.npz", array=qois)
    np.savez("benchmarks/half_lattice/ssn_study_half_lattice_params.npz", array=design_params)
    np.savez(
        "benchmarks/hohlraum/ssn_study_half_lattice_params_col_names.npz",
        array=design_param_names,
    )
    np.savez(
        "benchmarks/hohlraum/ssn_study_half_lattice_qois_col_names.npz",
        array=get_qois_col_names(),
    )
    print("======== Finished ===========")
    return 0


def call_models(
    design_params,
    hpc_operation_count,
):
    qois = []
    print(design_params.T.shape)
    for column in design_params:
        input = column.tolist()
        print(input)
        input.append(hpc_operation_count)
        res = model([input])
        qois.append(res[0])

    return np.array(qois)


def model(parameters):
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

    unique_name = f"half_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_p{n_cells}_q{quad_order}"
    if hpc_operation == 2:
        if os.path.exists(
            subfolder + "mesh/" + "hohlraum_variable_backup" + unique_name + ".geo"
        ):
            os.remove(
                subfolder + "mesh/" + "hohlraum_variable_backup" + unique_name + ".geo"
            )  # remove backup geo files

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

    kitrt_parameters = update_parameter(
        kitrt_parameters, key="LOG_FILE", new_value=unique_name
    )
    if hpc_operation < 2:
        remove_files(subfolder + kitrt_parameters["LOG_DIR"] + "/" + unique_name)
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="OUTPUT_FILE", new_value=unique_name
    )
    if hpc_operation < 2:
        remove_files(
            subfolder + kitrt_parameters["OUTPUT_DIR"] + "/" + unique_name + ".vtk"
        )

    # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
    generated_cfg_file = subfolder + unique_name + ".cfg"
    write_config_file(parameters=kitrt_parameters, output_file_path=generated_cfg_file)

    # Step 5: Run the C++ simulation
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
                float(log_data["Cur_absorption"]),
                float(log_data["Total_absorption"]),
                float(log_data["Max_absorption"]),
                float(log_data["Wall_time_[s]"]),
            ]
    else:
        quantities_of_interest = [0] * 7

    return [quantities_of_interest]


if __name__ == "__main__":
    main()
