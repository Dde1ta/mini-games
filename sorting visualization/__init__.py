def sevie():
    limit = int(2 * 10e5)
    arr = [True for i in range(limit+ 1)]
    to_wir = []

    for i in range(2, limit + 1):
        if(arr[i]):
            to_wir.append(i)
            for j in range(i + i, limit + 1, i):
                arr[j] = False

    return to_wir

file = open("primes.txt", 'w')

file.write(str(sevie()))

