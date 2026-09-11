import sys

input = sys.stdin.readline

n, q = map(int, input().split())
s = input().strip()

pref1 = [0] * (n + 1)
prefdiff = [0] * n

for i in range(n):
    pref1[i + 1] = pref1[i] + (s[i] == '1')

for i in range(n - 1):
    prefdiff[i + 1] = prefdiff[i] + (s[i] != s[i + 1])

ans = []

for _ in range(q):
    l, r = map(int, input().split())

    if l == r:
        ans.append("3")
        continue

    ones = pref1[r] - pref1[l - 1]
    length = r - l + 1
    zeros = length - ones

    diff = prefdiff[r - 1] - prefdiff[l - 1]

    if s[l - 1] != s[r - 1]:
        diff += 1

    c00 = zeros - diff // 2
    c11 = ones - diff // 2
    d = diff // 2

    k1 = d
    k2 = (c00 + d + 1) // 2
    k3 = (c11 + d + 1) // 2
    k4 = (c00 + c11 + d + 2) // 3

    k = max(k1, k2, k3, k4)

    ans.append(str(4 * k - length))

sys.stdout.write("\n".join(ans))