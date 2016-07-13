'''
Created on Jul 12, 2016

@author: Victoria Young
'''
import numpy as np
import os
import matplotlib.pyplot as plt
import io
from scipy.signal.ltisys import step2

def get_fixations( num ):
    '''gets all fixations from fixations.csv generated by pupil player'''
    permPath = '/Users/ei-student/Documents/Origami Tests'
    eyePath = os.path.join(permPath, num, num + '_eyetracker')
    fixPath = os.path.join(eyePath, 'exports', 'fixations.csv')
    fixations = np.genfromtxt(fixPath, delimiter = ',')
    fixations = np.asarray(fixations)
    return fixations

def get_points( data, bottom, top ):
    '''gets the points within a time frame in seconds'''
    points = []
    data = np.asarray(data)
    for i in range(len(data)):
        if data[i, 1] >= bottom and data [i, 1] <= top:
            points.append([data[i, 1], data[i, 3], data[i, 5], data[i, 6]])
    return np.asarray(points)

def get_sec(s):
    '''gets the number of seconds from a time in format 00:00:00'''
    l = s.split(':')
    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

def get_origami_times():
    '''gets the times for each origami task for each person'''
    p01, p02, p03, p04, p05, p06, p07 = [], [], [], [], [], [], []
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
            elif i == 18 or i ==19 or i == 20:
                p07.append(line)
            i += 1
    return np.asarray(p01), np.asarray(p02), np.asarray(p03), np.asarray(p04), np.asarray(p05), np.asarray(p06), np.asarray(p07)

def get_origami_steps_time():
    times = []
    with open('/Users/ei-student/Documents/Origami Step Times.txt', 'rb') as stepT:
        for line in stepT:
            line = line.split()
            print line
            times.append(line[1])
    return times

if __name__ == '__main__':
    
    p01, p02, p03, p04, p05, p06, p07 = get_origami_times()
    
