import sys
sys.path.insert(0,"./")
import marstime

try:
    import numpy as np
    use_numpy=True
except:
    use_numpy=False
    import math as np
 

def within(val, low, high):
    return (val>low)&(val<high)

def within_error(val, equal, error):
    #print val, equal
    return (val>(equal-error))&(val<(equal+error))

def test_numpy_or_math():
    try :
        import numpy as np
        print()
        print("Using Numpy")
        return True
    except:
        import math as np
        print() 
        print("Using Math")
        return True
        
def test_west_to_east():
    assert marstime.west_to_east(360.0) == 0.0 #0.271
    assert marstime.west_to_east(540.0) == marstime.west_to_east(180.0)

def test_east_to_west():
    assert marstime.west_to_east(0.0) == marstime.east_to_west(0.0)

def test_j2000_epoch():
    assert marstime.j2000_epoch() == 2451545.0

def test_mills():
    a=marstime.mills()
    for a in range(100):
        pass
    b=marstime.mills()
    assert a<b

def test_julian():
    assert marstime.julian() > 2456203.
    assert marstime.julian(0) == 2440587.5
    assert marstime.julian(8.64e7) == 2440588.5
    assert marstime.julian(8.64e10) == marstime.julian(0)+1000


def test_utc_to_tt_offset():

    #assert marstime.utc_to_tt_offset_math() >=35.
    #assert marstime.utc_to_tt_offset_numpy() >=35.
    
    t =  marstime.j2000_epoch()
    #j2000 is Jan 1 2000, utc offset should be =32+32.184
    assert within_error(marstime.utc_to_tt_offset(t), 64.184, 1e-3)

    t = marstime.j2000_epoch() - 5*365.
    assert within_error(marstime.utc_to_tt_offset(t), 61.184, 1e-3)

    t=0
    assert within_error(marstime.utc_to_tt_offset(t), 0, 1e-3)

def test_julian_tt():
    assert marstime.julian_tt() > 2456203.
    assert marstime.julian_tt(0) == 0
    v = marstime.julian_tt(marstime.j2000_epoch())-marstime.j2000_epoch()
    assert (v>64.183/86400.)&(v<64.185/86400.)

def test_j2000_offset_tt():
    assert marstime.j2000_offset_tt() > 2456203.-2451545.
    assert marstime.j2000_offset_tt(marstime.j2000_epoch())==0
    assert marstime.j2000_offset_tt(2451645)==100

def test_Mars_Mean_Anomaly():
    assert within(marstime.Mars_Mean_Anomaly(),0.0,360.0)
    assert within_error(marstime.Mars_Mean_Anomaly(0.0),19.387,1e-4)
    assert within_error(marstime.Mars_Mean_Anomaly(1000.0),183.4077, 1e-4)

def test_FMS_Angle():
    assert within(marstime.FMS_Angle(),0.0,360.0)
    assert within_error(marstime.FMS_Angle(0.0), 270.3863, 1e-4)
    assert within_error(marstime.FMS_Angle(1000.0), 74.4247, 1e-4)

def test_alpha_perturbs():
    assert within_error(marstime.alpha_perturbs(0.0), 0.001668,2e-5 )
    assert within_error(marstime.alpha_perturbs(1000.0), -0.007903, 2e-5)

def test_equation_of_center():
    assert within_error(marstime.equation_of_center(0.0), 3.98852, 2e-5)
    assert within_error(marstime.equation_of_center(1000.0),-0.57731, 2e-5)

def test_Mars_Ls():
    assert within(marstime.Mars_Ls(),0.,360.)
    assert within_error(marstime.Mars_Ls(4120),273,0.5)
    assert within_error(marstime.Mars_Ls(0),274.37,1e-2)
    assert within_error(marstime.Mars_Ls(1000),73.847,1e-2)

def test_equation_of_time():
    assert within_error(marstime.equation_of_time(0.0), -4.44596,1e-5)
    assert within_error(marstime.equation_of_time(1000.0), 2.17244,1e-5)

def test_j2000_from_Mars_Solar_Date():
    assert within_error(marstime.j2000_from_Mars_Solar_Date(44795.99904), 4.5,1e-2)
    assert within_error(marstime.j2000_from_Mars_Solar_Date(0), -46022.997,1e-3)

