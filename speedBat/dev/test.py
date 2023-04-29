import random as rd
x = []
for i in range(20):
    x.append(i%2)

rd.shuffle(x)
print(x)