#     print p01
#     print p02
#     print p03
#     print p04
#     print p05
#     print p06
#     print p07
    
    times = get_origami_steps_time()
    step1 = get_points( get_fixations( 'p02' ), get_sec(times[0]), get_sec(times[1]) )
    step2 = get_points( get_fixations( 'p02' ), get_sec(times[1]), get_sec(times[2]) )
    step3= get_points( get_fixations( 'p02' ), get_sec(times[2]), get_sec(times[3]) )
    step4= get_points( get_fixations( 'p02' ), get_sec(times[3]), get_sec(times[4]) )
    step5= get_points( get_fixations( 'p02' ), get_sec(times[4]), get_sec(times[5]) )
    step6= get_points( get_fixations( 'p02' ), get_sec(times[5]), get_sec(times[6]) )
    step7= get_points( get_fixations( 'p02' ), get_sec(times[6]), get_sec(times[7]) )
    step8= get_points( get_fixations( 'p02' ), get_sec(times[7]), get_sec(times[8]) )
    step9= get_points( get_fixations( 'p02' ), get_sec(times[8]), get_sec(times[9]) )
    step10= get_points( get_fixations( 'p02' ), get_sec(times[9]), get_sec(times[10]) )
    step11= get_points( get_fixations( 'p02' ), get_sec(times[10]), get_sec(times[11]) )
    step12= get_points( get_fixations( 'p02' ), get_sec(times[11]), get_sec(times[12]) )
    step13= get_points( get_fixations( 'p02' ), get_sec(times[12]), get_sec(times[13]) )
    step14= get_points( get_fixations( 'p02' ), get_sec(times[13]), get_sec(times[14]) )
    step15= get_points( get_fixations( 'p02' ), get_sec(times[14]), get_sec(times[15]) )
    
    print len(step1)
    print len(step2)
    print len(step3)
    print len(step4)
    print len(step5)
    print len(step6)
    print len(step7)
    print len(step8)
    print len(step9)
    print len(step10)
    print len(step11)
    print len(step12)
    print len(step13)
    print len(step14)
    print len(step15)
    labels = np.arange(1, 16)
    lbels = []
    for item in labels:
        lbels.append(str(item))

    plt.figure()
    plt.hist((step1[:, 1], step2[:, 1], step3[:, 1], step4[:, 1], step5[:, 1], step6[:, 1], step7[:, 1], step8[:, 1], step9[:, 1], step10[:, 1], step11[:, 1], step12[:, 1], step13[:, 1], step14[:, 1], step15[:, 1]), label = lbels, normed = True)
    plt.legend()
    plt.show()
    
    origami11 = get_points( get_fixations( 'p01' ), get_sec(p01[0, 2]), get_sec(p01[0, 3]) )
    origami21 = get_points( get_fixations( 'p02' ), get_sec(p02[0, 2]), get_sec(p02[0, 3]) )
    origami31 = get_points( get_fixations( 'p03' ), get_sec(p03[0, 2]), get_sec(p03[0, 3]) )
    origami41 = get_points( get_fixations( 'p04' ), get_sec(p04[0, 2]), get_sec(p04[0, 3]) )
    origami51 = get_points( get_fixations( 'p05' ), get_sec(p05[0, 2]), get_sec(p05[0, 3]) )
    origami61 = get_points( get_fixations( 'p06' ), get_sec(p06[0, 2]), get_sec(p06[0, 3]) )
    origami71 = get_points( get_fixations( 'p07' ), get_sec(p07[0, 2]), get_sec(p07[0, 3]) )
    
    origami12 = get_points( get_fixations( 'p01' ), get_sec(p01[1, 2]), get_sec(p01[1, 3]) )
    origami22 = get_points( get_fixations( 'p02' ), get_sec(p02[1, 2]), get_sec(p02[1, 3]) )
    origami32 = get_points( get_fixations( 'p03' ), get_sec(p03[1, 2]), get_sec(p03[1, 3]) )
    origami42 = get_points( get_fixations( 'p04' ), get_sec(p04[1, 2]), get_sec(p04[1, 3]))
    origami52 = get_points( get_fixations( 'p05' ), get_sec(p05[1, 2]), get_sec(p05[1, 3]) )
    origami62 = get_points( get_fixations( 'p06' ), get_sec(p06[1, 2]), get_sec(p06[1, 3]) )
    origami72 = get_points( get_fixations( 'p07' ), get_sec(p07[1, 2]), get_sec(p07[1, 3]) )
    
    origami13 = get_points( get_fixations( 'p01' ), get_sec(p01[2, 2]), get_sec(p01[2, 3]) )
    origami23 = get_points( get_fixations( 'p02' ), get_sec(p02[2, 2]), get_sec(p02[2, 3]) )
    origami33 = get_points( get_fixations( 'p03' ), get_sec(p03[2, 2]), get_sec(p03[2, 3]) )
    origami43 = get_points( get_fixations( 'p04' ), get_sec(p04[2, 2]), get_sec(p04[2, 3]) )
    origami53 = get_points( get_fixations( 'p05' ), get_sec(p05[2, 2]), get_sec(p05[2, 3]) )
    origami63 = get_points( get_fixations( 'p06' ), get_sec(p06[2, 2]), get_sec(p06[2, 3]) )
    origami73 = get_points( get_fixations( 'p07' ), get_sec(p07[2, 2]), get_sec(p07[2, 3]) )
    
#     print('1')
#     print
#     print((len(origami11)) / (origami11[-1, 0] - origami11[0, 0]))
#     print((len(origami21)) / (origami21[-1, 0] - origami21[0, 0]))
#     print((len(origami31)) / (origami31[-1, 0] - origami31[0, 0]))
#     print((len(origami41)) / (origami41[-1, 0] - origami41[0, 0]))
#     print((len(origami51)) / (origami51[-1, 0] - origami51[0, 0]))
#     print((len(origami61)) / (origami61[-1, 0] - origami61[0, 0]))
#     print((len(origami71)) / (origami71[-1, 0] - origami71[0, 0]))
#     print
#     print('2')
#     print
#     print((len(origami12)) / (origami12[-1, 0] - origami12[0, 0]))
#     print((len(origami22)) / (origami22[-1, 0] - origami22[0, 0]))
#     print((len(origami32)) / (origami32[-1, 0] - origami32[0, 0]))
#     print((len(origami42)) / (origami42[-1, 0] - origami42[0, 0]))
#     print((len(origami52)) / (origami52[-1, 0] - origami52[0, 0]))
#     print((len(origami62)) / (origami62[-1, 0] - origami62[0, 0]))
#     print((len(origami72)) / (origami72[-1, 0] - origami72[0, 0]))
#     print
#     print('3')
#     print
#     print((len(origami13)) / (origami13[-1, 0] - origami13[0, 0]))
#     print((len(origami23)) / (origami23[-1, 0] - origami23[0, 0]))
#     print((len(origami33)) / (origami33[-1, 0] - origami33[0, 0]))
#     print((len(origami43)) / (origami43[-1, 0] - origami43[0, 0]))
#     print((len(origami53)) / (origami53[-1, 0] - origami53[0, 0]))
#     print((len(origami63)) / (origami63[-1, 0] - origami63[0, 0]))
#     print((len(origami73)) / (origami73[-1, 0] - origami73[0, 0]))
    
    x = [1, 2, 3, 4, 5, 6, 7]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    