def test_j2000_ott_from_Mars_Solar_Date():
    assert within_error(marstime.j2000_ott_from_Mars_Solar_Date(0.0), -46022.997, 1e-3)
    assert within_error(marstime.j2000_ott_from_Mars_Solar_Date(1000), -44995.505, 1e-3)
    t=marstime.Mars_Solar_Date(0)
    assert within_error(marstime.j2000_ott_from_Mars_Solar_Date(t), 0.0007428,1e-5)

def test_Clancy_Year():
    #j2000_epoch = 0.0 offset
    assert within_error(marstime.Clancy_Year(0.0), 24, 0.5)
    #1955 april 11th 12pm, julian date = 2435208.955
    #offset = -16336.0
    #my 1
    assert within_error(marstime.Clancy_Year(-16335.0), 1, 0.5)
    #6 months later, same year
    assert within_error(marstime.Clancy_Year(-16200.0), 1, 0.5)
    #6 months earlier, 0 year
    assert within_error(marstime.Clancy_Year(-16500.0), 0, 0.5)

def test_marstime_Year():
    #j2000_epoch = 0.0 offset
    assert within_error(marstime.Mars_Year(0.0), 24, 0.5)
    #1955 april 11th 12pm, julian date = 2435208.955
    #offset = -16336.0
    #my 1
    assert within_error(marstime.Mars_Year(-16335.0), 1, 0.5)
    #6 months later, same year
    assert within_error(marstime.Mars_Year(-16200.0), 1, 0.5)
    #6 months earlier, 0 year
    assert within_error(marstime.Mars_Year(-16500.0), 0, 0.5)
    assert within_error(marstime.Mars_Year(-17025.0), -1, 0.5)

    
def test_Coordinated_Mars_Time():
    assert within_error(marstime.Coordinated_Mars_Time(0.0), 14.8665, 2e-4)
    #1 mars hour later
    assert within_error(marstime.Coordinated_Mars_Time(3698.9685/86400.), 15.8665, 2e-4)
    #1 mars day later
    assert within_error(marstime.Coordinated_Mars_Time(88775.244/86400.), 14.8665, 2e-4)
    

def test_Local_Mean_Solar_Time():
    assert within_error(marstime.Local_Mean_Solar_Time(0,0)
                        -marstime.Local_Mean_Solar_Time(15,0), 1.0, 1e-2)


def test_Local_True_Solar_Time():
    assert within_error(marstime.Local_True_Solar_Time(0,0)
                        -marstime.Local_True_Solar_Time(15,0), 1.0, 1e-2)

def test_subsolar_longitude():
    assert within_error(marstime.subsolar_longitude(0.0)-
                        marstime.subsolar_longitude(3698.9685/86400.),
                        -14.99, 1e-2)

def test_solar_declination():
    assert within_error(marstime.solar_declination(0.0)  ,0.0,1e-3)
    assert within_error(marstime.solar_declination(90.0) ,25.441,1e-3)
    assert within_error(marstime.solar_declination(180.0),0.0,1e-3)
    assert within_error(marstime.solar_declination(270.0),-25.441,1e-3)

def test_heliocentric_distance():
    assert within_error(marstime.heliocentric_distance(0.0), 1.391,1e-3)
    assert within_error(marstime.heliocentric_distance(1000.0), 1.665,1e-3)

def test_heliocentric_longitude():
    assert within_error(marstime.heliocentric_longitude(0.0), 359.45,1e-3)
    assert within_error(marstime.heliocentric_longitude(1000.0), 158.912,1e-3)

def test_heliocentric_latitude():
    assert within_error(marstime.heliocentric_latitude(0.0), -1.4195,1e-3)
    assert within_error(marstime.heliocentric_latitude(1000.0), 1.724,1e-3)

def test_hourangle():
    assert within_error(marstime.hourangle(0.0,0.0), -0.67287, 1e-4)
    assert within_error((marstime.hourangle(15.0,0.0)-
                        marstime.hourangle(0.0,0.0))*180/np.pi
                        , 15,1e-3)

def test_solar_zenith():
    j2day=151.2737 #ls=0
    x = marstime.subsolar_longitude(j2day)
    assert within_error(x,114.113,1e-3)
    assert within_error(marstime.solar_zenith(x,0,j2day),0,1e-4)

