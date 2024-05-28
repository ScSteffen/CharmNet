import umbridge
from src.config_utils import read_username_from_config
from src.simulation_utils import execute_slurm_scripts

url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


def main():
    hpc_operation = True  # Flag when using HPC cluster

    # Define parameter ranges
    parameter_range_n_cell = [0.03]  # characteristic length of the cells
    # GAUSS LEGENDRE  2D quadrature order (MUST BE EVEN)
    parameter_range_quad_order = [10]  # , 20, 30, 40, 50]
    parameter_range_green_center_x = [0.1]  # [0.0, 0.01, -0.01]
    parameter_range_green_center_y = [0.05]  # [0.0, 0.01, -0.01]
    parameter_range_red_right_top = [0.5]  # [0.4, 0.45, 0.35]
    parameter_range_red_right_bottom = [-0.5]  # [-0.4, -0.45, -0.35]
    parameter_range_red_left_top = [0.3]  # [0.4, 0.45, 0.35]
    parameter_range_red_left_bottom = [-0.3]  # [-0.4, -0.45, -0.35]
    parameter_range_horizontal_left = [-0.5]  # [-0.61, -0.6, -0.59]
    parameter_range_horizontal_right = [0.62]  # [0.61, 0.6, 0.59]

    design_params = create_dsgn_parameter_matrix(
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
        call_models(
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
            hpc_operation_count=1,
        )
        directory = "./benchmarks/hohlraum/slurm_scripts/"

        user = read_username_from_config("./slurm_config.txt")
        if user:
            execute_slurm_scripts(directory, user)
        else:
            print("Username could not be read from config file.")

        qois = call_models(
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
            hpc_operation_count=2,
        )
    else:
        qois = call_models(
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
            hpc_operation_count=0,
        )

    print("design parameter matrix")
    print(design_params)
    print(
        "quantities of interest: [ Wall_time_[s],  Cumulated_absorption_center,Cumulated_absorption_vertical_wall,Cumulated_absorption_horizontal_wall,Var. absorption green,Probe 0 u_0 [N=1:10],Probe 0 u_1 [N=1:10],Probe 0 u_2 [N=1:10],Probe 1 u_0 [N=1:10],Probe 1 u_1 [N=1:10],Probe 1 u_2 [N=1:10], Probe 3 u_0 [N=1:10],Probe 3 u_1 [N=1:10],Probe 3 u_2 [N=1:10],Probe 4 u_0 [N=1:10],Probe 4 u_1 [N=1:10],Probe 4 u_2 [N=1:10]]"
    )
    print(qois)
    print("======== Finished ===========")
    return 0


def call_models(
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
    hpc_operation_count=1,
):
    qois = []

    for n_cell in parameter_range_n_cell:
        for n_quad in parameter_range_quad_order:
            for x_green in parameter_range_green_center_x:
                for y_green in parameter_range_green_center_y:
                    for right_red_top in parameter_range_red_right_top:
                        for right_red_bottom in parameter_range_red_right_bottom:
                            for left_red_top in parameter_range_red_left_top:
                                for left_red_bottom in parameter_range_red_left_bottom:
                                    for (
                                        horizontal_left_red
                                    ) in parameter_range_horizontal_left:
                                        for (
                                            horizontal_right_red
                                        ) in parameter_range_horizontal_right:
                                            res = model(
                                                [
                                                    [
                                                        n_cell,
                                                        n_quad,
                                                        x_green,
                                                        y_green,
                                                        right_red_top,
                                                        right_red_bottom,
                                                        left_red_top,
                                                        left_red_bottom,
                                                        horizontal_left_red,
                                                        horizontal_right_red,
                                                        hpc_operation_count,
                                                    ]
                                                ]
                                            )
                                            qois.append(res[0])
    return qois


def create_dsgn_parameter_matrix(
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
):
    design_params = []
    for n_cell in parameter_range_n_cell:
        for n_quad in parameter_range_quad_order:
            for x_green in parameter_range_green_center_x:
                for y_green in parameter_range_green_center_y:
                    for right_red_top in parameter_range_red_right_top:
                        for right_red_bottom in parameter_range_red_right_bottom:
                            for left_red_top in parameter_range_red_left_top:
                                for left_red_bottom in parameter_range_red_left_bottom:
                                    for (
                                        horizontal_left_red
                                    ) in parameter_range_horizontal_left:
                                        for (
                                            horizontal_right_red
                                        ) in parameter_range_horizontal_right:
                                            design_params.append(
                                                [
                                                    n_cell,
                                                    n_quad,
                                                    x_green,
                                                    y_green,
                                                    right_red_top,
                                                    right_red_bottom,
                                                    left_red_top,
                                                    left_red_bottom,
                                                    horizontal_left_red,
                                                    horizontal_right_red,
                                                ]
                                            )
    return design_params


if __name__ == "__main__":
    main()
