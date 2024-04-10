import umbridge

url = "http://localhost:4242"
model = umbridge.HTTPModel(url, "forward")


# Assemble parameter matrix

parameter_range_n_cell = [
    0.05,
    0.02,
    0.01,
    # 0.005,
    # 0.0025,
    # 0.00125,
    # 0.00075,
]  # characteristic length of the cells
parameter_range_quad_order = [10, 20]  # , 30, 40, 50]  # GAUSS LEGENDRE quadrature


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
print(
    "quantities of interest: [ Wall_time_[s],  Cumulated_absorption_center,Cumulated_absorption_vertical_wall,Cumulated_absorption_horizontal_wall,Var. absorption green,Probe 0 u_0,Probe 0 u_1,Probe 0 u_2,Probe 1 u_0,Probe 1 u_1,Probe 1 u_2]"
)
print(qois)
print("======== Finished ===========")
