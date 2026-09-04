from math import gcd

t = int(input())

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))

    print(gcd(a[0], a[-1]))