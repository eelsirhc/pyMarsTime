"""Mars24 algorithm

Mars Calendar and orbit calculation based on Allison and McEwan (2000), Allison (1997)

Allison, M., and M. McEwen 2000. A post-Pathfinder evaluation of aerocentric solar coordinates with improved timing recipes for Mars seasonal/diurnal climate studies. Planet. Space Sci. 48, 215-235

Allison, M. 1997. Accurate analytic representations of solar time and seasons on Mars with applications to the Pathfinder/Surveyor missions. Geophys. Res. Lett. 24, 1967-1970.

http://www.giss.nasa.gov/tools/mars24/

"""

import time
try:
    import numpy as np
    use_numpy=True
except:
    use_numpy=False
    import math as np

def west_to_east(west):
    """Convert from aerographic west longitude to aerocentric east longitude,
    or vice versa. I may have made those words up"""
    east = 360 - west + 0.271
    return east % 360.

def east_to_west(east):
    """Interface, calls west_to_east to convert longitude"""
    return west_to_east(east)

def j2000_epoch():
    """Returns the j2000 epoch as a float"""
    return 2451545.0

def mills():
    """Returns the current time in milliseconds since Jan 1 1970"""
    return time.time()*1000.

def julian(m=None):
    """Returns the julian day number given milliseconds since Jan 1 1970"""
    if m is None:
        m= mills()
    return 2440587.5 + (m/8.64e7)

def utc_to_tt_offset(jday=None):
    """Returns the offset in seconds from a julian date in Terrestrial Time (TT)
    to a Julian day in Coordinated Universal Time (UTC)"""

    if use_numpy:
        return utc_to_tt_offset_numpy(jday)
    else:
        return utc_to_tt_offset_math(jday)

def utc_to_tt_offset_math(jday=None):
    """Returns the offset in seconds from a julian date in Terrestrial Time (TT)
    to a Julian day in Coordinated Universal Time (UTC) [MATH]"""
    if jday is None:
        jday_np=julian()
    else:
        jday_np = jday
    
    jday_min = 2441317.5
    jday_vals = [     -2441317.5, 0.,    182.,    366.,
                       731.,   1096.,   1461.,   1827.,
                       2192.,   2557.,   2922.,   3469.,
                       3834.,   4199.,   4930.,   5844.,
                       6575.,   6940.,   7487.,   7852.,
                       8217.,   8766.,   9313.,   9862.,
                       12419.,  13515.]

    offset_min = 32.184
    offset_vals = [-32.184,10., 11.0, 12.0, 13.0,
                    14.0, 15.0, 16.0, 17.0, 18.0,
                    19.0, 20.0, 21.0, 22.0, 23.0,
                    24.0, 25.0, 26.0, 27.0, 28.0,
                    29.0, 30.0, 31.0, 32.0, 33.0,
                    34.0]

    if jday_np <= jday_min+jday_vals[0]:
        return offset_min+offset_vals[0]
    else:
        for i in range(1, len(offset_vals)):
            if (jday_min+jday_vals[i] <= jday_np) and\
                    (jday_min+jday_vals[i+1] > jday_np) :
                break                
        return offset_min+offset_vals[i]


def utc_to_tt_offset_numpy(jday=None):
    """Returns the offset in seconds from a julian date in Terrestrial Time (TT)
    to a Julian day in Coordinated Universal Time (UTC) [NUMPY]"""
    if jday is None:
        jday_np=julian()
    elif type(jday) is not np.ndarray:
        jday_np = np.array(jday)
    else:
        jday_np = jday
        
    #offsets=np.zeros(jday.shape)


    jday_vals = 2441317.5 +\
        np.array([     -2441317.5, 0.,    182.,    366.,
                           731.,   1096.,   1461.,   1827.,
                           2192.,   2557.,   2922.,   3469.,
                           3834.,   4199.,   4930.,   5844.,
                           6575.,   6940.,   7487.,   7852.,
                           8217.,   8766.,   9313.,   9862.,
                           12419.,  13515.])

    offset_vals = 32.184 + np.array([-32.184,10., 11.0, 12.0, 13.0,
                                         14.0, 15.0, 16.0, 17.0, 18.0,
                                         19.0, 20.0, 21.0, 22.0, 23.0,
                                         24.0, 25.0, 26.0, 27.0, 28.0,
                                         29.0, 30.0, 31.0, 32.0, 33.0,
                                         34.0])

    try:
        offset = offset_vals[
            np.clip(np.digitize(jday_np, jday_vals)
                       ,1,offset_vals.size) -1]
    except:
        offset = offset_vals[
            np.clip(np.digitize([jday_np], jday_vals),
                       1,offset_vals.size) -1]
        offset=offset[0]

        
    return offset# 64.184


