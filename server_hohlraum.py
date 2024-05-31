import umbridge
import time
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
from src.scraping_utils import read_csv_file, get_integrated_hohraum_probe_moments
from src.simulation_utils import run_cpp_simulation_containerized


class KiTRTModelHohlraum(umbridge.Model):

    def __init__(self):
        super().__init__("forward")

    def get_input_sizes(self, config):
        return [11]

    def get_output_sizes(self, config):
        return [125]

    def __call__(self, parameters, config):

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
        if hpc_operation == 2:
            unique_name = f"hohlraum_variable_cl{n_cells}_q{quad_order}_ulr{left_red_top}_llr{left_red_bottom}_urr{right_red_top}_lrr{right_red_bottom}_hlr{horizontal_left_red}_hrr{horizontal_right_red}_cx{x_green}_cy{y_green}"
            if os.path.exists(subfolder + "mesh/" + "hohlraum_variable_backup " + unique_name + ".geo"):
                os.remove(
                    subfolder + "mesh/" + "hohlraum_variable_backup " + unique_name + ".geo"
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
        log_file_cur = f"hohlraum_variable_cl{n_cells}_q{quad_order}_ulr{left_red_top}_llr{left_red_bottom}_urr{right_red_top}_lrr{right_red_bottom}_hlr{horizontal_left_red}_hrr{horizontal_right_red}_cx{x_green}_cy{y_green}"
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="LOG_FILE", new_value=log_file_cur
        )
        if hpc_operation < 2:
            remove_files(subfolder + kitrt_parameters["LOG_DIR"] + "/" + log_file_cur)
        kitrt_parameters = update_parameter(
            kitrt_parameters, key="OUTPUT_FILE", new_value=log_file_cur
        )
        if hpc_operation < 2:
            remove_files(
                subfolder + kitrt_parameters["OUTPUT_DIR"] + "/" + log_file_cur + ".vtk"
            )

        # Step 4: Write a new config file, named corresponding to LATTICE_DSGN_ABSORPTION_BLUE
        unique_name = f"hohlraum_variable_cl{n_cells}_q{quad_order}_ulr{left_red_top}_llr{left_red_bottom}_urr{right_red_top}_lrr{right_red_bottom}_hlr{horizontal_left_red}_hrr{horizontal_right_red}_cx{x_green}_cy{y_green}"
        generated_cfg_file = subfolder + "cfg_files/" + unique_name + ".cfg"

        write_config_file(
            parameters=kitrt_parameters, output_file_path=generated_cfg_file
        )
        if hpc_operation == 0:
            # Step 5: Run the C++ simulation
            run_cpp_simulation_containerized(generated_cfg_file)
        elif hpc_operation == 1:
            # Write slurm file
            write_slurm_file(
                "benchmarks/hohlraum/slurm_scripts/",  unique_name, subfolder
            )

        if hpc_operation == 0 or hpc_operation == 2:
            # Step 6: Read the log file
            log_filename = generate_log_filename(kitrt_parameters)
            if log_filename:
                # Step 7: Read and convert the data from the CSV log file to a DataFrame
                log_data = read_csv_file(subfolder + log_filename + ".csv")
                N = 10
                integrated_probe_moments = get_integrated_hohraum_probe_moments(
                    subfolder + log_filename + ".csv", N=N
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

    def supports_evaluate(self):
        return True

    def gradient(self, out_wrt, in_wrt, kitrt_parameters, sens, config):
        return 0

    def supports_gradient(self):
        return True


kitrtmodel = KiTRTModelHohlraum()

umbridge.serve_models([kitrtmodel], 4242)
