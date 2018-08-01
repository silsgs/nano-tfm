"""
Mol-lead anchoring Python script

Description:
Move a 3D structure connected to 1 or 2 electrodes,
to different anchoring points.

Usage:
python anchoring_points.py <input_file>
"""

import sys
import os


# Functions

def readfile(path, delim):
    return (ln.split(delim) for ln in open(f, 'r'))


def read_xyz(file):
    l = []
    i = 0
    f = open(file, 'r')
    for line in f:
        vec = line.strip().split()
        if len(vec) < 3:
            continue
        elif len(vec) == 4:
            name = vec[0]
            x = vec[1]
            y = vec[2]
            z = vec[3]
            i += 1
            d = {}
            d['id'] = name + str(i)
            d['x'] = x
            d['y'] = y
            d['z'] = z
            l.append(d)
    return l



def point_1(molecule, Au1, Au2, Au3, S):
    """
    Mol anchored at 'hollow' site
    """
    M = {}
    A = float(Au1['x']) - float(Au2['x'])/2
    B = float(Au1['y']) - float(Au2['y'])/2

    M['x'] = float(S['x']) - float(A)
    M['y'] = float(S['y']) - float(B)

    A_2 = float(Au3['x']) - float(M['x'])/2
    B_2 = float(Au3['y']) - float(M['y'])/2

    for i in molecule:
        i['X'] = float(i['x']) + float(A_2)
        i['Y'] = float(i['y']) + float(B_2)
    return molecule
    #segmento a un tercer Au/2



def point_2(molecule, Au1, Au2, S):
    """
    Mol anchored at mid-point of a side of the triangle formed by (3)Au atoms
    """
    C = float(Au1['x']) - float(Au2['x'])/2
    D = float(Au1['y']) - float(Au2['y'])/2

    for i in molecule:
        i['X'] = float(i['x']) + float(C)
        i['Y'] = float(i['y']) - float(D)
    return molecule




#def point_3(molecule, Au1, Au2, Au3, S):
    """
    Mol anchored at the baricenter of a second triangle formed by perpendicular bisectors of an Au triangle
    """



def point_4(molecule, Au1, S):
    """
    An appex of an Au triangle
    """
    G = float(Au1['x']) - float(S['x'])
    H = float(Au1['y']) - float(S['y'])

    for i in molecule:
        i['X'] = float(i['x']) + float(G)
        i['Y'] = float(i['y']) + float(H)
    return molecule


## Definitions
cwd = os.getcwd() + '/'
input_file = cwd + sys.argv[1]


structure_xyz = read_xyz(input_file)
#print structure_xyz, len(structure_xyz)


# Extracting leads and molecule from structure
leads = list(item for item in structure_xyz if 'Au' in item['id']) # 175 atoms in total, right!
molecule = list(item for item in structure_xyz if 'Au' not in item['id']) # 25 atoms in total, right!
#print len(leads)

# Extracting single atoms within the structure
Au131 = (item for item in structure_xyz if item['id'] == 'Au131').next()
Au132 = (item for item in structure_xyz if item['id'] == 'Au132').next()
Au136 = (item for item in structure_xyz if item['id'] == 'Au136').next()
Aus_l = ['Au131', 'Au132', 'Au136']

S125 = (item for item in structure_xyz if item['id'] == 'S125').next()


## POINT 4
# Calls
#point4 = point_4(molecule, Au132, S125)
#point2 = point_2(molecule, Au132, Au136, S125)
#point1 = point_1(molecule, Au132, Au136, Au131, S125)


output_file = cwd + 'anchor_point_1_' + sys.argv[1] #change

out = open(output_file, 'w')

out.write(str(len(point1) + len(leads)) + '\n' + '\n') #change

for i in point1: # change
    if i['id'] == 'S125':
        out.write(str(i['id']) + ' ' + str(i['X']) + ' ' + str(i['Y']) + ' ' + str(i['z']) + '\n')
    else:
        out.write(str(i['id'][0:1]) + ' ' + str(i['X']) + ' ' + str(i['Y']) + ' ' + str(i['z']) + '\n')
for i in leads:
    if i['id'] in Aus_l:
        out.write(str(i['id']) + ' ' + str(i['x']) + ' ' + str(i['y']) + ' ' + str(i['z']) + '\n')
    else:
        out.write(str(i['id'][0:2]) + ' ' + str(i['x']) + ' ' + str(i['y']) + ' ' + str(i['z']) + '\n')
out.close()



##POINT 3
# Calls
#point3 = point_3()

##POINT 1
# Calls
#point1 = point_1()