def julian_tt(jday_utc=None):
    """Returns the TT Julian day given a UTC Julian day"""
    if jday_utc is None:
        jday_utc = julian()
    
    jdtt = jday_utc + utc_to_tt_offset(jday_utc)/86400.
    return jdtt

def j2000_offset_tt(jday_tt=None):
    """Returns the julian day offset since the J2000 epoch"""
    if jday_tt is None:
        jday_tt = julian_tt()

    return (jday_tt - j2000_epoch())

def Mars_Mean_Anomaly(j2000_ott=None):
    """Calculates the Mars Mean Anomaly given a j2000 julian day offset"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    M = 19.3870 + 0.52402075 * j2000_ott
    return M % 360.

def FMS_Angle(j2000_ott=None):
    """Returns the Fictional Mean Sun angle"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()
        
    alpha_fms = 270.3863 + 0.52403840 * j2000_ott
    return alpha_fms % 360.

def alpha_perturbs(j2000_ott=None):
    """Returns the perturbations to apply to the FMS Angle from orbital perturbations"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()
    
    array_A = [0.0071, 0.0057, 0.0039, 0.0037, 0.0021, 0.0020, 0.0018]
    array_tau = [2.2353, 2.7543, 1.1177, 15.7866, 2.1354, 2.4694, 32.8493]
    array_phi = [49.409, 168.173, 191.837, 21.736, 15.704, 95.528, 49.095]

    pbs = 0
    for (A,tau,phi) in zip(array_A, array_tau, array_phi):
        pbs+=A*np.cos(((0.985626 * j2000_ott/tau) + phi)*np.pi/180.)

    return pbs

def equation_of_center(j2000_ott=None):
    """The true anomaly (v) - the Mean anomaly (M)"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    M = Mars_Mean_Anomaly(j2000_ott)*np.pi/180.
    pbs = alpha_perturbs(j2000_ott)

    val = (10.691 + 3.0e-7 * j2000_ott)*np.sin(M)\
        + 0.6230 * np.sin(2*M)\
        + 0.0500 * np.sin(3*M)\
        + 0.0050 * np.sin(4*M)\
        + 0.0005 * np.sin(5*M) \
        + pbs

    return val

def Mars_Ls(j2000_ott=None):
    """Returns the Areocentric solar longitude (aka Ls)"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    alpha = FMS_Angle(j2000_ott)
    v_m   = equation_of_center(j2000_ott)

    ls = (alpha + v_m)
    ls = ls % 360
    return ls

def equation_of_time(j2000_ott=None):
    """Equation of Time, to convert between Local Mean Solar Time
    and Local True Solar Time, and make pretty analemma plots"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    ls = Mars_Ls(j2000_ott)*np.pi/180.

    EOT = 2.861*np.sin(2*ls)\
        - 0.071 * np.sin(4*ls)\
        + 0.002 * np.sin(6*ls) - equation_of_center(j2000_ott)

    return EOT

def j2000_from_Mars_Solar_Date(msd=0):
    """Returns j2000 based on MSD"""
    j2000_ott = ((msd + 0.00096 - 44796.0) * 1.027491252)+4.5
    return j2000_ott

