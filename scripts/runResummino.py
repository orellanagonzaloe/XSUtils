#! /usr/bin/env python

import os
import subprocess
import json



# mN1 = [150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1250, 1450]
mN1 = [150]

# ChiChi = [(1000022, 1000023), (1000022, 1000024), (-1000024, 1000022), (1000023, 1000024), (-1000024, 1000023), (-1000024, 1000024)]
ChiChi = [(-1000024, 1000023)]

outputDir = 'test'

precision = 'nlo'

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

for m in mN1:

	for xx in ChiChi:

		print m, xx

		lines = open('resummino.in').read().split('\n')

		new_lines = []

		for line in lines:

			if 'particle1 = XXX' in line:
				new_lines.append('particle1 = %s' % str(xx[0]))
			elif 'particle2 = XXX' in line:
				new_lines.append('particle2 = %s' % str(xx[1]))
			else:
				new_lines.append(line)

		with open('resummino.in.tmp', 'w+') as f:

			for line in new_lines:

				if line:
					f.write(line+'\n')

		###

		lines = open('param.GGM_N1N2C1.slha').read().split('\n')

		new_lines = []

		for line in lines:

			if '1000022     XXX   # ~chi_10' in line:
				new_lines.append('   1000022     %s   # ~chi_10' % str(m))
			elif '1000023     XXX   # ~chi_20' in line:
				new_lines.append('   1000023     %s   # ~chi_20' % str(-(m+11)))
			elif '1000024     XXX   # ~chi_1+' in line:
				new_lines.append('   1000024     %s   # ~chi_1+' % str(m+10))
			else:
				new_lines.append(line)

		with open('param.GGM_N1N2C1.slha.tmp', 'w+') as f:

			for line in new_lines:
				
				if line:
					f.write(line+'\n')

		###

		bashCommand = './resummino resummino.in.tmp --%s -o %s/xsec_%s_%s_%s.json --parameter-log=%s/params_%s_%s_%s.log' % (precision, outputDir, str(m), str(xx[0]), str(xx[1]), outputDir, str(m), str(xx[0]), str(xx[1]))
		process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE, shell=False)
		output, error = process.communicate()

		jsonFile = '%s/xsec_%s_%s_%s.json' % (outputDir, str(m), str(xx[0]), str(xx[1]))

		print output

		with open(jsonFile) as f:
			jsonTmp = json.load(f)

		for line in output.split('\n'):

			if line.startswith('LO = ('):

				unc = line.strip().split('+-')[1].replace(') pb','')
				jsonTmp['lo_unc'] = float(unc)

			elif line.startswith('NLO = ('):

				unc = line.strip().split('+-')[1].replace(') pb','')
				jsonTmp['nlo_unc'] = float(unc)

			elif line.startswith('NLO+NLL = ('):

				unc = line.strip().split('+-')[1].replace(') pb','')
				jsonTmp['nll_unc'] = float(unc)

			elif line.startswith('aNLO+NLL = ('):

				unc = line.strip().split('+-')[1].replace(') pb','')
				jsonTmp['nll_unc'] = float(unc)

		with open(jsonFile, 'w') as outfile:
			json.dump(jsonTmp, outfile, indent=2)

		# os.remove('resummino.in.tmp')
		# os.remove('param.GGM_N1N2C1.slha.tmp')












