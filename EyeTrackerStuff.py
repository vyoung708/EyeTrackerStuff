import pickle
import os
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import time

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

def read_csv( path ):
    csv_data = np.genfromtxt(path, delimiter = ',')
    return csv_data

def get_headtracker_data( motion_rec ):
    """Epoch Time, Sensor ID, Temperature, Euler X-, Y-, Z-axis, acc X, Y, Z, gyro X, Y, Z, Magnetic Field X, Y, Z,
       Orientation quaternion scalar, X, Y, Z, Linear acc X, Y, Z"""
    headData = []
    with open( motion_rec ) as htdata:
        for line in htdata:
            line = line.split()
            headData.append(line)
    return headData

def get_normal_time( trackData ):
    initialTime = trackData[0][0]
    nTime = []
    for item in trackData:
            nTime.append(float(item[0]) - float(initialTime))
    return nTime

def get_acc_data( hData, times ):
    acc = []
    for i in range(len(hData)):
        acc.append([times[i], float(hData[i][7]), float(hData[i][8]), float(hData[i][9])])
    return acc

def get_euler_data( hData, times ):
    euler = []
    for i in range(len(hData)):
        euler.append([times[i], hData[i][4], hData[i][5], hData[i][6]])
    return euler

def get_gyro_data( hData, times ):
    gyro = []
    for i in range(len(hData)):
        gyro.append([times[i], hData[i][10], hData[i][11], hData[i][12]])
    return gyro

def get_magField_data( hData, times ):
    mag = []
    for i in range(len(hData)):
        mag.append([times[i], hData[i][13], hData[i][14], hData[i][15]])
    return mag

def get_quatOrient_data( hData, times ):
    quat = []
    for i in range(len(hData)):
        quat.append([times[i], hData[i][16], hData[i][17], hData[i][18], hData[i][19]])
    return quat

def get_linAcc_data( hData, times ):
    lin = []
    for i in range(len(hData)):
        lin.append([times[i], hData[i][20], hData[i][21], hData[i][22]])
    return lin

def get_pos_data( data ):
    """Timestamp in Realtime, norm_pos, realtime gaze on Computer"""
    dataList = []
    initialTime = data["gaze_positions"][0]['timestamp']
    for item in data["gaze_positions"]:
        useTime = item['timestamp'] - initialTime
        dataList.append([useTime, item["base"][0]['norm_pos'][0] ,item["base"][0]['norm_pos'][1], item['norm_pos'][0], item['norm_pos'][1]])
    return np.array(dataList)

def get_angle_data( data ):
    dataList = []
    initialTime = data['pupil_positions'][0]['timestamp']
    for item in data['pupil_positions']:
        useTime = item['timestamp'] - initialTime
        dataList.append([useTime, item['ellipse']['angle']])
    return np.array(dataList)

def std_dev_sliding( dataUse, period ):
    time = []
    dist = []
    stdDevia = []
    timeData = dataUse[:, 0]
    timeData = np.array(timeData)
    for i in range(0, len(dataUse) - period + 1):
        time.append(np.mean(timeData[i : i+period]))
        stdDevia.append([np.std(dataUse[i:i+period, 3]), np.std(dataUse[i:i+period, 4])])
    dist = get_euclidean_dist(stdDevia)
    # print time
    # print "change"
    # print dist
    return time, dist

def get_euclidean_dist( points ):
    x = np.array(points)[:, 0]
    y = np.array(points)[:, 1]
    d = (x ** 2 + y ** 2) ** 0.5
    return d

def plotHist( array, title, x_name, y_name ):
    # for item in array:
    #     print(item)
    plt.figure()
    plt.hist(array, bins=10)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)

def plotVTime( times, array, title, x_name, y_name ):
    plt.figure()
    plt.plot(times, array)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)

def scatterPlot( times, array, title, x_name, y_name ):
    plt.figure()
    plt.scatter(times,array)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)

def barPlot( times, array, title, x_name, y_name ):
    plt.figure()
    plt.bar(times, array)
    plt.title(title)
    plt.xlabel(x_name)
    plt.ylabel(y_name)