def j2000_ott_from_Mars_Solar_Date(msd=0):
    """Returns j2000 offset based on MSD"""
    j2000 = j2000_from_Mars_Solar_Date(msd)
    j2000_ott = julian_tt(j2000+j2000_epoch())
    return j2000_ott-j2000_epoch()

def Mars_Solar_Date(j2000_ott = None):
    """Return the Mars Solar date"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
        
    MSD = (((j2000_ott - 4.5)/1.027491252) + 44796.0 - 0.00096)
    return MSD
    
def Clancy_Year(j2000_ott = None):
    """Returns the Mars Year date based on the reference date from Clancy(2000): 1955 April 11, 11am"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
    ref1955_4_11_11am = -16336.0416 #j200_offset_tt reference
    year = np.floor(1 + (j2000_ott-ref1955_4_11_11am)/(686.978))
    return year
        
def Coordinated_Mars_Time(j2000_ott = None):
    """The Mean Solar Time at the Prime Meridian"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
        
    MTC = 24 * (((j2000_ott - 4.5)/1.027491252) + 44796.0 - 0.00096)
    MTC = MTC % 24
    return MTC

def Local_Mean_Solar_Time(longitude=0, j2000_ott=None):
    """The Local Mean Solar Time given a planetographic longitude"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
        
    MTC = Coordinated_Mars_Time(j2000_ott)
    LMST = MTC - longitude * (24/360.)
    LMST = LMST % 24
    return LMST

def Local_True_Solar_Time(longitude=0, j2000_ott=None):
    """Local true solar time is the Mean solar time + equation of time perturbation"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
        
    eot = equation_of_time(j2000_ott)
    lmst = Local_Mean_Solar_Time(longitude, j2000_ott)
    ltst = lmst + eot*(24/360.)
    ltst = ltst % 24
    return ltst

def subsolar_longitude(j2000_ott=None):
    """returns the longitude of the subsolar point for a given julian day."""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)

    MTC = Coordinated_Mars_Time(j2000_ott)
    EOT = equation_of_time(j2000_ott)*24/360.
    subsol = (MTC + EOT)*(360/24.) + 180.
    return subsol % 360.

def solar_declination(ls=None):
    """Returns the solar declination"""
    if ls is None:
        ls= Mars_Ls()
    ls1 = ls * np.pi/180.

    if use_numpy:
        dec = np.arcsin(0.42565 * np.sin(ls1)) + 0.25*(np.pi/180) * np.sin(ls1)
    else:
        dec = np.asin(0.42565 * np.sin(ls1)) + 0.25*(np.pi/180) * np.sin(ls1)
    dec = dec * 180. / np.pi
    return dec

def heliocentric_distance(j2000_ott=None):
    """Instantaneous orbital radius"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    M = Mars_Mean_Anomaly(j2000_ott)*np.pi/180.
    
    rm = 1.523679 * \
        (1.00436 - 0.09309*np.cos(M) \
             - 0.004336*np.cos(2*M) \
             - 0.00031*np.cos(3*M)\
             - 0.00003*np.cos(4*M))

    return rm

def heliocentric_longitude(j2000_ott=None):
    """Heliocentric longitude, which is not Ls (offsets are different)"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt() 
    ls = Mars_Ls(j2000_ott)

    im = ls + 85.061 - \
        0.015 * np.sin((71+2*ls)*np.pi/180.) - \
        5.5e-6*j2000_ott
    
    return im % 360.


def heliocentric_latitude(j2000_ott=None):
    """Heliocentric Latitude, which is not Ls"""
    if j2000_ott is None:
        j2000_ott = j2000_offset_tt()

    ls        = Mars_Ls(j2000_ott)

    bm = -(1.8497 - 2.23e-5*j2000_ott) \
        * np.sin((ls - 144.50 + 2.57e-6*j2000_ott)*np.pi/180.)

    return bm

def hourangle(longitude=0, j2000_ott=None):
    """Hourangle is the longitude - subsolar longitude"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt()
        
    subsol = subsolar_longitude(j2000_ott)*np.pi/180.
    hourangle = longitude*np.pi/180. - subsol
    return hourangle

