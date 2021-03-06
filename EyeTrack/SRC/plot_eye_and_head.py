'''
Created on Jul 5, 2016

@author: Victoria Young
'''

import os
import pickle
import numpy as np
#import plot_videos as pltv
import matplotlib.pyplot as plt

def read_eyetracker_data( recording_dir ):
    """ Based on eyetracker data """
    p_file = os.path.join( recording_dir, "pupil_data")
    with open(p_file, 'rb') as handle:
        data = handle.read()
        pupil_data = pickle.loads(data)
    # print( pupil_data.keys() )
    # print( len(pupil_data["pupil_positions"]) )
    # print( pupil_data["pupil_positions"][0] )
    # print( pupil_data["gaze_positions"][0] )
    # print( pupil_data["gaze_positions"][0]["base"][0]['norm_pos'] )
    return pupil_data

def get_data( num ):
    permPath = '/Users/ei-student/Documents/Origami Tests'
    eyePath = os.path.join(permPath, num, num + '_eyetracker')
    eyeData = read_eyetracker_data( eyePath )
#    headPath = os.path.join(permPath, 'head_movement', num, num + '_headtrackerdata.log')
#    headData = np.genfromtxt( headPath, delimiter=" ", invalid_raise=False )
    fixData = get_fixations( eyePath )
    #with open(headPath, 'rb') as data:
    #    for line in data:
    #        line = line.split()
    #        headData.append(line)
    return fixData, eyeData

def get_fixations( path ):
    fixPath = os.path.join(path, 'exports', 'fixations.csv')
    fixations = np.genfromtxt(fixPath, delimiter = ',')
    fixations = np.asarray(fixations)
    return fixations

def get_linAccHead_data( hData, times ):
    lin = []
    for i in range(len(hData)):
        try:
            lin.append([times[i], hData[i][20], hData[i][21], hData[i][22]])
        except IndexError:
            print("Upps")
    return np.array(lin)

def get_pos_data( data ):
    """Timestamp in Realtime, norm_pos, realtime gaze on Computer"""
    dataList = []
    initialTime = data["gaze_positions"][0]['timestamp']
    for item in data["gaze_positions"]:
        useTime = item['timestamp'] - initialTime
        dataList.append([useTime, item["base"][0]['norm_pos'][0] ,item["base"][0]['norm_pos'][1], item['norm_pos'][0], item['norm_pos'][1]])
    return np.array(dataList)

def linVelocities( data ):
    times = data[:, 0]
    x = data[:, 1]
    y = data[:, 2]
    timeVel = []
    velocity = []
    points = []
    xVelocity = []
    yVelocity = []
    appended = False
    for i in range(len(times) - 1):
        velocityCalc = (abs(((((x[i+1] - x[i]) ** 2) + ((y[i+1] - y[i]) ** 2)) ** 0.5)  / (times[i + 1] - times[i])))
        xVelocity.append((x[i+1] - x[i]) / (times[i + 1] - times[i]))
        yVelocity.append((y[i+1] - y[i]) / (times[i + 1] - times[i]))
        velocity.append(velocityCalc)
        if appended == False:
            points.append([x[i], y[i]])
            appended = True
        points.append([x[i+1], y[i+1]])
        timeVel.append((times[i + 1] + times[i]) / 2)
    # print "Linear Velocity"
    # for item in velocity:
    #     print item
    return timeVel, velocity, xVelocity, yVelocity, points

def get_normal_time( trackData ):
    initialTime = trackData[0][0]
    nTime = []
    for item in trackData:
            nTime.append(float(item[0]) - float(initialTime))
    return nTime

if __name__ == '__main__':
    
    fixations1, eyeDat1 = get_data( 'p02' )
    fixations2, eyeDat2 = get_data( 'p04' )
#    signalData = []
#    eyeUse = get_pos_data( eyeData )
#    times, vels, xVels, yVels, pts = linVelocities( eyeUse )
#    for i in range(len(eyeUse)):
#        signalData.append([eyeUse[i, 3], eyeUse[i, 4]])
#    newTimes = []
#    for i in range(len(times)):
#        newTimes.append(times[i] * 1000)
    #headUse = get_linAccHead_data( headData, get_normal_time( headData ) )
    print len(fixations1)
    print len(fixations2)
    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot( fixations1[:, 5], fixations1[:, 6], '.c' )
    ax1.set_title('Fixations of second person')
    ax2.plot( fixations2[:, 5], fixations2[:, 6], '.k' )
    ax2.set_title('Fixations of fourth person')
#    ax3.plot( headUse[:, 0], headUse[:, 2], 'r' )
#    ax3.set_title('Y Velocities Head')
#    ax4.plot( headUse[:, 0], headUse[:, 3], 'g' )
#    ax4.set_title( 'Z Velocities Head')
    plt.show()
#    signalData = np.array(signalData)
#    pltv.create_plot_video_in_intervall(signalData, 'p01.avi', eyeUse[0][0], eyeUse[len(eyeUse) - 1][0])
    f2, (ax3, ax4, ax5, ax6) = plt.subplots(4, 1)
    times, velocities, xVels, yVels, pts = linVelocities( get_pos_data( eyeDat1 ) )
    times2, velocities2, xVels2, yVels2, pts2 = linVelocities( get_pos_data( eyeDat2 ) )
    ax3.plot( times, xVels, 'c')
    ax4.plot( times, yVels, 'k')
    ax5.plot( times2, xVels2, 'r')
    ax6.plot( times2, yVels2, 'm')
    ax3.set_title('x Velocities of second person')
    ax4.set_title('y Velocities of second person')
    ax5.set_title('x Velocities of fourth person')
    ax6.set_title('y Velocities of fourth person')
    
    plt.show()
    
    