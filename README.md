
Install everything:

	source scripts/install.sh

Currently it's not possible to install resummino 3.1.1 becuse an older version of boost
Using instead the version 3.0.0 stored and compiled in backup folder

In run directory, to run local:

	source run_local.sh

To run on HTCondor:

	condor_submit send_XSUtils.job

Both methods run the same script. It runs resummino-3.0.0 for each mass point and each SUSY proccess with:

CTEQ6.6 PDF + 44 variations + muR/muF = {0.5, 2}
MSTW2008nlo90cl PDF + 100 variations + muR/muF = {0.5, 2}
PDF4LHC15_nlo_mc_pdfas + 100 variations + muR/muF = {0.5, 2} + alpha_up/alpha_down variations


scripts/createXSFiles.py: creates all the output file with XS information
scripts/xsec: software from https://github.com/fuenfundachtzig/xsec, to plot XSs (also custom additional script)