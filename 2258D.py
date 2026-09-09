import sys

input = sys.stdin.readline


def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        seg = []

        for _ in range(n):
            l, r = map(int, input().split())
            seg.append((l, r, 0))

        for _ in range(m):
            l, r = map(int, input().split())
            seg.append((l, r, 1))

        
        seg.sort(key=lambda x: (x[0], -x[1]))

       
        useful = []
        mxr = -1

        for l, r, c in seg:
            if r <= mxr:
                continue
            useful.append((l, r, c))
            mxr = r

        seg = useful

        if not seg:
            print(0)
            print()
            continue

       
        pts = []

        for l, r, c in seg:
            pts.append(l)
            pts.append(r + 1)

        pts = sorted(set(pts))
        K = len(pts)

        pos = {x: i for i, x in enumerate(pts)}

        cover0 = [0] * (K - 1)
        cover1 = [0] * (K - 1)

        for l, r, c in seg:
            a = pos[l]
            b = pos[r + 1]

            arr = cover0 if c == 0 else cover1

            arr[a] += 1
            arr[b] -= 1

        cur = 0
        for i in range(K - 1):
            cur += cover0[i]
            cover0[i] = cur

        cur = 0
        for i in range(K - 1):
            cur += cover1[i]
            cover1[i] = cur

       

        right0 = [-1] * K
        right1 = [-1] * K

        for l, r, c in seg:
            a = pos[l]
            b = pos[r + 1]

            if c == 0:
                right0[a] = max(right0[a], b)
            else:
                right1[a] = max(right1[a], b)

       
        mx = -1
        for i in range(K):
            if right0[i] > mx:
                mx = right0[i]
            if mx >= i:
                right0[i] = mx

        mx = -1
        for i in range(K):
            if right1[i] > mx:
                mx = right1[i]
            if mx >= i:
                right1[i] = mx

        
        dp = [None] * K
        dp[0] = ()

        def better(a, b):
            if b is None:
                return a

            la = len(a)
            lb = len(b)

            z = min(la, lb)

            for i in range(z):
                if a[i] != b[i]:
                    return a if a[i] > b[i] else b

            return a if la > lb else b

       

        for i in range(1, K):
            best = dp[i - 1]

            # Find earliest j such that [j,i) can belong completely
            # to column 0 or column 1.
            left = i - 1

            while left >= 0:
                ok = False

                if right0[left] >= i:
                    ok = True

                if right1[left] >= i:
                    ok = True

                if not ok:
                    break

                if dp[left] is not None:
                    length = pts[i] - pts[left]

                    cand = list(dp[left])
                    cand.append(length)
                    cand.sort(reverse=True)
                    cand = tuple(cand)

                    best = better(cand, best)

                left -= 1

            dp[i] = best

        ans = list(dp[K - 1])
        ans.sort(reverse=True)

        print(len(ans))
        print(*ans)


if __name__ == "__main__":
    solve()