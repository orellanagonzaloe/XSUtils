
Installing resummino-3.0.0:

	source install_resummino3.sh

This also fix a possible bug (?) in the main.cc when reading the pdfset_lo and pdfset_nlo, it's always 0 independent of the argument you pass.

In run directory, to run local:

	source runLocal.sh

To run on HTCondor:

	condor_submit

Both methods run the same script. It runs resummino-3.0.0 for each mass point and each SUSY proccess with:

CTEQ6.6 PDF + 44 variations + muR/muF = {0.5, 2}
MSTW2008nlo90cl PDF + 100 variations + muR/muF = {0.5, 2}
PDF4LHC15_nlo_mc_pdfas + 100 variations + muR/muF = {0.5, 2} + alpha_up/alpha_down variations

For combination run:


