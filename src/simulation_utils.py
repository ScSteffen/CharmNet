import subprocess

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
    singularity_command = [ "singularity", "exec", "singularity/kit_rt.sif", "./KiT-RT/KiT-RT", config_file]

    # Command to run the C++ executable with the provided config file

    try:
        # Run the C++ executable
        subprocess.run(singularity_command, check=True)
        print("C++ simulation completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running C++ simulation. Return code: {e.returncode}")
        # You can handle the error as needed
