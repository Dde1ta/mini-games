from collections import defaultdict

map = defaultdict(int)

times = int(input())

names = [input() for i in range(times)]

out = []

for name in names:
    if map[name] > 0:
        out.append(name+str(map[name]))
        map[name] += 1
    else:
        map[name] += 1
        out.append("OK")

for i in out:
    print(i)
