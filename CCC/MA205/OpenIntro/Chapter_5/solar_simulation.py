import random
import statistics

random.seed()

n = 258000000
p = 0.88
k = int(round(n*p, 0))
population = ["support"]*k + ["not"]*(n-k)

def sample_prop(size = 1000):
    sample = random.sample(population, size)
    return float(len([x for x in sample if x == 'support'])) / float(len(sample))

phats = []
for i in range(9):
    phats.append(sample_prop())

s = r"\begin{center}"
s += "\n"
s += r"\begin{tabular}{cr|cr|cr}"
s += "\n"
s += r"$\hat{p}$ & Error & "
s += r"$\hat{p}$ & Error & "
s += r"$\hat{p}$ & Error \\\hline"
s += "\n"

i = 0
while i < len(phats):
    s += str(phats[i])
    s += " & "
    s += str(round(phats[i] - p, 4))
    if (i+1) % 3 == 0:
        s += r" \\" + "\n"
    else:
        s += r" & "
    i += 1

s += r"\end{tabular}"
s += "\n"
s += r"\end{center}"
print(s)

mean = statistics.fmean(phats)
print(f"Sampling mean is {mean}")

# build histogram data set
phats = []
with open("solar_sampling_dist_n_1000.dat", 'w') as f:
    f.write("data\n")
    for i in range(10000):
        phat = sample_prop()
        phats.append(phat)
        f.write(str(phat))
        f.write("\n")

print(f"mean:   {statistics.fmean(phats)}")
print(f"stddev: {statistics.stdev(phats)}")

phats = []
with open("solar_sampling_dist_n_50.dat", 'w') as f:
    f.write("data\n")
    for i in range(10000):
        phat = sample_prop(50)
        phats.append(phat)
        f.write(str(phat))
        f.write("\n")

print(f"mean:   {statistics.fmean(phats)}")
print(f"stddev: {statistics.stdev(phats)}")
