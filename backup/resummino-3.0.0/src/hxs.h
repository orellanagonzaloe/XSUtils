// This file is part of Resummino.
//
// Copyright 2011-2014 David R. Lamprea.
// Copyright 2011-2014 Marcel Rothering.
//
// Licensed under the terms of the EUPL version 1.1 or later.
// See the LICENCE file for more information.

// Computes the hadronic cross section at LO, NLO (collinear, virtual,
// gluon emission and quark emission) and NLL.

#ifndef HXS_H_
#define HXS_H_

#include "params.h"

// Computes the total hadronic cross section for a given set of parameters.
void hadronic_xs(double &res, double &err, int Flag, Parameters *params);

// Computes the differential hadronic cross section with respecto to $p_T^2$
// for a given set of parameters.
void hadronic_xs_dPT2(double &res, double &err, double &chi2, int Flag,
                      int Verb, Parameters *params);

// Computes the differential hadronic cross section with respecto to $ln M^2$
// for a given set of parameters.
void hadronic_xs_dlnM2(double &res, double &err, double &chi2, int Flag,
                       int Verb, Parameters *params);

#endif
