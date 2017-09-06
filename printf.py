# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 04:49:43 2017

@author: adm_cbrown
"""

from __future__ import print_function

def printf(str, *args):
    print(str % args, end = '')
    
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backend_bases import FigureManagerBase
    fig = plt.Figure()
    axes = fig.add_subplot(111)
    t = np.arange(0.0, 3.0, 0.01)
    s = np.cos(2*np.pi*t)
    axes.plot(t, s)
    plt.clf
    fig.clf
    