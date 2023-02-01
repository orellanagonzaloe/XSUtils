# ! /usr/bin/bash

setupATLAS 
asetup 21.2,AthAnalysis,latest

for mN1 in 150 250 350 450 550 650 750 850 950 1050 1250 1450
do

	for PDG in "1000022 1000023" "1000022 1000024" "-1000024 1000022" "1000023 1000024" "-1000024 1000023" "-1000024 1000024"
	do
		echo "$mN1" "$PDG"
	    set -- $PDG

		source run_resummino.sh "$mN1" "$1" "$2" outputLocal
	done

done

