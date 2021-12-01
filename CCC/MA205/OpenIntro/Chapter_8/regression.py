import csv
import collections
import numpy

# read in data
groups = collections.defaultdict(list)
with open('simulated_scatter.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        group = int(row['group'])
        x = float(row['x'])
        y = float(row['y'])
        groups[group].append([x,y] )

residuals = collections.defaultdict(list)

# calculate regression for each group
for k in groups.keys():
    x = []
    y = []
    for xval,yval in groups[k]:
        x.append(xval)
        y.append(yval)
    a,b = numpy.polyfit(x,y,1)
    s = f"Group {k}"
    f = " " * len(s)
    print(f"{s}: {a} * x + {b}")
    print(f"{f}: ymin = {min(y)}")
    print(f"{f}: ymax = {max(y)}")
    print(f"{f}: xmin = {min(x)}")
    print(f"{f}: xmax = {max(x)}")
    print()

    # calc residual for each point
    for xval, yval in groups[k]:
        yhat = a*xval+b
        e = yval - yhat
        residuals[k].append([xval,e])

n=1
# build regression data sets for each group
with open('residuals.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['n','group', 'x', 'y'])
    for k in groups.keys():
        for x, y in residuals[k]:
            writer.writerow([n,k,x,y])
            n += 1
