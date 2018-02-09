import sys
import os

path = os.getcwd() + '/'
structure_file = path + sys.argv[1]
out_file = path + 'A_5.xyz'

# def indentify the cental atom

# def calculate desplazadores from the central atom to a given x,y,z

# def desplazar todos los atomos las magnitudes de los desplazadores

structure = open(structure_file, 'r')
out_f = open(out_file, 'w')
for line in structure:
	vec = line.strip().split(' ')
	print vec
	W = -0.6660000000000004
	X = 0.8419999999999996
	Z = 6.647

	atom = vec[0]

	x = float(vec[1])
	y = float(vec[5])
	z = float(vec[9])

	xf = x + W
	yf = y + X
	zf = z + Z
	
	out_line = "%1s%s%8f%4s%8f%4s%8f%1s\n" % (atom, ' ', xf,  '  ', yf,  '  ', zf,  '  ' )
	out_f.write(out_line)

structure.close()
out_f.close()

