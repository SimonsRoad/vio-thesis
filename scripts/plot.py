#!/usr/bin/env python

import os, sys, inspect
import numpy as np
import matplotlib.pyplot as plt

from trajectory_toolkit.TimedData import TimedData
from trajectory_toolkit.Plotter import Plotter
from trajectory_toolkit.VIEvaluator import VIEvaluator
from trajectory_toolkit import Quaternion
from trajectory_toolkit import Utils
from trajectory_toolkit import RosDataAcquisition


def load_one_comparison(bag_file_name, odometry_topic_name):
    td_visual = TimedData()
    td_vicon = TimedData()

    eval = VIEvaluator()
    eval.bag = bag_file_name
    eval.odomTopic = odometry_topic_name
    eval.gtFile = bag_file_name
    eval.gtTopic = '/vicon/firefly_sbx/firefly_sbx'
    eval.alignMode = 0     # Align body frames to the same inertial (not viceversa)
    eval.derMode = 0    # Compute analytical derivatives for visual data as well

    eval.initTimedData(td_visual)
    eval.initTimedDataGT(td_vicon)
    eval.acquireData()
    eval.acquireDataGT()
    eval.getAllDerivatives()
    eval.alignTime()
    eval.alignBodyFrame()
    eval.alignInertialFrame()
    eval.getYpr()
    eval.evaluateSigmaBounds()

    return td_visual, td_vicon


def make_bag_path(filename):
    return os.path.join(os.path.expanduser('~'), 'data/out', filename)

plotterPos = Plotter(-1, [1,1],'',['time[s]'],['x[m]'],10000)

td_visual, td_vicon = load_one_comparison(make_bag_path('rovio_traj.bag'), '/rovio/odometry')
plotterPos.addDataToSubplot(td_visual, 1, 1, '', 'Rovio')
plotterPos.addDataToSubplot(td_vicon, 1, 1, '', 'Truth')

# store data
import pickle
f1 = open('td_visual.pckl', 'wb')
f2 = open('td_vicon.pckl', 'wb')
pickle.dump(td_visual, f1)
pickle.dump(td_vicon, f2)
f1.close()
f2.close()

quit()

# copy and paste to get vars in repl
import pickle
f1 = open('td_visual.pckl', 'rb')
f2 = open('td_vicon.pckl', 'rb')
td_visual = pickle.load(f1)
td_vicon = pickle.load(f2)