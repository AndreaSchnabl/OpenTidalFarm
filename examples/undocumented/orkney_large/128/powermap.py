from opentidalfarm import *
import sys
set_log_level(PROGRESS)

# Some domain information extracted from the geo file
site_x = 2000.
site_y = 1000.
site_x_start = 1.03068e+07 
site_y_start = 6.52276e+06 - site_y 

inflow_x = 8400.
inflow_y = -1390.
inflow_norm = (inflow_x**2 + inflow_y**2)**0.5
inflow_direction = [inflow_x/inflow_norm, inflow_y/inflow_norm]
print("inflow_direction: ", inflow_direction)

config = SteadyConfiguration("../mesh/earth_orkney_converted.xml", inflow_direction = inflow_direction) 
config.set_site_dimensions(site_x_start, site_x_start + site_x, site_y_start, site_y_start + site_y)
config.params['viscosity'] = 30.0
config.params['save_checkpoints'] = False
config.info()

# Place some turbines 
deploy_turbines(config, nx = 16, ny = 8)
config.params["turbine_friction"] = 0.5*numpy.array(config.params["turbine_friction"]) 

turbine_pos = [10306810.        ,   6521770.        ,  10306905.0475904 ,
        6521817.33940328,  10306940.90542021,   6521770.        ,
        10307069.5764367 ,   6521770.        ,  10307238.77732373,
        6521809.25612652,  10307323.16620786,   6521892.80425418,
        10307338.51611845,   6521918.58054101,  10307351.57622906,
        6521945.58941433,  10306840.        ,   6521770.        ,
        10306870.        ,   6521770.        ,  10306935.20237684,
        6521862.94284452,  10307135.15129106,   6521770.        ,
        10307264.44690585,   6521824.78265296,  10307284.80420606,
        6521846.81854618,  10307362.96193172,   6521973.34633893,
        10307373.16053287,   6522003.07852613,  10306900.        ,
        6521770.        ,  10306988.88086519,   6521770.        ,
        10307032.87477165,   6521770.        ,  10307195.15129106,
        6521770.        ,  10307212.78944411,   6521794.2672243 ,
        10307305.43603525,   6521868.60405183,  10307396.69459273,
        6522084.8277386 ,  10307672.34327195,   6522750.        ,
        10307104.77839875,   6521770.        ,  10307165.15129106,
        6521770.        ,  10307248.90489577,   6521770.        ,
        10307713.17461291,   6521770.        ,  10308061.24483636,
        6522040.70186749,  10308081.81241807,   6522097.0696045 ,
        10307383.84464772,   6522038.61019896,  10307805.8766179 ,
        6522750.        ,  10307444.77329409,   6521770.        ,
        10307337.24555004,   6521770.        ,  10307579.87357316,
        6521770.        ,  10307802.55247595,   6521770.        ,
        10308071.38173967,   6522068.93818279,  10308091.58709694,
        6522125.43367554,  10308100.74154968,   6522154.0045539 ,
        10307903.00870828,   6522750.        ,  10307867.34523232,
        6521770.        ,  10307986.71594791,   6521877.01869224,
        10308000.89895064,   6521903.45444793,  10308026.82034836,
        6521957.56898174,  10308050.5797327 ,   6522012.66083144,
        10308155.43971765,   6522387.43615461,  10308168.97071853,
        6522596.65602078,  10307985.20430792,   6522750.        ,
        10307915.25820767,   6521770.        ,  10307933.65300653,
        6521796.96082696,  10308013.6504213 ,   6521930.61009211,
        10308039.19292893,   6521984.90504172,  10308144.96725639,
        6522328.37252628,  10308159.23579793,   6522417.19579958,
        10308162.89632516,   6522446.97295129,  10308057.27187557,
        6522750.        ,  10308000.17101495,   6521770.        ,
        10307953.34081123,   6521825.03207929,  10308109.24828842,
        6522182.77368143,  10308139.36126096,   6522298.89992956,
        10308150.88124123,   6522357.78450361,  10308165.2069645 ,
        6522476.88567321,  10308167.26644424,   6522506.8151346 ,
        10308119.20947578,   6522750.        ,  10308126.49112453,
        6521770.        ,  10307971.2251802 ,   6521851.32678495,
        10308117.14151107,   6522211.72034299,  10308133.16610037,
        6522269.54627333,  10308182.98516195,   6522623.18153406,
        10308168.80534978,   6522661.50139268,  10308169.20765829,
        6522536.75227753,  10308157.25439103,   6522750.        ,
        10308270.61890185,   6521770.        ,  10308765.45491103,
        6521907.42959055,  10308125.14201022,   6522240.63609087,
        10308170.78992941,   6522566.71084706,  10308155.29158138,
        6522634.71701256,  10308162.78023248,   6522690.89016757,
        10308155.69061965,   6522720.04077911,  10308228.73797701,
        6522750.        ,  10308424.8558524 ,   6521770.        ,
        10308770.8308894 ,   6522003.70856404,  10308773.04099304,
        6522296.40191009,  10308739.0360747 ,   6522474.46730434,
        10308740.97101024,   6522533.4066916 ,  10308724.70746122,
        6522591.04237467,  10308686.80489788,   6522680.69493003,
        10308321.29632589,   6522750.        ,  10308548.2965282 ,
        6521770.        ,  10308775.35218728,   6522266.48917098,
        10308764.81873391,   6522355.71707763,  10308745.08479326,
        6522442.68266758,  10308777.46282022,   6522236.56277656,
        10308734.65531889,   6522562.73960228,  10308675.08512054,
        6522717.15025364,  10308432.70962471,   6522750.        ,
        10308645.09597156,   6521770.        ,  10308785.21225199,
        6521830.99068349,  10308784.92756445,   6522146.99073522,
        10308784.5797243 ,   6522176.98943392,  10308781.46590252,
        6522206.82859003,  10308712.88811452,   6522618.61598591,
        10308701.04344512,   6522647.00989673,  10308528.97092736,
        6522750.        ,  10308713.18171151,   6521770.        ,
        10308790.        ,   6521924.679027  ,  10308785.22493368,
        6522116.99199338,  10308767.06902013,   6522325.80150691,
        10308759.70316642,   6522385.28223141,  10308757.0435546 ,
        6522415.16717841,  10308768.75588863,   6522681.04777907,
        10308610.95745339,   6522750.        ,  10308760.        ,
        6521770.        ,  10308783.32791041,   6521860.93149942,
        10308779.16714427,   6521952.65491778,  10308790.        ,
        6521980.63080959,  10308785.27137131,   6522086.9917431 ,
        10308745.53518276,   6522503.75576127,  10308777.10476918,
        6522634.90921937,  10308667.16965067,   6522750.        ,
        10308790.        ,   6521770.        ,  10308787.06278387,
        6521801.04768118,  10308790.        ,   6521890.18015898,
        10308789.42307799,   6522027.25295304,  10308785.42685784,
        6522056.9866134 ,  10308766.88219959,   6522463.29767433,
        10308762.71888291,   6522720.55986918,  10308753.02665349,
        6522750.]
config.params['turbine_pos'] = numpy.reshape(turbine_pos, [-1, 2])

rf = ReducedFunctional(config)
J = rf.dj(turbine_pos, forget=False)
