import numpy as np

# import umbridge
import os

from src.config_utils import (
    generate_log_filename,
    read_config_file,
    update_parameter,
    write_config_file,
    remove_files,
    update_var_hohlraum_mesh_file,
    write_slurm_file,
)
from src.scraping_utils import read_csv_file, get_integrated_hohlraum_probe_moments
from src.simulation_utils import run_cpp_simulation_containerized


from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_hohlraum_samples_from_param_range,
    load_hohlraum_samples_from_npz,
    delete_slurm_scripts,
)

# url = "http://localhost:4242"
# model = umbridge.HTTPModel(url, "forward")


def main():
    hpc_operation = True  # Flag when using HPC cluster
    load_from_npz = True

    # Define parameter ranges
    parameter_range_n_cell = [0.03]  # characteristic length of the cells
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)
    parameter_range_quad_order = [10]  # , 20, 30, 40, 50]
    parameter_range_green_center_x = [0.1, -0.1, 0.05]  # [0.0, 0.01, -0.01]
    parameter_range_green_center_y = [0.05]  # [0.0, 0.01, -0.01]
    parameter_range_red_right_top = [0.5]  # [0.4, 0.45, 0.35]
    parameter_range_red_right_bottom = [-0.5]  # [-0.4, -0.45, -0.35]
    parameter_range_red_left_top = [0.3]  # [0.4, 0.45, 0.35]
    parameter_range_red_left_bottom = [-0.3]  # [-0.4, -0.45, -0.35]
    parameter_range_horizontal_left = [-0.5]  # [-0.61, -0.6, -0.59]
    parameter_range_horizontal_right = [0.62]  # [0.61, 0.6, 0.59]

    if load_from_npz:
        design_params, design_param_names = load_hohlraum_samples_from_npz(
            "sampling/pilot-study-samples-hohlraum-05-29-24.npz"
        )
    else:
        design_params, design_param_names = create_hohlraum_samples_from_param_range(
            parameter_range_n_cell,
            parameter_range_quad_order,
            parameter_range_green_center_x,
            parameter_range_green_center_y,
            parameter_range_red_right_top,
            parameter_range_red_right_bottom,
            parameter_range_red_left_top,
            parameter_range_red_left_bottom,
            parameter_range_horizontal_left,
            parameter_range_horizontal_right,
        )

    if hpc_operation:
        print("==== Execute HPC version ====")
        directory = "./benchmarks/hohlraum/slurm_scripts/"
        user = read_username_from_config("./slurm_config.txt")

        delete_slurm_scripts(directory)  # delete existing slurm files for hohlraum
        call_models(
            design_params, hpc_operation_count=1, singularity_hpc=singularity_hpc
        )
        wait_for_slurm_jobs(user=user, sleep_interval=10)

        if user:
            print("Executing slurm scripts with user " + user)
            execute_slurm_scripts(directory, user)
            wait_for_slurm_jobs(user=user, sleep_interval=10)
        else:
            print("Username could not be read from slurm config file.")
        qois = call_models(design_params, hpc_operation_count=2)
    else:
        qois = call_models(design_params, hpc_operation_count=0)

    print("design parameter matrix")
    print(design_param_names)
    print(design_params)
    print("quantities of interest:")
    print(get_qois_col_names())
    print(qois)
    np.savez(
        "benchmarks/hohlraum/sn_study_hohlraum.npz",
        qois=qois,
        design_params=design_params,
        qoi_column_names=get_qois_col_names(),
        design_param_column_names=design_param_names,
    )

    print("======== Finished ===========")
    return 0


def call_models(design_params, hpc_operation_count, singularity_hpc=True):
    qois = []
    for column in design_params.T:
        input = column.tolist()
        input.append(hpc_operation_count)
        input.append(singularity_hpc)
        res = model([input])
        qois.append(res[0])

    return np.array(qois)


