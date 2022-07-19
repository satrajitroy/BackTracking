import sys

def permute(n, k):
  m = n + 1
  x = [0 for i in range(m)]
  l = 1

  m = 0
  if l <= n:
    test(k, l, m, n, 1, x)
  else:
    print("Solution: " + str(m) + " -> " + str(x[1:k+1]) + "\n")
    m, l, t = backtrack(k, l, m+1, n, x)
    m = test(k, l, m, n, t, x)

def resetState(l, n, x):
  return x[l]

def test(k, l, m, n, t, x):
  while True:
    if reject(l, t, x):
        if t < n:
          t = t + 1
        else:
          m, l, t = backtrack(k, l, m, n, x)
    else:
      l = setState(l, t, x)
      if l <= k:
        t = 1
      else:
        print("Solution: " + str(m) + " -> " + str(x[1:k+1]) + "\n")
        m, l, t = backtrack(k, l, m + 1, n, x)


def reject(l, t, x):
  for i, s in enumerate(x[1:l]):
    if s == t:
      return True

  return False


def setState(l, t, x):
  x[l] = t
  return l + 1

def backtrack(k, l, m, n, x):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = resetState(l, n, x)
    if t < n:
      t = t + 1
      break
  return m, l, t

if __name__ == "__main__":
  permute(7, 3)
