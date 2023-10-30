from py_ecc.bn128 import G1, G2, add, multiply, curve_order

def solution_to_G1(vector):
  print("Generating sG1...\n")
  sG1 = []
  for i in range(len(vector)):
    sG1.append(multiply(G1, vector[i]))
  return sG1

def solution_to_G2(vector):
  print("Generating sG2...\n")
  sG2 = []
  for i in range(len(vector)):
    sG2.append(multiply(G2, vector[i]))
  return sG2

def hadamard_solution(matrix, solution):
  vec = []
  accum = []

  for row in matrix:
    for col in range(len(row)):
      if row[col] < 0:
        accum.append(multiply(solution[col], curve_order + row[col]))
        break
      if row[col] != 0:
        accum.append(multiply(solution[col], row[col]))
    if len(accum) == 1:
      vec.append(accum[0])
    else: 
      for i in range(len(accum) - 1):
        accum[0] = add(accum[i], accum[i + 1])
      vec.append(accum[0])

  return vec

def strG(G):
  return (
    repr(G)
    .replace("(", "[")
    .replace(")", "]")
    .replace("[[", "[")
    .replace("]]", "]")
    .replace("], ", "],\n\t")
  )

def print_G1_vector(vector, name):
  print("R1CS.G1Point[] memory %s = new R1CS.G1Point[](%s);" % (name, len(vector)))
  for i in vector:
    print("%s[%s] = R1CS.G1Point(%s, %s);" % (name, vector.index(i), i[0], i[1]))
  print("\n")

def print_G2_vector(vector, name):
  print("R1CS.G2Point[] memory %s = new R1CS.G2Point[](%s);" % (name, len(vector)))
  for i in vector:
    print("%s[%s] = R1CS.G2Point(\n\t%s\n);" % (name, vector.index(i), strG(i)))
  print("\n")

def generate_stuff():
    L = [
      [0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, -4, 0, 0]
    ]

    R = [
      [0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 1, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 1, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1, 0, 0, 0]
    ]

    O = [
      [0, 0, 0, 0, 1, 0, 0, 0],
      [0, 0, 0, 0, 0, 1, 0, 0],
      [0, 0, 0, 0, 0, 0, 1, 0],
      [0, 0, 0, 0, 0, 0, 0, 1],
      [0, 1, 0, 10, -1, 0, -5, -13]
    ]

    s = [1, 22, 1, 2, 1, 4, 1, 4]

    print("Generating solution vectors...\n")

    sG1 = solution_to_G1(s)
    sG2 = solution_to_G2(s)

    print("Generating input vectors...\n")

    Ls1 = hadamard_solution(L, sG1)
    Rs2 = hadamard_solution(R, sG2)
    Os1 = hadamard_solution(O, sG1)

    print_G1_vector(Ls1, "Ls1")
    print_G2_vector(Rs2, "Rs2")
    print_G1_vector(Os1, "Os1")

generate_stuff()
