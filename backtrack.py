def test(n, k, j, i, l, m, t, x, reject, domain, count):
  while True:
    if reject(l, n, t, x):
      if domain(t, n, k):
        t = t + 1
      else:
        m, l, t = revert(k, l - 1, m, n, x, domain)
    else:
      x[l] = t
      l = l + 1
      if count(l, n, k):
        t = i
      else:
        print("Solution: " + str(m) + " -> " + str(x[1:j + 1]) + "\n")
        m, l, t = revert(k, l - 1, m + 1, n, x, domain)
    if l < 1:
      break


def revert(k, l, m, n, x, domain):
  if l < 1:
    return m, l, x[0]

  t = x[l]
  if domain(t, n, k):
    t = t + 1
    return m, l, t

  return revert(k, l - 1, m, n, x, domain)


if __name__ == "__main__":
  test(12, 6, 6, 1, 1, 0, 1, [0] * 21, lambda l, n, t, x: False, lambda t, n, k: t < n,
       lambda t, n, k: t <= k)  # n-tuple
  test(12, 6, 6, 1, 1, 0, 1, [0] * 21, lambda l, n, t, x: any(s == t for s in x[1:l]),
       lambda t, n, k: t < n,
       lambda t, n, k: t <= k)  ##permute
  test(12, 6, 6, 1, 1, 0, 1, [0] * 21, lambda l, n, t, x: any(s <= t for s in x[1:l]),
       lambda t, n, k: t < n,
       lambda t, n, k: t <= k)  ##combine
  test(12, 12, 12, 1, 1, 0, 1, [0] * 21, lambda l, n, t, x: t > 1 + max(x[0:l]),
       lambda t, n, k: bool(t < k),
       lambda l, n, k: l <= n)  # partition
  test(20, 1, 20, 0, 1, 0, 1, [0] * 21,
       lambda l, n, t, x: (l > 1 and t > x[l - 1]) or
                          ((t + sum(x[i] for i in range(1, l))) > n) or
                          (n - (n - l) * t) > (t + sum(x[i] for i in range(1, l))) or
                          False,
       lambda t, n, k: t < 1 + n // k,
       lambda l, n, k: l <= n)  # integer partition
  test(20, 20, 20, 1, 1, 0, 1, [0] * 21,
       lambda l, n, t, x: any(s == t or abs(s - t) == abs(1 + i - l) for i, s in enumerate(x[1:l])),
       lambda t, n, k: bool(t < n),
       lambda l, n, k: l <= n)  # n-queens
