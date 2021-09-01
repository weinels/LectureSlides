import random

random.seed()

class LowRisk:
    def __init__(self,n):
        self.n = n
    def __repr__(self):
        return f"Low({self.n})"
    def latex(self):
        return r"\low{" + str(self.n) + r"}"
    def __eq__(self, other):
        return self.n == other.n

class HighRisk:
    def __init__(self,n):
        self.n = n
    def __repr__(self):
        return f"High({self.n})"
    def latex(self):
        return r"\high{" + str(self.n) + r"}"
    def __eq__(self, other):
        return self.n == other.n

def build_table(l, c, title=None):
    s = r"\begin{tabular}{|"
    s += 'c'*c
    s += r"|}"
    if title is not None:
        s += "\n"
        s += r"\multicolumn{"
        s += str(c)
        s += r"}{c}{"
        s += title
        s += r"}\\"
    s += r"\hline"
    s += "\n"

    r = 0
    x = 0
    i = 0
    while x < len(l):
        p = l[x]

        s += p.latex()
        s += r" & "

        i += 1
        if i >= c:
            s = s[:-2]
            s += r"\\"
            s += "\n"
            r += 1
            i = 0
        x = i + r*c

    if s[-3:] == r"\\" + "\n":
        s = s[:-3]
    else:
        while i < c-1:
            s += r"& "
            i += 1

    s += r"\\\hline"
    s += "\n"
    s += r"\end{tabular}"

    return s

n = 14*3
while True:
    k = random.randint(round(n*.4), round(n*.6))
    k = round(n / 2) + 3
    if k % 2 == 0:
        break

patients = [x+1 for x in range(n)]
random.shuffle(patients)
highrisk = [HighRisk(x) for x in sorted(patients[k:])]
lowrisk = [LowRisk(x) for x in sorted(patients[:k])]

for x in highrisk:
    assert(x not in lowrisk)
for x in lowrisk:
    assert(x not in highrisk)
for x in patients:
    assert((LowRisk(x) in lowrisk) or (HighRisk(x) in highrisk))

patients = lowrisk+highrisk
    
k = round(len(highrisk)/2)
random.shuffle(highrisk)
control_high_risk = highrisk[:k]
treatment_high_risk = highrisk[k:]

for x in control_high_risk:
    assert(x not in treatment_high_risk)
for x in treatment_high_risk:
    assert(x not in control_high_risk)
for x in highrisk:
    assert(x in control_high_risk or x in treatment_high_risk)

k = round(len(lowrisk)/2)
random.shuffle(lowrisk)
control_low_risk = lowrisk[:k]
treatment_low_risk = lowrisk[k:]

for x in control_low_risk:
    assert(x not in treatment_low_risk)
for x in treatment_low_risk:
    assert(x not in control_low_risk)
for x in lowrisk:
    assert(x in control_low_risk or x in treatment_low_risk)

print(r"\newcommand{\unsorted}[0]{")
print(build_table(sorted(patients, key=lambda x:x.n), 14))
print(r"} %chktex 31")

print(r"\newcommand{\highrisk}[0]{")
print(build_table(sorted(highrisk, key=lambda x:x.n), 5, "High-risk patients"))
print(r"} %chktex 31")

print(r"\newcommand{\lowrisk}[0]{")
print(build_table(sorted(lowrisk, key=lambda x:x.n), 7, "Low-risk patients"))
print(r"} %chktex 31")

print(r"\newcommand{\randhighcontrol}[0]{")    
print(build_table(sorted(control_high_risk, key=lambda x:x.n), 6))
print(r"} %chktex 31")

print(r"\newcommand{\randlowcontrol}[0]{")
print(build_table(sorted(control_low_risk, key=lambda x:x.n), 6))
print(r"} %chktex 31")

print(r"\newcommand{\randhightreatment}[0]{")    
print(build_table(sorted(treatment_high_risk, key=lambda x:x.n), 6))
print(r"} %chktex 31")

print(r"\newcommand{\randlowtreatment}[0]{")
print(build_table(sorted(treatment_low_risk, key=lambda x:x.n), 6))
print(r"} %chktex 31")
