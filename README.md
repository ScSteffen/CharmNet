# CharmNet
CharmNet Benchmarking Suite using the [UM-Bridge UQ suite](https://um-bridge-benchmarks.readthedocs.io/en/docs/) and the [KiT-RT PDE simulator](https://kit-rt.readthedocs.io/en/develop/index.html). 

CharmNet contains a series of testcases outlined below. 

## Installation

Install the python requirements in a local virtual environment

```
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

Install [singularity](https://docs.sylabs.io/guides/3.0/user-guide/installation.html) on your system. 

Build the kit_rt singularity container on your system (root access required).
```
cd singularity
sh build_container.sh
```
 If you use a cluster without root access, build the container locally and upload it to the directory `./singularity/` 

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


The absorption and scattering coefficient are the design parameters for this UQ study. 
Quantities of interest are: 

- CUR_OUTFLOW
- TOTAL_OUTFLOW
- MAX_OUTFLOW
- CUR_PARTICLE_ABSORPTION
- TOTAL_PARTICLE_ABSORPTION
- MAX_PARTICLE_ABSORPTION

Thus the KiT-RT model is a map $F:\mathbb{R}^2\mapsto\mathbb{R}^6$. 

The KiT-RT solver config is given in `benchmarks/lattice_homogeneous/lattice.cfg` 

There one can change the mesh resolution, quadrature order for the velocity space, CFL numbers, discretization order, etc. 

### Execution

Run the UM-Bridge model server

```
python server_lattice_homogeneous.py
```

Run the UQ script (with default settings)

```
python main_lattice_homogeneous.py
```

If you want to change the values of the design paramters, consider the file `main_lattice_homogeneous.py` (beta)