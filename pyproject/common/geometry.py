# from typing import List

# INF = 10000000000
# MAGIC = 998244353
# MOD = 1000000007


# class Vector2:
#     def __init__(self, x, y):
#         self.p = [x, y]

#     def __add__(self, other: Vector2) -> Vector2:
#         return Vector2(self.p[0] + other.p[0], self.p[1] + other.p[1])

#     def __sub__(self, other: Vector2) -> Vector2:
#         return Vector2(self.p[0] - other.p[0], self.p[1] - other.p[1])

#     def dot(self, other: Vector2):
#         return self.p[0] * other.p[0] + self.p[1] * other.p[1]

#     def det(self, other: Vector2):
#         return self.p[0] * other.p[1] - self.p[1] * other.p[0]

#     def __eq__(self, other: Vector2):
#         return self.p[0] == other.p[0] and self.p[1] == other.p[1]

#     def __hash__(self):
#         return (self.p[0] * MAGIC + self.p[1]) % MOD


# class Line2:
#     def __init__(self, a: Vector2, b: Vector2):
#         self.a = a
#         self.b = b

#     def get_direction(self):