def angVelocities( angData ):
    times = angData[:, 0]
    angle = angData[:, 1]
    velocity = []
    for i in range(len(times)-1):
        velocity.append(abs((angle[i+1] - angle[i]) / (times[i + 1] - times[i])))
    return velocity

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

def fixations( threshold, velData, points, times ):
    fixationsAm = 0
    fixPoints = []
    for i in range(len(velData)):
        if velData[i] < threshold:
            fixationsAm += 1
            fixPoints.append([times[i], [points[i][0], points[i, 1]]])
    return fixationsAm, fixPoints

def fixationGroup( timeThresh, timePoints ):
    groupNum = 0
    groups = []
    newGroup = True
    appended = False
    for i in range(len(timePoints) - 1):
        if (timePoints[i + 1][0] - timePoints[i][0]) < timeThresh:
            if newGroup == True:
                newGroup = False
                groupNum += 1
                if appended == False:
                    groups.append([timePoints[i][1], groupNum])
                    appended = True
                groups.append([timePoints[i+1][1], groupNum])
            else:
                if appended == False:
                    groups.append([timePoints[i][1], groupNum])
                    appended = True
                groups.append([timePoints[i+1][1], groupNum])
        else:
            newGroup = True
    return groupNum, groups

def centroids( points ):
    points = np.asarray(points)
    length = points.shape[0]
    sum_x = np.sum(points[:, 0])
    sum_y = np.sum(points[:, 1])
    return sum_x / length, sum_y / length

