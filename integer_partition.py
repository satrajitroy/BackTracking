import sys

s = 0
y = []

def partition(n, k):
  global y
  m = n + 1
  x = [0 for i in range(m)]
  y = [0 for i in range(m)]
  l = 1

  m = 0
  if l <= n:
    test(k, l, m, n, 1, x)
  # else:
  #   print("Solution: " + str(m) + " -> " + str(x[1:n + 1]) + "\n")
  #   m, l, t = backtrack(k, l, m + 1, n, x)
  #   test(k, l, m, n, t, x)


def reset_state(l, n, x):
  global y
  return y[l]


def test(k, l, m, n, t, x):
  while True:
    if reject(l, n, t, x):
      if t < n//k:
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


def reject(l, n, t, x):
  s = t
  if l > 1 and t > x[l-1]:
    return True

  s = t + sum(x[i] for i in range(1,l))
  if (s > n):
    return True

  u = n - (n-l)*t
  if u > s:
    return True

  return False


def set_state(l, t, x):
  global y
  y[l] = x[l]
  x[l] = t
  return l + 1


def backtrack(k, l, m, n, x):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = reset_state(l, n, x)
    if t < n//k:
      t = t + 1
      break
  return m, l, t


if __name__ == "__main__":
  partition(6, 6)
