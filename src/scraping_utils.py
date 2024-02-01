import csv
from datetime import datetime

def read_csv_file(csv_out_file):
    data_dict = {}

    with open(csv_out_file, 'r') as file:
        csv_reader = csv.reader(file)

        # Read the header row
        header_row = next(csv_reader)

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
            last_row_timestamp = datetime.strptime(last_row_timestamp_str, title_timestamp_format)
            for column_name, value in zip(header_row[1:], row[1:]):
                data_dict[column_name] = value

    # Calculate the difference in timestamps
    if last_row_timestamp is not None:
        simulation_time_difference = last_row_timestamp - title_timestamp
        data_dict['Simulation time'] = simulation_time_difference.total_seconds()

    return data_dict
