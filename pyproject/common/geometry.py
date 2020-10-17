from typing import List

INF = 10000000000
MAGIC = 998244353
MOD = 1000000007


class Vector2:
    def __init__(self, x, y):
        self.p = [x, y]

    def __add__(self, other):
        return Vector2(self.p[0] + other.p[0], self.p[1] + other.p[1])

    def __sub__(self, other):
        return Vector2(self.p[0] - other.p[0], self.p[1] - other.p[1])

    def dot(self, other):
        return self.p[0] * other.p[0] + self.p[1] * other.p[1]

    def det(self, other):
        return self.p[0] * other.p[1] - self.p[1] * other.p[0]

    def __eq__(self, other):
        return self.p[0] == other.p[0] and self.p[1] == other.p[1]

    def __hash__(self):
        return (self.p[0] * MAGIC + self.p[1]) % MOD

    def __getitem__(self, index: int):
        return self.p[index]


class Point2(Vector2):
    def __init__(self, x, y, **params):
        super().__init__(x, y)

    def transpose(self):
        return Point2(self.p[1], self.p[0])

    pass


class Line2:
    def __init__(self, a: Point2, b: Point2):
        self.a = a
        self.b = b

    def get_direction(self):
        return self.b - self.a

    def y_bound(self):
        l, r = self.a[0], self.b[0]
        if l > r:
            l, r = r, l
        return (l, r)

    def get_x(self, y):
        '''
        return (indicator, result)
        if indicator = -1, then there is no cross point
        else if indicator = 0, then cross line is exact the same as the segment
        else the result is the corresponding cordinate
        '''
        yl, yr = self.y_bound()
        if y < yl or y > yr:
            return (-1, 0)
        elif self.a[1] == self.b[1]:
            return (0, self.a[0])
        else:
            ratio = (y - self.a[1]) / (self.b[1] - self.a[1])
            return (1, ratio * (self.b[0] - self.a[0]) + self.a[0])

    def get_y(self, x):
        return Line2(self.a.transpose(), self.b.transpose()).get_x(x)
        