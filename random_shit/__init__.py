t = int(input())
out = []
for i in range(t):
    ans = 0
    n = input()
    s = input().split("#")

    for a in s:
        if len(a) >= 3:
            ans = 2
            break
        else:
            ans += len(a)

    out.append(ans)

for i in out:
    print(i)