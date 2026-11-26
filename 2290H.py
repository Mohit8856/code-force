import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    idx = 0
    t = int(data[idx])
    idx += 1
    out = list()

    for _ in range(t):
        n = int(data[idx])
        idx += 1

        rds = [list() for _ in range(n + 1)]
        for _ in range(n - 1):
            u = int(data[idx])
            v = int(data[idx + 1])
            idx += 2
            rds[u].append(v)
            rds[v].append(u)

        # Iterative BFS rooted at capital (node 1)
        parent = [0] * (n + 1)
        children = [list() for _ in range(n + 1)]
        order = [1]
        parent[1] = -1

        for u in order:
            for v in rds[u]:
                if v != parent[u]:
                    parent[v] = u
                    children[u].append(v)
                    order.append(v)

        # Bottom-up pass: compute subtree sizes and best downward chain
        sz = [1] * (n + 1)
        best_chain = [0] * (n + 1)

        for u in reversed(order):
            ch = children[u]
            if not ch:
                best_chain[u] = 0
                continue

            for c in ch:
                sz[u] += sz[c]

            ch.sort(key=lambda c: sz[c], reverse=True)

            first_child = ch[0]
            second_sz = sz[ch[1]] if len(ch) >= 2 else 0
            best_chain[u] = max(second_sz, best_chain[first_child])

        # Track the size of the top-level branch from root 1 containing each node
        top_branch_sz = [0] * (n + 1)
        for c in children[1]:
            top_branch_sz[c] = sz[c]
        for u in order:
            if u != 1:
                for c in children[u]:
                    top_branch_sz[c] = top_branch_sz[u]

        # Top-down pass: evaluate every valid path
        above_max = [0] * (n + 1)
        min_worst_cut = n

        for u in order:
            ch = children[u]
            k = len(ch)

            # Case 1: Path starts at root 1 and goes straight down to a leaf at depth >= 2
            if u == 1 and k >= 1:
                c1 = ch[0]
                if sz[c1] >= 2:
                    min_worst_cut = min(min_worst_cut, best_chain[u])

            # Case 2: Path bends at u through its two heaviest child branches
            if k >= 2:
                c1 = ch[0]
                c2 = ch[1]
                s3 = sz[ch[2]] if k >= 3 else 0
                # If u != 1, the edge from 1 into u's top branch is outside the cycle
                root_cut = top_branch_sz[u] if u != 1 else 0
                cand = max(root_cut, above_max[u], s3, best_chain[c1], best_chain[c2])
                min_worst_cut = min(min_worst_cut, cand)

            # Propagate above_max to children
            if k >= 1:
                s1 = sz[ch[0]]
                s2 = sz[ch[1]] if k >= 2 else 0
                for i in range(k):
                    c = ch[i]
                    best_sibling = s2 if i == 0 else s1
                    above_max[c] = max(above_max[u], best_sibling)

        rch = n - min_worst_cut
        out.append(str(rch))

    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()
