import csv
from datetime import datetime
import pandas as pd
import numpy as np
import os
import re


def read_csv_file(csv_out_file):
    data_dict = {}

    if not os.path.exists(csv_out_file):
        raise FileNotFoundError(f"File {csv_out_file} not found")
    print(csv_out_file)
    with open(csv_out_file, "r") as file:
        csv_reader = csv.reader(file)

        try:  # Read the header row
            header_row = next(csv_reader)
        except StopIteration:
            raise ValueError(f"File {csv_out_file} is empty")

        # Extract timestamps from the title and last row
        title_timestamp_str = header_row[0].strip()
        title_timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
        title_timestamp = datetime.strptime(title_timestamp_str, title_timestamp_format)

        last_row_timestamp = None

        # Initialize the data_dict with empty lists for each column
        for column_name in header_row[1:]:
            data_dict[column_name] = None

        # Read the rest of the rows and update the values in data_dict
        for row in csv_reader:
            last_row_timestamp_str = row[0].strip()
            last_row_timestamp = datetime.strptime(
                last_row_timestamp_str, title_timestamp_format
            )
            for column_name, value in zip(header_row[1:], row[1:]):
                data_dict[column_name] = value

    # Calculate the difference in timestamps
    if last_row_timestamp is not None:
        simulation_time_difference = last_row_timestamp - title_timestamp
        data_dict["Simulation time"] = simulation_time_difference.total_seconds()

    return data_dict


def get_integrated_hohraum_probe_moments(unique_name, t_final, N=10):
    dt = extract_time_step(unique_name)

    csv_out_file = unique_name + ".csv"
    df = pd.read_csv(csv_out_file)
    # Specify the column names to be averaged
    column_names = [
        "Probe 0 u_0",
        "Probe 0 u_1",
        "Probe 0 u_2",
        "Probe 1 u_0",
        "Probe 1 u_1",
        "Probe 1 u_2",
        "Probe 2 u_0",
        "Probe 2 u_1",
        "Probe 2 u_2",
        "Probe 3 u_0",
        "Probe 3 u_1",
        "Probe 3 u_2",
    ]

    # Define the number of intervals
    # N = 10  # Replace with the desired number of intervals

    # Compute the time averages
    averages = time_average(df, column_names, N, t_final, dt)
    # print(averages)
    return averages


def time_average(df, column_names, N, t_final, dt):
    averages = {}
    for col in column_names:
        data = df[col].values
        interval_length = len(data) // N

        interval_means = [
            np.sum(data[i * interval_length : (i + 1) * interval_length]) * dt
            for i in range(N - 1)
        ]
        tmp = np.sum(data[N - 2 * interval_length : -2]) * dt + data[-1] * dt
        interval_means.append(tmp)
        averages[col] = interval_means

    return averages


def extract_time_step(log_file_path):
    search_string = "Corresponding maximal time-step:"
    float_value = None

    with open(log_file_path, "r") as log_file:
        for line in log_file:
            if search_string in line:
                # Use regex to find the float value after the search string
                match = re.search(
                    rf"{re.escape(search_string)}\s*([0-9]*\.?[0-9]+)", line
                )
                if match:
                    float_value = float(match.group(1))
                    break  # Assuming there's only one such line in the log file

    if float_value is not None:
        print(f"Extracted float value: {float_value}")
    else:
        print("No matching line found.")

    return float_value
