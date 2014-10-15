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

gc = gspread.login('EMAIL@gmail.com','PASSWORD')
topo_sheet = gc.open("test_topo").sheet1
topo_data_str = np.array(topo_sheet.get_all_values())
topo_data = topo_data_str.astype(np.float)

matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

delta = 1.
x = np.arange(-5., 5., delta)
y = np.arange(-0., 10, delta)
X, Y = np.meshgrid(x, y)

nr, nc = topo_data.shape
print nr, nc

# Resample your data grid by a factor of 3 using cubic spline interpolation.
topo_data = scipy.ndimage.zoom(topo_data, 4)
topo_data = scipy.ndimage.gaussian_filter(topo_data,2.)
topo_data[-nr//.8:, -nc//.8:] = np.nan

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



########
#  Commented out other examples
########
## contour labels can be placed manually by providing list of positions
## (in data coordinate). See ginput_manual_clabel.py for interactive
## placement.
#plt.figure()
#CS = plt.contour(X, Y, Z)
#manual_locations = [(-1, -1.4), (-0.62, -0.7), (-2, 0.5), (1.7, 1.2), (2.0, 1.4), (2.4, 1.7)]
#plt.clabel(CS, inline=1, fontsize=10, manual=manual_locations)
#plt.title('labels at selected locations')
#
#
## You can force all the contours to be the same color.
#plt.figure()
#CS = plt.contour(X, Y, Z, 6,
#                 colors='k', # negative contours will be dashed by default
#                 )
#plt.clabel(CS, fontsize=9, inline=1)
#plt.title('Single color - negative contours dashed')
#
## You can set negative contours to be solid instead of dashed:
#matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
#plt.figure()
#CS = plt.contour(X, Y, Z, 6,
#                 colors='k', # negative contours will be dashed by default
#                 )
#plt.clabel(CS, fontsize=9, inline=1)
#plt.title('Single color - negative contours solid')
#
#
## And you can manually specify the colors of the contour
#plt.figure()
#CS = plt.contour(X, Y, Z, 6,
#                 linewidths=np.arange(.5, 4, .5),
#                 colors=('r', 'green', 'blue', (1,1,0), '#afeeee', '0.5')
#                 )
#plt.clabel(CS, fontsize=9, inline=1)
#plt.title('Crazy lines')
#
#
## Or you can use a colormap to specify the colors; the default
## colormap will be used for the contour lines
#plt.figure()
#im = plt.imshow(Z, interpolation='bilinear', origin='lower',
#                cmap=cm.gray, extent=(-3,3,-2,2))
#levels = np.arange(-1.2, 1.6, 0.2)
#CS = plt.contour(Z, levels,
#                 origin='lower',
#                 linewidths=2,
#                 extent=(-3,3,-2,2))

##Thicken the zero contour.
#zc = CS.collections[6]
#plt.setp(zc, linewidth=4)
#
#plt.clabel(CS, levels[1::2],  # label every second level
#           inline=1,
#           fmt='%1.1f',
#           fontsize=14)
#
## make a colorbar for the contour lines
#CB = plt.colorbar(CS, shrink=0.8, extend='both')
#
#plt.title('Lines with colorbar')
##plt.hot()  # Now change the colormap for the contour lines and colorbar
#plt.flag()
#
## We can still add a colorbar for the image, too.
#CBI = plt.colorbar(im, orientation='horizontal', shrink=0.8)
#
## This makes the original colorbar look a bit out of place,
## so let's improve its position.
#
#l,b,w,h = plt.gca().get_position().bounds
#ll,bb,ww,hh = CB.ax.get_position().bounds
#CB.ax.set_position([ll, b+0.1*h, ww, h*0.8])


#plt.show()