import sys

input = sys.stdin.read


def solve():
  data = input().split()
  if not data:
    return

  t = int(data[0])
  idx = 1
  out = []

  for _ in range(t):
    n = int(data[idx])
    s = data[idx + 1]
    idx += 2

    curr = 'R'
    switches = 0

    for ch in s:
      if curr != ch:
        switches += 1
      # After writing 'ch', the pen automatically switches to the opposite color
      curr = 'B' if ch == 'R' else 'R'

    out.append(str(switches))

  print('\n'.join(out))


if __name__ == '__main__':
  solve()
