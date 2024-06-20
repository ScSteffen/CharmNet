import numpy as np

# import umbridge
import os

from src.config_utils import (
    generate_log_filename,
    read_config_file,
    update_parameter,
    write_config_file,
    remove_files,
    update_var_quarter_hohlraum_mesh_file,
    write_slurm_file,
)
from src.scraping_utils import (
    read_csv_file,
    get_integrated_quarter_hohlraum_probe_moments,
)
from src.simulation_utils import run_cpp_simulation_containerized


from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_quarter_hohlraum_samples_from_param_range,
    load_quarter_hohlraum_samples_from_npz,
    delete_slurm_scripts,
)

# url = "http://localhost:4242"
# model = umbridge.HTTPModel(url, "forward")
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Process some flags for HPC and mesh operations."
    )

    # Add arguments
    parser.add_argument(
        "--no-hpc", action="store_true", help="Flag when using HPC cluster"
    )
    parser.add_argument(
        "--load-from-npz", action="store_true", help="Flag to load from NPZ file"
    )
    parser.add_argument(
        "--no-singularity-hpc",
        action="store_true",
        help="Flag to use Singularity on HPC",
    )
    parser.add_argument(
        "--rectangular-mesh",
        action="store_true",
        help="Flag for using rectangular mesh",
    )

    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print(f"HPC mode = { not args.no_hpc}")
    print(f"Load from npz = {args.load_from_npz}")
    print(f"HPC with singularity = { not args.no_singularity_hpc}")
    print(f"Use rectangular_mesh = {args.rectangular_mesh}")

    hpc_operation = not args.no_hpc  # Flag when using HPC cluster
    load_from_npz = args.load_from_npz
    singularity_hpc = not args.no_singularity_hpc
    rectangular_mesh = args.rectangular_mesh

    # Define parameter ranges
    parameter_range_n_cell = [
        # 0.025,
        0.000125,
        # 0.0075,
        # 0.005,
        # 0.0025,
        # 0.001,
        # 0.00075,
        # 0.0005,
        # 0.00025,
        # 0.0001,
    ]  # characteristic length of the cells
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)
    parameter_range_quad_order = [10, 20, 30, 40]
    parameter_range_red_right_top = [0.4]  # [0.4, 0.45, 0.35]
    parameter_range_horizontal_right = [0.6]  # [0.61, 0.6, 0.59]

    if load_from_npz:
        design_params, design_param_names = load_quarter_hohlraum_samples_from_npz(
            "sampling/pilot-study-samples-hohlraum-05-29-24.npz"
        )
    else:
        design_params, design_param_names = (
            create_quarter_hohlraum_samples_from_param_range(
                parameter_range_n_cell,
                parameter_range_quad_order,
                parameter_range_red_right_top,
                parameter_range_horizontal_right,
            )
        )
        print(design_params)

    if hpc_operation:
        print("==== Execute HPC version ====")
        directory = "./benchmarks/quarter_hohlraum/slurm_scripts/"
        user = read_username_from_config("./slurm_config.txt")

        delete_slurm_scripts(directory)  # delete existing slurm files for hohlraum
        call_models(
            design_params,
            hpc_operation_count=1,
            singularity_hpc=singularity_hpc,
            rectangular_mesh=rectangular_mesh,
        )
        wait_for_slurm_jobs(user=user, sleep_interval=10)

        if user:
            print("Executing slurm scripts with user " + user)
            execute_slurm_scripts(directory, user)
            wait_for_slurm_jobs(user=user, sleep_interval=10)
        else:
            print("Username could not be read from slurm config file.")
        qois = call_models(
            design_params, hpc_operation_count=2, rectangular_mesh=rectangular_mesh
        )
    else:
        qois = call_models(
            design_params, hpc_operation_count=0, rectangular_mesh=rectangular_mesh
        )

    print("design parameter matrix")
    print(design_param_names)
    print(design_params)
    print("quantities of interest:")
    print(get_qois_col_names())
    print(qois)
    np.savez(
        "benchmarks/quarter_hohlraum/sn_study_hohlraum.npz",
        qois=qois,
        design_params=design_params,
        qoi_column_names=get_qois_col_names(),
        design_param_column_names=design_param_names,
    )

    print("======== Finished ===========")
    return 0


def call_models(
    design_params, hpc_operation_count, singularity_hpc=True, rectangular_mesh=False
):
    qois = []
    for column in design_params:
        input = column.tolist()
        input.append(hpc_operation_count)
        input.append(singularity_hpc)
        input.append(rectangular_mesh)

        res = model([input])
        qois.append(res[0])

    return np.array(qois)


