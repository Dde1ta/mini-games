def rm(s):
    for i in range(len(s) - 1, -1,-1):
        if(s[i] == "1"):
            return s[0:i + 1]
    return s

t = int(input())

for i in range(t):
    n = int(input())
    s = rm(str(bin(n))[2::])

    if(len(s) % 2 == 1 and s[len(s) // 2] == "1"):
        print("NO")
    elif (s[::-1] == s):
        print("YES")
    else:
        print("NO")