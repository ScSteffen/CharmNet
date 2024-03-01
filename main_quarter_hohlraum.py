import umbridge
url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix

parameter_range_n_cell =[0.02,0.01, 0.005, 0.0025, 0.00125, 0.00075] #[10, 20, 40] # 10 means 10^2 cells per lattice square. Cell size reduces with geometric progression (1.05) towards square boundary
parameter_range_quad_order =[10, 20, 30, 40, 50]     # GAUSS LEGENDRE quadrature

# Open the file for writing
with open("slurm_run_all.sh", "w") as file:
    # Iterate over each value for {1}
    for val_1 in parameter_range_n_cell:
        # Iterate over each value for {2}
        for val_2 in parameter_range_quad_order:
            # Write the formatted string to the file
            file.write(f'sbatch slurm_scripts/quad_hohlraum_p{val_1}_q{val_2}.sh\n')


design_params = []
qois = []


for n_cell in parameter_range_n_cell:
    for n_quad in parameter_range_quad_order:
        design_params.append([n_cell, n_quad])
        res = model([[n_cell, n_quad]])
        qois.append(res[0])
# run model and print output
print("design parameter matrix")
print(design_params)
print("quantities of interest")
print(qois)
print("======== Finished ===========")