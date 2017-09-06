# -*- coding: utf-8 -*-
"""
Created on Tue Aug 29 04:21:07 2017

@author: adm_cbrown

Some (hopefully) useful tools for the LCLS experiment

Includes
--------
lineout

rotate_array

glob_checker
"""

import glob as glob
import os
import matplotlib.pyplot as plt
import numpy as np

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def lineout(imgarr, x_min, x_max, y_min, y_max, direction):
    """Function to return a lineout over a specific area and direction
    
    Parameters
    ----------
    imgarr : ndarray
        2D image array to take lineout from
    x_min, x_max, y_min, y_max : integer
        Minimum and maximum x and y values
    direction : "x" or "y"
        Direction to take lineout
    Returns
    -------
    out : ndarray(float64) (same size as max-min+1 in lineout direction)
        Array containing lineout averaged over max-min+1 width
        
    """
    imgarr = np.array(imgarr, dtype=np.float64)
    direction = direction.lower()
    if y_min > y_max or x_min > x_max:
        raise AttributeError("Min must be smaller than max")
    if direction == "y":
        lengthprof = abs(y_max - y_min + 1)
        widthprof = abs(x_max - x_min + 1)
        prof = np.zeros(lengthprof)
        for i in range(lengthprof):
            prof[i] = sum(imgarr[i+y_min, x_min:x_max+1]) / widthprof
        return prof
    if direction == "x":
        lengthprof = abs(x_max - x_min + 1)
        widthprof = abs(y_max - y_min + 1)
        prof = np.zeros(lengthprof)
        for i in range(lengthprof):
            prof[i] = sum(imgarr[y_min:y_max+1, i+x_min]) / widthprof
        return prof
    raise AttributeError("Direction must be x or y")

def rotate_array(l, n):
    """Rotate 1D array by n elements
    
    Parameters
    ----------
    l : ndarray
        Array to rotate
    n : int
        Number of elements to rotate
    
    Returns
    -------
    out : ndarray
        Rotated array
    """
    return np.append(l[n:],l[:n])

def glob_checker(dirpath, handler):
    """Cheap and nasty directory monitor for new file creation.
    
    Parameters
    ----------
    dirpath : string
        Path of directory to monitor
    handler : function
        Function to call when a new file is created
    """
    dirconts_old = filter(os.path.isfile, glob.glob(dirpath+"\*"))
    dirconts_old.sort(key=lambda x: os.path.getctime(x))
    print "Glob checker is running (Ctrl-C to stop):"
    try:
        while True:
            #printf(spinner.next())
            dirconts_new = filter(os.path.isfile, glob.glob(dirpath+"\*"))
            dirconts_new.sort(key=lambda x: os.path.getctime(x))
            if len(dirconts_old) < len(dirconts_new):
                
                handler(dirconts_new[-1])
                dirconts_old = dirconts_new
            if len(dirconts_old) > len(dirconts_new):
                print "File deleted!"
                dirconts_old = dirconts_new
            plt.pause(0.5)
            #printf('\b')
    except KeyboardInterrupt:
        print "Interrupted by user"
        return
    
if __name__ == "__main__":
    dirpath = "C:\Users\Public\Documents\Python\Testing\\"
    glob_checker(dirpath, create_handler)