if __name__ == '__main__':

    """path to eye tracker data"""
    path = "/Users/ei-student/recordings/2016_06_27/PAINTpoliticlash/"

    """call to translate data into readable numbers"""
    #data = read_eyetracker_data( path )

    """path to head tracker data"""
    #hPath = "/Users/ei-student/Desktop/imu_data/PropIndVid.log"

    """get head tracker data"""
    #headtdata = get_headtracker_data(hPath)

    """get human time, pupil position, gaze position in camera"""
    #newData = get_pos_data( data )

    """get human time, angle from ellipse dictionary"""
    #angleData = get_angle_data( data )

    """get times and standard deviation in a sliding window for the euclidean distance"""
    #avgTimes, stdDev = std_dev_sliding( newData, 5 )

    """different visualizations of standard deviation data"""
    # barPlot( avgTimes, stdDev, 'Standard Dev v. Time', 'Average Time', 'Standard Deviation' )
    # plotHist( stdDev, 'Standard Deviation', 'Standard Deviation', 'Frequency' )
    # plotVTime( avgTimes, stdDev, 'Standard Dev v. Time', 'Time', 'Standard Deviation' )
    # scatterPlot( avgTimes, stdDev, 'Standard Dev v. Time', 'Time', 'Standard Deviation' )
    # plt.show()

    """get times, linear velocity between points, and points for data"""
    #times, linVelocityVals, xVels, yVels, pointRec = linVelocities( newData )
    #msTime = []
    #for item in times:
        #msTime.append(item * 1000)

    """remove the last value of points array"""
    #pointRec = pointRec[:-1]

    """get angular velocity between points for data"""
    #angVelocityVals = angVelocities( angleData )

    """plot velocities for visualization"""
    # plotVTime( angleData[:-1, 0], angVelocityVals, 'Angular Velocity v. Time', 'Time', 'Angular Velocity' )

    #pointRec = np.array(pointRec)
    """plot pupil positions to visualize where pupil moved"""
    #scatterPlot( pointRec[:, 0], pointRec[:, 1], 'Pupil Positions', 'Pupil X', 'Pupil Y' )
    #plotVTime( newData[:-1, 0], pointRec[:, 0], 'Pupil Pos X', 'Time', 'Pupil X')

    """get number of fixation points, the times, and the points themselves using a velocity threshold"""
    #numFixPoints, timePoints = fixations(.005, linVelocityVals, pointRec, times)

    """extract the points for plotting purposes"""
    #pointsUse = []
    #for i in range(len(timePoints)):
        #pointsUse.append( timePoints[i][1] )

    """prints number of fixation points"""
    #print numFixPoints

    #pointsUse = np.array(pointsUse)
    """plot the fixation points"""
    #scatterPlot( pointsUse[:, 0], pointsUse[:, 1], 'Pupil Positions for Fixations', 'Pupil X', 'Pupil Y')

    """get the number of fixation groups and the points within those groups based on a time threshold"""
    #numGroups, pointGroups = fixationGroup( .250, timePoints )

    """print number of fixation groups"""
    #print numGroups

    """prints the groups and calculates the centroids"""
    #centroid = []
    #group = []
    #counter = 1
    #for i in range(numGroups + 1):
        #print i
        #for item in pointGroups:
            #if item[1] == i:
                # print item
               # group.append(item[0])
            #elif len(group) > 0:
  #              centroid.append(centroids(group))
 #               group = []

    """prints centroids"""
    # for item in centroid:
    #     print counter
    #     print item
    #     counter += 1

  #  centroid = np.array(centroid)

    """plot the centroids"""
    #scatterPlot( centroid[:, 0], centroid[:, 1], 'Centroids', 'Centroid X', 'Centroid Y')
    # plt.show()

    """get normal times for head tracker data"""
  #  headTime = get_normal_time( headtdata )

    """get sets of data """
    # accData = get_acc_data( headtdata, headTime )
    # eulerData = get_euler_data( headtdata, headTime )
    # gyroData = get_gyro_data( headtdata, headTime )
    # magData = get_magField_data( headtdata, headTime )
    # quatOrienData = get_quatOrient_data( headtdata, headTime )
    # linAccData = get_linAcc_data( headtdata, headTime )

    """plot accX,Y,Z of head v Time"""
    #accData = np.array(accData)
    #plotVTime( headTime, accData[:, 1], 'X Acc v Time', 'Time', 'X Acc' )
    #plotVTime( headTime, accData[:, 2], 'Y Acc v Time', 'Time', 'Y Acc' )
    #plotVTime( headTime, accData[:, 3], 'Z Acc v Time', 'Time', 'Z Acc' )

    """plot eulerX,Y,Z of head v Time"""
    #eulerData = np.array(eulerData)
    #plotVTime( headTime, eulerData[:, 1], 'X Euler Angle v Time', 'Time', 'X Angle' )
    #plotVTime( headTime, eulerData[:, 2], 'Y Euler Angle v Time', 'Time', 'Y Angle' )
    #plotVTime( headTime, eulerData[:, 3], 'Z Euler Angle v Time', 'Time', 'Z Angle' )

    """plot Quaternion Orientation v Time"""
   # quatOrienData = np.array(quatOrienData)
    #plotVTime( headTime, quatOrienData[:, 1], 'Quaternion Orientation Scalar v Time', 'Time', 'Quat Orien Scalar' )
    #plotVTime( headTime, quatOrienData[:, 2], 'X Quaternion Orientation v Time', 'Time', 'X Orientation' )
    #plotVTime( headTime, quatOrienData[:, 3], 'Y Quaternion Orientation v Time', 'Time', 'Y Orientation' )
    #plotVTime( headTime, quatOrienData[:, 4], 'Z Quaternion Orientation v Time', 'Time', 'Z Orientation' )

    """plot gyroX,Y,Z of head v Time"""
 #   gyroData = np.array(gyroData)
   # plotVTime( headTime, gyroData[:, 1], 'X Gyro v Time', 'Time', 'X Gyro' )
    #plotVTime( headTime, gyroData[:, 2], 'Y Gyro v Time', 'Time', 'Y Gyro' )
    #plotVTime( headTime, gyroData[:, 3], 'Z Gyro v Time', 'Time', 'Z Gyro' )

    """plot magFieldX,Y,Z of head v Time"""
   # magData = np.array(magData)
   # plotVTime( headTime, magData[:, 1], 'X Magnetic Field v Time', 'Time', 'X Field' )
    #plotVTime( headTime, magData[:, 2], 'Y Magnetic Field v Time', 'Time', 'Y Field' )
   # plotVTime( headTime, magData[:, 3], 'Z Magnetic Field v Time', 'Time', 'Z Field' )

    """plot linAccX,Y,Z of head v Time"""
    #linAccData = np.array(linAccData)
    #plotVTime( headTime, linAccData[:, 1], 'X Lin Acc v Time', 'Time', 'X Acc' )
    #plotVTime( headTime, linAccData[:, 2], 'Y Lin Acc v Time', 'Time', 'Y Acc' )
    #plotVTime( headTime, linAccData[:, 3], 'Z Lin Acc v Time', 'Time', 'Z Acc' )
    # plt.plot(headTime, linAccData[:, 1], 'b', label = 'X Linear Acceleration')

    """plot eyes lin acc v head lin acc"""
    # plt.figure()
    # plt.plot( msTime, xVels, 'r', label = 'X Linear Velocity Eyes')
    # plt.plot(headTime, linAccData[:, 2], 'g', label = 'Y Linear Acceleration')
    # plt.legend()
    #
    # plt.figure()
    # plt.plot( msTime, yVels, 'k', label = 'Y Linear Velocity Eyes')
    # plt.plot(headTime, linAccData[:, 3], 'c', label = 'Z Linear Acceleration')
    # plt.legend()

    """plot each var on the same graph"""
    # plt.figure()
    # plt.plot(headTime, accData[:, 1], 'b', label = 'Acceleration')
    # plt.plot(headTime, eulerData[:, 1], 'r', label = 'Euler Angle')
    # plt.plot(headTime, quatOrienData[:, 2], 'g', label = 'Quaternion Orientation')
    # plt.plot(headTime, gyroData[:, 1], 'y', label = 'Gyroscope')
    # plt.plot(headTime, magData[:, 1], 'c', label = 'Magnetic Field')
    # plt.plot(headTime, linAccData[:, 1], 'k', label = 'Linear Acceleration')
    # plt.title('X Plots')
    # plt.xlabel('Time')
    # plt.legend()
    #
    # plt.figure()
    # plt.plot(headTime, accData[:, 2], 'b', label = 'Acceleration')
    # plt.plot(headTime, eulerData[:, 2], 'r', label = 'Euler Angle')
    # plt.plot(headTime, quatOrienData[:, 3], 'g', label = 'Quaternion Orientation')
    # plt.plot(headTime, gyroData[:, 2], 'y', label = 'Gyroscope')
    # plt.plot(headTime, magData[:, 2], 'c', label = 'Magnetic Field')
    # plt.plot(headTime, linAccData[:, 2], 'k',  label = 'Linear Acceleration')
    # plt.title('Y Plots')
    # plt.xlabel('Time')
    # plt.legend()
    #
    # plt.figure()
    # plt.plot(headTime, accData[:, 3], 'b', label = 'Acceleration')
    # plt.plot(headTime, eulerData[:, 3], 'r', label = 'Euler Angle')
    # plt.plot(headTime, quatOrienData[:, 4], 'g', label = 'Quaternion Orientation')
    # plt.plot(headTime, gyroData[:, 3], 'y', label = 'Gyroscope')
    # plt.plot(headTime, magData[:, 3], 'c', label = 'Magnetic Field')
    # plt.plot(headTime, linAccData[:, 3], 'k',  label = 'Linear Acceleration')
    # plt.title('Z Plots')
    # plt.xlabel('Time')
    # plt.legend()

    #plt.show()

    path = '/Users/ei-student/recordings/2016_06_21/readingbiothesis/exports/0-8287/surfaces/fixations_on_surface_unnamed_1466499419.751.csv'
    path2 = '/Users/ei-student/recordings/2016_06_21/readingbiothesis/exports/0-8287/surfaces/gaze_positions_on_surface_unnamed_1466499419.751.csv'

    fix_data_export = read_csv( path )

    gaze_data = read_csv( path2 )

    #newData = np.array(newData)

    plt.figure()

    plt.plot( fix_data_export[:, 7], fix_data_export[:, 8], '.r-')
    for i in range(len(fix_data_export[:, 7])):
        plt.annotate(i, xy=(fix_data_export[i][7], fix_data_export[i][8]), xytext = ((fix_data_export[i][7]) + 1, (fix_data_export[i][8]) + 1))

    plt.figure()

    plt.plot( gaze_data[:, 5], gaze_data[:, 6], '.r-')
    for i in range(len(gaze_data[:, 5])):
        plt.annotate(i, xy=(gaze_data[i][5], gaze_data[i][6]), xytext = ((gaze_data[i][5]) + .02, (gaze_data[i][6]) + .02))

    plt.show()