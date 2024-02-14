import sys


def n_queens(n):
  m = n + 1
  x = [0 for i in range(m)]
  l = 1

  m = 0
  if l <= n:
    test(l, m, n, 1, x)


def test(l, m, n, t, x):
  while True:
    if reject(l, t, x):
      if t < n:
        t = t + 1
      else:
        m, l, t = backtrack(l, m, n, x)
    else:
      l = set_state(l, n, t, x)
      if l <= n:
        t = 1
      else:
        # print("Solution: " + str(m) + " -> " + str(x) + "\n")
        m, l, t = backtrack(l, m + 1, n, x)


def reject(l, t, x):
  for i, s in enumerate(x[1:l]):
    if s == t or abs(s - t) == abs(1 + i - l):
      return True

  return False


def set_state(l, n, t, x):
  x[l] = t
  return l + 1


def backtrack(l, m, n, x):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = reset_state(l, n, x)
    if t < n:
      t = t + 1
      break
  return m, l, t


def reset_state(l, n, x):
  return x[l]


if __name__ == "__main__":
  n_queens(13)
