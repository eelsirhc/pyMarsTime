#!/usr/bin/env python
import matplotlib as mpl
mpl.use("Agg")
mpl.rc("axes",labelsize=10)
mpl.rc("xtick",labelsize=10)
mpl.rc("ytick",labelsize=10)
mpl.rc("legend",fontsize=10)
import pylab as pl
import numpy as np
import marstime

#define mars solar days to use in the plot
start_j2000_ott = 151.27365 # sometime in May 2000, start of MY25

msd = np.linspace(0,669,120)
#calculate the j2000 offset dates
j2000_offsets = marstime.j2000_from_Mars_Solar_Date(msd + marstime.Mars_Solar_Date(start_j2000_ott))

eot_axis = marstime.equation_of_time(j2000_offsets)*60/15. #convert from degrees to minutes
dec_axis = marstime.solar_declination(marstime.Mars_Ls(j2000_offsets)) #takes Ls, not MSD

pl.figure(figsize=(4,6))
pl.subplots_adjust(left=0.15)
pl.plot(eot_axis, dec_axis, marker='.', ls='none',color='k')
pl.plot(eot_axis[::10], dec_axis[::10], marker='.', ls='none',color='r')
pl.ylim(-28,28)
pl.xlim(-55,45)
pl.xticks(np.arange(-50,50,10))
pl.yticks(np.arange(-30,30,5))
pl.ylabel("Declination (degrees)")
pl.xlabel("Equation of Time (minutes)")
pl.savefig("analemma.png")