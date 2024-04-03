import os
import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt
import vtk
import re
from tqdm import tqdm
def read_vtk(filename):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    output = reader.GetOutput()
    cell_coords = []
    values = []
    cell_data = output.GetCellData().GetArray(0)
    for i in range(output.GetNumberOfCells()):
        cell = output.GetCell(i)
        num_points = cell.GetNumberOfPoints()
        centroid = [0.0, 0.0]
        for j in range(num_points):
            point_id = cell.GetPointId(j)
            point = output.GetPoint(point_id)
            centroid[0] += point[0]
            centroid[1] += point[1]
        centroid[0] /= num_points
        centroid[1] /= num_points
        cell_coords.append(centroid)
        values.append(cell_data.GetValue(i))
    return np.array(cell_coords), np.array(values)



def compute_l2_norm(ref_points, ref_values, points, values):
    # Interpolate values
    interpolated_values = []
    for point in tqdm(points, desc="Interpolating", unit="point"):
        # Find the closest reference cell
        distances = np.sum((ref_points - point) ** 2, axis=1)
        closest_cell_idx = np.argmin(distances)

        # Use the values of the closest reference cell to interpolate
        closest_cell_value = ref_values[closest_cell_idx]


        interpolated_values.append(closest_cell_value)

    interpolated_values = np.array(interpolated_values)

    l2_norm = np.linalg.norm(interpolated_values - values) / np.sqrt(len(values))
    return l2_norm


def extract_dx_from_filename(filename):
    match = re.search(r'n([\d.]+)', filename)
    if match:
        return float(match.group(1))
    return None


def main(vtk_path, ref_vtk_file):
    vtk_files = [f for f in os.listdir(vtk_path) if f.endswith('.vtk')]
    ref_points, ref_values = read_vtk(os.path.join(vtk_path, ref_vtk_file))

    results = []
    for vtk_file in vtk_files:
        if vtk_file == ref_vtk_file:
            continue

        dx = extract_dx_from_filename(vtk_file)
        if dx is None:
            print(f"Could not extract dx from filename: {vtk_file}")
            continue

        points, values = read_vtk(os.path.join(vtk_path, vtk_file))
        l2_norm = compute_l2_norm(ref_points, ref_values, points, values)
        results.append({'dx': dx, 'L2 Norm': l2_norm})

    results_df = pd.DataFrame(results)
    sns.lineplot(x='dx', y='L2 Norm', data=results_df)
    plt.xlabel('dx')
    plt.ylabel('L2 Norm')
    plt.title('Convergence Plot')
    plt.show()

if __name__ == '__main__':
    vtk_path = "benchmarks/half_lattice_homogeneous/results/q10_vtk/"
    ref_vtk_file = 'lattice_abs10_scatter1_n0.0025_q10.vtk'
    main(vtk_path, ref_vtk_file)