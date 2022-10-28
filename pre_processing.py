from fpylll import FPLLL, IntegerMatrix, LLL

import numpy as np
import os
import random
import json

def dual(basis,sage):
  """
  computes the dual of the basis.
  (!) calles sage internally
  We do not know how to easily avoid usage of sage here
  """

  key = "basis_" + str( random.randint(0,2**64) )

  with open(key, "w+") as f:
    print(json.dumps( basis ), file=f)

  if sage != None:
    success = os.system(sage + " dual_basis.sage " + key)
  else:
    success = 1

  if success != 0:
    raise ValueError("Failed to run SAGE via command '" + str(sage) + "'")

  with open(key) as f:
    basis = json.loads( f.read() )

  os.remove(key)

  return basis

def swapLeftRight(basis):
	d = int( len(basis[0]) /2)

	for i in range(len(basis)):

		left = basis[i][:d]
		right = basis[i][d:]
		basis[i] = right + left

	return basis

def projection(basis, projectLeft):
	d = int( len(basis[0]) /2)

	if not projectLeft:
		basis = swapLeftRight(basis)

	for i, v in enumerate(basis):
		v_left = v[:d]
		v_right = v[d:]

		sum_left = sum(v_left)

		for j in range(d):
			v_left[j] = d*v_left[j] - sum_left
			v_right[j] = d*v_right[j]

		basis[i] = v_left + v_right

	if not projectLeft:
		basis = swapLeftRight(basis)

	return basis

def removeLinearDependencies(basis):
  d = len( basis[0] )
  B = IntegerMatrix(d, d)
  B.set_matrix(basis)

  B = LLL.reduction(B)
  while list(B[0]) == B.ncols*[0]:
    B = B[1:]

  basis = [ [ 0 for _ in range(B.ncols) ] for _ in range(B.nrows) ]
  B.to_matrix( basis )

  return basis

def sliceBasis(basis,sage,projectLeft=True):
  basis = dual(basis,sage)
  basis = projection(basis,projectLeft)
  basis = removeLinearDependencies(basis)
  basis = dual(basis,sage)
  return basis

def projectAgainstOne(basis):
  nRows = len(basis)
  d = int( len(basis[0]) / 2)
  ones = np.array( d*[1] )

  for i in range(nRows):
    b = basis[i]
    b_left = b[:d]
    b_right = b[d:]

    inner_left = sum(b_left)
    inner_right = sum(b_right)

    b_left = d*np.array(b_left) - inner_left * ones
    b_right = d*np.array(b_right) - inner_right * ones

    basis[i] = b_left.tolist() + b_right.tolist()

  return basis

def challenge(basis, sage):
	d = int( len(basis) / 2 )

	h = basis[d][:d]

	for i in range( d ):
		for j in range( d ):
			basis[d+i][j] *= 3


	basis = sliceBasis(basis,sage,projectLeft=False)

	def inner(v):
		return sum( [ v[i]*h[i] for i in range(len(h)) ] )

	sqNorm = inner(h)
	for i in range(len(basis)):
		b = basis[i]
		b_left = b[:d]
		b_right = b[d:]

		b_left = sqNorm*np.array( b_left ) - inner(b)*np.array( h )
		b_right = sqNorm*np.array( b_right )

		basis[i] = b_left.tolist() + b_right.tolist()

	return basis
