import umbridge
url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix
# design parameter vector is 2d (scatter_white, absorption_blue)

parameter_range_abs_blue = [0, 5, 10, 50, 100]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE
parameter_range_scatter_white = [0, 0.5, 1, 5, 10]  # Prescribed range for LATTICE_DSGN_ABSORPTION_BLUE

design_params = []
qois = []

for scatter_white_value in parameter_range_scatter_white:
        for absorption_blue_value in parameter_range_abs_blue:
            design_params.append([scatter_white_value,absorption_blue_value])
            res = model([[scatter_white_value,absorption_blue_value]])
            qois.append(res[0])
# run model and print output
print("design parameter matrix")
print(design_params)
print("quantities of interest")
print(qois)
print("======== Finished ===========")