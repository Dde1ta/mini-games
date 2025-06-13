import matplotlib.pyplot as plt
import math
from functools import cache

@cache
def fact(x):
    if x == 1 or x == 0:
        return 1
    return x*fact(x - 1)


def binomial(p: float = 0, n: int = 0):
    q = 1 - p
    x = [ i for i in range(n+1)]

    y = [(fact(n)/(fact(n-r)*fact(r)))*(p**r)*(q**(n-r)) for r in x]

    plt.plot(x,y)
    plt.show()

def normal(std: float, mean: float, ran: list[int]):
    def cal(x):
        f = 1/(std*(2*math.pi)**(0.5))
        s = math.e**((-1/2)*(((x-mean)/std)**2))

        return f*s

    x = [i for i in range(ran[0], ran[1]+1)]
    y = [cal(i) for i in x]

    plt.plot(x,y)
    plt.show()

def possion(rate: float, time :int):
    def cal(no_of_event:int):
        n = ((rate*time)**no_of_event)*math.e**(-1*rate*time)
        d = fact(no_of_event)

        return n/d

    x= [i for i in range(time+10)]

    y = [cal(i) for i in x]

    plt.plot(x,y)
    plt.show()

normal(2,5,[-10,20])