def test_solar_zenith_and_elevation():
    j2day=151.2737 #ls=0
    x = marstime.subsolar_longitude(j2day)
    assert within_error(x,114.113,1e-3)
    assert within_error(marstime.solar_zenith(x,0,j2day),0,1e-4)
    assert within_error(marstime.solar_zenith(x,15,j2day),15,1e-4)
    assert within_error(marstime.solar_zenith(x+15,0,j2day),15,1e-4)
    assert within_error(marstime.solar_elevation(x,45,j2day)-
                        marstime.solar_zenith(x,45,j2day)
                        ,0,1e-4)

    j2day=349.8778 #ls=90
    x = marstime.subsolar_longitude(j2day)
    assert within_error(x,232.7006,1e-3)
    assert within_error(marstime.solar_zenith(x,0,j2day),25.441,1e-3)
    assert within_error(marstime.solar_elevation(x,0,j2day),64.5581,1e-4)
    try:
        a= marstime.solar_zenith(0,100,0)
        assert False
    except ValueError:
        assert True
    except:
        assert False

    try:
        a= marstime.solar_zenith(0,-100,0)
        assert False
    except ValueError:
        assert True
    except:
        assert False

def test_solar_azimuth():
    j2day=151.2737 #ls=0
    x = marstime.subsolar_longitude(j2day)
    assert within_error(x,114.113,1e-3)
    assert within_error(marstime.solar_azimuth(x +10,0,j2day),90,1e-3)
    assert within_error(marstime.solar_azimuth(x-10,0,j2day),270,1e-3)
    assert within_error(marstime.solar_azimuth(x,45,j2day),180,1e-3)
    assert within_error(marstime.solar_azimuth(x,-45,j2day),0,1e-3)

def test_on_mills():
    mills=959804082*1e3
    j2k_ott = marstime.j2000_offset_tt(marstime.julian_tt(marstime.julian(mills)))
    assert within_error(j2k_ott, 151.344, 0.001)
    ls = marstime.Mars_Ls(j2k_ott)
    cy = marstime.Clancy_Year(j2k_ott)
    my = marstime.Mars_Year(j2k_ott)
    assert within_error(ls, 0.0352, 0.001)
    assert within_error(cy, 24, 0.5)
    assert within_error(my, 25, 0.5)
    

def test_midnight_crossing():
    mil = 947116800000
    longitude=0.
    latitude=0.
    jdut = marstime.julian(mil)
    assert within_error(jdut,2451549.5,1e-3)
    
    tt_utc = marstime.utc_to_tt_offset(jdut)
    assert within_error(tt_utc,64.184,1e-3)
    
    jday_tt = marstime.julian_tt(jdut)
    assert within_error(jday_tt, 2451549.50074,1e-3)
    
    j2000_ott = marstime.j2000_offset_tt(jday_tt)
    assert within_error(j2000_ott, 4.50074, 1e-3)

    m = marstime.Mars_Mean_Anomaly(j2000_ott)
    assert within_error(m, 21.74548,1e3)

    alpha = marstime.FMS_Angle(j2000_ott)
    assert within_error(alpha, 272.74486,1e-4)

    pbs = marstime.alpha_perturbs(j2000_ott)
    assert within_error(pbs, 0.00142, 1e-3)

    v_m = marstime.equation_of_center(j2000_ott)
    assert within_error(v_m, 4.44191, 1e-4)

    ls = marstime.Mars_Ls(j2000_ott)
    assert within_error(ls, 277.18677, 1e-4)

    eot = marstime.equation_of_time(j2000_ott)
    assert within_error(eot, -5.18764, 1e-4)

    mtc = marstime.Coordinated_Mars_Time(j2000_ott)
    assert within_error(mtc,23.99431, 1e-4)

    lmst = marstime.Local_Mean_Solar_Time(longitude,j2000_ott)
    assert within_error(lmst, 23.99431, 1e-4)

    ltst = marstime.Local_True_Solar_Time(longitude,j2000_ott)
    assert within_error(ltst, 23.64847, 1e-4)

    subsol = marstime.subsolar_longitude(j2000_ott)
    assert within_error(subsol, 174.72703,1e-4)

    dec = marstime.solar_declination(ls)
    assert within_error(dec, -25.22838,1e-4)

    rm = marstime.heliocentric_distance(j2000_ott)
    assert within_error(rm, 1.39358, 1e-4)

    im = marstime.heliocentric_longitude(j2000_ott)
    assert within_error(im, 2.26270, 1e-4)

    bm = marstime.heliocentric_latitude(j2000_ott)
    assert within_error(bm, -1.35959, 1e-4)

    sz = marstime.solar_zenith(longitude, latitude,j2000_ott)
    assert within_error(sz, 154.26182, 1e-4)

    sa = marstime.solar_azimuth(longitude, latitude,j2000_ott)
    assert within_error(sa, 191.03687,1e-4)


