import os
import sys

def extract_pdb_structure(path_to_a_file):
	"""
	Returns a list of lines containing x, y and z coordenates
	from a pdb structure file.
	"""
	pdb_file = path_to_a_file
	pdb_f = open(pdb_file, 'r')

	c = 0
	text = []
	s = ' '

	for line in pdb_f:
		if 'REMARK' in line:
			continue
		elif 'END' in line:
			continue
		else:
			c += 1
			atom_name = line[13:14].strip(' ')
						
			x = line[30:38].strip(' ')
			y = line[38:46].strip(' ')
			z = line[46:54].strip(' ')
			
			line = "%1s%s%8f%4s%8f%4s%8f%1s\n" % (atom_name, ' ', float(x), s, float(y), s, float(z), s)
			text.append(line)

	total_atoms = c
	return text

# Environment definitions
path = os.getcwd() + '/'
pdb_file = path + sys.argv[1]
out1_file = path + sys.argv[1].replace('.pdb','.xyz')

# Function call
coordenates_lines = extract_pdb_structure(pdb_file)

# Writing outputs
out1_f = open(out1_file, 'w')
for i in coordenates_lines:
	out1_f.write(i)
out1_f.close()