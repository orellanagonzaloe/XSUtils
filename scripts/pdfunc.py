#!/usr/bin/env python

# Copyright 2013 David R. Lamprea.
# Licensed under the European Union Public Licence (EUPL), version 1.1 or later.

import json
import sys
from math import sqrt

muf_central = 0.5
mur_central = 0.5
pdfset_central = 0

dic = {}

def get_pdf_error(central, data):
    if len(data) == 1:
        return 0, 0
    up = 0.0
    down = 0.0
    for i in range(1, len(data), 2):
        x = max([data[i] - central, data[i + 1] - central, 0])
        y = max([central - data[i], central - data[i + 1], 0])
        up = up + x * x
        down = down + y * y
    up = sqrt(up)
    down = sqrt(down)
    return down, up

def read_file(filename):
    data = json.load(open(filename))
    key = str(data["pt"]) + " " + str(data["m"])

    try:
        dic[key]
    except KeyError:
        dic[key] = {}
        dic[key]["pt"] = data["pt"]
        dic[key]["m"] = data["m"]
        dic[key]["lo_pdf"] = {}
        dic[key]["nlo_pdf"] = {}
        dic[key]["nll_pdf"] = {}
        dic[key]["lo_scale_muf"] = []
        dic[key]["nlo_scale_muf"] = []
        dic[key]["nll_scale_muf"] = []
        dic[key]["lo_scale_mur"] = []
        dic[key]["nlo_scale_mur"] = []
        dic[key]["nll_scale_mur"] = []


    if data["muf"] == muf_central and data["mur"] == mur_central:
        dic[key]["lo_pdf"][data["pdfsetlo"]] = data["lo"]
        dic[key]["nlo_pdf"][data["pdfsetnlo"]] = data["nlo"]
        dic[key]["nll_pdf"][data["pdfsetnlo"]] = data["nll"]

        if data["pdfsetlo"] == pdfset_central:
            dic[key]["lo"] = data["lo"]
        if data["pdfsetnlo"] == pdfset_central:
            dic[key]["nlo"] = data["nlo"]
            dic[key]["nll"] = data["nll"]

    if data["pdfsetlo"] == pdfset_central:
        if data["mur"] == mur_central:
            dic[key]["lo_scale_muf"].append(data["lo"])

        if data["muf"] == muf_central:
            dic[key]["lo_scale_mur"].append(data["lo"])

    if data["pdfsetnlo"] == pdfset_central:
        if data["mur"] == mur_central:
            dic[key]["nlo_scale_muf"].append(data["nlo"])
            dic[key]["nll_scale_muf"].append(data["nll"])

        if data["muf"] == muf_central:
            dic[key]["nlo_scale_mur"].append(data["nlo"])
            dic[key]["nll_scale_mur"].append(data["nll"])

            
def read_data(files):
    for f in files:
        read_file(f)

def print_results():
    print "# Generated by resummino_analysis."
    print "# [1]pt [2]m",
    print "[3]lo",
    print "[4]lo_scale_muf_minus [5]lo_scale_muf_plus",
    print "[6]lo_scale_mur_minus [7]lo_scale_mur_plus",
    print "[8]lo_pdf_minus [9]lo_pdf_plus",
    print "[10]nlo",
    print "[11]nlo_scale_muf_minus [12]nlo_scale_muf_plus",
    print "[13]nlo_scale_mur_minus [14]nlo_scale_mur_plus",
    print "[15]nlo_pdf_minus [16]nlo_pdf_plus",
    print "[17]res",
    print "[18]res_scale_muf_minus [19]res_scale_muf_plus",
    print "[20]res_scale_mur_minus [21]res_scale_mur_plus",
    print "[22]res_pdf_minus [23]res_pdf_plus"

    for el in dic:
        lo_pdf_error = get_pdf_error(dic[el]["lo"], dic[el]["lo_pdf"])
        nlo_pdf_error = get_pdf_error(dic[el]["nlo"], dic[el]["nlo_pdf"])
        nll_pdf_error = get_pdf_error(dic[el]["nll"], dic[el]["nll_pdf"])

        print ("{0:.4e} {1:.4e} "
               "{2:.4e} {3:.4e} {4:.4e} {5:.4e} {6:.4e} {7:.4e} {8:.4e} "
               "{9:.4e} {10:.4e} {11:.4e} {12:.4e} {13:.4e} {14:.4e} {15:.4e}"
               "{16:.4e} {17:.4e} {18:.4e} {19:.4e} {20:.4e} {21:.4e} {22:.4e}").format(
            dic[el]["pt"], dic[el]["m"],
            dic[el]["lo"],
            min(dic[el]["lo_scale_muf"]), max(dic[el]["lo_scale_muf"]),
            min(dic[el]["lo_scale_mur"]), max(dic[el]["lo_scale_mur"]),
            dic[el]["lo"] - lo_pdf_error[0], dic[el]["lo"] + lo_pdf_error[1],
            dic[el]["nlo"],
            min(dic[el]["nlo_scale_muf"]), max(dic[el]["nlo_scale_muf"]),
            min(dic[el]["nlo_scale_mur"]), max(dic[el]["nlo_scale_mur"]),
            dic[el]["nlo"] - nlo_pdf_error[0], dic[el]["nlo"] + nlo_pdf_error[1],
            dic[el]["nll"],
            min(dic[el]["nll_scale_muf"]),
            max(dic[el]["nll_scale_muf"]), min(dic[el]["nll_scale_mur"]),
            max(dic[el]["nll_scale_mur"]),
            dic[el]["nll"] - nll_pdf_error[0], dic[el]["nll"] + nll_pdf_error[1]
            )

if __name__ == "__main__":
    read_data(sys.argv[1:])
    print_results()