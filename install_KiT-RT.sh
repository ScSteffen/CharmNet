git clone git@github.com:CSMMLab/KiT-RT.git
cd KiT-RT
git checkout new_radiation_test_cases
git pull origin
cd tools/singularity
sh build_container.sh
cd ../..
mkdir build
cmake ../
make -j