import sys

def NQueens(n):
  m = n + 1
  l = 2 * n

  a = [0 for i in range(0, m)]
  b = [0 for i in range(0, l)]
  c = [0 for i in range(0, l)]

  x = [0 for i in range(m)]
  l = 1

  m = 0
  if l <= n:
    test(a, b, c, l, m, n, 1, x)
  else:
    print("Solution: " + str(m) + " -> " + str(x) + "\n")
    m, l, t = backtrack(a, b, c, l, m+1, n, x)
    m = test(a, b, c, l, m, n, t, x)

def resetState(a, b, c, l, n, x):
  t = x[l]
  c[t - l + n] = 0
  b[t + l - 1] = 0
  a[t] = 0
  return t

def test(a, b, c, l, m, n, t, x):
  while True:
    if validate(a, b, c, l, n, t):
        if t < n:
          t = t + 1
        else:
          m, l, t = backtrack(a, b, c, l, m, n, x)
    else:
      l = setState(a, b, c, l, n, t, x)
      if l <= n:
        t = 1
      else:
        print("Solution: " + str(m) + " -> " + str(x) + "\n")
        m, l, t = backtrack(a, b, c, l, m + 1, n, x)


def validate(a, b, c, l, n, t):
  return a[t] == 1 or b[t + l - 1] == 1 or c[t - l + n] == 1


def setState(a, b, c, l, n, t, x):
  a[t] = 1
  b[t + l - 1] = 1
  c[t - l + n] = 1
  x[l] = t
  l = l + 1
  return l

def backtrack(a, b, c, l, m, n, x):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = resetState(a, b, c, l, n, x)
    if t < n:
      t = t + 1
      break
  return m, l, t

if __name__ == "__main__":
  NQueens(8)