
t = int(input())

for _ in range(t):
    n, k = map(int, input().split())
    a = list(map(int, input().split()))

    b = [0] * n
    prefix = [0] * (n + 1)

    b[0] = 1
    prefix[1] = 1

    for i in range(1, n):
        left = max(0, i - k)

        b[i] = 1 ^ prefix[i] ^ prefix[left]
        prefix[i + 1] = prefix[i] ^ b[i]

    ans = 0

    for i in range(n):
        if b[i]:
            ans ^= (a[i] & 1)

    print("Alice" if ans else "Bob")
