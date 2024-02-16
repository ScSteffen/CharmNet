import umbridge
url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix
# design parameter vector is 2d (scatter_white, absorption_blue)

parameter_range_n_cell =[10,20,30,40] #[10, 20, 40] # 10 means 10^2 cells per lattice square. Cell size reduces with geometric progression (1.05) towards square boundary
parameter_range_quad_order =[1,2,3]     # LDFESA quadrature
parameter_range_abs_blue = [5] #[0, 5, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
parameter_range_scatter_white =[ 1] # [0, 0.5, 1, 5, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

design_params = []
qois = []

for scatter_white_value in parameter_range_scatter_white:
        for absorption_blue_value in parameter_range_abs_blue:
            for n_cell in parameter_range_n_cell:
                design_params.append([n_cell, scatter_white_value,absorption_blue_value])
                res = model([[n_cell, scatter_white_value,absorption_blue_value]])
                qois.append(res[0])
# run model and print output
print("design parameter matrix")
print(design_params)
print("quantities of interest")
print(qois)
print("======== Finished ===========")