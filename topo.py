# -*- coding: utf-8 -*-
"""
Generate topographic image from google sheet
Roy Haggerty October 2014
"""

# Dependent on gspread for reading google sheet. See and download at
#    https://github.com/burnash/gspread

import gspread
import matplotlib
import numpy as np
import scipy.ndimage
#import matplotlib.cm as cm
#import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import imp
ui = imp.load_source('userinfo', 'C:\\keys\\userinfo.py')

gc = gspread.login(ui.userid,ui.pw)
topo_sheet = gc.open_by_key("0AtY57GzQ69rodFNvb0hIWUxfcHBNV2pCcXE2RjM3cnc").sheet1
topo_data_str = np.array(topo_sheet.get_all_values())

topo_data = topo_data_str.astype(np.float)

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 1.
x = np.arange(-5., 5., delta)
y = np.arange(-0., 10, delta)
X, Y = np.meshgrid(x, y)

nr, nc = topo_data.shape

# Resample your data grid by a factor of 3 using cubic spline interpolation.
topo_data = scipy.ndimage.zoom(topo_data, 4)
topo_data = scipy.ndimage.gaussian_filter(topo_data,2.)

# Mask some data by making them nan.  Still need to figure out the coords here.
topo_data[-nr//2.:, -nc//.7:] = np.nan
topo_data[0:-nr//.29,0:] = np.nan

# Create a simple contour plot with labels using default colors.  The
# inline argument to clabel will control whether the labels are draw
# over the line segments of the contour, removing the lines beneath
# the label
plt.figure()
#CS = plt.contour(X, Y, topo_data, origin = 'image')
CS = plt.contour(topo_data, origin = 'upper')
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Topo data from google sheet')

plt.show()
