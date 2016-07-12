'''
Created on Jul 12, 2016

@author: Victoria Young
'''
import numpy as np
import os
import matplotlib.pyplot as plt

def get_fixations( num ):
    permPath = '/Users/ei-student/Documents/Origami Tests'
    eyePath = os.path.join(permPath, num, num + '_eyetracker')
    fixPath = os.path.join(eyePath, 'exports', 'fixations.csv')
    fixations = np.genfromtxt(fixPath, delimiter = ',')
    fixations = np.asarray(fixations)
    return fixations

def get_points( data, bottom, top ):
    points = []
    data = np.asarray(data)
    for i in range(len(data)):
        if data[i, 1] >= bottom and data [i, 1] <= top:
            points.append([data[i, 3], data[i, 5], data[i, 6]])
    return np.asarray(points)

def get_sec(s):
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def get_origami_times():
    p01, p02, p03, p04, p05, p06 = [], [], [], [], [], []
    i = 0
    with open('/Users/ei-student/Documents/Origami Times for all.txt', 'rb') as tInfo:
        for line in tInfo:
            line = line.split()
            if i == 0 or i == 1 or i == 2:
                p01.append(line)
            elif i == 3 or i == 4 or i == 5:
                p02.append(line)
            elif i == 6 or i == 7 or i == 8:
                p03.append(line)
            elif i == 9 or i == 10 or i == 11:
                p04.append(line)
            elif i == 12 or i == 13 or i == 14:
                p05.append(line)
            elif i == 15 or i == 16 or i == 17:
                p06.append(line)
            i += 1
    return np.asarray(p01), np.asarray(p02), np.asarray(p03), np.asarray(p04), np.asarray(p05), np.asarray(p06)


if __name__ == '__main__':
    
    p01, p02, p03, p04, p05, p06 = get_origami_times()
    print p01
    print p02
    print p03
    print p04
    print p05
    print p06
    
    
    origami21 = get_points( get_fixations( 'p02' ), get_sec(p02[0, 2]), get_sec(p02[0, 3]) )
    origami41 = get_points( get_fixations( 'p04' ), get_sec(p04[0, 2]), get_sec(p04[0, 3]) )
    
    origami22 = get_points( get_fixations( 'p02' ), get_sec(p02[1, 2]), get_sec(p02[1, 3]) )
    origami42 = get_points( get_fixations( 'p04' ), get_sec(p04[1, 2]), get_sec(p04[1, 3]))
    
    origami23 = get_points( get_fixations( 'p02' ), get_sec(p02[2, 2]), get_sec(p02[2, 3]) )
    origami43 = get_points( get_fixations( 'p04' ), get_sec(p04[2, 2]), get_sec(p04[2, 3]) )
    
    print('Mean fixation time for p2 and p4')
    print len(origami21)
    print('P2 O1: %f' % (np.mean(origami21[:, 0])))
    print len(origami22)
    print('P2 O2: %f' % (np.mean(origami22[:, 0])))
    print len(origami23)
    print('P2 O3: %f' % (np.mean(origami23[:, 0])))
    
    print
    
    print len(origami41)
    print('P4 O1: %f' % (np.mean(origami41[:, 0])))
    print len(origami42)
    print('P4 O2: %f' % (np.mean(origami42[:, 0])))
    print len(origami43)
    print('P4 O3: %f' % (np.mean(origami43[:, 0])))
        
    plt.figure()
    plt.hist(origami21[:, 0], alpha = .5, label = 'p2 o1')
    plt.hist(origami41[:, 0], alpha = .5, label = 'p4 o1')
    plt.legend()
    
    plt.figure()
    plt.hist(origami22[:, 0], alpha = .5, label = 'p2 o2')
    plt.hist(origami42[:, 0], alpha = .5, label = 'p4 o2')
    plt.legend()
    
    plt.figure()
    plt.hist(origami23[:, 0], alpha = .5, label = 'p2 o3')
    plt.hist(origami43[:, 0], alpha = .5, label = 'p4 o4')
    plt.legend()
    
    plt.show()
    
    
    