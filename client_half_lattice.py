import umbridge

url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix
# design parameter vector is 2d (scatter_white, absorption_blue)

parameter_range_n_cell = [
    0.01,
    0.0075,
    0.005,
    0.0025,
    0.001,
]  # [10, 20, 40] # 10 means 10^2 cells per lattice square. Cell size reduces with geometric progression (1.05) towards square boundary
parameter_range_quad_order = [10, 20, 30, 40, 50, 60]  # GAUSS LEGENDRE 2D quadrature
parameter_range_abs_blue = [
    10
]  # [0, 5, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
parameter_range_scatter_white = [
    1
]  # [0, 0.5, 1, 5, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

design_params = []
qois = []

filename = "benchmarks/lattice/pilot-study-samples-lattice-04-15-24.npz"
samples = np.load(filename)["samples"]

# with open("slurm_scripts/slurm_run_all_half_lattice.sh", "w") as file:
for scatter_white_value in parameter_range_scatter_white:
    for absorption_blue_value in parameter_range_abs_blue:
        for n_cell in parameter_range_n_cell:
            for n_quad in parameter_range_quad_order:
                # for i in range(samples.shape[1]):
                #    absorption_blue_value, scatter_white_value, n_cell, n_quad = samples[:, i]
                #    print(
                #        "Running configuration: [ n_cell, n_quad, scatter_white_value, absorption_blue_value] "
                #    )
                #    n_grid = 1 / (2.5 * n_cell)
                n_grid = n_cell
                print([n_grid, int(n_quad), scatter_white_value, absorption_blue_value])

                design_params.append(
                    [n_grid, n_quad, scatter_white_value, absorption_blue_value]
                )
                res = model(
                    [[n_grid, n_quad, scatter_white_value, absorption_blue_value]]
                )
                qois.append(res[0])
    # file.write(f'sbatch slurm_scripts/slurm_half_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_p{n_cell}_q{n_quad}.sh\n')

# run model and print output
print(
    "design parameter matrix: [grid_param, quad_order, scatter value white, absorption value blue]"
)
print(design_params)
np.savez("design parameters", samples=design_params)

print(
    "quantities of interest: [Cur_outflow, Total_outflow, Max_outflow, Cur_absorption, Total_absorption, Max_absorption, Wall_time_[s]]"
)
print(qois)
np.savez("qois", samples=qois)
