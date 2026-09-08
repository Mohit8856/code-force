def solve():
    try:
        line = input()
        if not line:
            return False
        n = int(line)
    except (IOError, ValueError, EOFError):
        return False
    
    def query(u, v, d):
        print(f"? {u} {v} {d}", flush=True)
        try:
            res = int(input())
        except (ValueError, EOFError):
            exit(0)
        if res == -1:
            exit(0)
        return res

    # Phase 1: Find a leaf node 'u' that is guaranteed to be a diameter endpoint.
    # We maintain the maximum known distance 'max_dist' from our current 'u'.
    u = 1
    max_dist = 0
    
    for i in range(2, n + 1):
        # We only ask if node 'i' is strictly further from 'u' than 'max_dist'.
        # This takes exactly 1 query per node.
        if query(u, i, max_dist + 1) == 1:
            # If yes, we need to find exactly how far 'i' is from 'u'.
            # We increment the distance until the grader says 0.
            max_dist += 1
            while query(u, i, max_dist + 1) == 1:
                max_dist += 1
            # Update our endpoint to this further node.
            u = i

    # Phase 2: Find the second endpoint 'v' and the exact diameter length 'd'
    # Since 'u' is now a validated endpoint of the tree's diameter, 
    # we just find the absolute furthest node from 'u'.
    v = 1
    d = 0
    
    for i in range(1, n + 1):
        if i == u:
            continue
        # Only query if node 'i' can beat our current diameter 'd'.
        if query(u, i, d + 1) == 1:
            d += 1
            while query(u, i, d + 1) == 1:
                d += 1
            v = i

    print(f"! {u} {v} {d}", flush=True)
    return True

def main():
    try:
        t_line = input()
        if not t_line:
            return
        t = int(t_line)
        for _ in range(t):
            if not solve():
                break
    except Exception:
        pass

if __name__ == '__main__':
    main()
