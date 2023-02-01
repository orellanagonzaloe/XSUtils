
# download and unzip resummino 3
curl -O https://resummino.hepforge.org/downloads/?f=resummino-3.1.1.zip
unzip \?f\=resummino-3.1.1.zip -d ./
rm \?f\=resummino-3.1.1.zip


# setup directory
mv resummino-releases/ resummino-3.1.1
cd resummino-3.1.1
setupATLAS
asetup 21.2,AthAnalysis,latest

# edit possible bug (?) when reading arguments (not needed in version 3.1.1)
# cp src/main.cc src/main.cc_bak
# sed -i 's/  pdf = LHAPDF::mkPDF(get_option("pdf_lo"), 0);/  pdf = LHAPDF::mkPDF(get_option("pdf_lo"), atoi(get_option("pdfset_lo").c_str()));/' src/main.cc
# sed -i 's/  pdf = LHAPDF::mkPDF(get_option("pdf_nlo"), 0);/  pdf = LHAPDF::mkPDF(get_option("pdf_nlo"), atoi(get_option("pdfset_nlo").c_str()));/' src/main.cc

# build
mkdir build
cd build/

cmake .. -B . -DLHAPDF=/cvmfs/atlas.cern.ch/repo/sw/software/21.2/sw/lcg/releases/LCG_88/MCGenerators/lhapdf/6.1.6.cxxstd/x86_64-centos7-gcc62-opt/lib/ -DCMAKE_INSTALL_PREFIX=../
cmake .. -B . -DLHAPDF=/cvmfs/atlas.cern.ch/repo/sw/software/21.2/sw/lcg/releases/LCG_95/MCGenerators/lhapdf/6.2.1/x86_64-centos7-gcc8-opt/lib/ -DCMAKE_INSTALL_PREFIX=../
make
make install

cp bin/resummino ../../

cd ..