#    names = ('p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07' )
    
    length11 = ((len(origami11)) / (origami11[-1, 0] - origami11[0, 0]))
    length21 = ((len(origami21)) / (origami21[-1, 0] - origami21[0, 0]))
    length31 = ((len(origami31)) / (origami31[-1, 0] - origami31[0, 0]))
    length41 = ((len(origami41)) / (origami41[-1, 0] - origami41[0, 0]))
    length51 = ((len(origami51)) / (origami51[-1, 0] - origami51[0, 0]))
    length61 = ((len(origami61)) / (origami61[-1, 0] - origami61[0, 0]))
    length71 = ((len(origami71)) / (origami71[-1, 0] - origami71[0, 0]))
    
    plt.figure()
    plt.bar(x, [length11, length21, length31, length41, length51, length61, length71], width = .4, color = colors) 
    plt.title('Origami 01 Fixations per Second per Person')
    
    length12 = ((len(origami12)) / (origami12[-1, 0] - origami12[0, 0]))
    length22 = ((len(origami22)) / (origami22[-1, 0] - origami22[0, 0]))
    length32 = ((len(origami32)) / (origami32[-1, 0] - origami32[0, 0]))
    length42 = ((len(origami42)) / (origami42[-1, 0] - origami42[0, 0]))
    length52 = ((len(origami52)) / (origami52[-1, 0] - origami52[0, 0]))
    length62 = ((len(origami62)) / (origami62[-1, 0] - origami62[0, 0]))
    length72 = ((len(origami72)) / (origami72[-1, 0] - origami72[0, 0]))
   
    plt.figure()
    plt.bar(x, [length12, length22, length32, length42, length52, length62, length72], width = .4, color = colors )
    plt.title('Origami 02 Fixations per Second per Person')
   
    length13 = ((len(origami13)) / (origami13[-1, 0] - origami13[0, 0]))
    length23 = ((len(origami23)) / (origami23[-1, 0] - origami23[0, 0]))
    length33 = ((len(origami33)) / (origami33[-1, 0] - origami33[0, 0]))
    length43 = ((len(origami43)) / (origami43[-1, 0] - origami43[0, 0]))
    length53 = ((len(origami53)) / (origami53[-1, 0] - origami53[0, 0]))
    length63 = ((len(origami63)) / (origami63[-1, 0] - origami63[0, 0]))
    length73 = ((len(origami73)) / (origami73[-1, 0] - origami73[0, 0]))
    
    plt.figure()
    plt.bar(x, [length13, length23, length33, length43, length53, length63, length73], width = .4, color = colors)
    plt.title('Origami 03 Fixations per Second per Person')
    
