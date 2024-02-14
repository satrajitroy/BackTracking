import sys

def backtrack(n, k, j, i, reject, domain, count):
  l = 1
  if l <= n:
    test(k, l, 0, n, 1, j, i, [0 for i in range(n + 1)], reject, domain, count)


def test(k, l, m, n, t, j, i, x, reject, domain, count):
  while True:
    if reject(l, n, t, x):
      if domain(t, n, k):
        t = t + 1
      else:
        m, l, t = revert(k, l, m, n, x, domain)
    else:
      l = set_state(l, t, x)
      if count(l, n, k):
        t = i
      else:
        print("Solution: " + str(m) + " -> " + str(x[1:j + 1]) + "\n")
        m, l, t = revert(k, l, m + 1, n, x, domain)


def set_state(l, t, x):
  x[l] = t
  return l + 1


def revert(k, l, m, n, x, domain):
  while True:
    l = l - 1
    if l <= 0:
      print("Solutions: " + str(m))
      sys.exit()

    t = reset_state(l, n, x)
    if domain(t, n, k):
      t = t + 1
      break
  return m, l, t


def reset_state(l, n, x):
  return x[l]

if __name__ == "__main__":
  # backtrack(12, 6, 6, 1, lambda l, n, t, x: False, lambda t, n, k: t < n, lambda t, n, k: t <= k)  # n-tuple
  # backtrack(12, 6, 6, 1, lambda l, n, t, x: any(s == t for s in x[1:l]), lambda t, n, k: t < n,
  #           lambda t, n, k: t <= k)  ##permute
  # backtrack(12, 6, 6, 1, lambda l, n, t, x: any(s <= t for s in x[1:l]), lambda t, n, k: t < n,
  #           lambda t, n, k: t <= k)  ##combine
  # backtrack(12, 12, 12, 1, lambda l, n, t, x: t > 1 + max(x[0:l]), lambda t, n, k: bool(t < k),
  #           lambda l, n, k: bool(l <= n))  # partition
  backtrack(12, 1, 12, 0,
            lambda l, n, t, x: (l > 1 and t > x[l - 1]) or \
                               ((t + sum(x[i] for i in range(1, l))) > n) or \
                               (n - (n - l) * t) > (t + sum(x[i] for i in range(1, l))) or \
                               False,
            lambda t, n, k: t < 1 + n // k,
            lambda l, n, k: l <= n)  # integer partition

