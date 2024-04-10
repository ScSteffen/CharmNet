git clone git@github.com:CSMMLab/KiT-RT.git
cd KiT-RT
git checkout new_radiation_test_cases
git submodule update --init --recursive
mkdir build_singularity
cd tools/singularity
sudo sh build_container.sh
chmod +x install_kitrt_singularity.sh
singularity exec kit_rt.sif ./install_kitrt_singularity.sh
cd ../../../