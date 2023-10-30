import numpy as np
import random
import galois
from py_ecc.bn128.bn128_curve import curve_order
from functools import reduce

def interpolate_column(col):
  xs = GF(np.array([1,2,3]))
  return galois.lagrange_poly(xs, col)

def inner_product_polynomials_with_witness(polys, witness):
  mul_ = lambda x, y: x * y
  sum_ = lambda x, y: x + y
  return reduce(sum_, map(mul_, polys, witness))

# -------------------
# Verify R1CS
# -------------------
print("Verifying R1CS...")

# Define the matrices
A = np.array([[0,0,3,0,0,0],
              [0,0,0,0,1,0],
              [0,0,1,0,0,0]])

B = np.array([[0,0,1,0,0,0],
              [0,0,0,1,0,0],
              [0,0,0,5,0,0]])

C = np.array([[0,0,0,0,1,0],
              [0,0,0,0,0,1],
              [-3,1,1,2,0,-1]])

# pick random values for x and y
x = random.randint(1,1000)
y = random.randint(1,1000)

# this is our orignal formula
out = 3 * x * x * y + 5 * x * y - x- 2*y + 3# the witness vector with the intermediate variables inside
v1 = 3*x*x
v2 = v1 * y
w = np.array([1, out, x, y, v1, v2])

result = C.dot(w) == np.multiply(A.dot(w),B.dot(w))
assert result.all(), "result contains an inequality"
print("success!")

# -------------------
# Verify Galois
# -------------------
print("Verifying galois...")

GF = galois.GF(curve_order)

# Define the matrices
L = np.array([[0,0,3,0,0,0],
              [0,0,0,0,1,0],
              [0,0,1,0,0,0]])

R = np.array([[0,0,1,0,0,0],
              [0,0,0,1,0,0],
              [0,0,0,5,0,0]])

O = np.array([[0,0,0,0,1,0],
              [0,0,0,0,0,1],
              [(curve_order - 3),1,1,2,0,(curve_order - 1)]])

# pick random values for x and y
x = GF(17)
y = GF(59)

# this is our orignal formula
out = GF(3)*x*x*y + GF(5)*x*y + GF(curve_order - 1)*x + GF(curve_order - 2)*y + GF(3) # the witness vector with the intermediate variables inside
v1 = GF(3)*x*x
v2 = v1 * y
w = np.array([1, out, x, y, v1, v2])

L_galois = GF(L)
R_galois = GF(R)
O_galois = GF(O)
w = GF(w)

assert all(np.equal(np.matmul(L_galois, w) * np.matmul(R_galois, w), np.matmul(O_galois, w))), "not equal"
print("success!")

# -------------------
# Check Polys
# -------------------
print("Generating polynomials...")

# axis 0 is the columns. apply_along_axis is the same as doing a for loop over the columns and collecting the results in an array
U_polys = np.apply_along_axis(interpolate_column, 0, L_galois)
V_polys = np.apply_along_axis(interpolate_column, 0, R_galois)
W_polys = np.apply_along_axis(interpolate_column, 0, O_galois)

print("U: %s" % U_polys[:2])
print("V: %s" % V_polys[:2])
print("W: %s" % W_polys[:1])

term_1 = inner_product_polynomials_with_witness(U_polys, w)
term_2 = inner_product_polynomials_with_witness(V_polys, w)
term_3 = inner_product_polynomials_with_witness(W_polys, w)

# -------------------
# Verify QAP
# -------------------
print("Verifying QAP...")

# t = (x - 1)(x - 2)(x - 3)(x - 4)
t = galois.Poly([1, 16], field = GF) * galois.Poly([1, 15], field = GF) * galois.Poly([1, 14], field = GF) * galois.Poly([1, 13], field = GF)

h = (term_1 * term_2 - term_3) // t

assert term_1 * term_2 == term_3 + h * t, "division has a remainder"
print("success!")
