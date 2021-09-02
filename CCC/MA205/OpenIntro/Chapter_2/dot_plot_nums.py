nums = [10.9, 9.92, 26.3, 9.92, 9.43, 9.92, 17.09, 6.08, 7.97, 12.62, 17.09, 5.31, 7.35, 5.31, 7.96, 24.85, 18.06, 10.42, 7.96, 19.42, 14.08, 20, 9.44, 9.92, 10.91, 5.32, 6.71, 15.04, 11.98, 12.62, 10.91, 9.44, 9.93, 7.35, 18.45, 17.09, 7.96, 6.08, 6.71, 7.34, 12.62, 16.02, 10.9, 9.93, 9.44, 10.42, 21.45, 10.91, 9.43, 6.08]

rounded = [int(round(x,0)) for x in nums]

dots = {}
for x in rounded:
    if x not in dots:
        dots[x] = 1
    else:
        dots[x] += 1

ymax = -1
for k,v in dots.items():
    for i in range(v):
        y = 1.8 + 1 * i
        print(f"({k}, {y})")
        if y > ymax:
            ymax = y
        
mean = round(sum(nums)/len(nums),3)

print(f"Largest y-value is {ymax}")
print(f"Mean is {mean}")

s = r"\dfrac{\tiny\left(\begin{array}{c}"
l = ""
for x in sorted(nums):
    l += str(x)
    l += r"\%"
    l += r"+"
    if len(l) >= 60:
        l = l[:-1]
        l += r"\\+"
        s += l
        l = ""
s += l
s = s[:-1]
if s[-2:] == r"\\":
    s = s[:-3]
s += r"\end{array}\right)}{"
s += str(len(nums))
s += r"}="
s += str(mean)
s += r"\%"
print(s)
