from scipy.interpolate import lagrange
import numpy as np

# The L, R, and O matrices from the R1CS example

L = np.array([
  [0, 0, 3, 0, 0, 0],
  [0, 0, 0, 0, 1, 0],
  [0, 0, 5, 0, 0, 0]
])

R = np.array([
  [0, 0, 1, 0, 0, 0],
  [0, 0, 0, 1, 0, 0],
  [0, 0, 0, 1, 0, 0]
])

O = np.array([
  [0, 0, 0, 0, 1, 0],
  [0, 0, 0, 0, 0, 1],
  [-3, 1, 1, 2, 0, -1]
])

# def interpolate_column(col):
#   xs = np.array([1, 2, 3])
#   return lagrange(xs, col)

# for i in range(L.shape[1]):
#   print(interpolate_column(L[:, i]))

# for i in range(R.shape[1]):
#   print(interpolate_column(R[:, i]))

# for i in range(O.shape[1]):
#   print(interpolate_column(O[:, i]))

U = [
  [0, 0, 4, 0, -1, 0],
  [0, 0, -15, 0, 4, 0],
  [0, 0, 14, 0, -3, 0]
]

V = [
  [0, 0, 0.5, -0.5, 0, 0],
  [0, 0, -2.5, 2.5, 0, 0],
  [0, 0, 3, -2, 0, 0]
]

W = [
  [-1.5, 0.5, 0.5, 1, 0.5, -1.5],
  [4.5, -1.5, -1.5, -3, -2.5, 5.5],
  [-3, 1, 1, 2, 3, -4]
]

# Solved using x = 2, y = 3
witness = [1,61,2,3,12,36]

print("Ua: %s" % np.matmul(U, witness))
print("Va: %s" % np.matmul(V, witness))
print("Wa: %s" % np.matmul(W, witness))

# Ua = -4*x**2 + 18*x - 8
# Va = -0.5*x**2 + 2.5*x
# Wa = -15*x**2 + 69*x - 42

a = np.poly1d([-4, 18, -8])
b = np.poly1d([-0.5, 2.5, 0])
c = np.poly1d([-15, 69, -42])
t = np.poly1d([1, -1])*np.poly1d([1, -2])*np.poly1d([1, -3])

print((a * b - c) / t)