def test_spirit_landing():
    mil = 1073137591000
    longitude=184.702
    latitude=-14.460
    jdut = marstime.julian(mil)
    assert within_error(jdut,2453008.07397,1e-3)
    
    tt_utc = marstime.utc_to_tt_offset(jdut)
    assert within_error(tt_utc,64.184,1e-3)
    
    jday_tt = marstime.julian_tt(jdut)
    assert within_error(jday_tt, 2453008.07471,1e-3)
    
    j2000_ott = marstime.j2000_offset_tt(jday_tt)
    assert within_error(j2000_ott, 1463.07471, 1e-3)

    m = marstime.Mars_Mean_Anomaly(j2000_ott)
    assert within_error(m, 66.06851,1e3)

    alpha = marstime.FMS_Angle(j2000_ott)
    assert within_error(alpha, 317.09363,1e-4)

    pbs = marstime.alpha_perturbs(j2000_ott)
    assert within_error(pbs, 0.01614, 1e-3)

    v_m = marstime.equation_of_center(j2000_ott)
    assert within_error(v_m, 10.22959, 1e-4)

    ls = marstime.Mars_Ls(j2000_ott)
    assert within_error(ls, 327.32322, 1e-4)

    eot = marstime.equation_of_time(j2000_ott)
    assert within_error(eot, -12.77557, 1e-4)

    mtc = marstime.Coordinated_Mars_Time(j2000_ott)
    assert within_error(mtc,13.16542, 1e-4)

    lmst = marstime.Local_Mean_Solar_Time(longitude,j2000_ott)
    assert within_error(lmst, 0.85196, 1e-4)

    ltst = marstime.Local_True_Solar_Time(longitude,j2000_ott)
    assert within_error(ltst, 0.00025, 1e-5)

    subsol = marstime.subsolar_longitude(j2000_ott)
    assert within_error(subsol, 4.70575,1e-4)

    dec = marstime.solar_declination(ls)
    assert within_error(dec, -13.42105,1e-2)

    rm = marstime.heliocentric_distance(j2000_ott)
    assert within_error(rm,1.47767, 1e-4)

    im = marstime.heliocentric_longitude(j2000_ott)
    assert within_error(im, 52.37469, 1e-4)

    bm = marstime.heliocentric_latitude(j2000_ott)
    assert within_error(bm, 0.08962, 1e-4)

#This is where we deviate significantly from the original marstime algorithm.
    sz = marstime.solar_zenith(longitude, latitude,j2000_ott)
    assert within_error(sz, 151.93895, 0.2)

    sa = marstime.solar_azimuth(longitude, latitude,j2000_ott)
    assert within_error(sa, 179.99225,1e-2)


def test_math_vs_numpy():
    try:
        import numpy as np
        use_numpy=True
    except:
        use_numpy=False
    
    if use_numpy:
        mil = 1073137591000
        jdut = marstime.julian(mil)
        marstime.use_numpy = False
        tt_math = marstime.utc_to_tt_offset(jdut)

        marstime.use_numpy = True
        tt_numpy = marstime.utc_to_tt_offset(jdut)
        assert within_error(tt_math,tt_numpy,1e-3)

        j2k = marstime.j2000_offset_tt(marstime.julian_tt(jdut))
        marstime.use_numpy = False
        mym = marstime.Mars_Year(j2k)
        marstime.use_numpy = True
        myn = marstime.Mars_Year(j2k)
        assert within_error(mym,myn,0.5)
#----        
        
        mil=0
        jdut = marstime.julian(mil)
        marstime.use_numpy = False
        tt_math = marstime.utc_to_tt_offset(jdut)

        marstime.use_numpy = True
        tt_numpy = marstime.utc_to_tt_offset(jdut)
        assert within_error(tt_math,tt_numpy,1e-4)

        j2k = marstime.j2000_offset_tt(marstime.julian_tt(jdut))
        marstime.use_numpy = False
        mym = marstime.Mars_Year(j2k)
        marstime.use_numpy = True
        myn = marstime.Mars_Year(j2k)
        assert within_error(mym,myn,0.5)

        

        
