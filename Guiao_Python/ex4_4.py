import cmath

positivo = lambda a,b : cmath.polar(complex(a,b))

print("Cordenadas polares de (0, -7):\n",positivo(0,-7))
print("Cordenadas polares de (-23, 11):\n",positivo(-23,11))