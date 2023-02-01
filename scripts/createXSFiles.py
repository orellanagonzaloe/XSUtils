#! /usr/bin/env python

import os
import json
import math
from decimal import Decimal


"""This recipe is:
we have the 1+44 variationes of cteq6.6, and the 1+40 variations of MSTW2008, plus each muR+muF variation, 0.5 and 2.
The PDF set unc for each PDF is the standard deviation wrt the nominal value (simmetric), and the mu unc is the difference
between both vairation divided by 2 (simmetric). The total unc is the squared root sum of each. Then the maximum and the minimum of both PDF (considering their corresponding unc) is taken as the total XS unc range, and the total XS. This is done for each process and each mass.
The final XS is the middle of that range.
The XS of the sum of all processes is the sum of each XS, and the unc is propagated aswell.
"""

mN1 = [150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1250, 1450]
# mN1 = [150, ]


ChiChi = [(1000022, 1000023), (1000022, 1000024), (-1000024, 1000022), (1000023, 1000024), (-1000024, 1000023), (-1000024, 1000024)]
# ChiChi = [(1000022, 1000023), (1000022, 1000024), (-1000024, 1000022), (1000023, 1000024), (-1000024, 1000023)]

partDict = {
	 1000022: 'N1',
	 1000023: 'N2',
	 1000024: 'C1p',
	-1000024: 'C1m',
}
partLaTeX = {
	 1000022: '$\\tilde\\chi_{1}^{0}$',
	 1000023: '$\\tilde\\chi_{2}^{0}$',
	 1000024: '$\\tilde\\chi_{1}^{+}$',
	-1000024: '$\\tilde\\chi_{1}^{-}$',
}


precision = 'nll'

inputDir = 'outputHT'
outputDir = 'testoutput'
pdfs = {
	'cteq66': 44,
	'MSTW2008': 40,
}

if not os.path.exists(outputDir):
	os.makedirs(outputDir)




d_mass_proc = {}

for m in mN1:

	d_mass_proc[m] = {
		'precision' : precision,
		'units' : '',
	}

	m_total = 0.
	m_totalUnc = 0.

	for xx in ChiChi:

		upper = []
		lower = []

		for pdf in pdfs:

			# nominal

			nom_file = '%s/xsec_%s_%s_%s_%s_pdf_0.json' % (inputDir, str(m), str(xx[0]), str(xx[1]), pdf)

			with open(nom_file) as f:
				_nom_file = json.load(f) 

			nom = _nom_file[precision]

			d_mass_proc[m]['units'] = _nom_file['units']

			# PDF error

			dPDF = 0.

			for i in xrange(1, pdfs[pdf]):

				PDF_file = '%s/xsec_%s_%s_%s_%s_pdf_%i.json' % (inputDir, str(m), str(xx[0]), str(xx[1]), pdf, i)

				with open(PDF_file) as f:
					_PDF_file = json.load(f) 

				PDF = _PDF_file[precision]

				dPDF += (nom-PDF)**2


			dPDF = math.sqrt(dPDF)

			# mu error
			
			mu05_file = '%s/xsec_%s_%s_%s_%s_mu_0.5.json' % (inputDir, str(m), str(xx[0]), str(xx[1]), pdf)

			with open(mu05_file) as f:
				_mu05_file = json.load(f) 

			mu05 = _mu05_file[precision]

			mu2_file = '%s/xsec_%s_%s_%s_%s_mu_2.json' % (inputDir, str(m), str(xx[0]), str(xx[1]), pdf)

			with open(mu2_file) as f:
				_mu2_file = json.load(f) 

			mu2 = _mu2_file[precision]

			dmu = abs(mu05-mu2)/2.

			# add total error

			dTotal = math.sqrt(dPDF**2 + dmu**2)

			upper.append(nom+dTotal)
			lower.append(nom-dTotal)


		# Total XS and unc for particular process

		U = max(upper)
		L = min(lower)

		xs = (U + L)/2.
		dxs = (U - L)/2.

		xxStr = '%s%s' % (partDict[xx[0]], partDict[xx[1]])

		d_mass_proc[m][xxStr] = xs
		d_mass_proc[m]['%s_unc' % xxStr] = dxs

		m_total += xs
		m_totalUnc += dxs**2


	# Total XS and unc for each mass

	m_totalUnc = math.sqrt(m_totalUnc)

	d_mass_proc[m]['ChiChi'] = m_total
	d_mass_proc[m]['ChiChi_unc'] = m_totalUnc



# Rever dictionary keys

d_proc_mass = {}

for xx in ChiChi:

	xxStr = '%s%s' % (partDict[xx[0]], partDict[xx[1]])

	d_proc_mass[xxStr] = {
		'process_latex': '%s%s'% (partLaTeX[xx[0]], partLaTeX[xx[1]]),
		'precision': precision,
		'data': {},
	}

	for m in mN1:

		d_proc_mass[xxStr]['units'] = d_mass_proc[m]['units']

		d_proc_mass[xxStr]['data'][str(m)] = {
			'xsec_pb': d_mass_proc[m][xxStr],
			'unc_pb': d_mass_proc[m]['%s_unc' % xxStr],
		}


d_proc_mass['ChiChi'] = {
	'process_latex': '$\\tilde\\chi\\tilde\\chi$',
	'precision': precision,
	'data': {},
}

for m in mN1:

	d_proc_mass['ChiChi']['units'] = d_mass_proc[m]['units']

	d_proc_mass['ChiChi']['data'][str(m)] = {
		'xsec_pb': d_mass_proc[m]['ChiChi'],
		'unc_pb': d_mass_proc[m]['ChiChi_unc'],
	}


# Dump files

for m in mN1:

	outFilename = '%s/EWK_xsec_%s.json' % (outputDir, str(m))

	with open(outFilename, 'w') as outfile:
		json.dump(d_mass_proc[m], outfile, indent=2)


for xx in ChiChi:

	xxStr = '%s%s' % (partDict[xx[0]], partDict[xx[1]])

	outFilename = '%s/xsec_inputfile_%s.json' % (outputDir, xxStr)

	with open(outFilename, 'w') as outfile:
		json.dump(d_proc_mass[xxStr], outfile, indent=2)


outFilename = '%s/xsec_inputfile_ChiChi.json' % (outputDir)

with open(outFilename, 'w') as outfile:
	json.dump(d_proc_mass['ChiChi'], outfile, indent=2)

for m in mN1:

	print('%.8E\t%.8E' % (Decimal(d_mass_proc[m]['ChiChi']*0.001), Decimal(d_mass_proc[m]['ChiChi_unc']/d_mass_proc[m]['ChiChi'])))
