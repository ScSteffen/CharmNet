# CharmKiT
CharmKiT is a enchmarking suite for the CharmNet project using the [UM-Bridge UQ suite](https://um-bridge-benchmarks.readthedocs.io/en/docs/) and the [KiT-RT PDE simulator](https://kit-rt.readthedocs.io/en/develop/index.html). 


## Installation

Preliminaries: 

1. Install [singularity](https://docs.sylabs.io/guides/latest/user-guide/quick_start.html) on your system. You can install it anywhere on your computer. 


2. Create a local python environment for CharmKiT and install the python requirements in a local virtual environment

    ```
    python3 -m venv ./venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2. Install [KiT-RT](https://github.com/CSMMLab/KiT-RT) as a submodule of CharmKiT on your system.

    Use the installer in the CharmKiT folder. Caution: The installer requires root privileges to build the singularity container.
    If you use a cluster without root access, build the container locally and upload it to the directory `CharmKiT/KiT-RT/tools/singularity/`.

    If you have root or sudo access, navigate to the  `CharmKiT` base directory and exectue the install script:

    ```
    sh install_KiT-RT.sh
    ```

    If you have KiT-RT already installed, and want to update it, use the update script below.
    ```
    sh update_KiT-RT.sh
    ```

## How CharmKiT works

CharmKiT uses [UM-Bridge](https://um-bridge-benchmarks.readthedocs.io/en/docs/) as a driver for easy access to the [KiT-RT](https://github.com/CSMMLab/KiT-RT) solver suite. 

In a nutshell: Each test case, i.e. Lattice, Hohlraum,..., consists of a server script and a client script.

- The client script, e.g.  `client_hohlraum.py` specifies the design parameters of the test case, e.g. mesh resolution, velocity space resolution, and problem specific quantities. It iterates over all specified parameter combinations, where it
    1. Sends an assembled design parameter combination  to the server.
    2. Waits for the server to run the simulation.
    3. Receives the quantities of interest.
    4. Outputs a table of all quantities of interest after the loop is finished.

- The server script, e.g. `server_hohlraum.py` creates a server at localhost, that waits for a configuration request from the client script. Then, it
    1. Creates a config file for KiT-RT
    2. Creates a mesh-file with the specified resolution. The mesh file for KiT-RT has `.su2` format. The output mesh files have `.vtk` format
    3. Runs the KiT-RT solver within the singularity container.
    4. Reads the quantities of interest from the KiT-RT output files, and sends them back to the client script

To run the hohlraum test case, open two (2) terminals and navigate to the CharmKiT directory. In both terminal, activate the CharmKiT local python environment

1. Start the server script:
```
    python server_hohlraum.py
```
2. Start the client script:
```
    python client_hohlraum.py
```
3. Wait for the client-server combination to iterate through the test cases that are specified in the client script. (This might take a while)

## How KiT-RT works

[KiT-RT](https://github.com/CSMMLab/KiT-RT) is a C++ based modular solver for radiation transport. It uses 1st and 2nd order finite volume schemes for space-time discretization and different Moment (PN) and Discrete Ordinates (SN) schemes for angular space. For the purpose of CharmKiT, we use the SN solver of KiT-RT. 

### How to run test cases (barebone)
You dont have to run KiT-RT directly, and can use the UM-Bridge wrapper. If you want to, here's how:

KiT-RT is configured with a configuration file, e.g. `hohlraum.cfg`, and then executed as

```
    ./path/to/kitrt/KiT-RT hohlraum.cfg
```
If you execute the `hohlraum.cfg` from the `benchmarks/hohlraum` subfolder, the command reads `../../KiT-RT/build/KiT-RT hohlraum.cfg`. Note that you need a system install of KiT-RT here.

If you want to run KiT-RT with a singularity container (recommended), the command reads

```
   singularity exec ./path/to/kitrt_singularity_container/kit_rt.sif ./path/to/kitrt_exec_folder/KiT-RT hohlraum.cfg
```
If you execute the `hohlraum.cfg` from the `benchmarks/hohlraum` subfolder, the command becomes `singularity exec ../../KiT-RT/tools/singularity/kit_rt.sif ../../KiT-RT/build_singularity/KiT-RT hohlraum.cfg`. Note that you need a singularity install of KiT-RT here.

Singularity does not require root access to your system and has the same permissions as your user.

### How to specify test-cases with config files.

The config files assemebles the solver modules, solver resolution and test case parameters. A config file may look like the one below. It allows a very fine grained access to the solver, but may be a bit much for starters. Therefore, we encapsulate this configuration process within the UM-Bridge server - client model. 

If you are still interested, a config file consists of 

- `% comment lines` which are not parsed by the solver

- parameter-value pairs `KIT_RT_PARAMETER = value`: You can find templates for all test cases in the `benchmark/` folder.


A few parameters for reduced order modeling: 

- `VOLUME_OUTPUT_FREQUENCY = n` specifies the frequency of `.vtk` file writes that output the whole flow-field. A high output frequency is very detrimental to the solver parallel performance!
- `HISTORY_OUTPUT_FREQUENCY = n` specifies the frequency of `.csv` file writes that output the scalar quantities of interest

Below is an example config file for the Hohlraum test case

```
%
% ---- File specifications ----
%
OUTPUT_DIR = result
% Output file
OUTPUT_FILE = sym_hohlraum
% Log directory
LOG_DIR =  result/logs
% Log file
LOG_FILE = sym_hohlraum_old_solver
% Mesh File
MESH_FILE = mesh/sym_hohlraum_n5.su2
%
% ---- Problem specifications ----
%
PROBLEM = SYMMETRIC_HOHLRAUM
SPATIAL_DIM = 2
TIME_FINAL =  2.6
%
% ---- Design Parameters ---
%
POS_CENTER_X = 0.0
POS_CENTER_Y = 0.0
POS_RED_RIGHT_TOP = 0.4
POS_RED_RIGHT_BOTTOM = -0.4
POS_RED_LEFT_TOP = 0.4
POS_RED_LEFT_BOTTOM = -0.4
%
N_SAMPLING_PTS_LINE_GREEN = 100
%
% ---- Solver specifications ----
%
% Solver type
HPC_SOLVER = YES
SOLVER = SN_SOLVER
% CFL number
CFL_NUMBER = 0.5
% Space Integration order
RECONS_ORDER =1
% Time integration order
TIME_INTEGRATION_ORDER = 1
%
% ---- Boundary Conditions ----
%
BC_NEUMANN = ( inflow, void )
%
% ----- Quadrature Specification ---
%
QUAD_TYPE = GAUSS_LEGENDRE_TENSORIZED_2D
QUAD_ORDER = 10
%
% ----- Output ----
%
VOLUME_OUTPUT = (MINIMAL)
VOLUME_OUTPUT_FREQUENCY = 0
SCREEN_OUTPUT = ( ITER,  WALL_TIME, MASS,   RMS_FLUX, VTK_OUTPUT, CSV_OUTPUT, CUR_OUTFLOW, TOTAL_OUTFLOW, MAX_OUTFLOW, TOTAL_PARTICLE_ABSORPTION_CENTER, TOTAL_PARTICLE_ABSORPTION_VERTICAL, TOTAL_PARTICLE_ABSORPTION_HORIZONTAL, PROBE_MOMENT_TIME_TRACE, VAR_ABSORPTION_GREEN)
SCREEN_OUTPUT_FREQUENCY = 20
HISTORY_OUTPUT =  ( ITER,  WALL_TIME, MASS,   RMS_FLUX, VTK_OUTPUT, CSV_OUTPUT, CUR_OUTFLOW, TOTAL_OUTFLOW, MAX_OUTFLOW, TOTAL_PARTICLE_ABSORPTION_CENTER, TOTAL_PARTICLE_ABSORPTION_VERTICAL, TOTAL_PARTICLE_ABSORPTION_HORIZONTAL, PROBE_MOMENT_TIME_TRACE, VAR_ABSORPTION_GREEN)
HISTORY_OUTPUT_FREQUENCY = 1
```

### What are the outputs of KiT-RT?

In the specified output directories, see config option `LOG_DIR` and `OUTPUT_DIR`,  KiT-RT saves `.csv` log files that contain the quantities of interest for every time-step, and `.vtk` mesh files, that contain the mesh information with the degrees of freedom in each grid cell. For the CharmKiT experiments, the scalar flux is the only degree of freedom in the output mesh. 

The `.vtk` outputs can be postprocessed with [Paraview](https://www.paraview.org/) and the [VTK Python package](https://pypi.org/project/vtk/), both open access frameworks. 
### Why singularity containers for KiT-RT?

KiT-RT has a few dependencies, e.g. VTK, Tensorflow, ... that are non-trivial (or at least annoying) to install on a system. We encapsule everything in a singularity container to keep your system clean. 

# Test case descriptions

## Homogeneous lattice test case

### Setup

The lattice test case models an isotroptic radiative source in the center of the computational domain sourounded by blue and white squares.
![Lattice test case](documentation/lattice_setup.png)
By default,  the absorption and scattering values as well as the source magnitude are given by the table below

|          | absorption | scattering | source |
|----------|----------|----------|----------|
| blue     | 10       | 0        | 0        |
| red      | 0        | 1        | 1        |
| white    | 0        | 1        | 0        |


The absorption and scattering coefficient are the design parameters for this UQ study. Additional design parameters are the the number of grid cells in each coordinate direction for each square of the lattice geometry and the quadrature order of the velocity space discretization. 

Design parameters are in this order: 

- number of grid points per square side
- quadrature order
- aborption in blue squares
- scattering in white squares

For illustration: 10 grid points means that each of the inner squares has (2*10)^2 cells, and each of the 24 outer squares has 10^2 cells.

Quantities of interest are in this order: 

- CUR_OUTFLOW
- TOTAL_OUTFLOW
- MAX_OUTFLOW
- CUR_PARTICLE_ABSORPTION
- TOTAL_PARTICLE_ABSORPTION
- MAX_PARTICLE_ABSORPTION
- WALL_TIME

Thus the KiT-RT model is a map $F:\mathbb{R}^4\mapsto\mathbb{R}^7$. 

The KiT-RT solver config is given in `benchmarks/lattice_homogeneous/lattice.cfg` 

There one can change the mesh resolution, quadrature order for the velocity space, CFL numbers, discretization order, etc. 

### Execution

Run the UM-Bridge model server

```
python server_lattice_homogeneous.py
```

Run the UQ script (with default settings)

```
python client_lattice.py
```

If you want to change the values of the design parameters, consider the file `client_lattice_homogeneous.py` (beta)