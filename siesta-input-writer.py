"""
Siesta input writer
from a pdb structure

Usage: python siesta-input-writer.py <type_analysis(GGA/***)> <chemical_formula> <pdb_file_name>
"""

import sys
import os
import os.path


def define_atoms_list(chem_formula):
	"""
	Returns a list of all atoms
	present in the molecule from its chemical formula.
	"""
	
	####### Two letters elements are not recognized!!!!!! eg. 'Xe'

	atoms_list = []
	nums_list = []
	
	for i in chem_formula:
		if i.isalpha():
			atoms_list.append(i)
		if i.isdigit():
			nums_list.append(i)

	return atoms_list


def check_if_pseudopotencials_in_WD(path, atoms_list, type):
	"""
	It check if the pseudopotential files exists
	already in the working dir; if FALSE, download them.
	"""
	for i in atoms_list:
		psf_path = 'https://departments.icmab.es/leem/siesta/Databases/Pseudopotentials/Pseudos_GGA_Abinit/' + at +'_html/' + at +'.psf'
		if os.path.isfile(path + at + '.psf'):
			print 'Pseudopotential file for ' + at + ' exist. :)'
		else:
			cmd = 'wget ' + psf_path
			os.system(cmd)



def get_atomic_numbers(atoms_list):
	"""
	Returns the atomic number of a list of elements.
	"""
	import periodic
	
	dictionary = {}
	
	for i in atoms_list:
		element = periodic.element(i)
		atomic_number = element.atomic
		dictionary[i] = [atomic_number]

	return dictionary




def define_chemical_species_siesta(atoms_dict):
	"""
	Returns many strings as atoms to be written in 
	#Chemical species definitions of siesta's input file.
	"""
	text = []
	d = {}
	c = 0
	for i in atoms_dict:
		c += 1
		line = ' ' + str(c) + ' ' + str(atoms_dict[i])[1:-1] + ' ' + str(i) + '\n'
		text.append(line)
		d[i] = c
	
	return text, d


def extract_pdb_structure(path_to_a_file, ref_dict):
	"""
	Returns a list of lines containing x, y and z coordenates
	from a pdb structure file.
	"""
	pdb_file = path_to_a_file
	pdb_f = open(pdb_file, 'r')
	d = ref_dict

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
			for i in atom_name:
				if i.isalpha():
					atom_ref = d[i]
			
			x = line[30:38].strip(' ')
			y = line[38:46].strip(' ')
			z = line[46:54].strip(' ')
			
			line = "%4s%8f%4s%8f%4s%8f%1s%1s\n" % (s, float(x), s, float(y), s, float(z), s, atom_ref)
			text.append(line)

	total_atoms = c
	return text



# Environment definitions
path = os.getcwd() + '/'
pdb_file = path + sys.argv[3]
out1_file = path + 'chemical_species.siesta'
out2_file = path + 'atomic_positions.siesta'


# Data definitions
type_analysis = str(sys.argv[1])
chem_formula = str(sys.argv[2])


# Function calls
atoms_list = define_atoms_list(chem_formula)
atoms_dict = get_atomic_numbers(atoms_list)
chemicalspecies_lines = define_chemical_species_siesta(atoms_dict)[0]
references_dict = define_chemical_species_siesta(atoms_dict)[1]
coordenates_lines = extract_pdb_structure(pdb_file, references_dict)


# Writing outputs
out1_f = open(out1_file, 'w')
for i in chemicalspecies_lines:
	out1_f.write(i)
out1_f.close()

out2_f = open(out2_file, 'w')
for i in coordenates_lines:
	out2_f.write(i)
out2_f.close()