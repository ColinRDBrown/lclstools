# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 05:40:33 2017

@author: adm_cbrown
"""

from lclstools import glob_checker
import os
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mplimage

run_number = 1
src_directory = "C:\Users\Public\Documents\Python\Testing\\"
dest_directory = "C:\Users\Public\Documents\Python\Testing2\\"
event_number = 1
def image_added(path):
    global event_number, fig, ax_prev, ax_curr, prev_im
    print "New file {0} added, copying...".format(os.path.basename(path))
    shutil.copy(path, dest_directory+"run"+str(run_number)+"\event_"+str(event_number)+".tiff")
    
    
    curr_im = mplimage.imread(dest_directory+"run"+str(run_number)+"\event_"+str(event_number)+".tiff")
    if event_number == 1:
        prev_im = curr_im
    ax_prev.imshow(prev_im)
    ax_curr.imshow(curr_im)
    plt.pause(0.05)
    prev_im = curr_im
    event_number = event_number +1
    ax_prev.set
    
if not os.path.exists(dest_directory+"run"+str(run_number)+"\\"):
    os.mkdir(dest_directory+"run"+str(run_number)+"\\")
plt.ion()    
fig, (ax_prev, ax_curr) = plt.subplots(1, 2)
fig.set_size_inches(20,10)
fig.tight_layout()
plt.pause(0.05)
glob_checker(src_directory, image_added)
print "Run {0} complete".format(run_number)