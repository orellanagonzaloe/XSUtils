# ! /usr/bin/bash
pwd
ls

mN1=$1
PDG1=$2
PDG2=$3
outputDir=$4
prescision="nll"

mN2=$((-(mN1+11))) 
mC1=$((mN1+10))

echo "Runnning with:"
echo "mN1=$mN1"
echo "PDG1=$PDG1"
echo "PDG2=$PDG2"
echo "mN2=$mN2"
echo "mC1=$mC1"
echo "prescision=$prescision"
echo "outputDir=$outputDir"

mkdir -pv "$outputDir"

echo "Editing param card..."

ls input/param.GGM_N1N2C1.slha
cp input/param.GGM_N1N2C1.slha input/param.GGM_N1N2C1.slha.tmp

sed -i "s/1000022     XXX   # ~chi_10/1000022     $mN1   # ~chi_10/" input/param.GGM_N1N2C1.slha.tmp
sed -i "s/1000023     XXX   # ~chi_20/1000023     $mN2   # ~chi_20/" input/param.GGM_N1N2C1.slha.tmp
sed -i "s/1000024     XXX   # ~chi_1+/1000024     $mC1   # ~chi_1+/" input/param.GGM_N1N2C1.slha.tmp


echo "Creating resummino.in.tmp ..."

ls input/resummino.in

cp input/resummino.in input/resummino.in.tmp

sed -i "s/particle1 = XXX/particle1 = $PDG1/" input/resummino.in.tmp
sed -i "s/particle2 = XXX/particle2 = $PDG2/" input/resummino.in.tmp


# cteq66

echo "Editing input/resummino.in.tmp for cteq66 PDF"

sed -i "s/pdf_lo     = XXX/pdf_lo    = cteq66/" input/resummino.in.tmp
sed -i "s/pdf_nlo    = XXX/pdf_nlo    = cteq66/" input/resummino.in.tmp


# PDF set variations
for PDF in {0..44}
do
	./resummino input/resummino.in.tmp --"$prescision" --pdfset_lo "$PDF" --pdfset_nlo "$PDF" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_cteq66_pdf_"$PDF".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_cteq66_pdf_"$PDF".log
done

# Scale variations

for MU in 0.5 2
do
	./resummino input/resummino.in.tmp --"$prescision" --mu_r "$MU" --mu_f "$MU" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_cteq66_mu_"$MU".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_cteq66_mu_"$MU".log
done

# MSTW2008nlo90cl

echo "Editing input/resummino.in.tmp for MSTW2008 PDF"

cp input/resummino.in input/resummino.in.tmp

sed -i "s/particle1 = XXX/particle1 = $PDG1/" input/resummino.in.tmp
sed -i "s/particle2 = XXX/particle2 = $PDG2/" input/resummino.in.tmp

sed -i "s/pdf_lo     = XXX/pdf_lo    = MSTW2008lo90cl/" input/resummino.in.tmp
sed -i "s/pdf_nlo    = XXX/pdf_nlo    = MSTW2008nlo90cl/" input/resummino.in.tmp

# PDF set variations
for PDF in {0..40}
do
	./resummino input/resummino.in.tmp --"$prescision" --pdfset_lo "$PDF" --pdfset_nlo "$PDF" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_MSTW2008_pdf_"$PDF".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_MSTW2008_pdf_"$PDF".log
done

# Scale variations

for MU in 0.5 2
do
	./resummino input/resummino.in.tmp --"$prescision" --mu_r "$MU" --mu_f "$MU" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_MSTW2008_mu_"$MU".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_MSTW2008_mu_"$MU".log
done


# PDF4LHC15_nlo_mc_pdfas

echo "Editing input/resummino.in.tmp for MSTW2008 PDF"

cp input/resummino.in input/resummino.in.tmp

sed -i "s/particle1 = XXX/particle1 = $PDG1/" input/resummino.in.tmp
sed -i "s/particle2 = XXX/particle2 = $PDG2/" input/resummino.in.tmp

sed -i "s/pdf_lo     = XXX/pdf_lo    = PDF4LHC15_nlo_mc_pdfas/" input/resummino.in.tmp
sed -i "s/pdf_nlo    = XXX/pdf_nlo    = PDF4LHC15_nlo_mc_pdfas/" input/resummino.in.tmp

# PDF set variations
for PDF in {0..100}
do
	./resummino input/resummino.in.tmp --"$prescision" --pdfset_lo "$PDF" --pdfset_nlo "$PDF" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_pdf_"$PDF".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_pdf_"$PDF".log
done

# Scale variations

for MU in 0.5 2
do
	./resummino input/resummino.in.tmp --"$prescision" --mu_r "$MU" --mu_f "$MU" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_mu_"$MU".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_mu_"$MU".log
done

# Alpha variations

for alp in {101..102}
do
	./resummino input/resummino.in.tmp --"$prescision" --pdfset_lo "$alp" --pdfset_nlo "$alp" -o "$outputDir"/xsec_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_alp_"$alp".json 
	# --parameter-log="$outputDir"/params_"$mN1"_"$PDG1"_"$PDG2"_PDF4LHC15_alp_"$alp".log
done


rm input/param.GGM_N1N2C1.slha.tmp
rm input/resummino.in.tmp