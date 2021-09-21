import random
import math

random.seed()

n_list = []
i = 1
while i <= 100:
    n_list.append(i)
    i += 1

while i <= 1000:
    n_list.append(i)
    i += 10

while i <= 10000:
    n_list.append(i)
    i += 100

while i <= 100000:
    n_list.append(i)
    i += 500

print("n, pn")
for n in n_list:
    count = 0
    for x in range(n):
        if random.randint(1,6) == 1:
            count += 1
    print(f"{n}, {float(count)/float(n)}")
