import umbridge
import numpy as np

from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts, wait_for_slurm_jobs
from src.general_utils import (
    create_lattice_samples_from_param_range,
    load_hohlraum_samples_from_npz,
    delete_slurm_scripts,
)

url = "http://localhost:4243"
model = umbridge.HTTPModel(url, "forward")


def main():
    hpc_operation = False  # Flag when using HPC cluster
    load_from_npz = False

    # Define parameter ranges
    # characteristic length of the cells
    parameter_range_n_cell = [
        0.01,
    ]
    #    0.0075,
    #    0.005,
    #    0.0025,
    #    0.001,
    # ]
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)

    parameter_range_quad_order = [
        10,
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
        design_params = load_hohlraum_samples_from_npz(
            "sampling/pilot-study-samples-hohlraum-05-29-24.npz"
        )
    else:
        design_params = create_lattice_samples_from_param_range(
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
    np.savez("sn_study_half_lattice.npz", array=qois)

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


if __name__ == "__main__":
    main()
