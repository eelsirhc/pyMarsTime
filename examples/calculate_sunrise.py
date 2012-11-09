#!/usr/bin/env python

## Copyright (c) 2012, Christopher Lee, 
## All rights reserved.
## 
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met:
##     * Redistributions of source code must retain the above copyright
##       notice, this list of conditions and the following disclaimer.
##     * Redistributions in binary form must reproduce the above copyright
##       notice, this list of conditions and the following disclaimer in the
##       documentation and/or other materials provided with the distribution.
##     * Neither the name of Ashima Research nor the
##       names of its contributors may be used to endorse or promote products
##       derived from this software without specific prior written permission.
## 
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
## ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
## WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
## DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
## DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
## (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
## LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
## ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import matplotlib
matplotlib.use("Agg")
matplotlib.rc("xtick",labelsize=8)
matplotlib.rc("ytick",labelsize=8)
matplotlib.rc("font",size=8)

import marstime
import ephem
import datetime
import scipy.optimize as so
import numpy
import argparse
import pylab as pl

def midnight(date, longitude, latitude):
    """Given a Mars Solar Date(MSD) and location, find the local midnight times.
    The input data is used to calculate the local True solar time (LTST)
    and the local midnight occurs LTST hours before and 24-LTST after"""
    lt = marstime.Local_True_Solar_Time(longitude, date)
    mid1 = date - lt/24.
    mid2 = date + (24-lt)/24.
    return (mid1, mid2)

def solelev(date, x,y, solar_angular_radius=0.0):
    """a wrapper for scipy.optimize to reverse the arguments for solar_elevation"""
    return marstime.solar_elevation(x,y,date)+solar_angular_radius
    
def sunrise_sunset(date, longitude, latitude, solar_angular_radius=0.0):
    """Interface to the scipy.optimize.
    Using the date (j2000 offset) and location, start by finding the local 
    midnights. the local mid-day is then (roughly) at the center of the two 
    midnights. Sunrise must occur between midnight and midday, sunset between 
    midday and midnight (except for polar night).
    
    This method uses Ian's method, which is less annoying than my method that required
    a conditional depending on whether 'date' was in the daytime or nighttime."""
    
    mid1,mid2=midnight(date, longitude, latitude)
    noon = 0.5*(mid1+mid2)
    sunrise = so.bisect(solelev, mid1, noon, args=(longitude, latitude, solar_angular_radius))
    sunset = so.bisect(solelev, noon, mid2, args=(longitude, latitude, solar_angular_radius))
    return sunrise, sunset
    
def hms(h):
    """Converts float hours to integer hours, minutes, seconds. loses milliseconds"""
    hi = int(h)
    m = 60.*(h-hi)
    mi = int(m)
    s = 60.*(m-mi)
    si = int(s)
    return hi,mi,si
    
def str_hms(h, prefix="", suffix=""):
    """String formatted time prefix HH:MM:SS suffix"""
    h,m,s = hms(h)
    return("{0} {1}:{2}:{3} {4}".format(prefix, h,m,s, suffix))
    
def str_hm(h, prefix="", suffix=""):
    """String formatted time prefix HH:MM suffix"""
    h,m,s = hms(h)
    return("{0} {1}:{2} {3}".format(prefix, h,m, suffix))


def sun_angular_radius(jdate, solar_radius = 6.96342e8, one_au=1.496e11):
    """Calculate the angular size of the sun at the specified date. Assumes that
    solar radius is 6.9e8m, one AU is 1.496e11m"""
    #as Google usefully says, solar_radius = 1 solar radius
    #wikipedia solar radius 6.96342x10^5 km
    # 1 Au 1.496x10^8 km
    orbit_radius = marstime.heliocentric_distance(jdate) #in AU.
    angular_radius = solar_radius / (orbit_radius * one_au)
    angular_radius_degree = numpy.rad2deg(angular_radius)
    return angular_radius_degree
    
