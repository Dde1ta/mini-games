t = int(input())

def permutation(n:int) -> list[int]:
    per = [input() for i in range(n)]
    pos = [0 for i in range(n)]

    for i in range(n - 1, -1, -1):
        j = 0
        number = 0
        while(j < i):
            if(per[i][j] == '1'):
                number += 1
            j += 1

        j = 0
        while(j < n):

            if(pos[j] == 0):
                number -= 1
                if (number < 0):
                    pos[j] = i + 1
                    break
                j += 1
            else:
                j += 1


    return pos

ans = [permutation(int(input())) for i in range(t)]

print(ans)