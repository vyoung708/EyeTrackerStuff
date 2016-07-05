'''
Created on Jul 5, 2016

@author: Victoria Young
'''

import os
import pickle
from numpy import eye

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

def get_data( name ):
    headData = []
    permPath = '/Users/ei-student/Documents/Origami Tests'
    eyePath = os.path.join(permPath, name)
    eyeData = read_eyetracker_data( eyePath )
    headPath = os.path.join(permPath, name, 'Nodding' + '.log')
    with open(headPath, 'rb') as data:
        for line in data:
            line = line.split()
            headData.append(line)
    return eyeData, headData


if __name__ == '__main__':
    eye, head = get_data( 'Nodding' )
    print eye.keys()
    print head[0]