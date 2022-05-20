#!/usr/bin/env python
#
# Author: Xiao Wang <xiaowang314159@gmail.com>
#
"""
This example first runs a closed-shell periodic EOM-EE-CCSD with K-point
sampling, a.k.a. EOM-EE-KRCCSD, for singlet excited states on one of the
three provided systems.
Then a molecular EOM-EE-RCCSD based on Gamma-point Hartree-Fock is done, where
a supercell (unit cell with its nmp replicas) is used.
Excitation energies from the two sets of calculations should match.
"""

import numpy as np
from pyscf import gto, scf, cc
from pyscf.cc import eom_rccsd as mol_eom_rccsd
from pyscf.pbc import gto, scf, cc
from pyscf.pbc.cc import eom_kccsd_rhf as eom_krccsd
from pyscf.pbc.tools.pbc import super_cell
from pyscf.cc.rccsd import RCCSD
from pyscf.pbc import tdscf

cell = gto.Cell()
cell.verbose = 7
#cell.unit = 'B'
cell.max_memory = 4000  # MB

#
# Hydrogen crystal
#
# cell.a = np.eye(3) * 7.0
# cell.basis = 'sto-3g'
# cell.atom = '''
#     H 0.000000000000   0.000000000000   0.000000000000
#     H 0.000000000000   0.000000000000   1.400000000000
#     '''

#
# Helium crystal
#
cell.atom = '''
C -0.58442   -0.32662  0.0    
C  0.58442   0.32662   0.0    
H  0.58442   1.40362   0.0    
H -0.58442   -1.40362  0.0    
C    1.8845799999999997       -0.32662  0.0    
C    3.05342    0.32662  0.0    
H    3.05342    1.40362  0.0    
H    1.8845799999999997       -1.40362  0.0    
'''
#cell.basis = [[0, (1., 1.)], [0, (.5, 1.)]]
cell.a = '''
4.938000000, 0.0000000000, 0.00000000
0.000000000, 25.000000000, 0.00000000
0.000000000, 0.000000000, 25.000000000
'''

#
# Diamond
#
# cell.atom = '''
# C 0.000000000000   0.000000000000   0.000000000000
# C 1.685068664391   1.685068664391   1.685068664391
# '''
cell.basis = 'cc-pvdz'
# cell.pseudo = 'gth-pade'
# cell.a = '''
# 0.000000000, 3.370137329, 3.370137329
# 3.370137329, 0.000000000, 3.370137329
# 3.370137329, 3.370137329, 0.000000000'''


cell.build()

nmp = [1,1,1]
#print (cas_list)
#mycc = cc.KRCCSD(kmf,frozen=cas_list)
# KRHF
kpts = cell.make_kpts(nmp)
kmf = scf.KRHF(cell, kpts=kpts, exxdiv=None).density_fit()
ekrhf = kmf.kernel()

td = tdscf.KTDHF(kmf)
td.nstates = 5
td.verbose = 5
print(td.kernel()[0] )
