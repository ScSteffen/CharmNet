import subprocess
import os
import time
from src.general_utils import get_user_job_count


def run_cpp_simulation(config_file):
    # Path to the C++ executable
    cpp_executable_path = "KiT-RT/KiT-RT"

    # Command to run the C++ executable with the provided config file
    command = [cpp_executable_path, config_file]

    print(command)
    try:
        # Run the C++ executable
        subprocess.run(command, check=True)
        print("C++ simulation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running C++ simulation. Return code: {e.returncode}")
        # You can handle the error as needed

        # You can handle the error as needed


def run_cpp_simulation_containerized(config_file):
    # Path to the C++ executable
    singularity_command = [
        "singularity",
        "exec",
        "KiT-RT/tools/singularity/kit_rt.sif",
        "./KiT-RT/build_singularity/KiT-RT",
        config_file,
    ]

    # Command to run the C++ executable with the provided config file

    try:
        # Run the C++ executable
        subprocess.run(singularity_command, check=True)
        print("C++ simulation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running C++ simulation. Return code: {e.returncode}")
        # You can handle the error as needed


def execute_slurm_scripts(directory, user, max_jobs=10, sleep_time=30):
    """
    Execute all SLURM scripts in the specified directory.
    If the number of jobs in the queue for the user is 10 or more, wait and sleep for 30 seconds.
    """
    # Get the list of SLURM scripts in the directory
    slurm_scripts = [f for f in os.listdir(directory) if f.endswith(".slurm")]

    for script in slurm_scripts:
        script_path = os.path.join(directory, script)

        # Check the number of jobs in the queue for the user
        while get_user_job_count(user) >= max_jobs:
            print(
                f"User has {max_jobs} or more jobs in the queue. Waiting for {sleep_time} seconds..."
            )
            time.sleep(sleep_time)

        # Execute the SLURM script
        try:
            result = subprocess.run(
                ["sbatch", script_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            if result.returncode == 0:
                print(f"Successfully submitted {script}")
            else:
                print(f"Failed to submit {script}: {result.stderr}")
        except Exception as e:
            print(f"Error submitting {script}: {e}")
