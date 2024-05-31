import umbridge
import numpy as np

from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_hohlraum_samples_from_param_range,
    load_hohlraum_samples_from_npz,
    delete_slurm_scripts,
)

url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


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
        call_models(design_params, hpc_operation_count=1)
        wait_for_slurm_jobs(user=user, sleep_interval=10)

        if user:
            print("Executing slurm scripts with user " + user)
            execute_slurm_scripts(directory, user)
            wait_for_slurm_jobs(user=user, sleep_interval=10)
        else:
            print("Username could not be read from config file.")

        qois = call_models(design_params, hpc_operation_count=2)
    else:
        qois = call_models(design_params, hpc_operation_count=0)

    print("design parameter matrix")
    print(design_params)
    print(
        "quantities of interest: [ Wall_time_[s],  Cumulated_absorption_center,Cumulated_absorption_vertical_wall,Cumulated_absorption_horizontal_wall,Var. absorption green,Probe 0 u_0 [N=1:10],Probe 0 u_1 [N=1:10],Probe 0 u_2 [N=1:10],Probe 1 u_0 [N=1:10],Probe 1 u_1 [N=1:10],Probe 1 u_2 [N=1:10], Probe 3 u_0 [N=1:10],Probe 3 u_1 [N=1:10],Probe 3 u_2 [N=1:10],Probe 4 u_0 [N=1:10],Probe 4 u_1 [N=1:10],Probe 4 u_2 [N=1:10]]"
    )
    print(qois)
    np.savez("benchmarks/hohlraum/sn_study_hohlraum_qois.npz", array=qois)
    np.savez("benchmarks/hohlraum/ssn_study_hohlraum_params.npz", array=design_params)
    np.savez(
        "benchmarks/hohlraum/ssn_study_hohlraum_params_col_names.npz",
        array=design_param_names,
    )
    np.savez(
        "benchmarks/hohlraum/ssn_study_hohlraum_qois_col_names.npz",
        array=get_qois_col_names(),
    )

    print("======== Finished ===========")
    return 0


def call_models(
    design_params,
    hpc_operation_count,
):
    qois = []
    for column in design_params.T:
        input = column.tolist()
        input.append(hpc_operation_count)
        res = model([input])
        qois.append(res[0])

    return np.array(qois)


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