#     with io.FileIO('Mean fixation times for Origami.txt', 'w') as ofile:
#            
#         ofile.write('Mean fixation time for all \n \n')
#         
#         ofile.write('P01: \n \n')
#         
#         ofile.write('length: %f \n' % len(origami11))
#         ofile.write('P1 O1: %f \n' % (np.mean(origami11[:, 0])))
#         ofile.write('length: %f \n' % len(origami12))
#         ofile.write('P1 O2: %f \n' % (np.mean(origami12[:, 0])))
#         ofile.write('length: %f \n' % len(origami13))
#         ofile.write('P1 O3: %f \n \n' % (np.mean(origami13[:, 0])))
#         
#         ofile.write('P02: \n \n')
#         
#         ofile.write('length: %f \n' % len(origami21))
#         ofile.write('P2 O1: %f \n' % (np.mean(origami21[:, 0])))
#         ofile.write('length: %f \n' % len(origami22))
#         ofile.write('P2 O2: %f \n' % (np.mean(origami22[:, 0])))
#         ofile.write('length: %f \n' % len(origami23))
#         ofile.write('P2 O3: %f \n \n' % (np.mean(origami23[:, 0])))
#     
#         ofile.write('P03: \n \n'  )
#     
#         ofile.write('length: %f \n' % len(origami31))
#         ofile.write('P3 O1: %f \n' % (np.mean(origami31[:, 0])))
#         ofile.write('length: %f \n' % len(origami32))
#         ofile.write('P3 O2: %f \n' % (np.mean(origami32[:, 0])))
#         ofile.write('length: %f \n' % len(origami33))
#         ofile.write('P3 O3: %f \n \n' % (np.mean(origami33[:, 0])))
#     
#         ofile.write('P04: \n \n')
#         
#         ofile.write('length: %f \n' % len(origami41))
#         ofile.write('P4 O1: %f \n' % (np.mean(origami41[:, 0])))
#         ofile.write('length: %f \n' % len(origami42))
#         ofile.write('P4 O2: %f \n' % (np.mean(origami42[:, 0])))
#         ofile.write('length: %f \n' % len(origami43))
#         ofile.write('P4 O3: %f \n \n'  % (np.mean(origami43[:, 0])))
#                 
#         ofile.write('P05: \n \n')        
#                 
#         ofile.write('length: %f \n' % len(origami51))
#         ofile.write('P5 O1: %f \n' % (np.mean(origami51[:, 0])))
#         ofile.write('length: %f \n' % len(origami52))
#         ofile.write('P5 O2: %f \n' % (np.mean(origami52[:, 0])))
#         ofile.write('length: %f \n' % len(origami53))
#         ofile.write('P5 O3: %f \n \n' % (np.mean(origami53[:, 0])))
#         
#         ofile.write('P06: \n \n')
#                 
#         ofile.write('length: %f \n' % len(origami61))
#         ofile.write('P6 O1: %f \n' % (np.mean(origami61[:, 0])))
#         ofile.write('length: %f \n' % len(origami62))
#         ofile.write('P6 O2: %f \n' % (np.mean(origami62[:, 0])))
#         ofile.write('length: %f \n' % len(origami63))
#         ofile.write('P6 O3: %f \n \n' % (np.mean(origami63[:, 0])))
#         
#         ofile.write('P07: \n \n')
#                 
#         ofile.write('length: %f \n' % len(origami71))
#         ofile.write('P7 O1: %f \n' % (np.mean(origami71[:, 0])))
#         ofile.write('length: %f \n' % len(origami72))
#         ofile.write('P7 O2: %f \n' % (np.mean(origami72[:, 0])))
#         ofile.write('length: %f \n' % len(origami73))
#         ofile.write('P7 O3: %f \n \n' % (np.mean(origami73[:, 0])))
#         
#     ofile.close()
  
#     plt.figure()
#     plt.hist(origami21[:, 0], alpha = .5, label = 'p2 o1')
#     plt.hist(origami41[:, 0], alpha = .5, label = 'p4 o1')
#     plt.legend()

    plt.figure()
    plt.hist((origami11[:, 1], origami21[:, 1], origami31[:, 1], origami41[:, 1], origami51[:, 1], origami61[:, 1], origami71[:, 1]), label = ['p01 o1', 'p02 o1', 'p03 o1', 'p04 o1', 'p05 o1', 'p06 o1', 'p07 o1'], normed = True)
    plt.legend()
    
#     plt.figure()
#     plt.hist(origami22[:, 0], alpha = .5, label = 'p2 o2')
#     plt.hist(origami42[:, 0], alpha = .5, label = 'p4 o2')
#     plt.legend()

    plt.figure()
    plt.hist((origami12[:, 1], origami22[:, 1], origami32[:, 1], origami42[:, 1], origami52[:, 1], origami62[:, 1], origami72[:, 1]), label = ['p01 o2', 'p02 o2', 'p03 o2', 'p04 o2', 'p05 o2', 'p06 o2', 'p07 o2'], normed = True)
    plt.legend()
    
#     plt.figure()
#     plt.hist(origami23[:, 0], alpha = .5, label = 'p2 o3')
#     plt.hist(origami43[:, 0], alpha = .5, label = 'p4 o4')
#     plt.legend()
    
    plt.figure()
    plt.hist((origami13[:, 1], origami23[:, 1], origami33[:, 1], origami43[:, 1], origami53[:, 1], origami63[:, 1], origami73[:, 1]), label = ['p01 o3', 'p02 o3', 'p03 o3', 'p04 o3', 'p05 o3', 'p06 o3', 'p07 o3'], normed = True)
    plt.legend()
    
#    plt.show()
    
    
    