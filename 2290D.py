
t = int(input())

for _ in range(t):
    n = int(input())
    s = input().strip()

    needed = [False] * 26

    for i in range(n // 2):
        a = ord(s[i]) - ord('a')
        b = ord(s[n - 1 - i]) - ord('a')

        if a != b:
            low = min(a, b)
            high = max(a, b)

            for j in range(low + 1, high + 1):
                needed[j] = True

    print(sum(needed))
