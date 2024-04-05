import umbridge
url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix

parameter_range_n_cell =[0.02,0.01, 0.005, 0.0025, 0.00125, 0.00075] #[10, 20, 40] # 10 means 10^2 cells per lattice square. Cell size reduces with geometric progression (1.05) towards square boundary
parameter_range_quad_order =[10, 20, 30, 40, 50]     # GAUSS LEGENDRE quadrature

# Open the file for writing

design_params = []
qois = []

with open("slurm_scripts/slurm_run_all_sym_hohlraum.sh", "w") as file:
    for n_cell in parameter_range_n_cell:
        for n_quad in parameter_range_quad_order:
            design_params.append([n_cell, n_quad])
            res = model([[n_cell, n_quad]])
            qois.append(res[0])
            file.write(f'sbatch slurm_scripts/slurm_sym_hohlraum_n{n_cell}_q{n_quad}.sh\n')

with open("slurm_scripts/run_all_sym_hohlraum.sh", "w") as file:
     for n_cell in parameter_range_n_cell:
        for n_quad in parameter_range_quad_order:
            file.write(f'../../build/KiT-RT sym_hohlraum_n{n_cell}_q{n_quad}.cfg\n')

# run model and print output
print("design parameter matrix")
print(design_params)
print("quantities of interest")
print(qois)
print("======== Finished ===========")