def model(parameters):
    # non umbridge call
    left_red_top = parameters[0][0]
    left_red_bottom = parameters[0][1]
    right_red_top = parameters[0][2]
    right_red_bottom = parameters[0][3]

    horizontal_left_red = parameters[0][4]
    horizontal_right_red = parameters[0][5]

    x_green = parameters[0][6]
    y_green = parameters[0][7]

    n_cells = parameters[0][8]
    quad_order = int(parameters[0][9])
    hpc_operation = parameters[0][10]
    singularity_hpc = parameters[0][11]
    subfolder = "benchmarks/hohlraum/"
    base_config_file = subfolder + "hohlraum.cfg"

    # Step 1: Read the base config file
    kitrt_parameters = read_config_file(base_config_file)
    hohlraum_file_new = update_var_hohlraum_mesh_file(
        hpc_mode=(hpc_operation == 1),
        filepath=subfolder + "mesh/",
        cl_fine=n_cells,
        capsule_x=x_green,
        capsule_y=y_green,
        upper_left_red=left_red_top,
        lower_left_red=left_red_bottom,
        upper_right_red=right_red_top,
        lower_right_red=right_red_bottom,
        horizontal_left_red=horizontal_left_red,
        horizontal_right_red=horizontal_right_red,
    )
    unique_name = f"hohlraum_variable_cl{n_cells}_q{quad_order}_ulr{left_red_top}_llr{left_red_bottom}_urr{right_red_top}_lrr{right_red_bottom}_hlr{horizontal_left_red}_hrr{horizontal_right_red}_cx{x_green}_cy{y_green}"

    if hpc_operation == 2:
        if os.path.exists(
            subfolder + "mesh/" + "hohlraum_variable_backup" + unique_name + ".geo"
        ):
            os.remove(
                subfolder + "mesh/" + "hohlraum_variable_backup" + unique_name + ".geo"
            )  # remove backup geo files

    # Step 2: Update kitrt_parameters for the current value of LATTICE_DSGN_ABSORPTION_BLUE
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="QUAD_ORDER", new_value=quad_order
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="MESH_FILE", new_value="mesh/" + hohlraum_file_new
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_CENTER_X", new_value=x_green
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_CENTER_Y", new_value=y_green
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_RED_RIGHT_TOP", new_value=right_red_top
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_RED_RIGHT_BOTTOM", new_value=right_red_bottom
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_RED_LEFT_TOP", new_value=left_red_top
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_RED_LEFT_BOTTOM", new_value=left_red_bottom
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_BORDER_RED_RIGHT", new_value=horizontal_right_red
    )
    kitrt_parameters = update_parameter(
        kitrt_parameters, key="POS_BORDER_RED_LEFT", new_value=horizontal_left_red
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
            "benchmarks/hohlraum/slurm_scripts/",
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
            integrated_probe_moments = get_integrated_hohlraum_probe_moments(
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
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 2 u_0"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 2 u_1"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 2 u_2"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 3 u_0"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 3 u_1"][i])
                )
            for i in range(N):
                quantities_of_interest.append(
                    float(integrated_probe_moments["Probe 3 u_2"][i])
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
            "Probe2_u0_N1",
            "Probe2_u0_N2",
            "Probe2_u0_N3",
            "Probe2_u0_N4",
            "Probe2_u0_N5",
            "Probe2_u0_N6",
            "Probe2_u0_N7",
            "Probe2_u0_N8",
            "Probe2_u0_N9",
            "Probe2_u0_N10",
            "Probe2_u1_N1",
            "Probe2_u1_N2",
            "Probe2_u1_N3",
            "Probe2_u1_N4",
            "Probe2_u1_N5",
            "Probe2_u1_N6",
            "Probe2_u1_N7",
            "Probe2_u1_N8",
            "Probe2_u1_N9",
            "Probe2_u1_N10",
            "Probe2_u2_N1",
            "Probe2_u2_N2",
            "Probe2_u2_N3",
            "Probe2_u2_N4",
            "Probe2_u2_N5",
            "Probe2_u2_N6",
            "Probe2_u2_N7",
            "Probe2_u2_N8",
            "Probe2_u2_N9",
            "Probe2_u2_N10",
            "Probe3_u0_N1",
            "Probe3_u0_N2",
            "Probe3_u0_N3",
            "Probe3_u0_N4",
            "Probe3_u0_N5",
            "Probe3_u0_N6",
            "Probe3_u0_N7",
            "Probe3_u0_N8",
            "Probe3_u0_N9",
            "Probe3_u0_N10",
            "Probe3_u1_N1",
            "Probe3_u1_N2",
            "Probe3_u1_N3",
            "Probe3_u1_N4",
            "Probe3_u1_N5",
            "Probe3_u1_N6",
            "Probe3_u1_N7",
            "Probe3_u1_N8",
            "Probe3_u1_N9",
            "Probe3_u1_N10",
            "Probe3_u2_N1",
            "Probe3_u2_N2",
            "Probe3_u2_N3",
            "Probe3_u2_N4",
            "Probe3_u2_N5",
            "Probe3_u2_N6",
            "Probe3_u2_N7",
            "Probe3_u2_N8",
            "Probe3_u2_N9",
            "Probe3_u2_N10",
        ]
    )


if __name__ == "__main__":
    main()
