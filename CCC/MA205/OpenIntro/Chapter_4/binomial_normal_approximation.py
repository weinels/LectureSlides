import random
import math

def binomial_data(p, n):
    data = []
    q = 1-p
    for k in range(0,n+1):
        data.append((k,math.comb(n,k) * (p ** k) * (q ** (n-k))))
    return data

if __name__ == "__main__":
    random.seed()

    data = binomial_data(0.1, 10)
    
    print(data)

