import get_pca
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from obspy.core import *

pca_win = 400
show_win = 5

fin = open('/home/zhangh/FZHW/phase_xj_zsy3_B16.dat')
event = fin.readline()
record = fin.readline()
# d_time = fin.readline()

while event:
    records = record.split(',')
    net, sta, time = records[0], records[1], records[2]
    y, m, d = time.split('T')[0].split('-')
    path = '/data2/ZSY_SAC/' + net + '/' + sta + '/' + y + '/' + m + '/' + d
    os.chdir(path)
    sts = glob.glob('*')
    st = read(sts[0])
    st += read(sts[1])
    st += read(sts[2])
    tp = UTCDateTime(time)
    st = st.slice(tp - show_win, tp + show_win).detrend('constant').filter('highpass', freq=1.).filter('lowpass',
                                                                                                       freq=15.)
    data_x = st[0].data
    data_y = st[1].data
    data_z = st[2].data
    pca = get_pca.get_pca(data_x, data_y, data_z, pca_win)
    #   t_fzhw = float(d_time.split(' ')[0])-0.01
    #   tp = float(d_time.split(' ')[1])-0.01
    title = net + ',' + sta + ',' + time
    timescale = np.arange(-show_win + pca_win / 100, show_win - 1.99, 0.01)
    plt.subplot(411)
    plt.title(title)
    plt.ylabel('HHE')
    #    plt.axvline(t_fzhw,color='black')
    #    plt.axvline(tp,color='black')
    plt.plot(timescale, data_x[pca_win:-200])
    plt.subplot(412)
    #    plt.axvline(t_fzhw,color='black')
    #    plt.axvline(tp,color='black')
    plt.plot(timescale, data_y[pca_win:-200])
    plt.ylabel('HHN')
    plt.subplot(413)
    #    plt.axvline(t_fzhw,color='black')
    #    plt.axvline(tp,color='black')
    plt.plot(timescale, data_z[pca_win:-200])
    plt.ylabel('HHZ')
    plt.subplot(414)
    #    plt.axvline(t_fzhw,color='black')
    #    plt.axvline(tp,color='black')
    plt.plot(timescale, pca[1:-200])
    plt.ylabel('Polarization')
    plt.show()

    event = fin.readline()
    record = fin.readline()
#    d_time = fin.readline()

fin.close()
