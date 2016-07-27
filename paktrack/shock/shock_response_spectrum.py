"""
__author__ = 'Supriya'

"""

import math
import numpy as np
from scipy.signal import lfilter


def srs(signal, amplification_factor=10, algorithm=1):
    """
    Algorithm
        1=Kelly-Richman  2=Smallwood
    """
    iunit = 1
    t = [float((1 / 800.0) * i) for i in xrange(1, 1025)]  # TIME VECTOR
    y = signal  # ACCELERATION VECTOR

    tmx = max(t)
    tmi = min(t)
    n = len(y)
    nnn = n
    print(n, " samples")
    dt = (tmx - tmi) / (n - 1)
    sr = 1. / dt
    print(sr, " samles/sec   ", dt, " sec")

    fn = [0] * 800
    fn[0] = 1  # Frequency 1Hz  the starting frequency
    if fn[0] > sr / 30.:
        fn[0] = sr / 30.

    Q = amplification_factor  # the amplification factor (typically Q=10)
    damp = 1. / (2. * Q)
    print(damp)

    print(' using algorithm: ', algorithm)
    ialgorithm = algorithm

    tmax = (tmx - tmi) + 1. / fn[0]

    limit = int(round(tmax / dt))
    n = limit
    yy = [0] * limit
    for i in range(len(y)):
        yy[i] = y[i]

    print(' Calculating response..... ')

    l = 0
    while l < 800:
        if fn[l] > sr / 8.:
            break
        if l < 799:
            fn[l + 1] = fn[0] * pow(2., ((l + 1) * (1. / 12.)))
        l = l + 1

    a1 = [0] * l
    a2 = [0] * l
    b1 = [0] * l
    b2 = [0] * l
    b3 = [0] * l

    rd_a1 = [0] * l
    rd_a2 = [0] * l
    rd_b1 = [0] * l
    rd_b2 = [0] * l
    rd_b3 = [0] * l

    x_neg = [0] * l
    x_pos = [0] * l
    x_std = [0] * l
    rd_neg = [0] * l
    rd_pos = [0] * l
    pi = 3.1416

    for j in range(l):

        omega = 2. * pi * fn[j]
        omegad = omega * math.sqrt(1. - (pow(damp, 2)))
        cosd = math.cos(omegad * dt)
        sind = math.sin(omegad * dt)
        domegadt = damp * omega * dt
        # rd_a1[j]=2.*math.exp(-domegadt)*cosd
        # rd_a2[j]=-math.exp(-2.*domegadt)
        # rd_b1[j]=0.
        # rd_b2[j]=-(dt/omegad)*math.exp(-domegadt)*sind
        # rd_b3[j]=0

        if ialgorithm == 1:
            a1[j] = 2. * math.exp(-domegadt) * cosd
            a2[j] = -math.exp(-2. * domegadt)
            b1[j] = 2. * domegadt
            b2[j] = omega * dt * math.exp(-domegadt)
            b2[j] *= (omega / omegad) * (1. - 2. * (pow(damp, 2))) * sind - 2. * damp * cosd
            b3[j] = 0

        else:
            E = math.exp(-damp * omega * dt)
            K = omegad * dt
            C = E * math.cos(K)
            S = E * math.sin(K)
            Sp = S / K
            a1[j] = 2 * C
            a2[j] = -(pow(E, 2))
            b1[j] = 1. - Sp
            b2[j] = 2. * (Sp - C)
            b3[j] = pow(E, 2) - Sp

        forward = [b1[j], b2[j], b3[j]]
        back = [1, -a1[j], -a2[j]]

        resp = lfilter(forward, back, yy)
        x_pos[j] = max(resp)
        x_neg[j] = min(resp)
        x_std[j] = np.std(resp)

        rd_forward = [rd_b1[j], rd_b2[j], rd_b3[j]]
        rd_back = [1, -rd_a1[j], -rd_a2[j]]

        rd_resp = lfilter(rd_forward, rd_back, yy)

        rd_pos[j] = max(rd_resp)
        rd_neg[j] = min(rd_resp)

        # Relative Displacement

        jnum = j
        # if  fn[j] > sr/8.:
        #     break
        # if j<799:
        #     fn[j+1]=fn[1]*pow(2.,(j*(1./12.)))

    tmax = (tmx - tmi)

    print(' Plotting output..... ')

    #  Find limits for plot

    srs_max = max(x_pos)
    if max(abs(i) for i in x_neg) > srs_max:
        srs_max = max(abs(i) for i in x_neg)

    maximaxSRS = srs_max

    srs_min = min(x_pos)
    if min(abs(i) for i in x_neg) < srs_min:
        srs_min = min(abs(i) for i in x_neg)

    Q = 1. / (2. * damp)
    out5 = ' Acceleration Shock Response Spectrum Q=%g ' + str(Q)
    print(out5)

    ymax = math.pow(10, (int(round(np.log10(srs_max) + 0.8))))
    ymin = math.pow(10, (int(round(np.log10(srs_min) - 0.6))))

    fmax = max(fn)
    fmin = fmax / 10.0

    fmax = math.pow(10, (int(round(np.log10(fmax) + 0.5))))

    fmin = 0.1

    x_neg_abs = [0] * len(x_neg)
    for i in range(len(x_neg)):
        x_neg_abs[i] = abs(x_neg[i])

    fn1 = [0] * l
    for i in range(l):
        fn1[i] = fn[i]

    return {'freq': fn1, 'positive': x_pos, 'negative': x_neg_abs}