def model(parameters):
    # non umbridge call
    print(parameters)
    right_red_top = parameters[0][0]
    horizontal_right_red = parameters[0][1]
    n_cells = parameters[0][2]
    quad_order = int(parameters[0][3])
    hpc_operation = parameters[0][4]
    singularity_hpc = parameters[0][5]
    rectangular_mesh = parameters[0][6]

    subfolder = "benchmarks/quarter_hohlraum/"
    base_config_file = subfolder + "quarter_hohlraum.cfg"

    # Step 1: Read the base config file
    kitrt_parameters = read_config_file(base_config_file)
    hohlraum_file_new = update_var_quarter_hohlraum_mesh_file(
        hpc_mode=(hpc_operation == 1),
        filepath=subfolder + "mesh/",
        cl_fine=n_cells,
        upper_right_red=right_red_top,
        horizontal_right_red=horizontal_right_red,
        rectangular_mesh=rectangular_mesh,
    )
    unique_name = f"quarter_hohlraum_variable_cl{n_cells}_q{quad_order}_urr{right_red_top}_hrr{horizontal_right_red}"

    if hpc_operation == 2:
        if os.path.exists(
            subfolder
            + "mesh/"
            + "quarter_hohlraum_variable_backup"
            + unique_name
            + ".geo"
        ):
            os.remove(
                subfolder
                + "mesh/"
                + "quarter_hohlraum_variable_backup"
                + unique_name
                + ".geo"
            )  # remove backup geo files

    # Step 2: Update kitrt_parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="QUAD_ORDER", new_value=quad_order
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="MESH_FILE", new_value="mesh/" + hohlraum_file_new
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_RED_RIGHT_TOP", new_value=right_red_top
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_BORDER_RED_RIGHT", new_value=horizontal_right_red
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
    if hpc_operation == 0:
        # Step 5: Run the C++ simulation
        run_cpp_simulation_containerized(generated_cfg_file)
    elif hpc_operation == 1:
        # Write slurm file
        write_slurm_file(
            "benchmarks/quarter_hohlraum/slurm_scripts/",
            unique_name,
            subfolder,
            singularity_hpc,
        )

    if hpc_operation == 0 or hpc_operation == 2:
        # Step 6: Read the log file
        log_filename = generate_log_filename(kitrt_parameters)
        if log_filename:
            # Step 7: Read and convert the data from the CSV log file to a DataFrame
            log_data = read_csv_file(subfolder + log_filename + ".csv")
            N = 10
            integrated_probe_moments = get_integrated_quarter_hohlraum_probe_moments(
                subfolder + log_filename, N=N, t_final=kitrt_parameters["TIME_FINAL"]
            )
            # print(integrated_probe_moments)
            quantities_of_interest = [
                float(log_data["Wall_time_[s]"]),
                float(log_data["Cumulated_absorption_center"]),
                float(log_data["Cumulated_absorption_vertical_wall"]),
                float(log_data["Cumulated_absorption_horizontal_wall"]),
                float(log_data["Var. absorption green"]),
            ]

            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 0 u_0"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 0 u_1"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 0 u_2"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 1 u_0"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 1 u_1"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 1 u_2"][i])
                )
    else:
        quantities_of_interest = [0] * 125

    return [quantities_of_interest]


def get_qois_col_names():
    return np.array(
        [
            "Wall_time_[s]",
            "Cumulated_absorption_center",
            "Cumulated_absorption_vertical_wall",
            "Cumulated_absorption_horizontal_wall",
            "Variation_absorption_green",
            "Probe0_u0_N1",
            "Probe0_u0_N2",
            "Probe0_u0_N3",
            "Probe0_u0_N4",
            "Probe0_u0_N5",
            "Probe0_u0_N6",
            "Probe0_u0_N7",
            "Probe0_u0_N8",
            "Probe0_u0_N9",
            "Probe0_u0_N10",
            "Probe0_u1_N1",
            "Probe0_u1_N2",
            "Probe0_u1_N3",
            "Probe0_u1_N4",
            "Probe0_u1_N5",
            "Probe0_u1_N6",
            "Probe0_u1_N7",
            "Probe0_u1_N8",
            "Probe0_u1_N9",
            "Probe0_u1_N10",
            "Probe0_u2_N1",
            "Probe0_u2_N2",
            "Probe0_u2_N3",
            "Probe0_u2_N4",
            "Probe0_u2_N5",
            "Probe0_u2_N6",
            "Probe0_u2_N7",
            "Probe0_u2_N8",
            "Probe0_u2_N9",
            "Probe0_u2_N10",
            "Probe1_u0_N1",
            "Probe1_u0_N2",
            "Probe1_u0_N3",
            "Probe1_u0_N4",
            "Probe1_u0_N5",
            "Probe1_u0_N6",
            "Probe1_u0_N7",
            "Probe1_u0_N8",
            "Probe1_u0_N9",
            "Probe1_u0_N10",
            "Probe1_u1_N1",
            "Probe1_u1_N2",
            "Probe1_u1_N3",
            "Probe1_u1_N4",
            "Probe1_u1_N5",
            "Probe1_u1_N6",
            "Probe1_u1_N7",
            "Probe1_u1_N8",
            "Probe1_u1_N9",
            "Probe1_u1_N10",
            "Probe1_u2_N1",
            "Probe1_u2_N2",
            "Probe1_u2_N3",
            "Probe1_u2_N4",
            "Probe1_u2_N5",
            "Probe1_u2_N6",
            "Probe1_u2_N7",
            "Probe1_u2_N8",
            "Probe1_u2_N9",
            "Probe1_u2_N10",
        ]
    )


if __name__ == "__main__":
    main()
