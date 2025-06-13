def removeOccurrences(s: str, part: str) -> str:
    s = list(s)
    j = []
    k = 0
    i = 0

    while i < len(s):
        if s[i] == part[k]:

            if k == len(part) - 1:
                if len(j) == 0:
                    del s[i - len(part)  + 1: i + 1]
                else:
                    del s[j[-1]:j[-1] + len(part)]
                    i = j.pop() - 1
                    k = 0
            else:
                k += 1
                i += 1

        else:
            if k == 0:
                i += 1
            else:
                k = 0
                j.append(i)

    return "".join(s)

ans = removeOccurrences("ccctltctlltlb","ctl")

print(ans)