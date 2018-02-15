import sys
import os

"""
Usage: 
python coordenates_fixer.py <input_file> <output_file> <number_line_central_atom> <central_point>
"""

# Definitions
path = os.getcwd() + '/'
structure_file = path + sys.argv[1]
out_file = path + sys.argv[2]
central_atom = int(sys.argv[3]) - 1
central_point = int(sys.argv[4])


def calculate_WXZ(n, text, p):
	
	central_atom_line = text[n].split('    ')
	
	x = central_atom_line[0][2:]
	y = central_atom_line[1]
	z = central_atom_line[2]

	W = float(x) - float(p)
	X = float(y) - float(p)
	Z = float(z) - float(p)

	return W, X, Z


def calculate_new_points(x,y,z,W,X,Z):

	xf = float(x) - float(W)
	yf = float(y) - float(X)
	zf = float(z) - float(Z)

	return xf, yf, zf



structure = open(structure_file, 'r')
c_structure = structure.read()
out_f = open(out_file, 'w')

lines = c_structure.split('\n')
#print lines

# Call function
WXZ = calculate_WXZ(central_atom, lines, central_point)
#print WXZ

W = WXZ[0]
X = WXZ[1]
Z = WXZ[2]

for line in lines[:-1]:
	line = line.split('    ')
	atom = line[0][0:1]
	x = line[0][2:]
	y = line[1]
	z = line[2]
	
	new_points = calculate_new_points(x,y,z,W,X,Z)

	out_line = "%1s%s%8f%4s%8f%4s%8f%1s\n" % (atom, ' ', new_points[0],  '  ', new_points[1],  '  ', new_points[2],  '  ' )
	out_f.write(out_line)

structure.close()
out_f.close()