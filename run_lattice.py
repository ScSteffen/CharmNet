import umbridge
import numpy as np
url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix
# design parameter vector is 2d (scatter_white, absorption_blue)

parameter_range_n_cell =[30]#,30,40,50, 60, 80, 160] #[10, 20, 40] # 10 means 10^2 cells per lattice square. Cell size reduces with geometric progression (1.05) towards square boundary
parameter_range_quad_order =[10]# 20 , 30 ,40 ,50 ]  # Gauss Legendre  quadrature
parameter_range_abs_blue = [10, 20]#, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
parameter_range_scatter_white = [ 1, 2, 5]#, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

design_params = []
qois = []



filename = "benchmarks/lattice/pilot-study-samples-lattice-04-15-24.npz"
samples = np.load(filename)["samples"]

#with open("slurm_scripts/slurm_run_all_lattice.sh", "w") as file:
#for scatter_white_value in parameter_range_scatter_white:
#    for absorption_blue_value in parameter_range_abs_blue:
#        for n_cell in parameter_range_n_cell:
#            for n_quad in parameter_range_quad_order:
for i in range(samples.shape[1]):
    n_cell, n_quad, scatter_white_value, absorption_blue_value = samples[:,i]
    design_params.append([int(n_cell),int(n_quad), scatter_white_value,absorption_blue_value])
    res = model([[n_cell, n_quad, scatter_white_value,absorption_blue_value]])
    qois.append(res[0])
                    #file.write(f'sbatch slurm_scripts/slurm_lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cell}_q{n_quad}.sh\n')

#with open("slurm_scripts/run_all_lattice.sh", "w") as file:
#    for scatter_white_value in parameter_range_scatter_white:
#        for absorption_blue_value in parameter_range_abs_blue:
#            for n_cell in parameter_range_n_cell:
#                for n_quad in parameter_range_quad_order:
#                    file.write(f'../../build/KiT-RT lattice_abs{absorption_blue_value}_scatter{scatter_white_value}_n{n_cell}_q{n_quad}.cfg\n')


# run model and print output
print("design parameter matrix: [grid_param, quad_order, scatter value white, absorption value blue]")
print(design_params)
np.savez('design parameters', samples=design_params)

print("quantities of interest: [Cur_outflow, Total_outflow, Max_outflow, Cur_absorption, Total_absorption, Max_absorption, Wall_time_[s]]")
print(qois)
np.savez('qois', samples=qois)

print("======== Finished ===========")