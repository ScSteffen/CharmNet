# clone KiT-RT
git clone git@github.com:CSMMLab/KiT-RT.git
# go to KiT-RT directory
cd KiT-RT

# checkout the branch new_radiation_test_cases
git checkout new_radiation_test_cases
# load all submodules
git submodule update --init --recursive

# create build directory
mkdir build_singularity

# navigate to directory where the singularity script is located
cd tools/singularity

# build the singularity container. This requires root privileges
sudo sh build_container.sh

# compile KiT-RT within the singularity container
chmod +x install_kitrt_singularity.sh
singularity exec kit_rt.sif ./install_kitrt_singularity.sh

# go back to CharmNet repo
cd ../../../