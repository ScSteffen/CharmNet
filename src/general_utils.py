import subprocess


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
