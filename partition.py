import sys


def partition(n, k):
  m = n + 1
  x = [0 for i in range(m)]
  l = 1

  m = 0
  if l <= n:
    test(k, l, m, n, 1, x)


def test(k, l, m, n, t, x):
  while True:
    if reject(l, t, x):
      if t < k:
        t = t + 1
      else:
        m, l, t = backtrack(k, l, m, n, x)
    else:
      l = set_state(l, t, x)
      if l <= n:
        t = 1
      else:
        print("Solution: " + str(m) + " -> " + str(x[1:n + 1]) + "\n")
        m, l, t = backtrack(k, l, m + 1, n, x)


def reject(l, t, x):
  m = max(x[0:l])
  if t > 1 + m:
    return True

  return False


def set_state(l, t, x):
  x[l] = t
  return l + 1


def backtrack(k, l, m, n, x):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = reset_state(l, n, x)
    if t < k:
      t = t + 1
      break
  return m, l, t


def reset_state(l, n, x):
  return x[l]


if __name__ == "__main__":
  partition(7,7)
