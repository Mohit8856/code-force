import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    t = int(input_data[0])
    idx = 1
    out = []
    
    for _ in range(t):
        n = int(input_data[idx])
        idx += 1
        h = list(map(int, input_data[idx : idx + n]))
        idx += n
        
        # Sort once in-place: O(n log n) with Timsort (O(n) if already sorted)
        h.sort()
        
        ans = [0] * n
        left = 0
        right = n - 1
        visible = 0
        
        i = 0
        while i < n:
            # Find the end of the current block of equal elements
            j = i + 1
            while j < n and h[j] == h[i]:
                j += 1
            
            count = j - i
            
            # Place the first copy on the left
            ans[left] = h[i]
            left += 1
            visible += 1
            
            # Place the second copy (if any) on the right
            if count >= 2:
                ans[right] = h[i]
                right -= 1
                visible += 1
            
            # Place any extra duplicates right next to the left pointer 
            # (they will be blocked once larger elements are placed further inside)
            for _ in range(count - 2):
                ans[left] = h[i]
                left += 1
                
            i = j
            
        out.append(str(visible))
        out.append(" ".join(map(str, ans)))
        
    sys.stdout.write("\n".join(out) + "\n")

if __name__ == "__main__":
    solve()

