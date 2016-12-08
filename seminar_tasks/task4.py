from random import randint
from math import sqrt, pow


if __name__ == '__main__':
    def gen_tuples(n=2):
        tuple = ()
        i = 0
        while i < n:
            tuple = (randint(-100, 100), randint(-100, 100))
            yield tuple
            i += 1

    dots = [tuple for tuple in gen_tuples(10)]
    print(dots)

    def min_dist(list):
        dist = []
        # # min = sqrt(pow(list[0][0] - list[1][0], 2) + pow(list[0][1] - list[1][0], 2))
        # print(min)
        for i in range(0, len(list)-1):
            sum = 0
            for j in range(i+1, len(list)):
                sum += sqrt(pow(list[i][0] - list[j][0], 2) + pow(list[i][1] - list[j][0], 2))
            dist.append(sum)
        return round(min(dist), 3)

    print(min_dist(dots))