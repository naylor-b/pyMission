"""
MISSION ANALYSIS/TRAJECTORY OPTIMIZATION
This is the runscript used for the trajectory optimization problem.
For details regarding the setup of the analysis problem, see mission.py
The mission analysis and trajectory optimization tool was developed by:
    Jason Kao*
    John Hwang*

* University of Michigan Department of Aerospace Engineering,
  Multidisciplinary Design Optimization lab
  mdolab.engin.umich.edu

copyright July 2014
"""

import time

import numpy as np

from pyopt_driver import pyopt_driver
from pyMission.segment import MissionSegment


num_elem = 100
num_cp_init = 10
num_cp_max = 10#200
num_cp_step = 10
x_range = 150.0

# define bounds for the flight path angle
gamma_lb = numpy.tan(-10.0 * (np.pi/180.0))/1e-1
gamma_ub = numpy.tan(10.0 * (np.pi/180.0))/1e-1


start = time.time()
while num_cp <= num_cp_max:

    x_init = x_range * 1e3 * (1-np.cos(np.linspace(0, 1, num_cp)*np.pi))/2/1e6
    v_init = np.ones(num_cp)*2.3
    h_init = 1 * np.sin(np.pi * x_init / (x_range/1e3))

    model = set_as_top(MissionSegment(num_elem, num_cp, x_init))
    model.add('driver', pyopt_driver())
    model.driver.optimizer = 'SNOPT'
    self.add_parameter('h_pt', low=0.0, high=20.0)
    self.add_objective('wf_obj')
    self.add_constraint('SysHi.h_i = 0.0')
    self.add_constraint('SysHf.h_f = 0.0')
    self.add_constraint('Tmin < 0.0')
    self.add_constraint('Tmax < 0.0')
    self.add_constraint('SysGammaBspline.Gamma > gamma_lb')
    self.add_constraint('SysGammaBspline.Gamma < gamma_ub')

    model.h_pt = h_init
    model.v_pt = v_init

    # Pull velocity from BSpline instead of calculating it.
    model.SysSpeed.v_specified = True

    # Initial parameters
    model.S = 427.8/1e2
    model.ac_w = 210000*9.81/1e6
    model.thrust_sl = 1020000.0/1e6/3
    model.SFCSL = 8.951
    model.AR = 8.68
    model.oswald = 0.8