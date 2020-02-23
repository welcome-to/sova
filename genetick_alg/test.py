from neural import Network
import random
import math

def func1(x,y):
    return bool(x) and bool(y)

def func2(x,y):
    return math.sin(x)



if __name__ == "__main__":
    w = [
        [[0.5, 0.5, 0.5],
         [0.5, 0.5, 0.5]],

         [[0.5, 0.5, 0.5],
         [0.5, 0.5, 0.5],
         [0.5, 0.5, 0.5]],

        [[1], [1], [1]]
    ]
    N = 10000
    n = Network(weights=w)
    print(n)
    features = []
    targets = []

    for i in range(N):
        p = [random.uniform(0,6),random.uniform(0,6)]
        features.append(p)
        targets.append(func2(*p))

    n.train(features, targets)

    print(n)

    for i in range(10):
        p = [random.uniform(0,6),random.uniform(0,6)]
        res = n.run(p)
        print(p,res,func2(*p))