def plot_solar_elevation(args, mdate, xup, xdown, output_date):
    """PLots the solar zenith angle as a function of mean time on Mars
        highlights the sunrise and sunset times, colors and scales the markers appropriately.
        """
    #generate a number of points to plot
    x=mdate[0]+numpy.arange(args.number_of_points)/(float(args.number_of_points)-1)
    xh=marstime.Local_Mean_Solar_Time( west_longitude, x)

    #define the figure size and resolution so that we can scale the marker appropriately
    dpi_plot = 72.
    dpi_save=150.
    plot_size = 4.
    border = 0.12
    box_size = plot_size*(1.-2*border)
    resolution = box_size * dpi_plot /180. #pixels per degree

    elev = solelev(x,west_longitude, north_latitude)
    day = numpy.where(elev > -solar_angular_radius)
    night = numpy.where(elev < -solar_angular_radius)
    
    #scale the marker size if necessary
    if not args.use_marker_radius and solar_angular_radius > 0:
        markersize = 2*solar_angular_radius * resolution * args.scale_marker
    else:
        markersize = 2*args.marker_radius*resolution
    
    title_str = "Solar Elevation Angle for {date}".format(date = "MSD {0}".format(output_date) if args.msd else "{0} (UTC)".format(output_date))
    sunrise_str = str_hm(xup, prefix="Sunrise:", suffix="LMST")
    sunset_str = str_hm(xdown, prefix="Sunset:", suffix="LMST")
    #open the figure
    pl.figure(figsize=(plot_size,plot_size))
    pl.subplots_adjust(left=border, top=1.-border, right=1.-border, bottom=border)
    
    #plot markers
    pl.plot(xh[day], elev[day], markeredgecolor='gold', 
                 marker='o',ls='none',markerfacecolor='none',markersize=markersize)
    pl.plot(xh[night], elev[night], markeredgecolor='navy', 
                 marker='o',ls='none',markerfacecolor='none',markersize=markersize)
    #grid
    pl.plot([xup,xup],[-90,90],color='grey', ls='--')
    pl.plot([xdown,xdown],[-90,90],color='grey', ls='--')
    pl.plot([0,24],[0,0],color='grey', ls='--')
    #axes
    pl.ylim(-90,90)
    pl.yticks([-90,-45,0,45,90])
    pl.xticks([0,4,8,12,16,20,24])
    pl.xlim(0,24)
    #labels
    pl.title(title_str)
    pl.text(12,-45,sunrise_str, horizontalalignment='center', verticalalignment='center')
    pl.text(12,-55,sunset_str, horizontalalignment='center', verticalalignment='center')
    pl.xlabel("Time (LMST)")
    pl.ylabel("Elevation Angle")
    #save
    pl.savefig(args.filename, dpi=dpi_save)

def simple_julian_offset(indate):
    """Simple conversion from date to J2000 offset"""
    datetime_epoch = datetime.datetime(2000,1,1,12,0,0)
    date = indate-datetime_epoch
    jdate = date.days + date.seconds/86400.
    return jdate
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plots and calculates sunrise/sunset times for a spherical flat Mars")
    parser.add_argument("date",type=str, nargs="?",
            help="Earth date in ISO format YYYY/MM/DD or MSD in DDDDD")
    parser.add_argument("--msd","-m", action='store_true', 
            help="Use Mars Solar Date instead of Earth Date")
    parser.add_argument("--ignore_solar_radius", action='store_true',
            help="calculate the time for the solar center, not the 'top' edge.")
    parser.add_argument("--longitude","-x",default=137.44,type=float,
            help="East Longitude")
    parser.add_argument("--latitude","-y",default=-4.5, type=float,
            help="North Latitude")
    parser.add_argument("--scale_marker","-s",default=1.0, type=float,
            help="Scale marker size")
    parser.add_argument("--use_marker_radius",action="store_true",
            help="Use the marker radius defined in marker_radius, instead of scaling properly")
    parser.add_argument("--marker_radius",type=float, default=2.0,
            help="set the marker radius in degrees, requires --use_marker_radius")
    parser.add_argument("--number_of_points","-n",type=int, default=72,
            help="set the number of markers to plot, evenly spaced throughout the day")
    parser.add_argument("--filename",type=str, default="sunrise.png",
            help="set the output filename and type")
    args = parser.parse_args()
    
    
    if args.date is None: #nodate, use now
        default_date = datetime.datetime.now()
        jdate = simple_julian_offset(default_date)
        output_date = default_date.strftime("%Y/%m/%d")
    elif args.msd: #Mars solar date
        output_date = args.date
        jdate = marstime.j2000_from_Mars_Solar_Date(args.date)
    else: #earth date
        output_date = args.date
        jdate = simple_julian_offset(datetime.datetime.strptime(args.date, "%Y/%m/%d"))
     
    #convert to west longitude
    west_longitude = marstime.east_to_west(args.longitude)
    north_latitude = args.latitude
    #find the midnight times
    mdate = midnight(jdate, west_longitude, north_latitude)

    #calculate the angular radius of the Sun to offset the bissect calculation
    solar_angular_radius = 0.0
    if not args.ignore_solar_radius:
        solar_angular_radius = sun_angular_radius(jdate)
    
    sup, sdown = sunrise_sunset(jdate, west_longitude, north_latitude, solar_angular_radius = solar_angular_radius)
    xup = marstime.Local_Mean_Solar_Time( west_longitude, sup) #sunrise
    xdown = marstime.Local_Mean_Solar_Time( west_longitude, sdown) #sunset
    
    print str_hms(xup, prefix="Sunrise at LMST of ")
    print str_hms(xdown, prefix="Sunset at LMST of ")
    print str_hms(marstime.Local_True_Solar_Time( west_longitude, sup), prefix="Sunrise at LTST of ")
    print str_hms(marstime.Local_True_Solar_Time( west_longitude, sdown), prefix="Sunset at LTST of ")

    
    #make a plot
    plot_solar_elevation(args, mdate, xup, xdown, output_date)