def solar_zenith(longitude=0,latitude=0, j2000_ott=None):
    """Zenith Angle, angle between sun and nadir"""
   
    if latitude > 90 or latitude < -90:
        raise ValueError("Latitude out of Bounds: {0}".format(latitude))
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt()
        
    ha = hourangle(longitude, j2000_ott)
    ls = Mars_Ls(j2000_ott)
    dec = solar_declination(ls)*np.pi/180

    cosZ = np.sin(dec) * np.sin(latitude*np.pi/180) + \
        np.cos(dec)*np.cos(latitude*np.pi/180.)*np.cos(ha)

    if use_numpy:
        Z = np.arccos(cosZ)*180./np.pi
    else:
        Z = np.acos(cosZ)*180./np.pi
    return Z

def solar_elevation(longitude=0, latitude=0, j2000_ott=None):
    """Elevation = 90-Zenith, angle between sun and flat surface """
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
        
    Z = solar_zenith(longitude, latitude, j2000_ott)
    return 90 - Z

def solar_azimuth(longitude=0, latitude=0, j2000_ott = None):
    """Azimuth Angle, between sun and north pole"""
    if j2000_ott is None:
        jday_tt = julian_tt()
        j2000_ott = j2000_offset_tt(jday_tt)
    
    ha = hourangle(longitude, j2000_ott)
    ls = Mars_Ls(j2000_ott)
    dec = solar_declination(ls)*np.pi/180.
    denom = (np.cos(latitude)*np.tan(dec)\
                 - np.sin(latitude)*np.cos(ha))

    num = np.sin(ha) 

    if use_numpy:
        az = (360+np.arctan2(num,denom)*180./np.pi) % 360.
    else:
        az = (360+np.atan2(num,denom)*180./np.pi) % 360.
    return az


if __name__=="__main__":

    mils = [947116800000,1073137591000]
    longitudes=[0., 184.702]
    latitudes=[0.,-14.640]

    for i in range(2):
        mil=mils[i]
        longitude=longitudes[i]
        latitude=latitudes[i]
        print "latitude = ", latitude
        print "longitude = ", longitude
        print "a1 = ", mil
        jdut = julian(mil)
        print "a2 = ", jdut
        tt_utc = utc_to_tt_offset(jdut)
        print "a4 = ", tt_utc
        jday_tt = julian_tt(jdut)
        print "a5 = ", jday_tt
        j2000_ott = j2000_offset_tt(jday_tt)
        print "a6 = ", j2000_ott
        m = Mars_Mean_Anomaly(j2000_ott)
        print "b1 = ", m
        alpha = FMS_Angle(j2000_ott)
        print "b2 = ", alpha
        pbs = alpha_perturbs(j2000_ott)
        print "b3 = ", pbs
        v_m = equation_of_center(j2000_ott)
        print "b4 = ", v_m
        ls = Mars_Ls(j2000_ott)
        print "b5 = ", ls
        eot = equation_of_time(j2000_ott)
        print "c1 = ", eot
        mtc = Coordinated_Mars_Time(j2000_ott)
        print "c2 = ", mtc
        lmst = Local_Mean_Solar_Time(longitude,j2000_ott)
        print "c3 = ", lmst
        ltst = Local_True_Solar_Time(longitude,j2000_ott)
        print "c4 = ", ltst
        subsol = subsolar_longitude(j2000_ott)
        print "c5 = ", subsol
        dec = solar_declination(ls)
        print "d1 = ", dec
        rm = heliocentric_distance(j2000_ott)
        print "d2 = ", rm
        im = heliocentric_longitude(j2000_ott)
        print "d3 = ", im
        bm = heliocentric_latitude(j2000_ott)
        print "d4 = ", bm
        sz = solar_zenith(longitude, latitude,j2000_ott)
        print "d5 = ", sz
        sz = solar_azimuth(longitude, latitude,j2000_ott)
        print "d6 = ", sz


