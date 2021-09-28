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

def read_xyz(filename):
    '''reads xyz file and returns Geometry object'''
    out = []

    with open(filename, "r") as f:
        line = f.readline()
        while line != "":
            natoms = int(line)
            comment = f.readline().rstrip()

            names = []
            coords = []
            extras = []

            for i in range(natoms):
                line = f.readline()
                data = line.split()
                name, x, y, z = data[0:4]
                extra = data[4:]

                names.append(name.capitalize())
                coords.append( [name, float(x), float(y), float(z)] )
                if extra:
                    extras.append(extra)

            #out.append(Geometry(names, np.array(coords), comment=comment, extras=extras))
            
            line = f.readline()

    return natoms, coords


def calculate_WXZ(n, text, p):
	
	central_atom_line = text[n]
	
	x = central_atom_line[1]
	y = central_atom_line[2]
	z = central_atom_line[3]

	W = float(x) - float(p)
	X = float(y) - float(p)
	Z = float(z) - float(p)

	return W, X, Z


def calculate_new_points(x,y,z,W,X,Z):

	xf = float(x) - float(W)
	yf = float(y) - float(X)
	zf = float(z) - float(Z)

	return xf, yf, zf


data = read_xyz(structure_file) 
natoms = data[0]
coords = data[1]
print(coords)

out_f = open(out_file, 'w')

#lines = c_structure.split('\n')
#print(lines)

# Call function
WXZ = calculate_WXZ(central_atom, coords, central_point)
print(WXZ)

W = WXZ[0]
X = WXZ[1]
Z = WXZ[2]

# Write
out_f.write(str(natoms) + '\n\n')
for at in coords:
	name = at[0]
	x = at[1]
	y = at[2]
	z = at[3]
	
	new_points = calculate_new_points(x,y,z,W,X,Z)

	out_line = "%4s%10f%10f%10f \n" % (name, new_points[0], new_points[1], new_points[2])
	out_f.write(out_line)

out_f.close()

