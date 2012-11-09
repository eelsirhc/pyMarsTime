import matplotlib
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
matplotlib.use("Agg")
matplotlib.rc("xtick",labelsize=8)
matplotlib.rc("ytick",labelsize=8)
matplotlib.rc("font",size=8)

import marstime
import numpy
import pylab

#define the start date as sometime in May 2000, start of MY25
start_j2000_ott = 151.27365

#create the calendar array with 120 points
msd = numpy.linspace(0,669,120)

#calculate the j2000 offset dates
j2000_offsets = marstime.j2000_from_Mars_Solar_Date(msd + marstime.Mars_Solar_Date(start_j2000_ott))

#calculate the equation of time in minutes and the declination.
eot = marstime.equation_of_time(j2000_offsets)*60/15. #convert from degrees to minutes
dec = marstime.solar_declination(marstime.Mars_Ls(j2000_offsets)) #takes Ls, not MSD

#create the plot
pylab.figure(figsize=(3,4.5))
ax = pylab.subplot(1,1,1)
pylab.subplots_adjust(left=0.2)
#plot the data, with 'monthly' data in red
ax.plot(eot,dec,'ko', ms=2, markeredgecolor='none')
ax.plot(eot[::10],dec[::10],'ro', ms=2, markeredgecolor='red')

#set the axes labels, ticks, limits
ax.set_ylabel("Declination (degrees)")
ax.set_xlabel("Equation of Time (minutes)")
ax.set_xlim(-55,45)
ax.set_ylim(-30,28)
ax.set_xticks(numpy.arange(-50,50,20))
ax.set_yticks(numpy.arange(-30,30,5))

#configure the minor ticks
ax.minorticks_on()
XminorLocator   = MultipleLocator(10)
YminorLocator   = MultipleLocator(5)
ax.yaxis.set_minor_locator(YminorLocator)
ax.xaxis.set_minor_locator(XminorLocator)

#save the figure
pylab.savefig("analemma.png",dpi=150)
