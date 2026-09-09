import sys

input = sys.stdin.readline


def solve():
    t = int(input())

    for _ in range(t):
        n, m = map(int, input().split())

        a = []
        b = []

        for _ in range(n):
            l, r = map(int, input().split())
            a.append((l, r))

        for _ in range(m):
            l, r = map(int, input().split())
            b.append((l, r))

        # ---------------------------------------------------------
        # Merge all intervals.
        # type = 0 -> column 1
        # type = 1 -> column 2
        # ---------------------------------------------------------
        seg = []

        for l, r in a:
            seg.append((l, r, 0))

        for l, r in b:
            seg.append((l, r, 1))

        seg.sort()

        # ---------------------------------------------------------
        # Remove intervals contained in another interval.
        #
        # After this operation the remaining intervals form
        # alternating chains.
        # ---------------------------------------------------------
        useful = []

        max_r = -1

        for l, r, c in seg:
            if r <= max_r:
                continue

            useful.append((l, r, c))
            max_r = r

        seg = useful

        k = len(seg)

        if k == 0:
            print(0)
            print()
            continue

        # ---------------------------------------------------------
        # Coordinate compression.
        #
        # [l,r] becomes [l,r+1)
        # ---------------------------------------------------------
        pts = []

        for l, r, c in seg:
            pts.append(l)
            pts.append(r + 1)

        pts = sorted(set(pts))

        pos = {x: i for i, x in enumerate(pts)}

        K = len(pts)

        # ---------------------------------------------------------
        # For every compressed elementary interval, store which
        # columns are available.
        #
        # mask[i] describes [pts[i], pts[i+1])
        #
        # bit 0 -> column 1
        # bit 1 -> column 2
        # ---------------------------------------------------------
        mask = [0] * (K - 1)

        for l, r, c in seg:
            x = pos[l]
            y = pos[r + 1]

            bit = 1 << c

            for i in range(x, y):
                mask[i] |= bit

        # ---------------------------------------------------------
        # DP representation.
        #
        # Because
        #
        # 100^(100^x)
        #
        # dominates every sum of terms with smaller x,
        # maximizing the score is equivalent to maximizing the
        # sorted list of segment lengths lexicographically.
        #
        # dp[i] = best list for the prefix ending at compressed
        # coordinate i.
        # ---------------------------------------------------------

        dp = [None] * K

        # State:
        # (lengths, last_column, last_start)
        #
        # lengths are kept sorted in decreasing order.
        dp[0] = [()]

        def better(x, y):
            if y is None:
                return x

            # Both lists are already sorted decreasingly.
            lx = len(x)
            ly = len(y)

            z = min(lx, ly)

            for i in range(z):
                if x[i] != y[i]:
                    return x if x[i] > y[i] else y

            return x if lx > ly else y

        # ---------------------------------------------------------
        # General interval DP.
        #
        # We construct one contiguous chosen segment at a time.
        # A segment can use column c while every elementary block
        # belongs to that column.
        # ---------------------------------------------------------

        dp = [None] * K
        dp[0] = ()

        for i in range(1, K):

            # We can leave this elementary interval unused.
            dp[i] = dp[i - 1]

            for j in range(i - 1, -1, -1):

                # Check whether [pts[j], pts[i]) belongs entirely
                # to one of the two columns.
                ok0 = True
                ok1 = True

                for p in range(j, i):
                    if not (mask[p] & 1):
                        ok0 = False
                    if not (mask[p] & 2):
                        ok1 = False

                    if not ok0 and not ok1:
                        break

                if not ok0 and not ok1:
                    continue

                length = pts[i] - pts[j]

                if dp[j] is None:
                    continue

                cand = list(dp[j])
                cand.append(length)
                cand.sort(reverse=True)
                cand = tuple(cand)

                dp[i] = better(cand, dp[i])

        ans = list(dp[K - 1])
        ans.sort(reverse=True)

        print(len(ans))
        print(*ans)


if __name__ == "__main__":
    solve()