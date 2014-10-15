#! /usr/bin/env python

import numpy as np
import scipy.io as sio
from glob import glob
#import matplotlib.pyplot as plt

# Choose which test to calculate results for
#testname = 'linear'
#testname = 'poly'
#testname = 'exp'
#testname = 'sin'
testname = 'tanh'
#testname = 'sign'

# Find data and result files
dataname = glob('../data/*{}*'.format(testname))
oppres = glob('opper/*{}*.mat'.format(testname))
oppres.sort()


# Define validation metrics
def SMSE(test, Epred):

    vartest = test.var()
    Ntest = test.shape[0]

    return ((test - Epred)**2).sum() / (Ntest * vartest)


def navll(test, Epred, Vpred):

    Ntest = test.shape[0]

    return 0.5 * (((test - Epred)**2 / Vpred + np.log(2 * np.pi
                  * Vpred))).sum() / Ntest

# Read in data and calculate metrics per fold
data = sio.loadmat(dataname[0], squeeze_me=True)

SMSEf = []
SMSEy = []
navllf = []

for i, oppfname in enumerate(oppres):

    # Leave out the bung result for opper - had issues converging
    if (testname is 'poly') and (i == 1):
        continue

    print "iter {}, opper fold {}".format(i, oppfname)

    xs = data['x'][data['test'][i, :]]
    ys = data['y'][data['test'][i, :]]
    fs = data['f'][data['test'][i, :]]

    oppfdata = sio.loadmat(oppfname, squeeze_me=True)

    Eys = oppfdata['yStar']
    Efs = oppfdata['mufPred']
    Vfs = oppfdata['sigmafStar']**2

    SMSEf.append(SMSE(fs, Efs))
    SMSEy.append(SMSE(ys, Eys))
    navllf.append(navll(fs, Efs, Vfs))

    #plt.plot(xs, fs, 'b.')
    #plt.plot(xs, Efs, 'g.')
    #plt.show()

SMSEf = np.array(SMSEf)
SMSEy = np.array(SMSEy)
navllf = np.array(navllf)

print "& \\cite{{Opper2009}} & {:.5f} & {:.5f} & {:.5f} & {:.5f} & {:.5f} & {:.5f} \\\\\n"\
    .format(navllf.mean(), navllf.std(),
            SMSEf.mean(), SMSEf.std(),
            SMSEy.mean(), SMSEy.std())
