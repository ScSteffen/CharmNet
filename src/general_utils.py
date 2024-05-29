import subprocess
import numpy as np


def replace_next_line(input_file, custom_line, output_file):
    with open(input_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "### command below":
            lines[i + 1] = custom_line + "\n"
            break

    with open(output_file, "w") as f:
        f.writelines(lines)


def get_user_job_count(user):
    """
    Get the number of jobs in the SLURM queue for the specified user.
    """
    try:
        # Run the 'squeue' command and filter for the current user
        result = subprocess.run(
            ["squeue", "-u", user],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        # Get the number of lines in the output, excluding the header line
        job_count = len(result.stdout.strip().split("\n")) - 1
        return job_count
    except Exception as e:
        print(f"Error checking job queue: {e}")
        return 0


def load_hohlraum_samples_from_npz(npz_file):
    samples = np.load(npz_file)["samples"]
    samples[0, :] = 0.4 + (0.2 - samples[0, :])  # tl
    samples[1, :] = -0.4 - (0.2 - samples[1, :])  # bl
    samples[2, :] = 0.4 + (0.2 - samples[2, :])  # tr
    samples[3, :] = -0.4 - (0.2 - samples[3, :])  # br
    samples[4, :] = -0.6 + (0.05 - samples[4, :])  # wl
    samples[5, :] = +0.6 - (0.05 - samples[5, :])  # wr

    cl = samples[6, :].reshape(1, -1)
    n_quad = samples[7, :].reshape(1, -1)
    samples[6, :] = np.zeros(shape=samples[0, :].shape)  # x deviation from center
    samples[7, :] = np.zeros(shape=samples[0, :].shape)  # y deviation from center

    samples_full = np.concatenate((samples, cl, n_quad), axis=0)

    return samples_full


def create_hohlraum_samples_from_param_range(
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
                            for x_green in parameter_range_green_center_x:
                                for y_green in parameter_range_green_center_y:
                                    for n_cell in parameter_range_n_cell:
                                        for n_quad in parameter_range_quad_order:
                                            design_params.append(
                                                [
                                                    left_red_top,
                                                    left_red_bottom,
                                                    right_red_top,
                                                    right_red_bottom,
                                                    horizontal_left_red,
                                                    horizontal_right_red,
                                                    x_green,
                                                    y_green,
                                                    n_cell,
                                                    n_quad,
                                                ]
                                            )
    return np.array(design_params)
